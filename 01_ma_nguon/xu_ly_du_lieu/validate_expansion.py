#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validator toan dien cho tap mo rong dot 02 (questions_expansion).
Kiem tra tinh toan ven, tinh doc lap nhom, khong giao cat pilot, doi chieu prepared va manifest.
Siết chặt schema, kieu du lieu va tinh nhat quan cua manifest.
Khong dung assert, su dung ngoai le ro nghia, ho tro chay voi python -O.
"""

import os
import sys
import csv
import json
import hashlib
import argparse
from collections import Counter

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

REQUIRED_CSV_FIELDS = [
    'id', 'dataset', 'question', 'group_id', 'provenance_ids',
    'topic_candidates', 'suggested_topic_label', 'keywords',
    'gold_topic_label', 'review_status', 'reviewer_id', 'reviewed_at', 'review_note'
]

REQUIRED_JSONL_FIELDS = [
    'id', 'dataset', 'question', 'group_id', 'provenance_ids',
    'topic_candidates', 'suggested_topic_label', 'keywords',
    'gold_topic_label', 'review_status', 'reviewer_id', 'reviewed_at', 'review_note'
]

STRING_FIELDS = [
    'id', 'dataset', 'question', 'group_id', 'suggested_topic_label',
    'gold_topic_label', 'review_status', 'reviewer_id', 'reviewed_at', 'review_note'
]

ARRAY_FIELDS = ['provenance_ids', 'topic_candidates', 'keywords']
NON_EMPTY_STRING_FIELDS = ['id', 'dataset', 'question', 'group_id']
INITIAL_REVIEW_EMPTY_FIELDS = ['gold_topic_label', 'reviewer_id', 'reviewed_at', 'review_note']

def sha256_file(filepath):
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def normalize_path(path):
    """Chuẩn hóa đường dẫn thực tế, đồng bộ chữ hoa/thường trên Windows."""
    return os.path.normcase(os.path.realpath(os.path.abspath(path)))

def validate_non_negative_int(val, name):
    """
    Kiem tra gia tri phai la so nguyen int >= 0 thuc su.
    Tu choi tuyet doi bool, float, str, None.
    """
    if type(val) is not int or isinstance(val, bool) or val < 0:
        raise TypeError(
            f"Truong '{name}' phai la so nguyen int >= 0, nhan duoc {type(val).__name__}: {val}"
        )

def check_safe_relative_path(path_str, base_dir, field_name="path"):
    """
    Kiem tra duong dan phai la duong dan tuong doi an toan, khong chua .. thoat ra ngoai base_dir.
    """
    if not isinstance(path_str, str):
        raise TypeError(f"Duong dan trong '{field_name}' phai la chuoi str, nhan duoc {type(path_str).__name__}")
    if os.path.isabs(path_str):
        raise ValueError(f"Duong dan trong '{field_name}' phai la duong dan tuong doi, nhan duoc: '{path_str}'")

    norm_path = os.path.normpath(path_str)
    parts = norm_path.split(os.sep)
    if '..' in parts:
        raise ValueError(f"Phat hien path traversal ('..') trong '{field_name}': '{path_str}'")

    full_path = os.path.abspath(os.path.join(base_dir, norm_path))
    base_norm = normalize_path(base_dir)
    full_norm = normalize_path(full_path)
    try:
        common = os.path.commonpath([full_norm, base_norm])
        if common != base_norm:
            raise ValueError(f"Duong dan '{path_str}' thoat ra ngoai thu muc co so '{base_dir}'")
    except ValueError as e:
        if "Paths don't have the same drive" in str(e):
            raise ValueError(f"Duong dan '{path_str}' nam tren o dia khac voi thu muc co so")
        raise
    return full_path

def parse_csv_json_array(val_str, field_name, qid):
    """Parse mang JSON tu cot CSV, bat buoc phai la JSON array chua toan bo chuoi str."""
    if not isinstance(val_str, str):
        raise TypeError(f"Truong '{field_name}' trong CSV cua ID '{qid}' phai la chuoi str, nhan duoc {type(val_str).__name__}")
    val_trimmed = val_str.strip()
    if not (val_trimmed.startswith('[') and val_trimmed.endswith(']')):
        raise ValueError(
            f"Truong '{field_name}' trong CSV cua ID '{qid}' phai la JSON array bat dau bang '[' va ket thuc bang ']': '{val_str}'"
        )
    try:
        parsed = json.loads(val_trimmed)
    except Exception as e:
        raise ValueError(f"Truong '{field_name}' trong CSV cua ID '{qid}' khong phai JSON hop le: {e}")

    if type(parsed) is not list:
        raise TypeError(f"Truong '{field_name}' trong CSV cua ID '{qid}' phai la list, nhan duoc {type(parsed).__name__}")

    for elem in parsed:
        if type(elem) is not str:
            raise TypeError(
                f"Phan tu trong '{field_name}' cua ID '{qid}' trong CSV phai la chuoi str, nhan duoc {type(elem).__name__}: {elem}"
            )
    return parsed

def validate_expansion_batch(batch_dir, base_dir=None):
    if base_dir is None:
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../02_du_lieu/filedata'))
    else:
        base_dir = os.path.abspath(base_dir)

    if not os.path.isdir(base_dir):
        raise FileNotFoundError(f"Thu muc co so khong ton tai: '{base_dir}'")

    batch_dir = os.path.abspath(batch_dir)
    if not os.path.isdir(batch_dir):
        raise FileNotFoundError(f"Thu muc batch khong ton tai: '{batch_dir}'")

    csv_path = os.path.join(batch_dir, 'questions_expansion.csv')
    jsonl_path = os.path.join(batch_dir, 'questions_expansion.jsonl')
    manifest_path = os.path.join(batch_dir, 'sampling_manifest.json')
    pilot_csv_path = os.path.join(base_dir, 'reviewed/pilot/questions_pilot.csv')
    prep_csv_path = os.path.join(base_dir, 'prepared/questions_ent.csv')

    # Kiem tra su ton tai cua cac file bat buoc
    for path, desc in [
        (csv_path, 'questions_expansion.csv'),
        (jsonl_path, 'questions_expansion.jsonl'),
        (manifest_path, 'sampling_manifest.json'),
        (pilot_csv_path, 'questions_pilot.csv'),
        (prep_csv_path, 'questions_ent.csv')
    ]:
        if not os.path.isfile(path):
            raise FileNotFoundError(f"Thieu file bat buoc ({desc}): '{path}'")

    # 1. Kiem tra va doc CSV
    with open(csv_path, 'r', encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != REQUIRED_CSV_FIELDS:
            raise ValueError(
                f"Header CSV khong khop schema chuan.\nThuc te: {reader.fieldnames}\nYeu cau: {REQUIRED_CSV_FIELDS}"
            )
        if len(reader.fieldnames) != len(set(reader.fieldnames)):
            raise ValueError("Phat hien cot trung ten trong header CSV")
        csv_rows = []
        for idx, row in enumerate(reader, start=1):
            if None in row or None in row.values():
                raise ValueError(f"Dong CSV thu {idx} co so luong o khong khop voi header")
            csv_rows.append(row)

    # 2. Kiem tra va doc JSONL
    jsonl_items = []
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for idx, line in enumerate(f, start=1):
            line_str = line.strip()
            if not line_str:
                raise ValueError(f"Phat hien dong trong tai dong {idx} trong JSONL")
            try:
                item = json.loads(line_str)
            except Exception as e:
                raise ValueError(f"Loi cu phap JSON tai dong {idx} trong JSONL: {e}")
            if type(item) is not dict:
                raise TypeError(f"Dong {idx} trong JSONL phai la JSON object (dict), nhan duoc {type(item).__name__}")

            # Kiem tra cac truong bat buoc cua JSONL
            item_keys = set(item.keys())
            req_set = set(REQUIRED_JSONL_FIELDS)
            if not req_set.issubset(item_keys):
                missing = req_set - item_keys
                raise ValueError(f"Dong {idx} trong JSONL thieu cac truong bat buoc: {sorted(list(missing))}")
            if len(item_keys) != len(REQUIRED_JSONL_FIELDS):
                extra = item_keys - req_set
                raise ValueError(f"Dong {idx} trong JSONL co cac truong thua: {sorted(list(extra))}")

            jsonl_items.append(item)

    if len(csv_rows) != len(jsonl_items):
        raise ValueError(
            f"So luong ban ghi CSV ({len(csv_rows)}) va JSONL ({len(jsonl_items)}) khong khop"
        )

    # 3. Doc prepared de doi chieu nguoc
    with open(prep_csv_path, 'r', encoding='utf-8-sig') as f:
        prep_rows = list(csv.DictReader(f))
    prep_by_id = {r['id']: r for r in prep_rows if r.get('id')}

    # 4. Kiem tra tung ban ghi: kieu du lieu, prepared, doi chieu CSV-JSONL
    batch_ids = []
    batch_groups = []
    batch_norm_texts = []
    batch_prov_ids = set()

    for idx, (c, j) in enumerate(zip(csv_rows, jsonl_items)):
        qid = c.get('id', '')

        # Kiem tra kieu cac truong chuoi trong JSONL
        for fld in STRING_FIELDS:
            if type(j[fld]) is not str:
                raise TypeError(f"Truong '{fld}' trong JSONL cua ID '{qid}' phai la chuoi str, nhan duoc {type(j[fld]).__name__}")

        # Kiem tra cac truong khong duoc rong
        for fld in NON_EMPTY_STRING_FIELDS:
            if not c[fld].strip():
                raise ValueError(f"Truong '{fld}' trong CSV tai dong {idx} khong duoc rong hoac chi co khoang trang")
            if not j[fld].strip():
                raise ValueError(f"Truong '{fld}' trong JSONL tai dong {idx} khong duoc rong hoac chi co khoang trang")

        if qid != j['id']:
            raise ValueError(f"ID khong khop tai dong {idx}: CSV='{qid}', JSONL='{j['id']}'")

        # Kiem tra trong prepared
        if qid not in prep_by_id:
            raise ValueError(f"Ban ghi '{qid}' khong ton tai trong nguon prepared ('{prep_csv_path}')")
        prep_r = prep_by_id[qid]

        # Khop chinh xac voi prepared
        if c['question'] != prep_r['question']:
            raise ValueError(f"Truong 'question' cua ID '{qid}' bi sai lech so voi prepared")
        if c['dataset'] != prep_r['dataset']:
            raise ValueError(f"Truong 'dataset' cua ID '{qid}' bi sai lech so voi prepared")
        if c['group_id'] != prep_r['group_id']:
            raise ValueError(f"Truong 'group_id' cua ID '{qid}' bi sai lech so voi prepared")
        if c['provenance_ids'] != prep_r['provenance_ids']:
            raise ValueError(f"Truong 'provenance_ids' cua ID '{qid}' bi sai lech so voi prepared")
        if c['topic_candidates'] != prep_r['topic_candidates']:
            raise ValueError(f"Truong 'topic_candidates' cua ID '{qid}' bi sai lech so voi prepared")
        if c['keywords'] != prep_r['keywords']:
            raise ValueError(f"Truong 'keywords' cua ID '{qid}' bi sai lech so voi prepared")
        if c['suggested_topic_label'] != prep_r['topic_label']:
            raise ValueError(f"Truong 'suggested_topic_label' cua ID '{qid}' khong khop 'topic_label' trong prepared")

        # Kiem tra nhan hop le
        if c['suggested_topic_label'] not in VALID_TOPIC_LABELS:
            raise ValueError(f"Nhan 'suggested_topic_label' khong hop le trong CSV tai ID '{qid}': '{c['suggested_topic_label']}'")
        if j['suggested_topic_label'] not in VALID_TOPIC_LABELS:
            raise ValueError(f"Nhan 'suggested_topic_label' khong hop le trong JSONL tai ID '{qid}': '{j['suggested_topic_label']}'")

        # Kiem tra cac truong ra soat ban dau
        if c['review_status'] != 'pending_manual_review' or j['review_status'] != 'pending_manual_review':
            raise ValueError(f"Truong 'review_status' cua ID '{qid}' phai la 'pending_manual_review'")

        for efld in INITIAL_REVIEW_EMPTY_FIELDS:
            if c[efld] != "" or j[efld] != "":
                raise ValueError(f"Truong '{efld}' cua ID '{qid}' phai de trong trong tap lay mau ban dau")

        # Kiem tra su nhat quan giua CSV va JSONL
        if c['dataset'] != j['dataset']:
            raise ValueError(f"Sai lech 'dataset' giua CSV va JSONL tai ID '{qid}'")
        if c['question'] != j['question']:
            raise ValueError(f"Sai lech 'question' giua CSV va JSONL tai ID '{qid}'")
        if c['group_id'] != j['group_id']:
            raise ValueError(f"Sai lech 'group_id' giua CSV va JSONL tai ID '{qid}'")
        if c['suggested_topic_label'] != j['suggested_topic_label']:
            raise ValueError(f"Sai lech 'suggested_topic_label' giua CSV va JSONL tai ID '{qid}'")

        # Kiem tra cac truong mang trong JSONL va so sanh voi CSV
        for afld in ARRAY_FIELDS:
            if type(j[afld]) is not list:
                raise TypeError(f"Truong '{afld}' trong JSONL cua ID '{qid}' phai la list thuc su, nhan duoc {type(j[afld]).__name__}")
            for elem in j[afld]:
                if type(elem) is not str:
                    raise TypeError(f"Phan tu trong list '{afld}' cua ID '{qid}' trong JSONL phai la chuoi str, nhan duoc {type(elem).__name__}: {elem}")

            c_parsed = parse_csv_json_array(c[afld], afld, qid)
            if c_parsed != j[afld]:
                raise ValueError(f"Noi dung '{afld}' giua CSV va JSONL khong khop tai ID '{qid}': {c_parsed} != {j[afld]}")

        batch_ids.append(qid)
        batch_groups.append(c['group_id'])
        batch_norm_texts.append(c['question'].strip().lower())
        batch_prov_ids.update(j['provenance_ids'])

    # 5. Kiem tra tinh duy nhat trong batch
    if len(set(batch_ids)) != len(batch_ids):
        raise ValueError("Phat hien ID bi trung lap ben trong tap lay mau")
    if len(set(batch_groups)) != len(batch_groups):
        raise ValueError("Phat hien group_id bi trung lap ben trong tap lay mau")
    if len(set(batch_norm_texts)) != len(batch_norm_texts):
        raise ValueError("Phat hien cau hoi trung lap nguyen van (normalized surface text) trong tap lay mau")

    # 6. Kiem tra khong giao cat voi tap pilot (ID, group_id, provenance_ids)
    with open(pilot_csv_path, 'r', encoding='utf-8-sig') as f:
        pilot_rows = list(csv.DictReader(f))

    pilot_ids = set(r['id'] for r in pilot_rows if r.get('id'))
    pilot_groups = set()
    pilot_prov_ids = set()
    for r in pilot_rows:
        if r.get('group_id'):
            pilot_groups.add(r['group_id'])
        if r.get('question_group_id'):
            pilot_groups.add(r['question_group_id'])
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

    id_overlap = set(batch_ids) & pilot_ids
    if id_overlap:
        raise ValueError(f"Phat hien giao cat ID voi tap pilot: {id_overlap}")

    group_overlap = set(batch_groups) & pilot_groups
    if group_overlap:
        raise ValueError(f"Phat hien giao cat group_id voi tap pilot: {group_overlap}")

    prov_overlap = batch_prov_ids & pilot_prov_ids
    if prov_overlap:
        raise ValueError(f"Phat hien giao cat provenance_ids voi tap pilot: {prov_overlap}")

    # 7. Kiem tra toan ven manifest va cac chi so
    with open(manifest_path, 'r', encoding='utf-8') as f:
        manifest = json.load(f)

    if not isinstance(manifest, dict):
        raise TypeError("Manifest phai la JSON object (dict)")

    for m_field in ['sampling_parameters', 'output_files', 'reference_files', 'deduplication_and_scope']:
        if m_field not in manifest:
            raise ValueError(f"Manifest thieu truong '{m_field}'")

    sp = manifest['sampling_parameters']
    if not isinstance(sp, dict):
        raise TypeError("sampling_parameters trong manifest phai la dict")

    # Kiem tra kieu so nguyen khong am
    validate_non_negative_int(sp.get('target_total'), 'sampling_parameters.target_total')
    validate_non_negative_int(sp.get('actual_total'), 'sampling_parameters.actual_total')

    target_total = sp['target_total']
    actual_total = sp['actual_total']

    if actual_total != len(csv_rows):
        raise ValueError(f"actual_total trong manifest ({actual_total}) khong khop so ban ghi thuc te ({len(csv_rows)})")

    # Kiem tra deduplication_and_scope counts
    ds_scope = manifest['deduplication_and_scope']
    if not isinstance(ds_scope, dict):
        raise TypeError("deduplication_and_scope trong manifest phai la dict")

    validate_non_negative_int(ds_scope.get('unique_ids_count'), 'deduplication_and_scope.unique_ids_count')
    validate_non_negative_int(ds_scope.get('unique_groups_count'), 'deduplication_and_scope.unique_groups_count')

    if ds_scope['unique_ids_count'] != len(set(batch_ids)):
        raise ValueError(
            f"unique_ids_count trong manifest ({ds_scope['unique_ids_count']}) khong khop so ID duy nhat thuc te ({len(set(batch_ids))})"
        )
    if ds_scope['unique_groups_count'] != len(set(batch_groups)):
        raise ValueError(
            f"unique_groups_count trong manifest ({ds_scope['unique_groups_count']}) khong khop so group_id duy nhat thuc te ({len(set(batch_groups))})"
        )

    target_quotas = sp.get('target_quotas', {})
    if not isinstance(target_quotas, dict):
        raise TypeError("target_quotas trong manifest phai la dict")
    for k, v in target_quotas.items():
        if k not in VALID_TOPIC_LABELS:
            raise ValueError(f"Nhan khong hop le trong target_quotas: '{k}'")
        validate_non_negative_int(v, f"target_quotas['{k}']")

    if sum(target_quotas.values()) != target_total:
        raise ValueError(f"Tong target_quotas ({sum(target_quotas.values())}) khong bang target_total ({target_total})")

    actual_by_label = sp.get('actual_by_suggested_label', {})
    if not isinstance(actual_by_label, dict):
        raise TypeError("actual_by_suggested_label trong manifest phai la dict")
    for k, v in actual_by_label.items():
        validate_non_negative_int(v, f"actual_by_suggested_label['{k}']")

    real_label_counts = Counter(r['suggested_topic_label'] for r in csv_rows)
    if dict(real_label_counts) != actual_by_label:
        raise ValueError(f"actual_by_suggested_label khong khop thuc te: {dict(real_label_counts)} != {actual_by_label}")

    actual_by_dataset = sp.get('actual_by_dataset', {})
    if not isinstance(actual_by_dataset, dict):
        raise TypeError("actual_by_dataset trong manifest phai la dict")
    for k, v in actual_by_dataset.items():
        validate_non_negative_int(v, f"actual_by_dataset['{k}']")

    real_ds_counts = Counter(r['dataset'] for r in csv_rows)
    if dict(real_ds_counts) != actual_by_dataset:
        raise ValueError(f"actual_by_dataset khong khop thuc te: {dict(real_ds_counts)} != {actual_by_dataset}")

    # Kiem tra thieu hut (deficits)
    if 'deficits' not in sp:
        raise ValueError("sampling_parameters thieu truong 'deficits'")

    deficits = sp['deficits']
    if not isinstance(deficits, dict):
        raise TypeError(f"deficits trong manifest phai la dict, nhan duoc {type(deficits).__name__}")

    # 1. Tinh expected_deficits tu target_quotas va actual_by_label
    expected_deficits = {}
    for lbl, t_quota in target_quotas.items():
        act_cnt = actual_by_label.get(lbl, 0)
        if act_cnt > t_quota:
            raise ValueError(
                f"So luong thuc te cua nhan '{lbl}' ({act_cnt}) vuot qua target quota ({t_quota})"
            )
        if act_cnt < t_quota:
            expected_deficits[lbl] = {
                'target': t_quota,
                'actual': act_cnt,
                'deficit': t_quota - act_cnt
            }

    # 2. Kiem tra tap khoa cua deficits phai khop chinh xac expected_deficits
    # deficits chi chua dung cac nhan co actual < target. Nhan du/vuot quota khong duoc xuat hien.
    if set(deficits.keys()) != set(expected_deficits.keys()):
        extra_keys = set(deficits.keys()) - set(expected_deficits.keys())
        missing_keys = set(expected_deficits.keys()) - set(deficits.keys())
        err_msgs = []
        if extra_keys:
            err_msgs.append(f"Khoa thua trong deficits (nhan da du/vuot quota hoac nhan la): {sorted(list(extra_keys))}")
        if missing_keys:
            err_msgs.append(f"Khoa thieu trong deficits (nhan thieu hut chua khai bao): {sorted(list(missing_keys))}")
        raise ValueError("; ".join(err_msgs))

    # 3. Kiem tra tung muc trong deficits: du 3 truong, dung kieu int, dung gia tri
    for lbl, exp_d in expected_deficits.items():
        act_d = deficits[lbl]
        if not isinstance(act_d, dict):
            raise TypeError(f"Muc deficit cho nhan '{lbl}' phai la dict, nhan duoc {type(act_d).__name__}")

        required_d_fields = {'target', 'actual', 'deficit'}
        if set(act_d.keys()) != required_d_fields:
            missing_f = required_d_fields - set(act_d.keys())
            extra_f = set(act_d.keys()) - required_d_fields
            err_parts = []
            if missing_f:
                err_parts.append(f"thieu truong: {sorted(list(missing_f))}")
            if extra_f:
                err_parts.append(f"thua truong: {sorted(list(extra_f))}")
            raise ValueError(f"Muc deficit cho nhan '{lbl}' khong dung truong quy dinh: {', '.join(err_parts)}")

        validate_non_negative_int(act_d['target'], f"deficits['{lbl}'].target")
        validate_non_negative_int(act_d['actual'], f"deficits['{lbl}'].actual")
        validate_non_negative_int(act_d['deficit'], f"deficits['{lbl}'].deficit")

        if act_d['target'] != exp_d['target']:
            raise ValueError(f"deficits['{lbl}'].target ({act_d['target']}) khong khop target_quotas ({exp_d['target']})")
        if act_d['actual'] != exp_d['actual']:
            raise ValueError(f"deficits['{lbl}'].actual ({act_d['actual']}) khong khop so dem thuc te ({exp_d['actual']})")
        if act_d['deficit'] != exp_d['deficit']:
            raise ValueError(f"deficits['{lbl}'].deficit ({act_d['deficit']}) khong khop target - actual ({exp_d['deficit']})")

    # 4. Kiem tra tong deficit
    total_deficit = sum(d['deficit'] for d in deficits.values())
    if (target_total - actual_total) != total_deficit:
        raise ValueError(
            f"Tong thieu hut ({total_deficit}) khong khop voi target_total - actual_total ({target_total - actual_total})"
        )

    # Kiem tra sampled_ids va sampled_group_ids khop dung thu tu
    manifest_sampled_ids = manifest.get('sampled_ids')
    if manifest_sampled_ids != batch_ids:
        raise ValueError("sampled_ids trong manifest khong khop dung thu tu voi ID trong tap du lieu CSV")

    manifest_sampled_groups = manifest.get('sampled_group_ids')
    if manifest_sampled_groups != batch_groups:
        raise ValueError("sampled_group_ids trong manifest khong khop dung thu tu voi group_id trong CSV")

    # Kiem tra output_files
    out_files = manifest['output_files']
    if 'csv' not in out_files or 'jsonl' not in out_files:
        raise ValueError("Manifest output_files thieu muc 'csv' hoac 'jsonl'")

    csv_meta = out_files['csv']
    jsonl_meta = out_files['jsonl']

    # Kiem tra path traversal va file ton tai
    full_csv_path = check_safe_relative_path(csv_meta['path'], base_dir, 'output_files.csv.path')
    full_jsonl_path = check_safe_relative_path(jsonl_meta['path'], base_dir, 'output_files.jsonl.path')

    # Kiem tra duong dan output_files phai tro dung vao file dang xac minh
    if normalize_path(full_csv_path) != normalize_path(csv_path):
        raise ValueError(
            f"output_files.csv.path trong manifest ('{csv_meta['path']}') khong tro dung file CSV dang xac minh ('{csv_path}')"
        )
    if normalize_path(full_jsonl_path) != normalize_path(jsonl_path):
        raise ValueError(
            f"output_files.jsonl.path trong manifest ('{jsonl_meta['path']}') khong tro dung file JSONL dang xac minh ('{jsonl_path}')"
        )

    validate_non_negative_int(csv_meta.get('record_count'), 'output_files.csv.record_count')
    validate_non_negative_int(jsonl_meta.get('record_count'), 'output_files.jsonl.record_count')

    if csv_meta['record_count'] != len(csv_rows):
        raise ValueError(f"record_count cua CSV trong manifest ({csv_meta['record_count']}) != thuc te ({len(csv_rows)})")
    if jsonl_meta['record_count'] != len(jsonl_items):
        raise ValueError(f"record_count cua JSONL trong manifest ({jsonl_meta['record_count']}) != thuc te ({len(jsonl_items)})")

    # Kiem tra checksum file output
    real_csv_hash = sha256_file(csv_path)
    real_jsonl_hash = sha256_file(jsonl_path)

    if csv_meta['sha256'] != real_csv_hash:
        raise ValueError(f"Checksum CSV khong khop manifest: {real_csv_hash} != {csv_meta['sha256']}")
    if jsonl_meta['sha256'] != real_jsonl_hash:
        raise ValueError(f"Checksum JSONL khong khop manifest: {real_jsonl_hash} != {jsonl_meta['sha256']}")

    # Kiem tra reference_files: khong duoc rong, phai chua du dau vao bat buoc
    ref_files = manifest.get('reference_files')
    if not isinstance(ref_files, list) or len(ref_files) == 0:
        raise ValueError("reference_files trong manifest khong duoc rong")

    ref_paths = set()
    for ref in ref_files:
        rpath = ref.get('path', '')
        full_ref = check_safe_relative_path(rpath, base_dir, f"reference_files[{rpath}]")
        if not os.path.isfile(full_ref):
            raise FileNotFoundError(f"File tham chieu khong ton tai: '{full_ref}'")
        real_ref_hash = sha256_file(full_ref)
        if ref.get('sha256') != real_ref_hash:
            raise ValueError(f"Checksum file tham chieu '{rpath}' khong khop: {real_ref_hash} != {ref.get('sha256')}")
        ref_paths.add(rpath.replace('\\', '/'))

    # Bat buoc phai co prepared va pilot
    if 'prepared/questions_ent.csv' not in ref_paths:
        raise ValueError("reference_files thieu file tham chieu bat buoc 'prepared/questions_ent.csv'")
    if 'reviewed/pilot/questions_pilot.csv' not in ref_paths:
        raise ValueError("reference_files thieu file tham chieu bat buoc 'reviewed/pilot/questions_pilot.csv'")

    print(f"=== XAC MINH THANH CONG TAP LAY MAU TAI: {batch_dir} ===")
    print(f"- Tong so cau hoi: {len(csv_rows)}")
    print(f"- So nhom duy nhat: {len(set(batch_groups))}")
    print(f"- Phan bo nguon: {dict(real_ds_counts)}")
    print(f"- Phan bo nhan: {dict(real_label_counts)}")
    if deficits:
        print(f"- Thieu hut ghi nhan: {deficits}")
    else:
        print("- Thieu hut: Khong co (dat 100% chi tieu)")
    print("Luu y: Bo loc trung lap chi nhan dien cau tuong tu be mat (normalized surface text), khong bao dam tinh doc lap ngu nghia.")
    return True

def main():
    parser = argparse.ArgumentParser(description="Cong cu kiem tra tap lay mau mo rong")
    parser.add_argument(
        '--batch-dir',
        default=None,
        help="Thu muc batch (mac dinh: 02_du_lieu/filedata/reviewed/expansion/batch_02_v1)"
    )
    parser.add_argument(
        '--base-dir',
        default=None,
        help="Thu muc goc du lieu (mac dinh: 02_du_lieu/filedata)"
    )

    args = parser.parse_args()

    if args.base_dir is None:
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../02_du_lieu/filedata'))
    else:
        base_dir = os.path.abspath(args.base_dir)

    if args.batch_dir is None:
        batch_dir = os.path.join(base_dir, 'reviewed/expansion/batch_02_v1')
    else:
        batch_dir = os.path.abspath(args.batch_dir)

    try:
        validate_expansion_batch(batch_dir=batch_dir, base_dir=base_dir)
        sys.exit(0)
    except Exception as e:
        sys.stderr.write(f"LOI XAC MINH: {type(e).__name__}: {e}\n")
        sys.exit(1)

if __name__ == '__main__':
    main()
