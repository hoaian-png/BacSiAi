#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script lay mau mo rong dot 02 (200 cau hoi ung vien tu kho prepared).
Co co che bao ve chong ghi de nghiem ngat, xac thuc quota chat che va don dep khi loi.
"""

import os
import sys
import csv
import json
import random
import hashlib
import argparse
from datetime import datetime, timezone
from collections import Counter, defaultdict

VALID_TOPIC_LABELS = {
    'cam_lanh',
    'sot',
    'cam_cum',
    'ho_dom',
    'trieu_chung_mui',
    'trieu_chung_tai',
    'hong_amidan',
    'xoang',
    ''
}

DEFAULT_QUOTAS = {
    'cam_lanh': 9,
    'sot': 30,
    'cam_cum': 30,
    'ho_dom': 25,
    'trieu_chung_mui': 25,
    'trieu_chung_tai': 25,
    'hong_amidan': 20,
    'xoang': 20,
    '': 16
}

REQUIRED_FIELDS = [
    'id', 'dataset', 'question', 'group_id', 'provenance_ids',
    'topic_candidates', 'suggested_topic_label', 'keywords',
    'gold_topic_label', 'review_status', 'reviewer_id', 'reviewed_at', 'review_note'
]

def sha256_file(filepath):
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def normalize_path(path):
    """Chuẩn hóa đường dẫn thực tế, đồng bộ chữ hoa/thường trên Windows."""
    return os.path.normcase(os.path.realpath(os.path.abspath(path)))

def check_protected_paths(target_dir, base_dir):
    """
    Kiem tra thu muc xuat:
    - Phai nam ben trong base_dir.
    - Khong duoc la chinh base_dir hoac to tien cua base_dir.
    - Khong duoc trung hoac la to tien/thu muc con cua: raw, normalized, prepared, reviewed/pilot.
    """
    target_norm = normalize_path(target_dir)
    base_norm = normalize_path(base_dir)

    try:
        common_base = os.path.commonpath([target_norm, base_norm])
    except ValueError:
        raise ValueError(
            f"Thu muc xuat '{target_dir}' khong cung o dia hoac khong nam trong thu muc co so '{base_dir}'."
        )

    if common_base != base_norm or target_norm == base_norm:
        raise ValueError(
            f"Thu muc xuat '{target_dir}' phai la thu muc con nam ben trong thu muc co so '{base_dir}'."
        )

    protected_subdirs = [
        os.path.join(base_dir, 'raw'),
        os.path.join(base_dir, 'normalized'),
        os.path.join(base_dir, 'prepared'),
        os.path.join(base_dir, 'reviewed', 'pilot')
    ]

    for psub in protected_subdirs:
        psub_norm = normalize_path(psub)
        try:
            common = os.path.commonpath([target_norm, psub_norm])
        except ValueError:
            continue

        if common == target_norm:
            raise ValueError(
                f"Thu muc xuat '{target_dir}' la chinh no hoac to tien cua vung bao ve '{psub}'."
            )
        if common == psub_norm:
            raise ValueError(
                f"Thu muc xuat '{target_dir}' nam ben trong vung bao ve '{psub}'."
            )

def validate_quota_inputs(target_quotas):
    """Xác thực kiểu và giá trị của quota trước khi tạo thư mục hoặc ghi tệp."""
    if target_quotas is None:
        return dict(DEFAULT_QUOTAS)

    if not isinstance(target_quotas, dict):
        raise TypeError(f"target_quotas phai la dict, nhan duoc {type(target_quotas).__name__}")

    validated = {}
    for k, v in target_quotas.items():
        if k not in VALID_TOPIC_LABELS:
            raise ValueError(
                f"Nhan quota khong hop le: '{k}'. Cac nhan hop le: {sorted(list(VALID_TOPIC_LABELS))}"
            )
        if type(v) is not int or isinstance(v, bool) or v < 0:
            raise TypeError(
                f"Quota cho nhan '{k}' phai la so nguyen int >= 0, nhan duoc {type(v).__name__}: {v}"
            )
        validated[k] = v

    total = sum(validated.values())
    if total == 0:
        raise ValueError("Tong quota bang 0. Khong co cau hoi nao duoc yeu cau lay mau.")

    return validated

def sample_expansion(base_dir=None, output_dir=None, seed=42, target_quotas=None):
    # 1. Kiem tra kieu cua seed
    if type(seed) is not int or isinstance(seed, bool):
        raise TypeError(f"Seed phai la so nguyen int, nhan duoc {type(seed).__name__}: {seed}")

    # 2. Xac thuc quotas truoc khi lam bat cu thao tac tao thu muc hay doc/ghi nao
    quotas = validate_quota_inputs(target_quotas)
    target_total = sum(quotas.values())

    if base_dir is None:
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../02_du_lieu/filedata'))
    else:
        base_dir = os.path.abspath(base_dir)

    if not os.path.isdir(base_dir):
        raise FileNotFoundError(f"Thu muc co so khong ton tai: '{base_dir}'")

    if output_dir is None:
        output_dir = os.path.join(base_dir, 'reviewed/expansion/batch_02_v1')
    else:
        if not os.path.isabs(output_dir):
            output_dir = os.path.abspath(os.path.join(base_dir, output_dir))
        else:
            output_dir = os.path.abspath(output_dir)

    # 3. Kiem tra bao ve duong dan
    check_protected_paths(output_dir, base_dir)

    # 4. Kiem tra chong ghi de: thu muc ton tai (ke ca rong) phai bi tu choi ngay
    if os.path.exists(output_dir):
        raise FileExistsError(
            f"Thu muc xuat da ton tai: '{output_dir}'. Nghiem cam ghi de de bao toan du lieu."
        )

    prep_csv_path = os.path.join(base_dir, 'prepared/questions_ent.csv')
    pilot_csv_path = os.path.join(base_dir, 'reviewed/pilot/questions_pilot.csv')

    if not os.path.isfile(prep_csv_path):
        raise FileNotFoundError(f"Thieu file du lieu prepared: '{prep_csv_path}'")
    if not os.path.isfile(pilot_csv_path):
        raise FileNotFoundError(f"Thieu file du lieu pilot: '{pilot_csv_path}'")

    # Xac dinh danh sach thu muc can tao de don dep neu xay ra loi
    dirs_created = []
    curr = output_dir
    while curr and not os.path.exists(curr):
        dirs_created.append(curr)
        parent = os.path.dirname(curr)
        if parent == curr:
            break
        curr = parent
    dirs_created.reverse()

    files_created = []

    try:
        # Tao thu muc
        for d in dirs_created:
            os.mkdir(d)

        out_csv_path = os.path.join(output_dir, 'questions_expansion.csv')
        out_jsonl_path = os.path.join(output_dir, 'questions_expansion.jsonl')
        manifest_path = os.path.join(output_dir, 'sampling_manifest.json')

        # 5. Load pilot to exclude
        with open(pilot_csv_path, 'r', encoding='utf-8-sig') as f:
            pilot_rows = list(csv.DictReader(f))

        pilot_ids = set(r['id'] for r in pilot_rows if r.get('id'))
        pilot_group_ids = set()
        pilot_prov_ids = set()
        for r in pilot_rows:
            if r.get('group_id'):
                pilot_group_ids.add(r['group_id'])
            if r.get('question_group_id'):
                pilot_group_ids.add(r['question_group_id'])
            p = r.get('provenance_ids', '')
            if p:
                p_str = p.strip()
                if p_str.startswith('['):
                    try:
                        parsed = json.loads(p_str)
                        if isinstance(parsed, list):
                            pilot_prov_ids.update(str(x) for x in parsed)
                    except Exception:
                        pilot_prov_ids.add(p_str)
                else:
                    pilot_prov_ids.add(p_str)

        # 6. Load prepared
        with open(prep_csv_path, 'r', encoding='utf-8-sig') as f:
            prep_rows = list(csv.DictReader(f))

        # Stable sort by ID
        prep_rows.sort(key=lambda x: x['id'])

        # Filter candidate pool
        candidates = []
        for r in prep_rows:
            qid = r.get('id', '')
            gid = r.get('group_id', '')
            qgid = r.get('question_group_id', '')
            if qid in pilot_ids:
                continue
            if gid and gid in pilot_group_ids:
                continue
            if qgid and qgid in pilot_group_ids:
                continue

            p = r.get('provenance_ids', '')
            r_provs = set()
            if p:
                p_str = p.strip()
                if p_str.startswith('['):
                    try:
                        parsed = json.loads(p_str)
                        if isinstance(parsed, list):
                            r_provs.update(str(x) for x in parsed)
                    except Exception:
                        r_provs.add(p_str)
                else:
                    r_provs.add(p_str)
            if r_provs & pilot_prov_ids:
                continue

            candidates.append(r)

        # 7. Stratified sampling
        by_label = defaultdict(list)
        for r in candidates:
            by_label[r.get('topic_label', '')].append(r)

        rng = random.Random(seed)
        selected = []
        used_group_ids = set()
        used_ids = set()
        used_norm_texts = set()

        deficit_report = {}

        for lbl, target_quota in quotas.items():
            # Quota 0 bo qua ngay lap tuc truoc khi chon mau
            if target_quota == 0:
                continue

            pool = list(by_label[lbl])
            rng.shuffle(pool)

            label_selected = []
            for r in pool:
                if len(label_selected) >= target_quota:
                    break

                gid = r.get('group_id')
                if gid and gid in used_group_ids:
                    continue
                if r['id'] in used_ids:
                    continue

                q_text = r['question'].strip().lower()
                if q_text in used_norm_texts:
                    continue

                label_selected.append(r)
                if gid:
                    used_group_ids.add(gid)
                used_ids.add(r['id'])
                used_norm_texts.add(q_text)

                if len(label_selected) >= target_quota:
                    break

            actual_sampled = len(label_selected)
            if actual_sampled < target_quota:
                deficit_report[lbl] = {
                    'target': int(target_quota),
                    'actual': int(actual_sampled),
                    'deficit': int(target_quota - actual_sampled)
                }
            selected.extend(label_selected)

        # Stable sort selected questions by ID
        selected.sort(key=lambda x: x['id'])

        # Kiem tra tinh duy nhat
        if len(used_ids) != len(selected):
            raise ValueError(f"Phat hien ID trung lap trong tap lay mau: {len(used_ids)} != {len(selected)}")
        if len(used_group_ids) != len(selected):
            raise ValueError(f"Phat hien group_id trung lap trong tap lay mau: {len(used_group_ids)} != {len(selected)}")

        # 8. Export CSV (UTF-8 with BOM)
        files_created.append(out_csv_path)
        with open(out_csv_path, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(REQUIRED_FIELDS)
            for r in selected:
                writer.writerow([
                    r['id'],
                    r['dataset'],
                    r['question'],
                    r['group_id'],
                    r['provenance_ids'],
                    r['topic_candidates'],
                    r['topic_label'],
                    r['keywords'],
                    '',
                    'pending_manual_review',
                    '',
                    '',
                    ''
                ])

        # 9. Export JSONL (UTF-8)
        files_created.append(out_jsonl_path)
        with open(out_jsonl_path, 'w', encoding='utf-8') as f:
            for r in selected:
                p_ids = r['provenance_ids']
                if p_ids.startswith('['):
                    p_parsed = [str(x) for x in json.loads(p_ids)]
                else:
                    p_parsed = [str(p_ids)]

                t_cands = r['topic_candidates']
                if t_cands.startswith('['):
                    t_parsed = [str(x) for x in json.loads(t_cands)]
                else:
                    t_parsed = [str(t_cands)]

                k_words = r['keywords']
                if k_words.startswith('['):
                    k_parsed = [str(x) for x in json.loads(k_words)]
                else:
                    k_parsed = [str(k_words)]

                item = {
                    'id': str(r['id']),
                    'dataset': str(r['dataset']),
                    'question': str(r['question']),
                    'group_id': str(r['group_id']),
                    'provenance_ids': p_parsed,
                    'topic_candidates': t_parsed,
                    'suggested_topic_label': str(r['topic_label']),
                    'keywords': k_parsed,
                    'gold_topic_label': '',
                    'review_status': 'pending_manual_review',
                    'reviewer_id': '',
                    'reviewed_at': '',
                    'review_note': ''
                }
                f.write(json.dumps(item, ensure_ascii=False) + '\n')

        # 10. Checksums and manifest
        csv_hash = sha256_file(out_csv_path)
        jsonl_hash = sha256_file(out_jsonl_path)
        prep_csv_hash = sha256_file(prep_csv_path)
        pilot_csv_hash = sha256_file(pilot_csv_path)

        counts_by_label = Counter(r['topic_label'] for r in selected)
        counts_by_dataset = Counter(r['dataset'] for r in selected)

        batch_id = os.path.basename(os.path.normpath(output_dir))
        rel_csv_path = os.path.relpath(out_csv_path, base_dir).replace('\\', '/')
        rel_jsonl_path = os.path.relpath(out_jsonl_path, base_dir).replace('\\', '/')

        manifest_data = {
            'batch_id': batch_id,
            'description': f'Đợt lấy mẫu mở rộng {len(selected)}/{target_total} câu hỏi từ kho prepared, loại trừ hoàn toàn các ID, nhóm và provenance thuộc Pilot.',
            'created_at_utc': datetime.now(timezone.utc).isoformat(),
            'sampling_parameters': {
                'seed': int(seed),
                'algorithm': f'Deterministic stratified sampling with random seed {seed} over sorted candidate pool',
                'quota_processing_order': list(quotas.keys()),
                'target_total': int(target_total),
                'actual_total': int(len(selected)),
                'target_quotas': {k: int(v) for k, v in quotas.items()},
                'actual_by_suggested_label': {k: int(v) for k, v in counts_by_label.items()},
                'actual_by_dataset': {k: int(v) for k, v in counts_by_dataset.items()},
                'deficits': deficit_report
            },
            'deduplication_and_scope': {
                'rules': [
                    'Loại bỏ toàn bộ ID đã thuộc tập Pilot (questions_pilot.csv)',
                    'Loại bỏ toàn bộ các câu hỏi có group_id đã xuất hiện trong tập Pilot',
                    'Loại bỏ toàn bộ provenance_ids đã xuất hiện trong tập Pilot',
                    'Mỗi group_id chỉ được chọn tối đa một câu hỏi trong toàn bộ đợt mở rộng',
                    'Kiểm tra và loại bỏ câu trùng lặp nguyên văn (normalized case-insensitive text)',
                    'Lọc trùng lặp chỉ nhận diện câu tương tự bề mặt, không bảo đảm tính độc lập ngữ nghĩa'
                ],
                'unique_ids_count': int(len(used_ids)),
                'unique_groups_count': int(len(used_group_ids))
            },
            'reference_files': [
                {
                    'role': 'prepared_dataset_csv',
                    'path': 'prepared/questions_ent.csv',
                    'sha256': prep_csv_hash
                },
                {
                    'role': 'pilot_dataset_csv',
                    'path': 'reviewed/pilot/questions_pilot.csv',
                    'sha256': pilot_csv_hash
                }
            ],
            'output_files': {
                'csv': {
                    'path': rel_csv_path,
                    'sha256': csv_hash,
                    'record_count': int(len(selected))
                },
                'jsonl': {
                    'path': rel_jsonl_path,
                    'sha256': jsonl_hash,
                    'record_count': int(len(selected))
                }
            },
            'sampled_ids': [r['id'] for r in selected],
            'sampled_group_ids': [r['group_id'] for r in selected]
        }

        files_created.append(manifest_path)
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest_data, f, ensure_ascii=False, indent=2)

        print(f"Lay mau thanh cong {len(selected)} cau hoi vao '{output_dir}'")
        print(f"CSV SHA-256: {csv_hash}")
        print(f"JSONL SHA-256: {jsonl_hash}")
        return manifest_data

    except Exception:
        # Don dep chi nhung file va thu muc do chinh lan chay nay tao ra
        for fpath in files_created:
            try:
                if os.path.isfile(fpath):
                    os.remove(fpath)
            except OSError:
                pass
        for dpath in reversed(dirs_created):
            try:
                if os.path.isdir(dpath) and not os.listdir(dpath):
                    os.rmdir(dpath)
            except OSError:
                pass
        raise

def main():
    parser = argparse.ArgumentParser(description="Cong cu lay mau mo rong dot 02")
    parser.add_argument(
        '--output-dir',
        default=None,
        help="Thu muc dich (mac dinh: 02_du_lieu/filedata/reviewed/expansion/batch_02_v1)"
    )
    parser.add_argument(
        '--base-dir',
        default=None,
        help="Thu muc goc du lieu (mac dinh: 02_du_lieu/filedata)"
    )
    parser.add_argument(
        '--seed',
        type=int,
        default=42,
        help="Random seed (mac dinh: 42)"
    )

    args = parser.parse_args()

    try:
        sample_expansion(
            base_dir=args.base_dir,
            output_dir=args.output_dir,
            seed=args.seed
        )
    except Exception as e:
        sys.stderr.write(f"LOI: {type(e).__name__}: {e}\n")
        sys.exit(1)

if __name__ == '__main__':
    main()
