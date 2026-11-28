#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bo kiem thu hoi quy toan dien cho cong cu lay mau mo rong dot 02 va validator.
Bao quat day du cac nhom loi A-L duoc yeu cau kiem tra doc lap:
A. Tung thu muc con moi duoi raw, normalized, prepared va pilot bi tu choi.
B. Thu muc dich da ton tai, rong hoac co du lieu, deu khong bi ghi de.
C. Quota 0 khong chon cau nao trong nhom do; quota hon hop 0 va duong hoat dong dung.
D. Quota am, bool, float, chuoi, null va nhan la bi tu choi truoc khi ghi.
E. Thieu quota hop le duoc chap nhan; khong lay qua quota.
F. JSONL dung chuoi thay list bi tu choi cho tung truong mang.
G. Xoa tung truong duyet bat buoc bi tu choi.
H. Sai kieu cac truong chuoi hoac phan tu mang bi tu choi.
I. unique_ids_count/unique_groups_count sai so luong hoac sai kieu bi tu choi.
J. Manifest sai duong dan dau ra, thieu tham chieu bat buoc hoac deficits gia bi tu choi.
K. Bundle batch_02_v1 hien tai van hop le.
L. Cung seed va cau hinh cho cung ID/thu tu o hai thu muc moi.
"""

import os
import sys
import csv
import json
import shutil
import hashlib
import tempfile
import unittest
import subprocess

# Import modules can kiem thu
sys.path.insert(0, os.path.dirname(__file__))
from sample_expansion import sample_expansion, sha256_file
from validate_expansion import validate_expansion_batch

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../02_du_lieu/filedata'))
BATCH_02_DIR = os.path.join(BASE_DIR, 'reviewed/expansion/batch_02_v1')

class TestExpansionRegressionSuite(unittest.TestCase):

    def setUp(self):
        self.temp_dir_obj = tempfile.TemporaryDirectory()
        self.test_root = self.temp_dir_obj.name

        # Tao mock base_dir day du cau truc de kiem thu sample_expansion ma khong dong vao filedata that
        self.mock_base = os.path.join(self.test_root, 'mock_filedata')
        os.makedirs(os.path.join(self.mock_base, 'raw'), exist_ok=True)
        os.makedirs(os.path.join(self.mock_base, 'normalized'), exist_ok=True)
        os.makedirs(os.path.join(self.mock_base, 'prepared'), exist_ok=True)
        os.makedirs(os.path.join(self.mock_base, 'reviewed/pilot'), exist_ok=True)
        os.makedirs(os.path.join(self.mock_base, 'reviewed/expansion'), exist_ok=True)

        shutil.copy2(
            os.path.join(BASE_DIR, 'prepared/questions_ent.csv'),
            os.path.join(self.mock_base, 'prepared/questions_ent.csv')
        )
        shutil.copy2(
            os.path.join(BASE_DIR, 'reviewed/pilot/questions_pilot.csv'),
            os.path.join(self.mock_base, 'reviewed/pilot/questions_pilot.csv')
        )

    def tearDown(self):
        self.temp_dir_obj.cleanup()

    def _copy_batch(self, subname):
        """Sao chep batch_02_v1 vao mock_base/reviewed/expansion/subname de kiem thu bien the"""
        dst_dir = os.path.join(self.mock_base, 'reviewed/expansion', subname)
        os.makedirs(dst_dir, exist_ok=True)
        for fname in ['questions_expansion.csv', 'questions_expansion.jsonl', 'sampling_manifest.json']:
            shutil.copy2(os.path.join(BATCH_02_DIR, fname), os.path.join(dst_dir, fname))

        # Cap nhat duong dan output_files trong manifest de tro dung vao dst_dir
        m_path = os.path.join(dst_dir, 'sampling_manifest.json')
        with open(m_path, 'r', encoding='utf-8') as f:
            m = json.load(f)
        rel_csv = os.path.relpath(os.path.join(dst_dir, 'questions_expansion.csv'), self.mock_base).replace('\\', '/')
        rel_jsonl = os.path.relpath(os.path.join(dst_dir, 'questions_expansion.jsonl'), self.mock_base).replace('\\', '/')
        m['output_files']['csv']['path'] = rel_csv
        m['output_files']['jsonl']['path'] = rel_jsonl
        m['output_files']['csv']['sha256'] = sha256_file(os.path.join(dst_dir, 'questions_expansion.csv'))
        m['output_files']['jsonl']['sha256'] = sha256_file(os.path.join(dst_dir, 'questions_expansion.jsonl'))
        with open(m_path, 'w', encoding='utf-8') as f:
            json.dump(m, f, ensure_ascii=False, indent=2)
        return dst_dir

    def _update_manifest_hashes(self, batch_dir):
        """Cap nhat lai checksum file output trong manifest de validator kiem tra schema/thong ke"""
        m_path = os.path.join(batch_dir, 'sampling_manifest.json')
        with open(m_path, 'r', encoding='utf-8') as f:
            m = json.load(f)
        csv_file = os.path.join(batch_dir, 'questions_expansion.csv')
        jsonl_file = os.path.join(batch_dir, 'questions_expansion.jsonl')
        if os.path.exists(csv_file):
            m['output_files']['csv']['sha256'] = sha256_file(csv_file)
        if os.path.exists(jsonl_file):
            m['output_files']['jsonl']['sha256'] = sha256_file(jsonl_file)
        with open(m_path, 'w', encoding='utf-8') as f:
            json.dump(m, f, ensure_ascii=False, indent=2)

    # A. Tung thu muc con moi duoi raw, normalized, prepared va pilot bi tu choi
    def test_a_protected_zones_subdirs_rejected(self):
        protected_zones = ['raw', 'normalized', 'prepared', 'reviewed/pilot']
        for pz in protected_zones:
            sub_target = os.path.join(self.mock_base, pz, 'new_export')
            with self.assertRaises(ValueError, msg=f"Chua chan thu muc con duoi '{pz}'"):
                sample_expansion(base_dir=self.mock_base, output_dir=sub_target)
            self.assertFalse(os.path.exists(sub_target))

            # Chinh thu muc bao ve
            direct_target = os.path.join(self.mock_base, pz)
            with self.assertRaises((ValueError, FileExistsError)):
                sample_expansion(base_dir=self.mock_base, output_dir=direct_target)

    # B. Thu muc dich da ton tai, rong hoac co du lieu, deu khong bi ghi de
    def test_b_existing_target_dir_never_overwritten(self):
        # Thu muc rong
        empty_dir = os.path.join(self.mock_base, 'reviewed/expansion/empty_dir')
        os.makedirs(empty_dir)
        with self.assertRaises(FileExistsError):
            sample_expansion(base_dir=self.mock_base, output_dir=empty_dir)

        # Thu muc co du lieu
        non_empty_dir = os.path.join(self.mock_base, 'reviewed/expansion/non_empty_dir')
        os.makedirs(non_empty_dir)
        sentinel_file = os.path.join(non_empty_dir, 'sentinel.txt')
        with open(sentinel_file, 'w', encoding='utf-8') as f:
            f.write("DO_NOT_OVERWRITE")
        with self.assertRaises(FileExistsError):
            sample_expansion(base_dir=self.mock_base, output_dir=non_empty_dir)
        with open(sentinel_file, 'r', encoding='utf-8') as f:
            self.assertEqual(f.read(), "DO_NOT_OVERWRITE")

        # Thu muc batch_02_v1 that
        with self.assertRaises(FileExistsError):
            sample_expansion(base_dir=BASE_DIR, output_dir=BATCH_02_DIR)

    # C. Quota 0 khong chon cau nao trong nhom do; quota hon hop 0 va duong hoat dong dung
    def test_c_zero_quota_and_mixed_quotas(self):
        target_dir = os.path.join(self.mock_base, 'reviewed/expansion/mixed_quota_batch')
        mixed_quotas = {
            'ho_dom': 0, # Phai bo qua, lay dung 0 cau
            'sot': 10,
            'cam_lanh': 5
        }
        manifest = sample_expansion(
            base_dir=self.mock_base,
            output_dir=target_dir,
            target_quotas=mixed_quotas
        )
        self.assertEqual(manifest['sampling_parameters']['actual_total'], 15)
        self.assertEqual(manifest['sampling_parameters']['actual_by_suggested_label'].get('ho_dom', 0), 0)
        self.assertEqual(manifest['sampling_parameters']['actual_by_suggested_label'].get('sot'), 10)
        self.assertEqual(manifest['sampling_parameters']['actual_by_suggested_label'].get('cam_lanh'), 5)
        # Validator chap nhan tap nay
        self.assertTrue(validate_expansion_batch(target_dir, self.mock_base))

        # Tong quota bang 0 phai bi tu choi truoc khi tao thu muc
        zero_total_dir = os.path.join(self.mock_base, 'reviewed/expansion/zero_total_batch')
        with self.assertRaises(ValueError):
            sample_expansion(
                base_dir=self.mock_base,
                output_dir=zero_total_dir,
                target_quotas={'ho_dom': 0, 'sot': 0}
            )
        self.assertFalse(os.path.exists(zero_total_dir))

    # D. Quota am, bool, float, chuoi, null va nhan la bi tu choi truoc khi ghi
    def test_d_invalid_quotas_rejected_before_writing(self):
        invalid_cases = [
            ({'sot': -5}, (ValueError, TypeError)),
            ({'sot': True}, TypeError),
            ({'sot': False}, TypeError),
            ({'sot': 5.5}, TypeError),
            ({'sot': '10'}, TypeError),
            ({'sot': None}, TypeError),
            ({'nhan_la_khong_hop_le': 10}, ValueError),
        ]
        target_dir = os.path.join(self.mock_base, 'reviewed/expansion/invalid_quota_batch')

        for bad_quota, exc_type in invalid_cases:
            with self.assertRaises(exc_type, msg=f"Failed on quota: {bad_quota}"):
                sample_expansion(base_dir=self.mock_base, output_dir=target_dir, target_quotas=bad_quota)
            self.assertFalse(os.path.exists(target_dir))

        # Seed sai kieu
        for bad_seed in ['42', True, 3.14, None]:
            with self.assertRaises(TypeError, msg=f"Failed on seed: {bad_seed}"):
                sample_expansion(base_dir=self.mock_base, output_dir=target_dir, seed=bad_seed)
            self.assertFalse(os.path.exists(target_dir))

    # E. Thieu quota hop le duoc chap nhan; khong lay qua quota
    def test_e_valid_deficit_accepted_and_never_exceed_quota(self):
        target_dir = os.path.join(self.mock_base, 'reviewed/expansion/deficit_batch')
        # cam_lanh trong prepared chi co 9 ung vien ngoai pilot, dat quota la 20
        custom_quotas = {
            'cam_lanh': 20,
            'sot': 5
        }
        manifest = sample_expansion(
            base_dir=self.mock_base,
            output_dir=target_dir,
            target_quotas=custom_quotas
        )
        self.assertIn('cam_lanh', manifest['sampling_parameters']['deficits'])
        d_cam_lanh = manifest['sampling_parameters']['deficits']['cam_lanh']
        self.assertEqual(d_cam_lanh['target'], 20)
        self.assertEqual(d_cam_lanh['actual'], 9)
        self.assertEqual(d_cam_lanh['deficit'], 11)
        # Khong bao gio lay qua quota: sot phai dung 5
        self.assertEqual(manifest['sampling_parameters']['actual_by_suggested_label']['sot'], 5)
        # Validator chap nhan tap thieu hut hop le nay
        self.assertTrue(validate_expansion_batch(target_dir, self.mock_base))

    # F. JSONL dung chuoi thay list bi tu choi cho tung truong mang
    def test_f_jsonl_array_as_string_rejected(self):
        array_fields = ['provenance_ids', 'topic_candidates', 'keywords']
        for fld in array_fields:
            target_dir = self._copy_batch(f'bad_jsonl_{fld}')
            jsonl_path = os.path.join(target_dir, 'questions_expansion.jsonl')
            with open(jsonl_path, 'r', encoding='utf-8') as f:
                lines = [json.loads(l) for l in f]
            # Bien list thanh chuoi JSON
            lines[0][fld] = json.dumps(lines[0][fld])
            with open(jsonl_path, 'w', encoding='utf-8') as f:
                for item in lines:
                    f.write(json.dumps(item, ensure_ascii=False) + '\n')
            self._update_manifest_hashes(target_dir)

            with self.assertRaises(TypeError, msg=f"Chua chan chuoi thay list cho '{fld}'") as ctx:
                validate_expansion_batch(target_dir, self.mock_base)
            self.assertIn(fld, str(ctx.exception))

    # G. Xoa tung truong duyet bat buoc bi tu choi
    def test_g_missing_required_review_fields_rejected(self):
        review_fields = ['gold_topic_label', 'review_status', 'reviewer_id', 'reviewed_at', 'review_note']
        for fld in review_fields:
            target_dir = self._copy_batch(f'missing_{fld}')
            jsonl_path = os.path.join(target_dir, 'questions_expansion.jsonl')
            with open(jsonl_path, 'r', encoding='utf-8') as f:
                lines = [json.loads(l) for l in f]
            del lines[0][fld]
            with open(jsonl_path, 'w', encoding='utf-8') as f:
                for item in lines:
                    f.write(json.dumps(item, ensure_ascii=False) + '\n')
            self._update_manifest_hashes(target_dir)

            with self.assertRaises(ValueError, msg=f"Chua chan thieu truong '{fld}' trong JSONL") as ctx:
                validate_expansion_batch(target_dir, self.mock_base)
            self.assertIn(fld, str(ctx.exception))

    # H. Sai kieu cac truong chuoi hoac phan tu mang bi tu choi
    def test_h_wrong_types_for_strings_or_array_elements_rejected(self):
        # H1: So int thay cho chuoi question trong JSONL
        target_dir = self._copy_batch('wrong_type_string')
        jsonl_path = os.path.join(target_dir, 'questions_expansion.jsonl')
        with open(jsonl_path, 'r', encoding='utf-8') as f:
            lines = [json.loads(l) for l in f]
        lines[0]['question'] = 99999
        with open(jsonl_path, 'w', encoding='utf-8') as f:
            for item in lines:
                f.write(json.dumps(item, ensure_ascii=False) + '\n')
        self._update_manifest_hashes(target_dir)
        with self.assertRaises(TypeError):
            validate_expansion_batch(target_dir, self.mock_base)

        # H2: So int ben trong mang keywords cua JSONL
        target_dir2 = self._copy_batch('wrong_type_array_elem')
        jsonl_path = os.path.join(target_dir2, 'questions_expansion.jsonl')
        with open(jsonl_path, 'r', encoding='utf-8') as f:
            lines = [json.loads(l) for l in f]
        lines[0]['keywords'].append(12345)
        with open(jsonl_path, 'w', encoding='utf-8') as f:
            for item in lines:
                f.write(json.dumps(item, ensure_ascii=False) + '\n')
        self._update_manifest_hashes(target_dir2)
        with self.assertRaises(TypeError):
            validate_expansion_batch(target_dir2, self.mock_base)

    # I. unique_ids_count/unique_groups_count sai so luong hoac sai kieu bi tu choi
    def test_i_unique_counts_validation(self):
        invalid_type_cases = [
            ('unique_ids_count', True, TypeError),
            ('unique_groups_count', -10, TypeError),
            ('unique_ids_count', '200', TypeError),
            ('unique_groups_count', 200.0, TypeError),
            ('unique_ids_count', 199, ValueError), # Sai so luong thuc te
            ('unique_groups_count', 199, ValueError) # Sai so luong thuc te
        ]
        for field, bad_val, exc_type in invalid_type_cases:
            target_dir = self._copy_batch(f'bad_count_{field}_{bad_val}')
            m_path = os.path.join(target_dir, 'sampling_manifest.json')
            with open(m_path, 'r', encoding='utf-8') as f:
                m = json.load(f)
            m['deduplication_and_scope'][field] = bad_val
            with open(m_path, 'w', encoding='utf-8') as f:
                json.dump(m, f, ensure_ascii=False, indent=2)
            with self.assertRaises(exc_type, msg=f"Failed on {field}={bad_val}"):
                validate_expansion_batch(target_dir, self.mock_base)

    # J. Manifest sai duong dan dau ra, thieu tham chieu bat buoc hoac deficits gia bi tu choi
    def test_j_manifest_paths_references_and_fake_deficits(self):
        # J1: Duong dan output khong tro dung file dang xac minh
        target_dir = self._copy_batch('wrong_out_path')
        m_path = os.path.join(target_dir, 'sampling_manifest.json')
        with open(m_path, 'r', encoding='utf-8') as f:
            m = json.load(f)
        m['output_files']['csv']['path'] = 'reviewed/expansion/batch_02_v1/another_file.csv'
        with open(m_path, 'w', encoding='utf-8') as f:
            json.dump(m, f, ensure_ascii=False, indent=2)
        with self.assertRaises(ValueError) as ctx:
            validate_expansion_batch(target_dir, self.mock_base)
        self.assertIn("khong tro dung file CSV", str(ctx.exception))

        # J2: reference_files rong
        target_dir2 = self._copy_batch('missing_ref')
        m_path = os.path.join(target_dir2, 'sampling_manifest.json')
        with open(m_path, 'r', encoding='utf-8') as f:
            m = json.load(f)
        m['reference_files'] = []
        with open(m_path, 'w', encoding='utf-8') as f:
            json.dump(m, f, ensure_ascii=False, indent=2)
        with self.assertRaises(ValueError) as ctx:
            validate_expansion_batch(target_dir2, self.mock_base)
        self.assertIn("reference_files trong manifest khong duoc rong", str(ctx.exception))

        # J3: Deficit gia cho nhan da dat du chi tieu (deficit = 1)
        target_dir3 = self._copy_batch('fake_deficit')
        m_path = os.path.join(target_dir3, 'sampling_manifest.json')
        with open(m_path, 'r', encoding='utf-8') as f:
            m = json.load(f)
        m['sampling_parameters']['deficits']['cam_cum'] = {'target': 30, 'actual': 30, 'deficit': 1}
        with open(m_path, 'w', encoding='utf-8') as f:
            json.dump(m, f, ensure_ascii=False, indent=2)
        with self.assertRaises(ValueError) as ctx:
            validate_expansion_batch(target_dir3, self.mock_base)
        self.assertIn("Khoa thua trong deficits", str(ctx.exception))

        # J4: Deficit cho nhan da du chi tieu nhung deficit = 0 (khong duoc xuat hien trong deficits)
        target_dir4 = self._copy_batch('deficit_zero_full_quota')
        m_path = os.path.join(target_dir4, 'sampling_manifest.json')
        with open(m_path, 'r', encoding='utf-8') as f:
            m = json.load(f)
        m['sampling_parameters']['deficits']['ho_dom'] = {'target': 25, 'actual': 25, 'deficit': 0}
        with open(m_path, 'w', encoding='utf-8') as f:
            json.dump(m, f, ensure_ascii=False, indent=2)
        with self.assertRaises(ValueError) as ctx:
            validate_expansion_batch(target_dir4, self.mock_base)
        self.assertIn("Khoa thua trong deficits", str(ctx.exception))

        # J5: Payload loi da tai hien: target=True, actual='FAKE', deficit=False
        target_dir5 = self._copy_batch('reproduced_fake_payload')
        m_path = os.path.join(target_dir5, 'sampling_manifest.json')
        with open(m_path, 'r', encoding='utf-8') as f:
            m = json.load(f)
        m['sampling_parameters']['deficits']['ho_dom'] = {
            'target': True,
            'actual': 'FAKE',
            'deficit': False
        }
        with open(m_path, 'w', encoding='utf-8') as f:
            json.dump(m, f, ensure_ascii=False, indent=2)
        with self.assertRaises((ValueError, TypeError)) as ctx:
            validate_expansion_batch(target_dir5, self.mock_base)

        # J6: Nhan du quota nhung deficits la kieu sai (str hoac int)
        target_dir6 = self._copy_batch('bad_deficit_type_for_full_quota')
        m_path = os.path.join(target_dir6, 'sampling_manifest.json')
        with open(m_path, 'r', encoding='utf-8') as f:
            m = json.load(f)
        m['sampling_parameters']['deficits']['ho_dom'] = "invalid_string"
        with open(m_path, 'w', encoding='utf-8') as f:
            json.dump(m, f, ensure_ascii=False, indent=2)
        with self.assertRaises((ValueError, TypeError)):
            validate_expansion_batch(target_dir6, self.mock_base)

        # J7: Khoa deficit la khong nam trong target_quotas
        target_dir7 = self._copy_batch('strange_deficit_key')
        m_path = os.path.join(target_dir7, 'sampling_manifest.json')
        with open(m_path, 'r', encoding='utf-8') as f:
            m = json.load(f)
        m['sampling_parameters']['deficits']['strange_label'] = {'target': 10, 'actual': 5, 'deficit': 5}
        with open(m_path, 'w', encoding='utf-8') as f:
            json.dump(m, f, ensure_ascii=False, indent=2)
        with self.assertRaises(ValueError) as ctx:
            validate_expansion_batch(target_dir7, self.mock_base)
        self.assertIn("Khoa thua trong deficits", str(ctx.exception))

    # J_ext: Kiem thu thieu hut thuc te: sai kieu, sai gia tri, thieu truong, thieu khoa
    def test_j_ext_real_deficit_validation(self):
        import copy
        # Tao mot batch thieu quota hop le: cam_lanh quota 20 (chi co 9), sot quota 5
        deficit_dir = os.path.join(self.mock_base, 'reviewed/expansion/deficit_test_base')
        sample_expansion(
            base_dir=self.mock_base,
            output_dir=deficit_dir,
            target_quotas={'cam_lanh': 20, 'sot': 5}
        )
        # Kiem tra bundle goc hop le
        self.assertTrue(validate_expansion_batch(deficit_dir, self.mock_base))

        m_path = os.path.join(deficit_dir, 'sampling_manifest.json')
        with open(m_path, 'r', encoding='utf-8') as f:
            clean_manifest = json.load(f)

        # J_ext1: target=True (bool) trong muc deficit
        m = copy.deepcopy(clean_manifest)
        m['sampling_parameters']['deficits']['cam_lanh']['target'] = True
        with open(m_path, 'w', encoding='utf-8') as f: json.dump(m, f, indent=2)
        with self.assertRaises(TypeError):
            validate_expansion_batch(deficit_dir, self.mock_base)

        # J_ext2: actual='9' (str) trong muc deficit
        m = copy.deepcopy(clean_manifest)
        m['sampling_parameters']['deficits']['cam_lanh']['actual'] = '9'
        with open(m_path, 'w', encoding='utf-8') as f: json.dump(m, f, indent=2)
        with self.assertRaises(TypeError):
            validate_expansion_batch(deficit_dir, self.mock_base)

        # J_ext3: deficit=False (bool) trong muc deficit
        m = copy.deepcopy(clean_manifest)
        m['sampling_parameters']['deficits']['cam_lanh']['deficit'] = False
        with open(m_path, 'w', encoding='utf-8') as f: json.dump(m, f, indent=2)
        with self.assertRaises(TypeError):
            validate_expansion_batch(deficit_dir, self.mock_base)

        # J_ext4: deficit=-1 (so am)
        m = copy.deepcopy(clean_manifest)
        m['sampling_parameters']['deficits']['cam_lanh']['deficit'] = -1
        with open(m_path, 'w', encoding='utf-8') as f: json.dump(m, f, indent=2)
        with self.assertRaises((TypeError, ValueError)):
            validate_expansion_batch(deficit_dir, self.mock_base)

        # J_ext5: deficit=10 (sai gia tri, dung phai la 11)
        m = copy.deepcopy(clean_manifest)
        m['sampling_parameters']['deficits']['cam_lanh']['deficit'] = 10
        with open(m_path, 'w', encoding='utf-8') as f: json.dump(m, f, indent=2)
        with self.assertRaises(ValueError):
            validate_expansion_batch(deficit_dir, self.mock_base)

        # J_ext6: Thieu truong 'deficit' trong muc deficit
        m = copy.deepcopy(clean_manifest)
        del m['sampling_parameters']['deficits']['cam_lanh']['deficit']
        with open(m_path, 'w', encoding='utf-8') as f: json.dump(m, f, indent=2)
        with self.assertRaises(ValueError):
            validate_expansion_batch(deficit_dir, self.mock_base)

        # J_ext7: Thieu khoa cam_lanh khoi deficits khi dang thieu hut
        m = copy.deepcopy(clean_manifest)
        m['sampling_parameters']['deficits'] = {}
        with open(m_path, 'w', encoding='utf-8') as f: json.dump(m, f, indent=2)
        with self.assertRaises(ValueError) as ctx:
            validate_expansion_batch(deficit_dir, self.mock_base)
        self.assertIn("Khoa thieu trong deficits", str(ctx.exception))

        # J_ext8: actual vuot qua target quota (target quota giam xuong 4 trong khi actual la 5)
        m = copy.deepcopy(clean_manifest)
        m['sampling_parameters']['target_quotas']['sot'] = 4
        m['sampling_parameters']['target_quotas']['cam_lanh'] = 21 # Giu tong target_total khong doi
        with open(m_path, 'w', encoding='utf-8') as f: json.dump(m, f, indent=2)
        with self.assertRaises(ValueError) as ctx:
            validate_expansion_batch(deficit_dir, self.mock_base)
        self.assertIn("vuot qua target quota", str(ctx.exception))

    # K. Bundle batch_02_v1 hien tai van hop le
    def test_k_batch_02_v1_remains_valid(self):
        self.assertTrue(os.path.isdir(BATCH_02_DIR))
        result = validate_expansion_batch(BATCH_02_DIR, BASE_DIR)
        self.assertTrue(result)

    # L. Cung seed va cau hinh cho cung ID/thu tu o hai thu muc moi
    def test_l_sampler_determinism(self):
        dir_run1 = os.path.join(self.mock_base, 'reviewed/expansion/repro_1')
        dir_run2 = os.path.join(self.mock_base, 'reviewed/expansion/repro_2')

        m1 = sample_expansion(base_dir=self.mock_base, output_dir=dir_run1, seed=42)
        m2 = sample_expansion(base_dir=self.mock_base, output_dir=dir_run2, seed=42)

        self.assertEqual(m1['sampled_ids'], m2['sampled_ids'])
        self.assertEqual(m1['sampled_group_ids'], m2['sampled_group_ids'])
        self.assertEqual(m1['output_files']['csv']['sha256'], m2['output_files']['csv']['sha256'])
        self.assertEqual(m1['output_files']['jsonl']['sha256'], m2['output_files']['jsonl']['sha256'])

        # So sanh voi batch_02_v1
        with open(os.path.join(BATCH_02_DIR, 'sampling_manifest.json'), 'r', encoding='utf-8') as f:
            m_existing = json.load(f)
        self.assertEqual(m1['sampled_ids'], m_existing['sampled_ids'])
        self.assertEqual(m1['sampled_group_ids'], m_existing['sampled_group_ids'])

if __name__ == '__main__':
    unittest.main()
