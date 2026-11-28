"""Shared rules, schema validation, and path protection for pilot dataset (Python 3.11+).

Provides a single source of truth for:
- Field names and data types.
- Strict ISO YYYY-MM-DD date validation.
- Reference pilot ID and source field integrity.
- Manual annotation rules (reviewed, needs_discussion, excluded, pending).
- Statistical computation and training readiness boundaries.
- Path resolution and directory overwrite protection.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / '02_du_lieu' / 'filedata'
DEFAULT_PILOT_DIR = DATA_DIR / 'reviewed' / 'pilot'
CONFIG_LABELS_PATH = DATA_DIR / 'config' / 'labels.json'
INPUT_PREPARED_PATH = DATA_DIR / 'prepared' / 'questions_ent.jsonl'

COLUMNS = [
    'id',
    'dataset',
    'question',
    'group_id',
    'provenance_ids',
    'topic_candidates',
    'suggested_topic_label',
    'keywords',
    'gold_topic_label',
    'review_status',
    'reviewer_id',
    'reviewed_at',
    'review_note',
]

SOURCE_COLUMNS = [
    'dataset',
    'question',
    'group_id',
    'suggested_topic_label',
]

LIST_COLUMNS = [
    'provenance_ids',
    'topic_candidates',
    'keywords',
]

VALID_STATUSES = {
    'pending_manual_review',
    'reviewed',
    'needs_discussion',
    'excluded',
}

EXPECTED_PILOT_TOTAL = 120


def compute_sha256(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open('rb') as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


def load_valid_topic_labels(config_path: Path | None = None) -> set[str]:
    cfg = config_path or CONFIG_LABELS_PATH
    if cfg.exists():
        with cfg.open('r', encoding='utf-8') as f:
            data = json.load(f)
            labels = set(data.get('labels', {}).keys())
            if labels:
                return labels
    return {
        'ho_dom', 'trieu_chung_mui', 'xoang', 'hong_amidan',
        'trieu_chung_tai', 'cam_lanh', 'cam_cum', 'sot'
    }


def is_valid_iso_date(val: str) -> bool:
    """Check if date matches exact ASCII [0-9]{4}-[0-9]{2}-[0-9]{2} format and is a real calendar date."""
    if not isinstance(val, str):
        return False
    val = val.strip()
    if not re.fullmatch(r'[0-9]{4}-[0-9]{2}-[0-9]{2}', val):
        return False
    try:
        datetime.strptime(val, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def unescape_excel_value(val: str) -> str:
    """Remove leading single quote added to prevent Excel formula execution."""
    if isinstance(val, str) and val.startswith("'") and len(val) > 1 and val[1] in ('=', '+', '-', '@'):
        return val[1:]
    return val if isinstance(val, str) else str(val)


def parse_list_field(val: str | list, field_name: str, row_id: str) -> list:
    """Parse JSON string list representation or return list directly."""
    if isinstance(val, list):
        return val
    if not isinstance(val, str):
        raise ValueError(f"Dong id='{row_id}', cot '{field_name}' co kieu khong hop le: {type(val)}")
    val = val.strip()
    if not val:
        return []
    try:
        parsed = json.loads(val)
        if not isinstance(parsed, list):
            raise ValueError(f"Khong phai kieu list JSON (nhan duoc {type(parsed).__name__})")
        return parsed
    except Exception as exc:
        raise ValueError(f"Dong id='{row_id}', cot '{field_name}' chua chuoi JSON loi: '{val}' ({exc})") from exc


def load_reference_pilot(pilot_dir: Path) -> dict[str, dict]:
    """Load canonical reference pilot records. Must contain exactly 120 unique records."""
    ref_jsonl = pilot_dir / 'questions_pilot.jsonl'
    if not ref_jsonl.exists():
        raise FileNotFoundError(f"Khong tim thay file JSONL pilot tham chieu: {ref_jsonl}")

    records = {}
    with ref_jsonl.open('r', encoding='utf-8') as f:
        for idx, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            item = json.loads(line)
            row_id = item['id']
            if row_id in records:
                raise ValueError(f"File pilot tham chieu {ref_jsonl} chua ID trung lap: '{row_id}'")
            records[row_id] = item

    if len(records) != EXPECTED_PILOT_TOTAL:
        raise ValueError(f"File pilot tham chieu {ref_jsonl} phai co dung {EXPECTED_PILOT_TOTAL} cau, thuc te co {len(records)}")
    return records


def validate_single_row(
    row: dict,
    ref_row: dict,
    valid_labels: set[str],
    line_desc: str = '',
    allow_pending: bool = True
) -> list[str]:
    """Validate a single record against reference pilot and labeling rules. Returns list of error strings."""
    errors: list[str] = []
    row_id = row.get('id', '').strip()
    prefix = f"{line_desc} (id='{row_id}'): " if line_desc else f"id='{row_id}': "

    # 1. Verify source fields match reference pilot
    for col in SOURCE_COLUMNS:
        actual_val = unescape_excel_value(row.get(col, '')).strip()
        expected_val = str(ref_row.get(col, '')).strip()
        if actual_val != expected_val:
            errors.append(
                f"{prefix}Cot du lieu nguon '{col}' bi sua doi!\n"
                f"  Goc: '{expected_val}'\n"
                f"  Nhan duoc: '{actual_val}'"
            )

    # 2. Verify list fields match reference pilot
    for col in LIST_COLUMNS:
        raw_val = row.get(col, [])
        if isinstance(raw_val, str):
            raw_val = unescape_excel_value(raw_val)
        try:
            parsed_list = parse_list_field(raw_val, col, row_id)
        except ValueError as err:
            errors.append(f"{prefix}{err}")
            continue

        expected_list = ref_row.get(col, [])
        if parsed_list != expected_list:
            errors.append(
                f"{prefix}Danh sach nguon '{col}' bi sua doi!\n"
                f"  Goc: {expected_list}\n"
                f"  Nhan duoc: {parsed_list}"
            )

    # 3. Validate editable manual review fields
    status = str(row.get('review_status', '')).strip()
    gold_label = str(row.get('gold_topic_label', '')).strip()
    reviewer_id = str(row.get('reviewer_id', '')).strip()
    reviewed_at = str(row.get('reviewed_at', '')).strip()
    review_note = str(row.get('review_note', '')).strip()

    if status not in VALID_STATUSES:
        errors.append(f"{prefix}review_status='{status}' khong hop le. Phai thuoc {sorted(VALID_STATUSES)}")
        return errors

    if status == 'pending_manual_review':
        if not allow_pending:
            errors.append(f"{prefix}Khong chap nhan trang thai 'pending_manual_review' trong che do nay")
        if gold_label:
            errors.append(f"{prefix}Trang thai 'pending_manual_review' bat buoc gold_topic_label phai de trong, nhung co '{gold_label}'")
        if reviewed_at and not is_valid_iso_date(reviewed_at):
            errors.append(f"{prefix}Ngay reviewed_at='{reviewed_at}' khong dung dinh dang YYYY-MM-DD hoac khong ton tai")

    elif status == 'reviewed':
        if not gold_label:
            errors.append(f"{prefix}Trang thai 'reviewed' bat buoc phai co gold_topic_label")
        elif gold_label not in valid_labels:
            errors.append(f"{prefix}gold_topic_label='{gold_label}' khong hop le. Phai la 1 trong 8 nhan hop le: {sorted(valid_labels)}")

        if not reviewer_id:
            errors.append(f"{prefix}Trang thai 'reviewed' bat buoc phai co reviewer_id")
        if not reviewed_at:
            errors.append(f"{prefix}Trang thai 'reviewed' bat buoc phai co reviewed_at")
        elif not is_valid_iso_date(reviewed_at):
            errors.append(f"{prefix}Ngay reviewed_at='{reviewed_at}' khong dung dinh dang YYYY-MM-DD hoac khong ton tai trong lich")

    elif status in ('needs_discussion', 'excluded'):
        if gold_label:
            errors.append(f"{prefix}Trang thai '{status}' bat buoc gold_topic_label phai de trong (''), nhung co '{gold_label}'")
        if not review_note:
            errors.append(f"{prefix}Trang thai '{status}' bat buoc phai ghi ro ly do/dieu can thao luan vao review_note")
        if not reviewer_id:
            errors.append(f"{prefix}Trang thai '{status}' bat buoc phai co reviewer_id")
        if not reviewed_at:
            errors.append(f"{prefix}Trang thai '{status}' bat buoc phai co reviewed_at")
        elif not is_valid_iso_date(reviewed_at):
            errors.append(f"{prefix}Ngay reviewed_at='{reviewed_at}' khong dung dinh dang YYYY-MM-DD hoac khong ton tai trong lich")

    return errors


def compute_review_summary(rows: list[dict]) -> dict:
    """Calculate status and label summary metrics. Avoid premature ready_for_training claim."""
    status_counts = Counter(r.get('review_status', '').strip() for r in rows)
    reviewed_labels = [
        r.get('gold_topic_label', '').strip()
        for r in rows
        if r.get('review_status', '').strip() == 'reviewed' and r.get('gold_topic_label', '').strip()
    ]
    label_distribution = dict(Counter(reviewed_labels))
    pending_cnt = status_counts.get('pending_manual_review', 0)
    discussion_cnt = status_counts.get('needs_discussion', 0)
    reviewed_cnt = status_counts.get('reviewed', 0)
    excluded_cnt = status_counts.get('excluded', 0)

    annotation_complete = (pending_cnt == 0 and discussion_cnt == 0 and len(rows) == EXPECTED_PILOT_TOTAL)

    return {
        'total_records': len(rows),
        'status_counts': {
            'reviewed': reviewed_cnt,
            'needs_discussion': discussion_cnt,
            'excluded': excluded_cnt,
            'pending_manual_review': pending_cnt,
        },
        'usable_for_training_count': len(reviewed_labels),
        'gold_label_distribution': label_distribution,
        'annotation_complete': annotation_complete,
        'train_readiness_status': 'not_evaluated_in_pilot_phase',
        'ready_for_training': False,  # Never declare ready in pilot phase
    }


def validate_count_dict(
    actual_dict: dict,
    expected_dict: dict,
    field_name: str,
    context_desc: str = ''
) -> None:
    """Strictly validate dictionary keys, types (exact int, not bool), non-negativity, and counts."""
    prefix = f"Loi: review_summary.{field_name}"
    if not isinstance(actual_dict, dict) or type(actual_dict) is not dict:
        actual_type = type(actual_dict).__name__
        raise ValueError(f"{prefix} phai la dict, nhan duoc {actual_type}")

    actual_keys = set(actual_dict.keys())
    expected_keys = set(expected_dict.keys())

    if actual_keys != expected_keys:
        missing = expected_keys - actual_keys
        extra = actual_keys - expected_keys
        reasons = []
        if missing:
            reasons.append(f"thieu khoa: {sorted(missing)}")
        if extra:
            reasons.append(f"thua khoa: {sorted(extra)}")
        raise ValueError(f"{prefix} sai tap khoa ({', '.join(reasons)})")

    for k, expected_count in expected_dict.items():
        val = actual_dict[k]
        # In Python, bool is subclass of int; type(True) is bool, type(1) is int
        if isinstance(val, bool) or type(val) is not int:
            actual_type = type(val).__name__
            raise ValueError(f"{prefix}.{k} phai la int khong am, nhan duoc {actual_type} ({val})")
        if val < 0:
            raise ValueError(f"{prefix}.{k} khong duoc la so am ({val})")
        if val != expected_count:
            raise ValueError(
                f"{prefix}.{k} sai gia tri dem:\n"
                f"  Manifest: {val}\n"
                f"  Thuc te:  {expected_count}"
            )


def assert_safe_output_dir(output_dir: Path, pilot_dir: Path, input_file: Path | None = None) -> None:
    """Enforce strict non-destructive destination directory rules."""
    out_res = output_dir.resolve()
    pilot_res = pilot_dir.resolve()

    # Rule 1: Cannot export inside or at the reference pilot directory
    if out_res == pilot_res or pilot_res in out_res.parents:
        raise PermissionError(
            f"Thu muc xuat ({out_res}) trung hoac nam trong thu muc pilot goc ({pilot_res})!\n"
            f"Tuyet doi khong ghi de vao vung du lieu pilot goc."
        )

    # Rule 2: Cannot export inside the same parent as input_file if names collide
    if input_file is not None:
        in_res = input_file.resolve()
        if out_res == in_res.parent or out_res == in_res:
            raise PermissionError(f"Thu muc xuat ({out_res}) trung voi thu muc chua file dau vao ({in_res})!")

    # Rule 3: Output directory must NOT exist already (must be a fresh version directory)
    if out_res.exists():
        raise FileExistsError(
            f"Thu muc xuat da ton tai: {out_res}\n"
            f"Vui long chi dinh mot thu muc phien ban moi hoan toan (vi du: .../annotations/v1, /v2)."
        )


def check_markdown_relative_links(md_path: Path) -> list[str]:
    """Find all local markdown links in a file and verify target exists."""
    errors = []
    text = md_path.read_text(encoding='utf-8')
    link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
    for match in link_pattern.finditer(text):
        link_target = match.group(2).strip()
        if link_target.startswith(('http://', 'https://', 'mailto:', '#')):
            continue
        clean_target = link_target.split('#')[0]
        if not clean_target:
            continue
        if clean_target.startswith('file:'):
            errors.append(f"{md_path.name}: absolute file URI found: '{link_target}'")
            continue
        resolved_path = (md_path.parent / clean_target).resolve()
        if not resolved_path.exists():
            errors.append(f"{md_path.name}: broken relative link '{link_target}' -> '{resolved_path}'")
    return errors
