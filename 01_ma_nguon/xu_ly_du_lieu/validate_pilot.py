"""Validate pilot dataset or exported reviewed bundle for consistency, schema, and rules (Python 3.11+).

Supports runtime validation without relying on Python assertions (works with -O).
Validates:
- Exact 120 IDs matching reference pilot (rejects arbitrary prepared questions).
- Source field immutability.
- Strict ASCII YYYY-MM-DD date existence (rejects 2026-02-30, 2026-1-2, ２０２６-11-28).
- Equivalence between CSV and JSONL in bundle.
- Re-computed review_summary (types, values, and training readiness boundaries).
- Complete provenance manifest schema and 64-hex reference checksum verification.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / '02_du_lieu' / 'filedata'
DEFAULT_PILOT_DIR = DATA_DIR / 'reviewed' / 'pilot'

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pilot_rules as rules

HEX_SHA256_PATTERN = re.compile(r'^[0-9a-fA-F]{64}$')
REQUIRED_REF_FILES = (
    'questions_pilot.csv',
    'questions_pilot.jsonl',
    'sampling_manifest.json'
)


def validate_review_summary_strict(summary: dict, jsonl_rows: list[dict], manifest_path: Path) -> None:
    """Strictly validate each field, type, and value of review_summary against computed ground truth."""
    computed = rules.compute_review_summary(jsonl_rows)
    expected_fields = [
        ('total_records', int),
        ('status_counts', dict),
        ('usable_for_training_count', int),
        ('gold_label_distribution', dict),
        ('annotation_complete', bool),
        ('train_readiness_status', str),
        ('ready_for_training', bool),
    ]

    for field, expected_type in expected_fields:
        if field not in summary:
            sys.exit(f"Loi: review_summary trong {manifest_path} thieu truong bat buoc: '{field}'")
        actual_val = summary[field]

        # Enforce exact boolean vs int separation (in Python, bool is subclass of int)
        if expected_type is bool:
            if not isinstance(actual_val, bool) or type(actual_val) is not bool:
                sys.exit(
                    f"Loi: review_summary.{field} sai kieu: mong doi bool, nhan duoc {type(actual_val).__name__} ({actual_val})"
                )
        elif expected_type is int:
            if isinstance(actual_val, bool) or type(actual_val) is not int:
                sys.exit(
                    f"Loi: review_summary.{field} sai kieu: mong doi int, nhan duoc {type(actual_val).__name__} ({actual_val})"
                )
        elif expected_type is dict:
            if not isinstance(actual_val, dict) or type(actual_val) is not dict:
                sys.exit(
                    f"Loi: review_summary.{field} sai kieu: mong doi dict, nhan duoc {type(actual_val).__name__} ({actual_val})"
                )
        else:
            if type(actual_val) is not expected_type:
                sys.exit(
                    f"Loi: review_summary.{field} sai kieu: mong doi {expected_type.__name__}, nhan duoc {type(actual_val).__name__}"
                )

        # Enforce exact value match for scalar fields
        if expected_type is not dict:
            expected_val = computed[field]
            if actual_val != expected_val:
                sys.exit(
                    f"Loi: review_summary.{field} sai gia tri:\n"
                    f"  Manifest: {actual_val}\n"
                    f"  Thuc te:  {expected_val}"
                )

    # In pilot phase, ready_for_training must always be strictly False
    if summary.get('ready_for_training') is not False:
        sys.exit(f"Loi: review_summary.ready_for_training bat buoc phai la False trong giai doan pilot")

    # Strictly validate status_counts keys, types (non-bool int), and values
    try:
        rules.validate_count_dict(summary['status_counts'], computed['status_counts'], 'status_counts')
    except ValueError as exc:
        sys.exit(str(exc))

    # Strictly validate gold_label_distribution keys, types (non-bool int), and values
    try:
        rules.validate_count_dict(summary['gold_label_distribution'], computed['gold_label_distribution'], 'gold_label_distribution')
    except ValueError as exc:
        sys.exit(str(exc))


def validate_manifest_schema_and_checksums(
    manifest: dict,
    manifest_path: Path,
    is_reviewed_bundle: bool,
    jsonl_rows: list[dict],
    ref_pilot_dir: Path
) -> None:
    """Validate manifest schema completeness, provenance links, and SHA-256 hashes."""
    if is_reviewed_bundle:
        # Schema check for review_manifest.json
        required_root = [
            'created_at_utc',
            'source_input_csv',
            'reference_pilot',
            'output_files',
            'review_summary',
            'reviewed_ids',
        ]
        for field in required_root:
            if field not in manifest:
                sys.exit(f"Loi: Manifest {manifest_path} thieu truong bat buoc '{field}'")

        # 1. created_at_utc
        created_at = manifest['created_at_utc']
        if not isinstance(created_at, str) or not created_at.strip():
            sys.exit(f"Loi: Manifest.created_at_utc phai la chuoi khong rong")

        # 2. source_input_csv
        src_csv = manifest['source_input_csv']
        if not isinstance(src_csv, dict):
            sys.exit(f"Loi: Manifest.source_input_csv phai la dict")
        if not isinstance(src_csv.get('path'), str) or not src_csv['path'].strip():
            sys.exit(f"Loi: source_input_csv.path phai la chuoi khong rong")
        sha = src_csv.get('sha256', '')
        if not isinstance(sha, str) or not HEX_SHA256_PATTERN.fullmatch(sha):
            sys.exit(f"Loi: source_input_csv.sha256 khong hop le (phai la 64 ky tu hex): '{sha}'")

        # 3. reference_pilot
        ref_info = manifest['reference_pilot']
        if not isinstance(ref_info, dict):
            sys.exit(f"Loi: Manifest.reference_pilot phai la dict")
        if not isinstance(ref_info.get('path'), str) or not ref_info['path'].strip():
            sys.exit(f"Loi: reference_pilot.path phai la chuoi khong rong")

        checksums = ref_info.get('sha256_checksums')
        if not isinstance(checksums, dict) or not checksums:
            sys.exit(f"Loi: reference_pilot.sha256_checksums khong duoc de trong")

        for fname in REQUIRED_REF_FILES:
            if fname not in checksums:
                sys.exit(f"Loi: reference_pilot.sha256_checksums thieu file '{fname}'")
            f_sha = checksums[fname]
            if not isinstance(f_sha, str) or not HEX_SHA256_PATTERN.fullmatch(f_sha):
                sys.exit(f"Loi: Checksum cho '{fname}' trong manifest khong hop le (phai la 64 ky tu hex): '{f_sha}'")

            ref_file = ref_pilot_dir / fname
            if not ref_file.exists():
                sys.exit(f"Loi: Thu muc pilot tham chieu '{ref_pilot_dir}' thieu file bat buoc '{fname}'")

            real_sha = rules.compute_sha256(ref_file)
            if f_sha != real_sha:
                sys.exit(
                    f"Loi: Checksum pilot tham chieu cho '{fname}' trong manifest ({f_sha}) "
                    f"khong khop voi pilot tham chieu thuc te ({real_sha})"
                )

        # 4. output_files
        out_files = manifest['output_files']
        if not isinstance(out_files, dict):
            sys.exit(f"Loi: Manifest.output_files phai la dict")
        if not isinstance(out_files.get('csv'), str) or not out_files['csv'].strip():
            sys.exit(f"Loi: output_files.csv phai la chuoi khong rong")
        if not isinstance(out_files.get('jsonl'), str) or not out_files['jsonl'].strip():
            sys.exit(f"Loi: output_files.jsonl phai la chuoi khong rong")

        # 5. reviewed_ids
        reviewed_ids = manifest['reviewed_ids']
        if not isinstance(reviewed_ids, list) or len(reviewed_ids) != rules.EXPECTED_PILOT_TOTAL:
            sys.exit(f"Loi: Manifest.reviewed_ids phai la danh sach chua dung {rules.EXPECTED_PILOT_TOTAL} ID")

        actual_sorted_ids = sorted(r['id'] for r in jsonl_rows)
        if reviewed_ids != actual_sorted_ids:
            sys.exit(f"Loi: Danh sach ID trong manifest khong khop voi ID thuc te cua du lieu")

        # 6. review_summary
        validate_review_summary_strict(manifest['review_summary'], jsonl_rows, manifest_path)

    else:
        # Schema check for sampling_manifest.json (original pilot)
        required_root = [
            'created_at_utc',
            'seed',
            'input_file',
            'output_files',
            'sampling_strategy',
            'statistics',
            'selected_ids',
        ]
        for field in required_root:
            if field not in manifest:
                sys.exit(f"Loi: Manifest {manifest_path} thieu truong bat buoc '{field}'")

        if not isinstance(manifest['created_at_utc'], str) or not manifest['created_at_utc'].strip():
            sys.exit("Loi: sampling_manifest.created_at_utc phai la chuoi khong rong")
        if type(manifest['seed']) is not int or isinstance(manifest['seed'], bool):
            sys.exit("Loi: sampling_manifest.seed phai la kieu int")

        in_f = manifest['input_file']
        if not isinstance(in_f, dict) or not isinstance(in_f.get('path'), str) or not in_f['path'].strip():
            sys.exit("Loi: input_file.path phai la chuoi khong rong")
        if not isinstance(in_f.get('sha256'), str) or not HEX_SHA256_PATTERN.fullmatch(in_f['sha256']):
            sys.exit("Loi: input_file.sha256 khong hop le")

        out_f = manifest['output_files']
        if not isinstance(out_f, dict) or not isinstance(out_f.get('csv'), str) or not isinstance(out_f.get('jsonl'), str):
            sys.exit("Loi: output_files phai chua duong dan csv va jsonl")

        selected_ids = manifest['selected_ids']
        if not isinstance(selected_ids, list) or len(selected_ids) != rules.EXPECTED_PILOT_TOTAL:
            sys.exit(f"Loi: selected_ids phai la danh sach chua dung {rules.EXPECTED_PILOT_TOTAL} ID")

        actual_sorted_ids = sorted(r['id'] for r in jsonl_rows)
        if selected_ids != actual_sorted_ids:
            sys.exit("Loi: selected_ids trong sampling_manifest khong khop voi du lieu thuc te")


def validate_bundle(
    target_dir: Path,
    mode: str = 'auto',
    reference_pilot_dir: Path = DEFAULT_PILOT_DIR
) -> bool:
    target_dir = target_dir.resolve()
    ref_pilot_dir = reference_pilot_dir.resolve()
    print(f"Validating dataset in '{target_dir}' (mode: {mode})...")

    # 1. Determine target files
    if (target_dir / 'questions_reviewed.csv').exists() or (target_dir / 'questions_reviewed.jsonl').exists():
        csv_path = target_dir / 'questions_reviewed.csv'
        jsonl_path = target_dir / 'questions_reviewed.jsonl'
        manifest_path = target_dir / 'review_manifest.json'
        is_reviewed_bundle = True
    else:
        csv_path = target_dir / 'questions_pilot.csv'
        jsonl_path = target_dir / 'questions_pilot.jsonl'
        manifest_path = target_dir / 'sampling_manifest.json'
        is_reviewed_bundle = False

    if not csv_path.exists():
        sys.exit(f"Loi: Thieu file CSV: {csv_path}")
    if not jsonl_path.exists():
        sys.exit(f"Loi: Thieu file JSONL: {jsonl_path}")
    if not manifest_path.exists():
        sys.exit(f"Loi: Thieu file Manifest: {manifest_path}")

    # 2. Load reference pilot (strictly 120 canonical IDs)
    try:
        ref_pilot = rules.load_reference_pilot(ref_pilot_dir)
    except Exception as exc:
        sys.exit(f"Loi khi nap pilot tham chieu tu '{ref_pilot_dir}': {exc}")

    valid_labels = rules.load_valid_topic_labels()

    # 3. Read JSONL
    jsonl_rows = []
    with jsonl_path.open('r', encoding='utf-8') as f:
        for idx, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                item = json.loads(line)
            except Exception as exc:
                sys.exit(f"Loi cu phap JSONL tai dong {idx} trong {jsonl_path}: {exc}")
            jsonl_rows.append(item)

    if len(jsonl_rows) != rules.EXPECTED_PILOT_TOTAL:
        sys.exit(f"Loi: File JSONL {jsonl_path} co {len(jsonl_rows)} dong, yeu cau dung {rules.EXPECTED_PILOT_TOTAL} dong")

    # Check IDs against reference pilot
    jsonl_ids = [r.get('id', '').strip() for r in jsonl_rows]
    if len(jsonl_ids) != len(set(jsonl_ids)):
        sys.exit(f"Loi: File JSONL {jsonl_path} chua ID trung lap")

    missing_ids = set(ref_pilot.keys()) - set(jsonl_ids)
    extra_ids = set(jsonl_ids) - set(ref_pilot.keys())
    if missing_ids or extra_ids:
        sys.exit(
            f"Loi vi pham tap ID pilot tham chieu trong {jsonl_path}:\n"
            f"- ID thieu: {missing_ids}\n"
            f"- ID la/ngoai pilot: {extra_ids}"
        )

    # Detect auto mode
    has_annotations = any(
        r.get('gold_topic_label') or
        r.get('review_status') not in (None, '', 'pending_manual_review') or
        r.get('reviewer_id') or
        r.get('reviewed_at') or
        r.get('review_note')
        for r in jsonl_rows
    )
    effective_mode = mode
    if mode == 'auto':
        effective_mode = 'annotated' if (has_annotations or is_reviewed_bundle) else 'initial'
        print(f"Che do tu dong nhan dien: {effective_mode}")

    # Validate each JSONL row against rules and reference pilot
    all_row_errors = []
    for idx, r in enumerate(jsonl_rows, 1):
        missing_cols = [c for c in rules.COLUMNS if c not in r]
        if missing_cols:
            all_row_errors.append(f"JSONL dong {idx}: Thieu cot {missing_cols}")
            continue

        row_id = r['id']
        ref_row = ref_pilot[row_id]
        row_errs = rules.validate_single_row(
            row=r,
            ref_row=ref_row,
            valid_labels=valid_labels,
            line_desc=f"JSONL dong {idx}",
            allow_pending=(effective_mode == 'initial' or is_reviewed_bundle)
        )
        all_row_errors.extend(row_errs)

        if effective_mode == 'initial':
            status = r.get('review_status', '')
            gold = r.get('gold_topic_label', '')
            rev = r.get('reviewer_id', '')
            rev_at = r.get('reviewed_at', '')
            note = r.get('review_note', '')
            if status != 'pending_manual_review':
                all_row_errors.append(f"JSONL dong {idx} ({row_id}): initial mode yeu cau review_status='pending_manual_review', nhung co '{status}'")
            if gold != '':
                all_row_errors.append(f"JSONL dong {idx} ({row_id}): initial mode yeu cau gold_topic_label de trong, nhung co '{gold}'")
            if rev != '':
                all_row_errors.append(f"JSONL dong {idx} ({row_id}): initial mode yeu cau reviewer_id de trong, nhung co '{rev}'")
            if rev_at != '':
                all_row_errors.append(f"JSONL dong {idx} ({row_id}): initial mode yeu cau reviewed_at de trong, nhung co '{rev_at}'")
            if note != '':
                all_row_errors.append(f"JSONL dong {idx} ({row_id}): initial mode yeu cau review_note de trong, nhung co '{note}'")

    if all_row_errors:
        sys.exit(f"PHAT HIEN {len(all_row_errors)} LOI TRONG JSONL:\n" + "\n".join(f"- {e}" for e in all_row_errors))

    # 4. Read and validate CSV equivalence
    with csv_path.open('r', encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            sys.exit(f"Loi: CSV rong: {csv_path}")
        missing_csv_cols = [c for c in rules.COLUMNS if c not in reader.fieldnames]
        if missing_csv_cols:
            sys.exit(f"Loi: CSV thieu cot: {missing_csv_cols}")
        csv_rows = list(reader)

    if len(csv_rows) != rules.EXPECTED_PILOT_TOTAL:
        sys.exit(f"Loi: CSV co {len(csv_rows)} dong, yeu cau dung {rules.EXPECTED_PILOT_TOTAL} dong")

    csv_by_id = {}
    for idx, c_row in enumerate(csv_rows, 1):
        cid = c_row.get('id', '').strip()
        if not cid:
            sys.exit(f"Loi: CSV dong {idx} thieu 'id'")
        if cid in csv_by_id:
            sys.exit(f"Loi: CSV dong {idx} trung lap id='{cid}'")
        csv_by_id[cid] = c_row

    if set(csv_by_id.keys()) != set(jsonl_ids):
        sys.exit("Loi: Tap ID giua CSV va JSONL khong khop nhau hoan toan")

    # Strict column-by-column equivalence between CSV and JSONL
    for idx, j_row in enumerate(jsonl_rows, 1):
        row_id = j_row['id']
        c_row = csv_by_id[row_id]
        for col in rules.COLUMNS:
            expected_val = j_row[col]
            if isinstance(expected_val, (list, dict)):
                expected_str = json.dumps(expected_val, ensure_ascii=False, separators=(',', ':'))
            elif isinstance(expected_val, str) and expected_val.startswith(('=', '+', '-', '@')):
                expected_str = "'" + expected_val
            else:
                expected_str = str(expected_val)

            actual_str = str(c_row[col])
            if actual_str != expected_str:
                sys.exit(
                    f"Loi khong tuong duong giua JSONL va CSV tai row_id='{row_id}', cot '{col}':\n"
                    f"  JSONL: '{expected_str}'\n"
                    f"  CSV:   '{actual_str}'"
                )

    # 5. Validate Manifest Schema and Provenance Checksums
    with manifest_path.open('r', encoding='utf-8') as f:
        try:
            manifest = json.load(f)
        except Exception as exc:
            sys.exit(f"Loi doc manifest {manifest_path}: {exc}")

    validate_manifest_schema_and_checksums(
        manifest=manifest,
        manifest_path=manifest_path,
        is_reviewed_bundle=is_reviewed_bundle,
        jsonl_rows=jsonl_rows,
        ref_pilot_dir=ref_pilot_dir
    )

    # 6. Check markdown links in documentation
    doc_paths = [
        PROJECT_ROOT / '06_tai_lieu' / 'HUONG_DAN_GAN_NHAN.md',
        PROJECT_ROOT / '05_bao_cao' / 'kiem_tra_du_lieu' / 'BAO_CAO_CHUAN_BI_GAN_NHAN.md',
    ]
    link_errors = []
    for doc in doc_paths:
        if doc.exists():
            link_errors.extend(rules.check_markdown_relative_links(doc))
    if link_errors:
        sys.exit(f"Loi lien ket tuong doi trong tai lieu:\n" + "\n".join(f"- {e}" for e in link_errors))

    print(
        f"THANH CONG: Bo du lieu hop le (che do '{effective_mode}').\n"
        f"- 120 ID khop pilot tham chieu 100%.\n"
        f"- CSV va JSONL tuong duong tuyet doi.\n"
        f"- Quy tac nhan va ngay thang ASCII YYYY-MM-DD da kiem tra.\n"
        f"- Manifest khop thong ke, schema va checksum truy vet 100%."
    )
    return True


def main():
    parser = argparse.ArgumentParser(description='Validate pilot dataset or exported reviewed bundle.')
    parser.add_argument('--pilot-dir', type=Path, default=DEFAULT_PILOT_DIR,
                        help=f'Path to pilot directory or exported reviewed bundle (default: {DEFAULT_PILOT_DIR})')
    parser.add_argument('--mode', choices=['initial', 'annotated', 'auto'], default='auto',
                        help="Validation mode: 'initial' (all blank), 'annotated' (valid annotations), or 'auto' (default: 'auto')")
    parser.add_argument('--reference-pilot-dir', type=Path, default=DEFAULT_PILOT_DIR,
                        help=f'Reference pilot directory (default: {DEFAULT_PILOT_DIR})')
    args = parser.parse_args()

    validate_bundle(
        target_dir=args.pilot_dir,
        mode=args.mode,
        reference_pilot_dir=args.reference_pilot_dir
    )


if __name__ == '__main__':
    main()
