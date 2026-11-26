"""Download pinned upstream datasets and prepare traceable ENT data (Python 3.11+)."""
from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import re
import sys
import time
import unicodedata
import urllib.request
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ROOT = PROJECT_ROOT / '02_du_lieu' / 'filedata'
RAW = ROOT / 'raw'
NORMALIZED = ROOT / 'normalized'
PREPARED = ROOT / 'prepared'
REPORTS = PROJECT_ROOT / '05_bao_cao' / 'kiem_tra_du_lieu'
HEADERS = {'User-Agent': 'ENT-Research-Data/1.0'}
sys.path.insert(0, str(PROJECT_ROOT / '01_ma_nguon' / '.data-tools'))


def clean(value, segmented=False):
    if value is None:
        return ''
    value = unicodedata.normalize('NFC', html.unescape(str(value)))
    value = re.sub(r'</?[A-Za-z][A-Za-z0-9]*(?:\s[^>]*)?/?>', ' ', value)
    value = ''.join(c for c in value if not unicodedata.category(c).startswith('C') or c in '\n\r\t')
    if segmented:
        value = value.replace('_', ' ')
    value = re.sub(r'\s+', ' ', value).strip()
    # ViMQ uses pretokenized punctuation. Rejoin it without changing word order.
    if segmented:
        value = re.sub(r'\s+([,.;:!?%])', r'\1', value)
        value = re.sub(r'\(\s+', '(', value)
        value = re.sub(r'\s+\)', ')', value)
    return value


def text_key(value):
    return ' '.join(re.findall(r'\w+', clean(value).casefold(), flags=re.UNICODE))


def digest(value):
    return hashlib.sha256(value.encode('utf-8')).hexdigest()


def write_jsonl(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8', newline='\n') as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, separators=(',', ':')) + '\n')


def write_csv(path, rows, fields=None):
    path.parent.mkdir(parents=True, exist_ok=True)
    if fields is None:
        fields = list(rows[0]) if rows else []
    with path.open('w', encoding='utf-8-sig', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction='raise')
        writer.writeheader()
        for row in rows:
            values = {}
            for key in fields:
                value = row.get(key, '')
                if isinstance(value, (list, dict)):
                    value = json.dumps(value, ensure_ascii=False, separators=(',', ':'))
                # CSV is a human review view. JSONL retains the exact canonical values.
                if isinstance(value, str) and value.startswith(('=', '+', '-', '@')):
                    value = "'" + value
                values[key] = value
            writer.writerow(values)


def load_lexicon():
    with (ROOT / 'config/keywords.csv').open(encoding='utf-8-sig', newline='') as handle:
        rows = list(csv.DictReader(handle))
    return [(r, re.compile(r'(?<!\w)' + re.escape(r['variant']).replace(r'\ ', r'\s+') + r'(?!\w)', re.IGNORECASE))
            for r in rows]


def matches(text, lexicon):
    found = []
    for entry, pattern in lexicon:
        for match in pattern.finditer(text):
            prefix = text[max(0, match.start() - 45):match.start()]
            # Only a review hint: this is deliberately not a clinical polarity classifier.
            hint = bool(re.search(r'(?:không|chưa|chẳng|hết|đỡ|giảm)(?:\s+\w+){0,3}\s*$', prefix, re.IGNORECASE))
            found.append({'surface': match.group(), 'canonical': entry['canonical'], 'topic': entry['topic'],
                          'start': match.start(), 'end': match.end(), 'negation_or_resolution_hint': hint})
    # Keep the longest match when nested keywords describe the same span and topic.
    found.sort(key=lambda x: (x['start'], -(x['end'] - x['start'])))
    result = []
    for item in found:
        if not any(other['topic'] == item['topic'] and other['start'] <= item['start']
                   and item['end'] <= other['end'] for other in result):
            result.append(item)
    return result


EMAIL = re.compile(r'[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}')
PHONE = re.compile(r'(?<!\w)(?:\+84|0084|0)[ .-]?(?:\d[ .-]?){8,10}(?!\w)')


def mask_contact(text):
    return PHONE.sub('[PHONE]', EMAIL.sub('[EMAIL]', text))


def base_record(dataset, split, original_id, location, question, **extra):
    row = {'id': f'{dataset}:{split}:{original_id}', 'dataset': dataset, 'original_id': str(original_id),
           'source_split': split, 'raw_location': location, 'question': clean(question),
           'answer': '', 'context': '', 'title': '', 'source_url': '', 'source_topic': '',
           'source_intent_label': '', 'intent_label': '', 'source_keyword': '', 'source_entities': [],
           'author': '', 'author_url': '', 'keywords': [], 'keyword_matches': [],
           'topic_candidates': [], 'topic_label': '', 'topic_label_method': 'unassigned',
           'scope_status': '', 'scope_evidence': [], 'negation_review_required': False,
           'gold_topic_label': '', 'review_status': 'pending_manual_review',
           'privacy_status': '', 'question_group_id': '', 'group_id': '', 'split_suggested': '', 'duplicate_of': ''}
    row.update(extra)
    for field in ('answer', 'context', 'title', 'source_url', 'source_keyword', 'author', 'author_url'):
        row[field] = clean(row[field])
    return row


def read_records():
    rows = []
    for upstream_split in ('train', 'dev', 'test'):
        split = 'validation' if upstream_split == 'dev' else upstream_split
        path = RAW / 'ViMQ/data' / f'{upstream_split}.json'
        source = json.loads(path.read_text(encoding='utf-8'))
        for index, sample in enumerate(source, 1):
            tokens = sample['sentence'].split()
            entities = []
            for start, end, kind in sample['seq_label']:
                assert 0 <= start <= end < len(tokens), (path, index)
                entities.append({'text': clean(' '.join(tokens[start:end + 1]), segmented=True),
                                 'type': kind, 'source_token_start': start, 'source_token_end_inclusive': end})
            intent = sample['sent_label']
            assert intent in ('method_diagnosis', 'treatment', 'severity', 'cause'), intent
            rows.append(base_record('ViMQ', split, index,
                                    f'raw/ViMQ/data/{upstream_split}.json#row={index}',
                                    clean(sample['sentence'], segmented=True),
                                    source_intent_label=intent,
                                    intent_label={'method_diagnosis': 'diagnosis'}.get(intent, intent),
                                    source_entities=entities))
    for upstream_split in ('train', 'val', 'test'):
        split = 'validation' if upstream_split == 'val' else upstream_split
        path = RAW / 'ViHealthQA' / f'{upstream_split}.csv'
        with path.open(encoding='utf-8-sig', newline='') as handle:
            for index, sample in enumerate(csv.DictReader(handle), 1):
                assert set(sample) == {'id', 'question', 'answer', 'link'}
                rows.append(base_record('ViHealthQA', split, sample['id'],
                                        f'raw/ViHealthQA/{upstream_split}.csv#row={index}', sample['question'],
                                        answer=sample['answer'], source_url=sample['link']))
    try:
        import pyarrow.parquet as pq
    except ImportError as exc:
        raise SystemExit('Install pyarrow==26.0.1 or use: python -m pip install --target 01_ma_nguon/.data-tools pyarrow==26.0.1') from exc
    names = {0: 'body-part', 1: 'disease', 2: 'drug', 3: 'medicine'}
    for split in ('train', 'validation', 'test'):
        for path in sorted((RAW / 'ViMedAQA/all').glob(f'{split}-*.parquet')):
            for index, sample in enumerate(pq.read_table(path).to_pylist(), 1):
                rows.append(base_record('ViMedAQA', split, sample['question_idx'],
                                        f'{path.relative_to(ROOT).as_posix()}#row={index}', sample['question'],
                                        answer=sample['answer'], context=sample['context'], title=sample['title'],
                                        source_keyword=sample['keyword'], source_topic=names[sample['topic']],
                                        source_url=sample['article_url'], author=sample['author'], author_url=sample['author_url']))
    return rows


class UnionFind:
    def __init__(self, size):
        self.parent = list(range(size))

    def find(self, node):
        while self.parent[node] != node:
            self.parent[node] = self.parent[self.parent[node]]
            node = self.parent[node]
        return node

    def union(self, a, b):
        a, b = self.find(a), self.find(b)
        if a != b:
            self.parent[max(a, b)] = min(a, b)


def enrich(rows):
    lexicon = load_lexicon()
    first_question = {}
    first_document = {}
    groups = UnionFind(len(rows))
    for index, row in enumerate(rows):
        question = row['question']
        assert question, row['id']
        hits = matches(question, lexicon)
        row['keyword_matches'] = hits
        row['keywords'] = list(dict.fromkeys(h['surface'] for h in hits))
        topics = sorted({h['topic'] for h in hits})
        row['topic_candidates'] = topics
        row['topic_label'] = topics[0] if len(topics) == 1 else ''
        row['topic_label_method'] = 'keyword_rule_suggestion' if topics else 'unassigned'
        evidence = ['question'] if hits else []
        for field in ('title', 'source_keyword'):
            if row[field] and matches(row[field], lexicon):
                evidence.append(field)
        row['scope_status'] = 'ent_candidate' if evidence else 'no_keyword_match'
        row['scope_evidence'] = evidence
        row['negation_review_required'] = any(h['negation_or_resolution_hint'] for h in hits)
        all_text = ' '.join(row[f] for f in ('question', 'answer', 'context'))
        row['privacy_status'] = ('contact_pattern_detected_needs_review' if EMAIL.search(all_text) or PHONE.search(all_text)
                                 else 'not_fully_anonymized_needs_review')
        key = text_key(question)
        row['question_group_id'] = 'QG_' + digest(key)[:20]
        if key in first_question:
            prev = first_question[key]
            row['duplicate_of'] = rows[prev]['id']
            groups.union(index, prev)
        else:
            first_question[key] = index
        if row['source_url']:
            document = row['source_url'].split('#')[0].split('?')[0].rstrip('/').lower()
            if document in first_document:
                groups.union(index, first_document[document])
            else:
                first_document[document] = index
    members = defaultdict(list)
    for index, row in enumerate(rows):
        members[groups.find(index)].append(row['id'])
    group_keys = {root: digest('\n'.join(sorted(ids))) for root, ids in members.items()}
    for index, row in enumerate(rows):
        key = group_keys[groups.find(index)]
        row['group_id'] = 'G_' + key[:20]
        bucket = int(key[:8], 16) % 100
        row['split_suggested'] = 'train' if bucket < 70 else 'validation' if bucket < 85 else 'test'
    return rows


def prepare(rows):
    by_question = defaultdict(list)
    for row in rows:
        by_question[row['question_group_id']].append(row['id'])
    questions = []
    knowledge = []
    seen_questions = set()
    seen_knowledge = set()
    question_fields = ['id', 'dataset', 'original_id', 'raw_location', 'source_split', 'question',
                       'source_intent_label', 'intent_label', 'keywords', 'source_entities', 'keyword_matches',
                       'topic_candidates', 'topic_label', 'topic_label_method', 'scope_evidence',
                       'negation_review_required', 'gold_topic_label', 'review_status', 'privacy_status',
                       'question_group_id', 'group_id', 'split_suggested']
    for row in rows:
        if row['scope_status'] != 'ent_candidate':
            continue
        if row['question_group_id'] not in seen_questions:
            seen_questions.add(row['question_group_id'])
            q = {field: row[field] for field in question_fields}
            q['question'] = mask_contact(q['question'])
            # Match offsets and entity spans refer to the unmasked normalized source question.
            q['annotation_reference'] = 'normalized_source_question_before_contact_masking'
            q['provenance_ids'] = by_question[row['question_group_id']]
            questions.append(q)
        content = row['context'] or row['answer']
        if content:
            key = digest(row['source_url'] + '\n' + content)
            if key in seen_knowledge:
                continue
            seen_knowledge.add(key)
            knowledge.append({'id': 'K_' + key[:20], 'source_record_id': row['id'], 'dataset': row['dataset'],
                              'question': mask_contact(row['question']), 'answer': mask_contact(row['answer']),
                              'context': mask_contact(row['context']), 'text': mask_contact(content),
                              'text_origin': 'context' if row['context'] else 'answer',
                              'title': row['title'], 'source_url': row['source_url'],
                              'source_keyword': row['source_keyword'], 'topic_candidates': row['topic_candidates'],
                              'group_id': row['group_id'], 'split_suggested': row['split_suggested'],
                              'review_status': 'pending_medical_and_privacy_review', 'approved_for_rag': False})
    write_jsonl(PREPARED / 'questions_ent.jsonl', questions)
    write_csv(PREPARED / 'questions_ent.csv', questions, question_fields + ['annotation_reference', 'provenance_ids'])
    write_jsonl(PREPARED / 'knowledge_ent.jsonl', knowledge)
    write_csv(PREPARED / 'knowledge_ent.csv', knowledge)
    return questions, knowledge


def audit(rows, questions, knowledge):
    assert len({r['id'] for r in rows}) == len(rows), 'Duplicate record IDs'
    allowed_topics = set(json.loads((ROOT / 'config/labels.json').read_text(encoding='utf-8'))['labels'])
    for row in rows:
        assert set(row['topic_candidates']) <= allowed_topics
        assert row['gold_topic_label'] == '' and row['review_status'] == 'pending_manual_review'
        for hit in row['keyword_matches']:
            assert row['question'][hit['start']:hit['end']] == hit['surface']
    group_splits = defaultdict(set)
    for row in rows:
        group_splits[row['group_id']].add(row['split_suggested'])
    assert all(len(splits) == 1 for splits in group_splits.values())
    expected_counts = {'ViMQ': 9000, 'ViHealthQA': 10015, 'ViMedAQA': 44313}
    actual_counts = Counter(r['dataset'] for r in rows)
    assert dict(actual_counts) == expected_counts, actual_counts
    summary = {'generated_at_utc': datetime.now(timezone.utc).isoformat(),
               'total_normalized': len(rows), 'datasets': {},
               'prepared_unique_questions_ent': len(questions), 'prepared_knowledge_ent': len(knowledge),
               'duplicate_question_rows': sum(bool(r['duplicate_of']) for r in rows),
               'exact_question_groups': len({r['question_group_id'] for r in rows}),
               'document_and_question_groups': len(group_splits),
               'prepared_splits_suggested': dict(Counter(r['split_suggested'] for r in questions)),
               'prepared_topic_suggestions': dict(Counter(r['topic_label'] or 'multiple_or_no_question_topic' for r in questions)),
               'prepared_negation_review_required': sum(r['negation_review_required'] for r in questions),
               'gold_topic_labels_reviewed': 0,
               'checks': {'expected_source_counts': True, 'unique_record_ids': True,
                          'keyword_character_offsets': True, 'no_group_crossing_suggested_splits': True,
                          'raw_file_sha256_verified': True},
               'limitations': ['Topic labels are rule suggestions, not human gold labels.',
                              'No clinical validation has been performed.',
                              'Near duplicates and paraphrases require additional review.',
                              'Suggested splits group exact normalized questions and matching source URLs; not stratified.',
                              'Contact masking is heuristic, not full anonymization.',
                              'ENT candidates include fever-only questions and may be outside the final ENT scope.',
                              'Knowledge candidates are not approved for patient-facing RAG.']}
    for dataset in expected_counts:
        subset = [r for r in rows if r['dataset'] == dataset]
        summary['datasets'][dataset] = {'normalized_records': len(subset),
                                        'source_splits': dict(Counter(r['source_split'] for r in subset)),
                                        'ent_candidate_rows': sum(r['scope_status'] == 'ent_candidate' for r in subset),
                                        'with_answer': sum(bool(r['answer']) for r in subset),
                                        'with_context': sum(bool(r['context']) for r in subset),
                                        'with_source_entities': sum(bool(r['source_entities']) for r in subset),
                                        'contact_pattern_rows': sum(r['privacy_status'].startswith('contact_pattern') for r in subset)}
    manifest = json.loads((ROOT / 'sources.json').read_text(encoding='utf-8'))
    for file in manifest['files']:
        assert hashlib.sha256((ROOT / file['path']).read_bytes()).hexdigest() == file['sha256'], file['path']
    save_json(REPORTS / 'summary.json', summary)
    write_csv(REPORTS / 'dataset_counts.csv', [dict(dataset=k, **{key: value for key, value in v.items() if key != 'source_splits'})
                                              for k, v in summary['datasets'].items()])
    write_csv(REPORTS / 'topic_counts.csv', [{'topic_label_suggested': label, 'count': count}
                                           for label, count in summary['prepared_topic_suggestions'].items()])
    duplicates = [{'id': r['id'], 'dataset': r['dataset'], 'duplicate_of': r['duplicate_of'],
                   'question_group_id': r['question_group_id'], 'group_id': r['group_id'],
                   'source_split': r['source_split'], 'split_suggested': r['split_suggested']}
                  for r in rows if r['duplicate_of']]
    write_csv(REPORTS / 'duplicates.csv', duplicates)
    print(json.dumps(summary, ensure_ascii=True, indent=2), flush=True)


def normalize():
    rows = enrich(read_records())
    for dataset in ('ViMQ', 'ViHealthQA', 'ViMedAQA'):
        subset = [r for r in rows if r['dataset'] == dataset]
        write_jsonl(NORMALIZED / f'{dataset}.jsonl', subset)
        write_csv(NORMALIZED / f'{dataset}.csv', subset)
    questions, knowledge = prepare(rows)
    audit(rows, questions, knowledge)


def get(url):
    for attempt in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=HEADERS), timeout=90) as response:
                return response.read()
        except Exception:
            if attempt == 3:
                raise
            time.sleep(attempt + 1)


def save_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def download():
    for directory in (RAW, NORMALIZED, PREPARED, REPORTS):
        directory.mkdir(parents=True, exist_ok=True)
    sources = []
    jobs = []
    for dataset, repo, service in [('ViMQ', 'tadeephuy/ViMQ', 'github'),
                                    ('ViHealthQA', 'tarudesu/ViHealthQA', 'huggingface'),
                                    ('ViMedAQA', 'tmnam20/ViMedAQA', 'huggingface')]:
        if service == 'github':
            api = f'https://api.github.com/repos/{repo}/git/trees/main?recursive=1'
            metadata = json.loads(get(api))
            revision = metadata['sha']
            paths = [r['path'] for r in metadata['tree'] if r['type'] == 'blob'
                     and (r['path'].startswith('data/') or r['path'] == 'README.md'
                          or 'license' in r['path'].lower())]
            base = f'https://raw.githubusercontent.com/{repo}/{revision}/'
            page = f'https://github.com/{repo}'
        else:
            api = f'https://huggingface.co/api/datasets/{repo}'
            metadata = json.loads(get(api))
            revision = metadata['sha']
            paths = [r['rfilename'] for r in metadata['siblings']
                     if r['rfilename'] == 'README.md' or 'license' in r['rfilename'].lower()
                     or (dataset == 'ViHealthQA' and r['rfilename'].endswith('.csv'))
                     or (dataset == 'ViMedAQA' and r['rfilename'].startswith('all/')
                         and r['rfilename'].endswith('.parquet'))]
            base = f'https://huggingface.co/datasets/{repo}/resolve/{revision}/'
            page = f'https://huggingface.co/datasets/{repo}'
        save_json(RAW / dataset / 'repository_metadata.json', metadata)
        sources.append({'dataset': dataset, 'repository': page, 'revision': revision,
                        'metadata_url': api, 'downloaded_at_utc': datetime.now(timezone.utc).isoformat(),
                        'selection': 'all configuration only; other ViMedAQA configurations are subsets' if dataset == 'ViMedAQA' else 'all upstream data splits'})
        for name in paths:
            jobs.append((dataset, name, base + name))

    def fetch(job):
        dataset, name, url = job
        path = RAW / dataset / name
        path.parent.mkdir(parents=True, exist_ok=True)
        content = get(url)
        if name.endswith('.parquet'):
            assert content[:4] == b'PAR1' and content[-4:] == b'PAR1', name
        path.write_bytes(content)
        print(f'Downloaded {dataset}/{name}: {len(content):,} bytes', flush=True)
        return {'dataset': dataset, 'path': str(path.relative_to(ROOT)).replace('\\', '/'),
                'url': url, 'bytes': len(content), 'sha256': hashlib.sha256(content).hexdigest()}

    with ThreadPoolExecutor(max_workers=4) as pool:
        files = list(pool.map(fetch, jobs))
    save_json(ROOT / 'sources.json', {'sources': sources, 'files': files})


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--download-only', action='store_true')
    parser.add_argument('--offline', action='store_true')
    args = parser.parse_args()
    if not args.offline:
        download()
    if not args.download_only:
        normalize()
