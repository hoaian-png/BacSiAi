"""Validate and export manually reviewed pilot annotations from CSV (Python 3.11+).

Allows annotators to work exclusively in Excel via CSV while ensuring full
traceability, schema conformance, and non-destructive versioned exports.
"""
from __future__ import annotations

import argparse
import csv
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / '02_du_lieu' / 'filedata'
DEFAULT_PILOT_DIR = DATA_DIR / 'reviewed' / 'pilot'

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pilot_rules as rules


def validate_reviewed_csv(
    input_csv: Path,
    ref_pilot: dict[str, dict],
    valid_labels: set[str]
) -> tuple[list[dict], dict]:
    """Strictly validate manually edited CSV against reference pilot and labeling rules."""
    if not input_csv.exists():
        sys.exit(f"Loi: File CSV dau vao khong ton tai: {input_csv}")

    # Read CSV (supports utf-8 and utf-8-sig automatically via utf-8-sig)
    with input_csv.open('r', encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            sys.exit(f"Loi: File CSV rong: {input_csv}")

        missing_cols = [c for c in rules.COLUMNS if c not in reader.fieldnames]
        if missing_cols:
            sys.exit(f"Loi: File CSV thieu cot bat buoc: {missing_cols}")

        csv_rows = list(reader)

    if len(csv_rows) != rules.EXPECTED_PILOT_TOTAL:
        sys.exit(f"Loi: File CSV phai co dung {rules.EXPECTED_PILOT_TOTAL} dong du lieu, hien co {len(csv_rows)} dong")

    seen_ids = set()
    errors: list[str] = []
    processed_rows: list[dict] = []

    for idx, row in enumerate(csv_rows, 1):
        row_id = row.get('id', '').strip()
        if not row_id:
            errors.append(f"Dong {idx}: Thieu 'id'")
            continue
        if row_id in seen_ids:
            errors.append(f"Dong {idx}: Trung lap id='{row_id}'")
            continue
        seen_ids.add(row_id)

        if row_id not in ref_pilot:
            errors.append(f"Dong {idx}: ID '{row_id}' khong thuoc danh sach 120 cau pilot tham chieu")
            continue

        ref_row = ref_pilot[row_id]
        row_errors = rules.validate_single_row(
            row=row,
            ref_row=ref_row,
            valid_labels=valid_labels,
            line_desc=f"Dong {idx}",
            allow_pending=True
        )
        errors.extend(row_errors)

        if not row_errors:
            # Reconstruct clean row with true JSON list structures
            status = row.get('review_status', '').strip()
            gold_label = row.get('gold_topic_label', '').strip()
            clean_row = {
                'id': row_id,
                'dataset': ref_row['dataset'],
                'question': ref_row['question'],
                'group_id': ref_row.get('group_id', ''),
                'provenance_ids': ref_row.get('provenance_ids', []),
                'topic_candidates': ref_row.get('topic_candidates', []),
                'suggested_topic_label': ref_row.get('suggested_topic_label', ref_row.get('topic_label', '')),
                'keywords': ref_row.get('keywords', []),
                'gold_topic_label': gold_label if status == 'reviewed' else '',
                'review_status': status,
                'reviewer_id': row.get('reviewer_id', '').strip(),
                'reviewed_at': row.get('reviewed_at', '').strip(),
                'review_note': row.get('review_note', '').strip(),
            }
            processed_rows.append(clean_row)

    if errors:
        error_msg = f"PHAT HIEN {len(errors)} LOI TRONG FILE CSV '{input_csv}':\n" + "\n".join(f"- {e}" for e in errors)
        sys.exit(error_msg)

    # Check for missing IDs from reference pilot
    missing_from_pilot = set(ref_pilot.keys()) - seen_ids
    if missing_from_pilot:
        sys.exit(f"Loi: File CSV thieu {len(missing_from_pilot)} ID tu tap pilot goc: {missing_from_pilot}")

    summary = rules.compute_review_summary(processed_rows)
    return processed_rows, summary


def export_reviewed_dataset(
    rows: list[dict],
    summary: dict,
    input_csv: Path,
    pilot_dir: Path,
    output_dir: Path
) -> None:
    """Safely export reviewed bundle with path protection and clean rollbacks on failure."""
    # Enforce safe output directory at function entry (protects direct programmatic calls)
    rules.assert_safe_output_dir(output_dir, pilot_dir, input_csv)

    sorted_rows = sorted(rows, key=lambda x: x['id'])
    output_dir.mkdir(parents=True, exist_ok=False)

    out_csv = output_dir / 'questions_reviewed.csv'
    out_jsonl = output_dir / 'questions_reviewed.jsonl'
    out_manifest = output_dir / 'review_manifest.json'

    try:
        # 1. Export JSONL (UTF-8)
        with out_jsonl.open('w', encoding='utf-8') as f:
            for r in sorted_rows:
                f.write(json.dumps(r, ensure_ascii=False) + '\n')

        # 2. Export CSV (UTF-8 with BOM for Excel)
        with out_csv.open('w', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=rules.COLUMNS)
            writer.writeheader()
            for r in sorted_rows:
                row_dict = {}
                for col in rules.COLUMNS:
                    val = r[col]
                    if isinstance(val, (list, dict)):
                        val = json.dumps(val, ensure_ascii=False, separators=(',', ':'))
                    elif isinstance(val, str) and val.startswith(('=', '+', '-', '@')):
                        val = "'" + val
                    row_dict[col] = val
                writer.writerow(row_dict)

        # 3. Compute reference pilot checksums
        ref_checksums = {}
        for fname in ('questions_pilot.csv', 'questions_pilot.jsonl', 'sampling_manifest.json'):
            fpath = pilot_dir / fname
            if fpath.exists():
                ref_checksums[fname] = rules.compute_sha256(fpath)

        # 4. Relative paths for manifest
        try:
            source_csv_rel = str(input_csv.relative_to(PROJECT_ROOT)).replace('\\', '/')
        except ValueError:
            source_csv_rel = str(input_csv).replace('\\', '/')

        try:
            out_csv_rel = str(out_csv.relative_to(PROJECT_ROOT)).replace('\\', '/')
            out_jsonl_rel = str(out_jsonl.relative_to(PROJECT_ROOT)).replace('\\', '/')
        except ValueError:
            out_csv_rel = str(out_csv).replace('\\', '/')
            out_jsonl_rel = str(out_jsonl).replace('\\', '/')

        manifest = {
            'created_at_utc': datetime.now(timezone.utc).isoformat(),
            'source_input_csv': {
                'path': source_csv_rel,
                'sha256': rules.compute_sha256(input_csv),
            },
            'reference_pilot': {
                'path': str(pilot_dir.relative_to(PROJECT_ROOT) if pilot_dir.is_relative_to(PROJECT_ROOT) else pilot_dir).replace('\\', '/'),
                'sha256_checksums': ref_checksums,
            },
            'output_files': {
                'csv': out_csv_rel,
                'jsonl': out_jsonl_rel,
            },
            'review_summary': summary,
            'notes': [
                'Du lieu xuat tu quy trinh gan nhan CSV qua Excel sau khi vuot qua kiem tra nghiem ngat.',
                'annotation_complete chi True khi khong con pending va khong con needs_discussion.',
                'Pilot chua danh gia dieu kien san sang huan luyen (train_readiness_status: not_evaluated_in_pilot_phase).',
            ],
            'reviewed_ids': [r['id'] for r in sorted_rows],
        }

        with out_manifest.open('w', encoding='utf-8') as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)

    except Exception:
        # Clean up partial directory if write failed
        shutil.rmtree(output_dir, ignore_errors=True)
        raise


def main():
    parser = argparse.ArgumentParser(description='Validate and export reviewed pilot annotations from CSV.')
    parser.add_argument('--input-csv', type=Path, required=True,
                        help='Path to the manually edited CSV file (e.g. reviewed/working/questions_working.csv)')
    parser.add_argument('--output-dir', type=Path, default=None,
                        help='Destination directory for reviewed export (must not exist, e.g. reviewed/annotations/v1)')
    parser.add_argument('--reference-pilot-dir', type=Path, default=DEFAULT_PILOT_DIR,
                        help=f'Path to the reference pilot directory (default: {DEFAULT_PILOT_DIR})')
    parser.add_argument('--check-only', action='store_true',
                        help='Run validation checks only; do not export files')
    args = parser.parse_args()

    input_csv = args.input_csv.resolve()
    pilot_dir = args.reference_pilot_dir.resolve()

    if not input_csv.exists():
        sys.exit(f"Loi: File CSV dau vao khong ton tai: {input_csv}")

    print(f"Nap du lieu tham chieu tu {pilot_dir}...")
    try:
        ref_pilot = rules.load_reference_pilot(pilot_dir)
    except Exception as exc:
        sys.exit(f"Loi khi doc pilot tham chieu: {exc}")

    valid_labels = rules.load_valid_topic_labels()

    print(f"Kiem tra tinh hop le cua file CSV: {input_csv}...")
    rows, summary = validate_reviewed_csv(input_csv, ref_pilot, valid_labels)

    print("\n" + "=" * 60)
    print("KET QUA KIEM TRA DU LIEU GAN NHAN (CSV):")
    print(f"- Tong so ban ghi: {summary['total_records']}")
    print(f"- Da hoan tat duyet (reviewed): {summary['status_counts']['reviewed']}")
    print(f"- Can thao luan them (needs_discussion): {summary['status_counts']['needs_discussion']}")
    print(f"- Loai khoi tap TMH (excluded): {summary['status_counts']['excluded']}")
    print(f"- Con chua duyet (pending_manual_review): {summary['status_counts']['pending_manual_review']}")
    print(f"- So cau co the dung train (reviewed co nhan hop le): {summary['usable_for_training_count']}")
    print(f"- Trang thai hoan tat danh sach (annotation_complete): {'CO' if summary['annotation_complete'] else 'CHUA'}")
    print(f"- Dieu kien huan luyen: {summary['train_readiness_status']} (Chua danh gia o giai doan pilot)")
    if summary['gold_label_distribution']:
        print("\nPhan bo nhan da duyet (gold_topic_label):")
        for lbl, count in sorted(summary['gold_label_distribution'].items()):
            print(f"  + {lbl}: {count}")
    print("=" * 60 + "\n")

    if args.check_only:
        print("Che do --check-only: Kiem tra thanh cong, khong tao file hoac thu muc.")
        return

    if args.output_dir is None:
        sys.exit("Loi: Phai chi dinh --output-dir khi xuat du lieu (hoac dung --check-only neu chi muon kiem tra).")

    output_dir = args.output_dir.resolve()
    try:
        rules.assert_safe_output_dir(output_dir, pilot_dir, input_csv)
    except Exception as exc:
        sys.exit(f"Loi bao ve duong dan: {exc}")

    print(f"Xuat du lieu da kiem tra vao {output_dir}...")
    try:
        export_reviewed_dataset(rows, summary, input_csv, pilot_dir, output_dir)
    except Exception as exc:
        sys.exit(f"Loi khi xuat du lieu: {exc}")

    print("Xuat thanh cong bo du lieu: questions_reviewed.csv, questions_reviewed.jsonl, review_manifest.json.")


if __name__ == '__main__':
    main()
