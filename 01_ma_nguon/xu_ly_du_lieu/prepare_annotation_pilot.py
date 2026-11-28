"""Prepare reproducible pilot annotation dataset for topic labeling (Python 3.11+).

This script selects a stratified sample of 120 real candidate questions from
02_du_lieu/filedata/prepared/questions_ent.jsonl, covering 8 starter topics,
multi-topic questions, unassigned questions, negation cases, and all 3 datasets.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import random
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / '02_du_lieu' / 'filedata'
INPUT_PATH = DATA_DIR / 'prepared' / 'questions_ent.jsonl'
DEFAULT_OUTPUT_DIR = DATA_DIR / 'reviewed' / 'pilot'

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pilot_rules as rules

COLUMNS = rules.COLUMNS

TARGET_QUOTAS = {
    # Single-topic candidates (suggested_topic_label in 8 starter topics)
    'ho_dom': 10,
    'trieu_chung_mui': 10,
    'xoang': 10,
    'hong_amidan': 10,
    'trieu_chung_tai': 10,
    'cam_cum': 10,
    'sot': 10,
    'cam_lanh': 8,  # only 32 exist in total
    # Multi-topic and unassigned candidates
    'multiple_topics': 28,
    'unassigned_no_keywords': 14,
}


def load_input_rows(path: Path) -> list[dict]:
    rows = []
    with path.open('r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            item = json.loads(line)
            item['_line_num'] = line_num
            rows.append(item)
    return rows


def is_manually_edited_record(row: dict) -> bool:
    """Check if any manual review field contains custom data."""
    if row.get('gold_topic_label'):
        return True
    status = row.get('review_status')
    if status and status != 'pending_manual_review':
        return True
    if row.get('reviewer_id'):
        return True
    if row.get('reviewed_at'):
        return True
    if row.get('review_note'):
        return True
    return False


def check_existing_annotations(csv_path: Path, jsonl_path: Path) -> tuple[bool, str]:
    """Return (True, reason) if any target file exists and contains manual annotations."""
    if jsonl_path.exists():
        with jsonl_path.open('r', encoding='utf-8') as f:
            for idx, line in enumerate(f, 1):
                if not line.strip():
                    continue
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    return True, f'File JSONL {jsonl_path} bi loi cu phap hoac da bi can thiep tai dong {idx}.'
                if is_manually_edited_record(row):
                    return True, f'File JSONL {jsonl_path} chua du lieu gan nhan/chinh sua thu cong tai dong {idx} (id={row.get("id")}).'

    if csv_path.exists():
        with csv_path.open('r', encoding='utf-8-sig', newline='') as f:
            reader = csv.DictReader(f)
            for idx, row in enumerate(reader, 1):
                if is_manually_edited_record(row):
                    return True, f'File CSV {csv_path} chua du lieu gan nhan/chinh sua thu cong tai dong {idx} (id={row.get("id")}).'

    return False, ''


def categorize_row(row: dict) -> str:
    topic_candidates = row.get('topic_candidates', [])
    topic_label = row.get('topic_label', '')
    if len(topic_candidates) == 1 and topic_label:
        return topic_label
    elif len(topic_candidates) > 1:
        return 'multiple_topics'
    else:
        return 'unassigned_no_keywords'


def sample_pilot_questions(rows: list[dict], seed: int = 42) -> tuple[list[dict], dict]:
    rng = random.Random(seed)

    # Group candidates by category
    buckets: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        cat = categorize_row(r)
        buckets[cat].append(r)

    selected_rows: list[dict] = []
    selected_ids: set[str] = set()
    selected_question_groups: set[str] = set()
    category_counts: dict[str, int] = defaultdict(int)

    # For each category, sample with diversity across datasets and prioritize negation cases
    for cat, quota in TARGET_QUOTAS.items():
        candidates = buckets.get(cat, [])
        if not candidates:
            continue

        # Split candidates into negation review required vs normal
        neg_candidates = [c for c in candidates if c.get('negation_review_required')]
        norm_candidates = [c for c in candidates if not c.get('negation_review_required')]

        # Shuffle deterministically
        rng.shuffle(neg_candidates)
        rng.shuffle(norm_candidates)

        # Decide how many negation cases to include (1-2 per category if available)
        neg_target = min(len(neg_candidates), max(1, quota // 5) if neg_candidates else 0)

        cat_picked: list[dict] = []

        # Pick from negation candidates first
        for item in neg_candidates:
            if len(cat_picked) >= neg_target:
                break
            qg = item.get('question_group_id')
            if item['id'] not in selected_ids and qg not in selected_question_groups:
                cat_picked.append(item)
                selected_ids.add(item['id'])
                selected_question_groups.add(qg)

        # Then pick from normal candidates, balancing datasets
        by_dataset = defaultdict(list)
        for item in norm_candidates:
            by_dataset[item['dataset']].append(item)

        datasets = sorted(by_dataset.keys())
        ds_idx = 0
        while len(cat_picked) < quota and any(by_dataset.values()):
            curr_ds = datasets[ds_idx % len(datasets)]
            ds_idx += 1
            if not by_dataset[curr_ds]:
                continue
            item = by_dataset[curr_ds].pop(0)
            qg = item.get('question_group_id')
            if item['id'] not in selected_ids and qg not in selected_question_groups:
                cat_picked.append(item)
                selected_ids.add(item['id'])
                selected_question_groups.add(qg)

        # If quota still not met, grab any remaining candidate from bucket
        remaining = [c for c in candidates if c['id'] not in selected_ids and c.get('question_group_id') not in selected_question_groups]
        rng.shuffle(remaining)
        while len(cat_picked) < quota and remaining:
            item = remaining.pop(0)
            cat_picked.append(item)
            selected_ids.add(item['id'])
            selected_question_groups.add(item.get('question_group_id'))

        category_counts[cat] = len(cat_picked)
        selected_rows.extend(cat_picked)

    # Sort selected rows deterministically by id
    selected_rows.sort(key=lambda x: x['id'])

    # Format rows for pilot
    formatted_rows = []
    for r in selected_rows:
        formatted = {
            'id': r['id'],
            'dataset': r['dataset'],
            'question': r['question'],
            'group_id': r.get('group_id', ''),
            'provenance_ids': r.get('provenance_ids', []),
            'topic_candidates': r.get('topic_candidates', []),
            'suggested_topic_label': r.get('topic_label', ''),
            'keywords': r.get('keywords', []),
            'gold_topic_label': '',
            'review_status': 'pending_manual_review',
            'reviewer_id': '',
            'reviewed_at': '',
            'review_note': '',
            '_negation_review_required': r.get('negation_review_required', False),
            '_sampling_category': categorize_row(r),
        }
        formatted_rows.append(formatted)

    stats = {
        'total_selected': len(formatted_rows),
        'by_category': dict(category_counts),
        'by_dataset': dict(Counter(r['dataset'] for r in formatted_rows)),
        'by_suggested_label': dict(Counter(r['suggested_topic_label'] or 'unassigned_or_multiple' for r in formatted_rows)),
        'negation_review_count': sum(1 for r in formatted_rows if r['_negation_review_required']),
    }

    return formatted_rows, stats


def export_pilot(rows: list[dict], stats: dict, input_checksum: str, seed: int, output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / 'questions_pilot.csv'
    jsonl_path = output_dir / 'questions_pilot.jsonl'
    manifest_path = output_dir / 'sampling_manifest.json'

    # Clean rows for final export (remove private _ fields)
    export_rows = []
    for r in rows:
        item = {k: r[k] for k in rules.COLUMNS}
        export_rows.append(item)

    # Export JSONL (UTF-8)
    with jsonl_path.open('w', encoding='utf-8') as f:
        for r in export_rows:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')

    # Export CSV (UTF-8 with BOM for Excel compatibility)
    with csv_path.open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=rules.COLUMNS)
        writer.writeheader()
        for r in export_rows:
            row_dict = {}
            for col in rules.COLUMNS:
                val = r[col]
                if isinstance(val, (list, dict)):
                    val = json.dumps(val, ensure_ascii=False, separators=(',', ':'))
                elif isinstance(val, str) and val.startswith(('=', '+', '-', '@')):
                    val = "'" + val
                row_dict[col] = val
            writer.writerow(row_dict)

    # Resolve display paths for manifest
    try:
        manifest_csv_str = str(csv_path.relative_to(PROJECT_ROOT)).replace('\\', '/')
        manifest_jsonl_str = str(jsonl_path.relative_to(PROJECT_ROOT)).replace('\\', '/')
    except ValueError:
        manifest_csv_str = str(csv_path).replace('\\', '/')
        manifest_jsonl_str = str(jsonl_path).replace('\\', '/')

    # Export Manifest
    manifest = {
        'created_at_utc': datetime.now(timezone.utc).isoformat(),
        'seed': seed,
        'input_file': {
            'path': str(INPUT_PATH.relative_to(PROJECT_ROOT)).replace('\\', '/'),
            'sha256': input_checksum,
        },
        'output_files': {
            'csv': manifest_csv_str,
            'jsonl': manifest_jsonl_str,
        },
        'sampling_strategy': {
            'target_total': sum(TARGET_QUOTAS.values()),
            'target_quotas': TARGET_QUOTAS,
            'rules': [
                f'Deterministic random sample with seed={seed}',
                'Covers all 8 starter topics + multiple topics + unassigned topics',
                'Includes negation / context-demanding cases across categories',
                'Balanced representation across ViMQ, ViHealthQA, and ViMedAQA',
                'Strictly unique question_group_ids (no duplicate questions)',
                'Initial review_status is pending_manual_review',
                'gold_topic_label, reviewer_id, reviewed_at, and review_note left empty',
            ],
        },
        'statistics': stats,
        'selected_ids': [r['id'] for r in export_rows],
    }

    with manifest_path.open('w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(description='Prepare pilot annotation dataset for topic labeling.')
    parser.add_argument('--seed', type=int, default=42, help='Random seed for sampling (default: 42)')
    parser.add_argument('--output-dir', type=Path, default=DEFAULT_OUTPUT_DIR,
                        help=f'Output directory for pilot files (default: {DEFAULT_OUTPUT_DIR})')
    args = parser.parse_args()

    output_dir = args.output_dir.resolve()
    target_csv = output_dir / 'questions_pilot.csv'
    target_jsonl = output_dir / 'questions_pilot.jsonl'

    if not INPUT_PATH.exists():
        sys.exit(f'Error: Input file does not exist: {INPUT_PATH}')

    # Strict protection: Never overwrite manual work
    has_annotations, reason = check_existing_annotations(target_csv, target_jsonl)
    if has_annotations:
        sys.exit(
            f'NGAN GHI DE: Thu muc dich ({output_dir}) da chua du lieu gan nhan thu cong!\n'
            f'Ly do: {reason}\n'
            f'Tuyet doi khong ghi de ban da chinh sua. Neu muon tao ban moi, hay truyen --output-dir sang thu muc khac hoac sao luu truoc.'
        )

    print(f'Reading input questions from {INPUT_PATH}...')
    input_checksum = rules.compute_sha256(INPUT_PATH)
    rows = load_input_rows(INPUT_PATH)
    print(f'Total input questions: {len(rows)} (SHA-256: {input_checksum})')

    print(f'Sampling pilot questions (seed={args.seed})...')
    selected_rows, stats = sample_pilot_questions(rows, seed=args.seed)

    print(f'Sampled {len(selected_rows)} questions.')
    print(f'By category: {stats["by_category"]}')
    print(f'By dataset: {stats["by_dataset"]}')
    print(f'Negation review cases: {stats["negation_review_count"]}')

    print(f'Writing output to {output_dir}...')
    export_pilot(selected_rows, stats, input_checksum, args.seed, output_dir)
    print('Export completed successfully.')


if __name__ == '__main__':
    main()
