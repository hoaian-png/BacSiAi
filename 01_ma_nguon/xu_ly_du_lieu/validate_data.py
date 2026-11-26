"""Validate exported ML data and source checksums using only the Python standard library."""
import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import prepare_data as pipeline

ROOT = pipeline.ROOT


def load_jsonl(path):
    with path.open(encoding='utf-8') as handle:
        return [json.loads(line) for line in handle if line.strip()]


def main():
    report = {'validated_at_utc': datetime.now(timezone.utc).isoformat(), 'files': {}, 'checks': {}}
    all_rows = []
    for stem in ('normalized/ViMQ', 'normalized/ViHealthQA', 'normalized/ViMedAQA',
                 'prepared/questions_ent', 'prepared/knowledge_ent'):
        rows = load_jsonl(ROOT / f'{stem}.jsonl')
        with (ROOT / f'{stem}.csv').open(encoding='utf-8-sig', newline='') as handle:
            reader = csv.DictReader(handle)
            count = 0
            for count, actual in enumerate(reader, 1):
                assert count <= len(rows), (stem, 'extra CSV row')
                expected = rows[count - 1]
                assert set(actual) == set(expected), (stem, count, 'columns')
                for key, value in expected.items():
                    if isinstance(value, (list, dict)):
                        value = json.dumps(value, ensure_ascii=False, separators=(',', ':'))
                    if isinstance(value, str) and value.startswith(('=', '+', '-', '@')):
                        value = "'" + value
                    assert actual[key] == str(value), (stem, count, key)
            assert count == len(rows), (stem, count, len(rows))
        assert len({r['id'] for r in rows}) == len(rows), stem
        report['files'][stem] = {'rows': len(rows), 'csv_jsonl_equivalent': True, 'unique_ids': True}
        if stem.startswith('normalized/'):
            all_rows.extend(rows)

    by_id = {r['id']: r for r in all_rows}
    groups = {}
    for row in all_rows:
        assert row['gold_topic_label'] == ''
        assert row['topic_label_method'] in ('keyword_rule_suggestion', 'unassigned')
        if row['duplicate_of']:
            other = by_id[row['duplicate_of']]
            assert pipeline.text_key(row['question']) == pipeline.text_key(other['question'])
            assert row['group_id'] == other['group_id']
        for match in row['keyword_matches']:
            assert row['question'][match['start']:match['end']] == match['surface']
        assert groups.setdefault(row['group_id'], row['split_suggested']) == row['split_suggested']
    for question in load_jsonl(ROOT / 'prepared/questions_ent.jsonl'):
        assert 'answer' not in question and 'context' not in question
        assert all(by_id[record_id]['question_group_id'] == question['question_group_id']
                   for record_id in question['provenance_ids'])
    for item in load_jsonl(ROOT / 'prepared/knowledge_ent.jsonl'):
        assert item['source_record_id'] in by_id
        assert item['text']
        assert item['approved_for_rag'] is False

    manifest = json.loads((ROOT / 'sources.json').read_text(encoding='utf-8'))
    for item in manifest['files']:
        content = (ROOT / item['path']).read_bytes()
        assert len(content) == item['bytes']
        assert hashlib.sha256(content).hexdigest() == item['sha256']
    lexicon = pipeline.load_lexicon()
    assert not pipeline.matches('Kế hoạch học tập', lexicon), 'Keyword boundary false positive'
    assert pipeline.matches('Tôi không sốt.', lexicon)[0]['negation_or_resolution_hint']
    assert pipeline.clean('Nhiệt độ < 38 và > 35') == 'Nhiệt độ < 38 và > 35'
    assert pipeline.clean('<p>Ho &amp; sốt</p>') == 'Ho & sốt'
    assert pipeline.clean('Đau_họng ?', segmented=True) == 'Đau họng?'
    report['checks'] = dict.fromkeys([
        'csv_jsonl_roundtrip', 'unique_ids', 'duplicate_links', 'keyword_offsets',
        'group_split_consistency', 'question_provenance', 'questions_exclude_answers',
        'knowledge_unapproved', 'source_sha256', 'keyword_word_boundaries',
        'negation_hint', 'medical_comparison_symbols_preserved', 'html_cleanup',
        'vimq_detokenization'], True)
    pipeline.save_json(pipeline.REPORTS / 'validation.json', report)
    print(json.dumps(report, ensure_ascii=True, indent=2))


if __name__ == '__main__':
    main()
