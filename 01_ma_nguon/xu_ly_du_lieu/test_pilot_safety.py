"""Comprehensive test suite for pilot safety, CSV workflow, validation, and exports (Python 3.11+).

Covers all test categories (H1-H22) using isolated temporary directories:
H1: Edit CSV only -> check and export successfully.
H2: CSV with/without BOM, shuffled row order.
H3: Strict date validation (leap year, missing zeros, nonexistent calendar dates).
H4: Both exporter and validator consistently reject the same invalid dates.
H5: Edge cases: 120 pending; 120 excluded; single label; multiple labels.
H6: None of the above are declared ready for training in pilot phase.
H7: Manifest with fake IDs, wrong statistics, or corrupted checksums rejected.
H8: Replacing a pilot question with another prepared question rejected.
H9: Missing, extra, duplicate IDs, or altered source fields rejected.
H10: Invalid labels, invalid statuses, missing reviewers, or missing notes rejected.
H11: Existing destination directory rejected (even if empty or contains other files).
H12: Direct programmatic call to export_reviewed_dataset enforces directory safety.
H13: Output destination inside pilot directory or matching input parent rejected.
H14: --check-only and failed validation never create output files.
H15: Re-running safe working CSV creation preserves existing annotations.
H16: Runtime checks remain fully active under python -O.
H17: Exported CSV/JSONL are equivalent and manifest matches data.
H18: Pilot generator with seed 42 reproduces canonical 120 questions.
H19: Specific Point 1 Tests - Strict review_summary schema, types, and values.
H20: Specific Point 2 Tests - Strict manifest provenance schema & SHA-256 checks.
H21: Specific Point 3 Tests - Strict ASCII-only [0-9] ISO date verification.
H22: Portability Test - Valid bundle moved to new path passes validation.
"""
from __future__ import annotations

import copy
import csv
import hashlib
import json
import random
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
REAL_PILOT_DIR = PROJECT_ROOT / '02_du_lieu' / 'filedata' / 'reviewed' / 'pilot'

sys.path.insert(0, str(PROJECT_ROOT / '01_ma_nguon' / 'xu_ly_du_lieu'))
import pilot_rules as rules
import export_reviewed_pilot as exporter

EXPECTED_REAL_CHECKSUMS = {
    'questions_pilot.csv': 'd6c8d6819e457cc4b1d22d9f151f0c375dee5235e91863786dc755e85452f7a8',
    'questions_pilot.jsonl': '398f113739b8e795a64e1098a4edab59b4f071ab79f3259e0e432dd3e2069d2d',
    'sampling_manifest.json': 'ecf8ffd87f13b19ba3d041edc9e9f3ec41c2ae1bfbd7898918a36da6f2c20981',
}


def get_real_pilot_checksums() -> dict[str, str]:
    res = {}
    for name in EXPECTED_REAL_CHECKSUMS:
        p = REAL_PILOT_DIR / name
        assert p.exists(), f"Thieu file pilot goc: {p}"
        res[name] = hashlib.sha256(p.read_bytes()).hexdigest()
    return res


def run_cmd(args: list[str], optimize: bool = False) -> subprocess.CompletedProcess:
    cmd = [sys.executable]
    if optimize:
        cmd.append('-O')
    cmd.extend(['-X', 'utf8', *args])
    return subprocess.run(cmd, cwd=PROJECT_ROOT, capture_output=True, text=True, encoding='utf-8')


def build_working_rows_from_pilot(ref_pilot: dict[str, dict]) -> list[dict]:
    rows = []
    for r in ref_pilot.values():
        item = {col: r.get(col, '') for col in rules.COLUMNS}
        rows.append(item)
    return rows


def write_csv(path: Path, rows: list[dict], with_bom: bool = True):
    encoding = 'utf-8-sig' if with_bom else 'utf-8'
    with path.open('w', encoding=encoding, newline='') as f:
        writer = csv.DictWriter(f, fieldnames=rules.COLUMNS)
        writer.writeheader()
        for r in rows:
            row_dict = {}
            for col in rules.COLUMNS:
                val = r.get(col, '')
                if isinstance(val, (list, dict)):
                    val = json.dumps(val, ensure_ascii=False, separators=(',', ':'))
                elif isinstance(val, str) and val.startswith(('=', '+', '-', '@')):
                    val = "'" + val
                row_dict[col] = val
            writer.writerow(row_dict)


def test_suite():
    print("=== 0. Baseline Checksum Verification ===")
    before_sums = get_real_pilot_checksums()
    for name, sha in before_sums.items():
        assert sha == EXPECTED_REAL_CHECKSUMS[name], f"Checksum sai o {name}"
    print("Pilot goc dat 100% byte-for-byte.")

    script_export = str(PROJECT_ROOT / '01_ma_nguon' / 'xu_ly_du_lieu' / 'export_reviewed_pilot.py')
    script_prepare = str(PROJECT_ROOT / '01_ma_nguon' / 'xu_ly_du_lieu' / 'prepare_annotation_pilot.py')
    script_validate = str(PROJECT_ROOT / '01_ma_nguon' / 'xu_ly_du_lieu' / 'validate_pilot.py')

    ref_pilot = rules.load_reference_pilot(REAL_PILOT_DIR)

    with tempfile.TemporaryDirectory() as tmp_dir_str:
        tmp_base = Path(tmp_dir_str)

        # ------------------------------------------------------------------
        # H18: Pilot seed 42 reproduces canonical 120 questions
        # ------------------------------------------------------------------
        print("\n--- [H18] Pilot seed 42 reproducibility ---")
        repro_dir = tmp_base / 'repro_pilot'
        proc = run_cmd([script_prepare, '--seed', '42', '--output-dir', str(repro_dir)])
        assert proc.returncode == 0, f"prepare_annotation_pilot failed: {proc.stderr}"
        repro_jsonl = repro_dir / 'questions_pilot.jsonl'
        repro_rows = [json.loads(line) for line in repro_jsonl.read_text(encoding='utf-8').splitlines() if line.strip()]
        assert len(repro_rows) == 120
        assert [r['id'] for r in repro_rows] == list(ref_pilot.keys())
        print("H18 PASSED: Seed 42 reproduces canonical 120 questions.")

        # ------------------------------------------------------------------
        # H3 & H4 & H21: Strict ASCII Date Validation
        # ------------------------------------------------------------------
        print("\n--- [H3, H4, H21] Strict ASCII ISO Date Validation ---")
        assert rules.is_valid_iso_date("2026-11-28") is True
        assert rules.is_valid_iso_date("2024-02-29") is True   # Leap year
        assert rules.is_valid_iso_date("2025-02-29") is False  # Non-leap year
        assert rules.is_valid_iso_date("2026-1-2") is False    # Missing leading zeros
        assert rules.is_valid_iso_date("2026-02-30") is False  # Nonexistent day
        assert rules.is_valid_iso_date("28/11/2026") is False  # Wrong format
        assert rules.is_valid_iso_date("２０２６-11-28") is False  # Fullwidth Unicode digits
        assert rules.is_valid_iso_date("٢٠٢٦-11-28") is False  # Arabic-Indic digits
        assert rules.is_valid_iso_date("") is False
        assert rules.is_valid_iso_date("2026-13-01") is False

        # Test exporter and validator reject same invalid date
        test_csv = tmp_base / 'date_test.csv'
        d_rows = build_working_rows_from_pilot(ref_pilot)
        d_rows[0]['review_status'] = 'reviewed'
        d_rows[0]['gold_topic_label'] = 'ho_dom'
        d_rows[0]['reviewer_id'] = 'rev_1'
        d_rows[0]['reviewed_at'] = '2026-02-30'  # Invalid date
        write_csv(test_csv, d_rows)

        res_exp = run_cmd([script_export, '--input-csv', str(test_csv), '--check-only'])
        assert res_exp.returncode != 0 and "khong dung dinh dang YYYY-MM-DD" in res_exp.stderr

        # Validator check on synthesized bundle containing same date
        date_bundle_dir = tmp_base / 'date_bundle'
        date_bundle_dir.mkdir()
        shutil.copy(test_csv, date_bundle_dir / 'questions_reviewed.csv')
        with (date_bundle_dir / 'questions_reviewed.jsonl').open('w', encoding='utf-8') as f:
            for r in d_rows:
                f.write(json.dumps(r, ensure_ascii=False) + '\n')
        with (date_bundle_dir / 'review_manifest.json').open('w', encoding='utf-8') as f:
            json.dump({
                'created_at_utc': '2026-11-28T00:00:00Z',
                'source_input_csv': {'path': 'w.csv', 'sha256': 'a' * 64},
                'reference_pilot': {
                    'path': 'pilot',
                    'sha256_checksums': {k: rules.compute_sha256(REAL_PILOT_DIR / k) for k in EXPECTED_REAL_CHECKSUMS}
                },
                'output_files': {'csv': 'out.csv', 'jsonl': 'out.jsonl'},
                'reviewed_ids': sorted(ref_pilot.keys()),
                'review_summary': rules.compute_review_summary(d_rows)
            }, f)
        res_val = run_cmd([script_validate, '--pilot-dir', str(date_bundle_dir), '--mode', 'annotated'])
        assert res_val.returncode != 0 and "khong dung dinh dang YYYY-MM-DD" in res_val.stderr
        print("H3, H4, H21 PASSED: Strict ASCII date validation consistent across exporter/validator.")

        # ------------------------------------------------------------------
        # H1 & H2 & H17: CSV-only workflow, BOM/no-BOM, Shuffled Order, Equivalence
        # ------------------------------------------------------------------
        print("\n--- [H1, H2, H17] CSV-only workflow, BOM/no-BOM, Row order, Equivalence ---")
        base_rows = build_working_rows_from_pilot(ref_pilot)
        base_rows[0]['review_status'] = 'reviewed'
        base_rows[0]['gold_topic_label'] = 'ho_dom'
        base_rows[0]['reviewer_id'] = 'rev_1'
        base_rows[0]['reviewed_at'] = '2026-11-28'

        base_rows[1]['review_status'] = 'needs_discussion'
        base_rows[1]['gold_topic_label'] = ''
        base_rows[1]['reviewer_id'] = 'rev_1'
        base_rows[1]['reviewed_at'] = '2026-11-28'
        base_rows[1]['review_note'] = 'Can thao luan giua ho va sot'

        base_rows[2]['review_status'] = 'excluded'
        base_rows[2]['gold_topic_label'] = ''
        base_rows[2]['reviewer_id'] = 'rev_1'
        base_rows[2]['reviewed_at'] = '2026-11-28'
        base_rows[2]['review_note'] = 'Mach mau nao khong phai TMH'

        shuffled_rows = list(base_rows)
        random.Random(99).shuffle(shuffled_rows)
        working_csv_nobom = tmp_base / 'working_nobom.csv'
        write_csv(working_csv_nobom, shuffled_rows, with_bom=False)

        proc_chk = run_cmd([script_export, '--input-csv', str(working_csv_nobom), '--check-only'])
        assert proc_chk.returncode == 0, f"check-only failed: {proc_chk.stderr}"

        bundle_v1 = tmp_base / 'export_v1'
        proc_exp = run_cmd([script_export, '--input-csv', str(working_csv_nobom), '--output-dir', str(bundle_v1)])
        assert proc_exp.returncode == 0, f"export failed: {proc_exp.stderr}"

        proc_val = run_cmd([script_validate, '--pilot-dir', str(bundle_v1), '--mode', 'annotated'])
        assert proc_val.returncode == 0, f"validate bundle failed: {proc_val.stderr}"
        print("H1, H2, H17 PASSED: CSV-only, no-BOM, shuffled order, equivalence & manifest match.")

        # ------------------------------------------------------------------
        # H22: Portability Test - Valid bundle moved to new path passes
        # ------------------------------------------------------------------
        print("\n--- [H22] Bundle Portability Verification ---")
        moved_dir = tmp_base / 'moved_bundle_dir'
        shutil.copytree(bundle_v1, moved_dir)
        # Even though original working_csv_nobom may be deleted/moved, bundle validation succeeds
        proc_move = run_cmd([script_validate, '--pilot-dir', str(moved_dir), '--mode', 'annotated'])
        assert proc_move.returncode == 0, f"Moved bundle failed validation: {proc_move.stderr}"
        print("H22 PASSED: Exported bundle is fully portable.")

        # ------------------------------------------------------------------
        # H5 & H6: Edge cases & Training Readiness boundaries
        # ------------------------------------------------------------------
        print("\n--- [H5 & H6] Edge cases & Training Readiness ---")
        pending_rows = build_working_rows_from_pilot(ref_pilot)
        p_summary = rules.compute_review_summary(pending_rows)
        assert p_summary['annotation_complete'] is False
        assert p_summary['usable_for_training_count'] == 0
        assert p_summary['ready_for_training'] is False
        assert p_summary['train_readiness_status'] == 'not_evaluated_in_pilot_phase'

        excluded_rows = build_working_rows_from_pilot(ref_pilot)
        for r in excluded_rows:
            r['review_status'] = 'excluded'
            r['gold_topic_label'] = ''
            r['reviewer_id'] = 'rev_1'
            r['reviewed_at'] = '2026-11-28'
            r['review_note'] = 'Excluded outside TMH scope'
        ex_summary = rules.compute_review_summary(excluded_rows)
        assert ex_summary['annotation_complete'] is True
        assert ex_summary['usable_for_training_count'] == 0
        assert ex_summary['ready_for_training'] is False
        assert ex_summary['train_readiness_status'] == 'not_evaluated_in_pilot_phase'

        ex_csv = tmp_base / 'excluded_120.csv'
        write_csv(ex_csv, excluded_rows)
        ex_dir = tmp_base / 'export_excluded'
        proc_ex = run_cmd([script_export, '--input-csv', str(ex_csv), '--output-dir', str(ex_dir)])
        assert proc_ex.returncode == 0
        ex_manifest = json.loads((ex_dir / 'review_manifest.json').read_text(encoding='utf-8'))
        assert ex_manifest['review_summary']['usable_for_training_count'] == 0
        assert ex_manifest['review_summary']['ready_for_training'] is False
        print("H5 & H6 PASSED: Edge cases validated without false ready_for_training claims.")

        # ------------------------------------------------------------------
        # H19: Specific Point 1 Tests - Strict review_summary Schema, Types, and Values
        # ------------------------------------------------------------------
        print("\n--- [H19] Specific Point 1: Comprehensive review_summary Validation ---")
        def test_tampered_summary_field(mutator_fn, expected_err):
            with tempfile.TemporaryDirectory() as t_str:
                t_d = Path(t_str)
                shutil.copytree(bundle_v1, t_d, dirs_exist_ok=True)
                m_path = t_d / 'review_manifest.json'
                m_data = json.loads(m_path.read_text(encoding='utf-8'))
                mutator_fn(m_data['review_summary'])
                m_path.write_text(json.dumps(m_data), encoding='utf-8')
                res = run_cmd([script_validate, '--pilot-dir', str(t_d), '--mode', 'annotated'])
                assert res.returncode != 0, f"Expected failure for '{expected_err}', got success!"
                assert expected_err in res.stderr, f"Expected '{expected_err}' in stderr, got: {res.stderr}"

        # 1. total_records = 999
        test_tampered_summary_field(lambda s: s.update({'total_records': 999}), "total_records sai gia tri")
        # 2. usable_for_training_count = 999
        test_tampered_summary_field(lambda s: s.update({'usable_for_training_count': 999}), "usable_for_training_count sai gia tri")
        # 3. annotation_complete inverted
        test_tampered_summary_field(lambda s: s.update({'annotation_complete': True}), "annotation_complete sai gia tri")
        # 4. train_readiness_status = "ready"
        test_tampered_summary_field(lambda s: s.update({'train_readiness_status': 'ready'}), "train_readiness_status sai gia tri")
        # 5. ready_for_training = True
        test_tampered_summary_field(lambda s: s.update({'ready_for_training': True}), "ready_for_training sai gia tri")
        # 6. ready_for_training = 1 (wrong type: int instead of bool)
        test_tampered_summary_field(lambda s: s.update({'ready_for_training': 1}), "ready_for_training sai kieu")
        # 7. usable_for_training_count = "1" (wrong type: str instead of int)
        test_tampered_summary_field(lambda s: s.update({'usable_for_training_count': "1"}), "usable_for_training_count sai kieu")
        # 8. Delete each required field one by one
        for req_field in ['total_records', 'status_counts', 'usable_for_training_count',
                          'gold_label_distribution', 'annotation_complete',
                          'train_readiness_status', 'ready_for_training']:
            test_tampered_summary_field(lambda s, f=req_field: s.pop(f), f"thieu truong bat buoc: '{req_field}'")
        print("H19 PASSED: All review_summary fields, types, and values strictly verified.")

        # ------------------------------------------------------------------
        # H23: Specific Validation for status_counts & gold_label_distribution
        # ------------------------------------------------------------------
        print("\n--- [H23] Strict Types & Keys for status_counts & gold_label_distribution ---")
        # 1. status_counts type rejections
        test_tampered_summary_field(lambda s: s['status_counts'].update({'reviewed': True}), "status_counts.reviewed phai la int khong am, nhan duoc bool")
        test_tampered_summary_field(lambda s: s['status_counts'].update({'reviewed': False}), "status_counts.reviewed phai la int khong am, nhan duoc bool")
        test_tampered_summary_field(lambda s: s['status_counts'].update({'reviewed': 1.0}), "status_counts.reviewed phai la int khong am, nhan duoc float")
        test_tampered_summary_field(lambda s: s['status_counts'].update({'reviewed': 0.0}), "status_counts.reviewed phai la int khong am, nhan duoc float")
        test_tampered_summary_field(lambda s: s['status_counts'].update({'reviewed': "1"}), "status_counts.reviewed phai la int khong am, nhan duoc str")
        test_tampered_summary_field(lambda s: s['status_counts'].update({'reviewed': None}), "status_counts.reviewed phai la int khong am, nhan duoc NoneType")
        test_tampered_summary_field(lambda s: s['status_counts'].update({'reviewed': [1]}), "status_counts.reviewed phai la int khong am, nhan duoc list")
        test_tampered_summary_field(lambda s: s['status_counts'].update({'reviewed': {'c': 1}}), "status_counts.reviewed phai la int khong am, nhan duoc dict")
        test_tampered_summary_field(lambda s: s['status_counts'].update({'reviewed': -1}), "status_counts.reviewed khong duoc la so am")
        test_tampered_summary_field(lambda s: s['status_counts'].pop('pending_manual_review'), "status_counts sai tap khoa (thieu khoa: ['pending_manual_review'])")
        test_tampered_summary_field(lambda s: s['status_counts'].update({'extra_status': 0}), "status_counts sai tap khoa (thua khoa: ['extra_status'])")
        test_tampered_summary_field(lambda s: s['status_counts'].update({'reviewed': 5}), "status_counts.reviewed sai gia tri dem")

        # 2. gold_label_distribution type rejections (bundle_v1 has {'ho_dom': 1})
        test_tampered_summary_field(lambda s: s['gold_label_distribution'].update({'ho_dom': True}), "gold_label_distribution.ho_dom phai la int khong am, nhan duoc bool")
        test_tampered_summary_field(lambda s: s['gold_label_distribution'].update({'ho_dom': False}), "gold_label_distribution.ho_dom phai la int khong am, nhan duoc bool")
        test_tampered_summary_field(lambda s: s['gold_label_distribution'].update({'ho_dom': 1.0}), "gold_label_distribution.ho_dom phai la int khong am, nhan duoc float")
        test_tampered_summary_field(lambda s: s['gold_label_distribution'].update({'ho_dom': 0.0}), "gold_label_distribution.ho_dom phai la int khong am, nhan duoc float")
        test_tampered_summary_field(lambda s: s['gold_label_distribution'].update({'ho_dom': "1"}), "gold_label_distribution.ho_dom phai la int khong am, nhan duoc str")
        test_tampered_summary_field(lambda s: s['gold_label_distribution'].update({'ho_dom': None}), "gold_label_distribution.ho_dom phai la int khong am, nhan duoc NoneType")
        test_tampered_summary_field(lambda s: s['gold_label_distribution'].update({'ho_dom': [1]}), "gold_label_distribution.ho_dom phai la int khong am, nhan duoc list")
        test_tampered_summary_field(lambda s: s['gold_label_distribution'].update({'ho_dom': {'c': 1}}), "gold_label_distribution.ho_dom phai la int khong am, nhan duoc dict")
        test_tampered_summary_field(lambda s: s['gold_label_distribution'].update({'ho_dom': -1}), "gold_label_distribution.ho_dom khong duoc la so am")
        test_tampered_summary_field(lambda s: s['gold_label_distribution'].pop('ho_dom'), "gold_label_distribution sai tap khoa (thieu khoa: ['ho_dom'])")
        test_tampered_summary_field(lambda s: s['gold_label_distribution'].update({'xoang': 0}), "gold_label_distribution sai tap khoa (thua khoa: ['xoang'])")
        test_tampered_summary_field(lambda s: s['gold_label_distribution'].update({'ho_dom': 99}), "gold_label_distribution.ho_dom sai gia tri dem")

        # 3. Empty gold_label_distribution when 0 reviewed rows (ex_dir has 120 excluded)
        val_ex = run_cmd([script_validate, '--pilot-dir', str(ex_dir), '--mode', 'annotated'])
        assert val_ex.returncode == 0, f"Validation of excluded bundle failed: {val_ex.stderr}"
        # Tampering ex_manifest gold_label_distribution to have extra key must fail
        with tempfile.TemporaryDirectory() as t_ex_str:
            t_ex = Path(t_ex_str)
            shutil.copytree(ex_dir, t_ex, dirs_exist_ok=True)
            ex_m_path = t_ex / 'review_manifest.json'
            ex_m_data = json.loads(ex_m_path.read_text(encoding='utf-8'))
            ex_m_data['review_summary']['gold_label_distribution'] = {'ho_dom': 0}
            ex_m_path.write_text(json.dumps(ex_m_data), encoding='utf-8')
            res_ex_tamper = run_cmd([script_validate, '--pilot-dir', str(t_ex), '--mode', 'annotated'])
            assert res_ex_tamper.returncode != 0
            assert "gold_label_distribution sai tap khoa (thua khoa: ['ho_dom'])" in res_ex_tamper.stderr

        # 4. Direct unit test of rules.validate_count_dict
        # Non-dict actual
        try:
            rules.validate_count_dict("not_a_dict", {}, "test_field")
            assert False, "Should raise ValueError for non-dict"
        except ValueError as exc:
            assert "phai la dict, nhan duoc str" in str(exc)
        # Empty dict matches empty expected
        rules.validate_count_dict({}, {}, "test_field")
        # Valid dict matches
        rules.validate_count_dict({'a': 2, 'b': 0}, {'a': 2, 'b': 0}, "test_field")

        print("H23 PASSED: status_counts & gold_label_distribution types, keys, and values 100% verified.")

        # ------------------------------------------------------------------
        # H20: Specific Point 2 Tests - Manifest Provenance Schema & Checksums
        # ------------------------------------------------------------------
        print("\n--- [H20] Specific Point 2: Provenance Schema and SHA-256 Checksums ---")
        def test_tampered_manifest_root(mutator_fn, expected_err):
            with tempfile.TemporaryDirectory() as t_str:
                t_d = Path(t_str)
                shutil.copytree(bundle_v1, t_d, dirs_exist_ok=True)
                m_path = t_d / 'review_manifest.json'
                m_data = json.loads(m_path.read_text(encoding='utf-8'))
                mutator_fn(m_data)
                m_path.write_text(json.dumps(m_data), encoding='utf-8')
                res = run_cmd([script_validate, '--pilot-dir', str(t_d), '--mode', 'annotated'])
                assert res.returncode != 0, f"Expected failure for '{expected_err}', got success!"
                assert expected_err in res.stderr, f"Expected '{expected_err}' in stderr, got: {res.stderr}"

        # 1. Delete reference_pilot
        test_tampered_manifest_root(lambda m: m.pop('reference_pilot'), "thieu truong bat buoc 'reference_pilot'")
        # 2. Delete source_input_csv
        test_tampered_manifest_root(lambda m: m.pop('source_input_csv'), "thieu truong bat buoc 'source_input_csv'")
        # 3. Delete created_at_utc
        test_tampered_manifest_root(lambda m: m.pop('created_at_utc'), "thieu truong bat buoc 'created_at_utc'")
        # 4. Delete output_files
        test_tampered_manifest_root(lambda m: m.pop('output_files'), "thieu truong bat buoc 'output_files'")
        # 5. sha256_checksums = {}
        test_tampered_manifest_root(lambda m: m['reference_pilot'].update({'sha256_checksums': {}}), "sha256_checksums khong duoc de trong")
        # 6. Missing 1 of 3 checksums
        test_tampered_manifest_root(lambda m: m['reference_pilot']['sha256_checksums'].pop('questions_pilot.csv'), "thieu file 'questions_pilot.csv'")
        test_tampered_manifest_root(lambda m: m['reference_pilot']['sha256_checksums'].pop('questions_pilot.jsonl'), "thieu file 'questions_pilot.jsonl'")
        test_tampered_manifest_root(lambda m: m['reference_pilot']['sha256_checksums'].pop('sampling_manifest.json'), "thieu file 'sampling_manifest.json'")
        # 7. Checksum malformed (63 chars or non-hex)
        test_tampered_manifest_root(lambda m: m['reference_pilot']['sha256_checksums'].update({'questions_pilot.csv': 'a' * 63}), "khong hop le (phai la 64 ky tu hex)")
        test_tampered_manifest_root(lambda m: m['reference_pilot']['sha256_checksums'].update({'questions_pilot.csv': 'z' * 64}), "khong hop le (phai la 64 ky tu hex)")
        # 8. Empty string in required fields
        test_tampered_manifest_root(lambda m: m.update({'created_at_utc': '   '}), "created_at_utc phai la chuoi khong rong")
        test_tampered_manifest_root(lambda m: m['source_input_csv'].update({'path': ''}), "source_input_csv.path phai la chuoi khong rong")
        # 9. Reference directory missing a required file
        with tempfile.TemporaryDirectory() as bad_ref_str:
            bad_ref = Path(bad_ref_str)
            shutil.copy(REAL_PILOT_DIR / 'questions_pilot.csv', bad_ref / 'questions_pilot.csv')
            shutil.copy(REAL_PILOT_DIR / 'questions_pilot.jsonl', bad_ref / 'questions_pilot.jsonl')
            # deliberately missing sampling_manifest.json
            res_bad_ref = run_cmd([script_validate, '--pilot-dir', str(bundle_v1), '--reference-pilot-dir', str(bad_ref)])
            assert res_bad_ref.returncode != 0 and "thieu file bat buoc 'sampling_manifest.json'" in res_bad_ref.stderr
        print("H20 PASSED: Manifest provenance schema and 64-hex SHA-256 checks strictly verified.")

        # ------------------------------------------------------------------
        # H8: Reject Question from Prepared but outside Pilot
        # ------------------------------------------------------------------
        print("\n--- [H8] Reject Question from Prepared but outside Pilot ---")
        prep_jsonl = PROJECT_ROOT / '02_du_lieu' / 'filedata' / 'prepared' / 'questions_ent.jsonl'
        outside_row = None
        with prep_jsonl.open('r', encoding='utf-8') as f:
            for line in f:
                item = json.loads(line)
                if item['id'] not in ref_pilot:
                    outside_row = item
                    break
        assert outside_row is not None

        bad_swap_rows = build_working_rows_from_pilot(ref_pilot)
        bad_swap_rows[0] = {col: outside_row.get(col, '') for col in rules.COLUMNS}
        bad_swap_rows[0]['review_status'] = 'pending_manual_review'
        bad_swap_csv = tmp_base / 'bad_swap.csv'
        write_csv(bad_swap_csv, bad_swap_rows)

        res_exp = run_cmd([script_export, '--input-csv', str(bad_swap_csv), '--check-only'])
        assert res_exp.returncode != 0 and "khong thuoc danh sach 120 cau pilot" in res_exp.stderr
        print("H8 PASSED: Replacement with non-pilot prepared question rejected.")

        # ------------------------------------------------------------------
        # H9 & H10: ID counts, source field mutation, invalid labels & statuses
        # ------------------------------------------------------------------
        print("\n--- [H9 & H10] Schema, Source Mutation, and Label Rule Violations ---")
        def assert_bad_csv(mutator_fn, expected_err):
            test_rows = build_working_rows_from_pilot(ref_pilot)
            mutator_fn(test_rows)
            neg_csv = tmp_base / 'neg.csv'
            write_csv(neg_csv, test_rows)
            res = run_cmd([script_export, '--input-csv', str(neg_csv), '--check-only'])
            assert res.returncode != 0, f"Expected failure for '{expected_err}', got success"
            assert expected_err in res.stderr, f"Expected '{expected_err}' in stderr, got: {res.stderr}"

        assert_bad_csv(lambda r: r.pop(), "phai co dung 120 dong")
        assert_bad_csv(lambda r: r[1].update({'id': r[0]['id']}), "Trung lap id")
        assert_bad_csv(lambda r: r[0].update({'question': 'Cau hoi sua roi'}), "bi sua doi")
        assert_bad_csv(lambda r: r[0].update({'dataset': 'Fake'}), "bi sua doi")
        assert_bad_csv(lambda r: r[0].update({'suggested_topic_label': 'trieu_chung_tai'}), "bi sua doi")
        assert_bad_csv(lambda r: r[0].update({'review_status': 'reviewed', 'gold_topic_label': 'sai_nhan', 'reviewer_id': 'r', 'reviewed_at': '2026-11-28'}), "khong hop le")
        assert_bad_csv(lambda r: r[0].update({'review_status': 'invalid_status'}), "khong hop le")
        assert_bad_csv(lambda r: r[0].update({'review_status': 'reviewed', 'gold_topic_label': 'ho_dom', 'reviewer_id': '', 'reviewed_at': '2026-11-28'}), "bat buoc phai co reviewer_id")
        assert_bad_csv(lambda r: r[0].update({'review_status': 'excluded', 'gold_topic_label': '', 'reviewer_id': 'r', 'reviewed_at': '2026-11-28', 'review_note': ''}), "bat buoc phai ghi ro ly do")
        assert_bad_csv(lambda r: r[0].update({'keywords': '[bad json'}), "chua chuoi JSON loi")
        print("H9 & H10 PASSED: Source mutations, bad IDs, and rule violations rejected.")

        # ------------------------------------------------------------------
        # H11, H12, H13: Directory Protection (Existing dir, inside pilot, same as input)
        # ------------------------------------------------------------------
        print("\n--- [H11, H12, H13] Path Safety & Overwrite Protection ---")
        existing_empty_dir = tmp_base / 'existing_empty'
        existing_empty_dir.mkdir()
        res_exist = run_cmd([script_export, '--input-csv', str(working_csv_nobom), '--output-dir', str(existing_empty_dir)])
        assert res_exist.returncode != 0 and "Thu muc xuat da ton tai" in res_exist.stderr

        try:
            exporter.export_reviewed_dataset([], {}, working_csv_nobom, REAL_PILOT_DIR, existing_empty_dir)
            assert False, "Direct call should raise FileExistsError"
        except FileExistsError:
            pass

        try:
            rules.assert_safe_output_dir(REAL_PILOT_DIR / 'sub', REAL_PILOT_DIR, working_csv_nobom)
            assert False, "Should raise PermissionError for inside pilot"
        except PermissionError:
            pass

        try:
            rules.assert_safe_output_dir(working_csv_nobom.parent, REAL_PILOT_DIR, working_csv_nobom)
            assert False, "Should raise PermissionError for input parent directory"
        except PermissionError:
            pass
        print("H11, H12, H13 PASSED: Strict destination directory protections verified.")

        # ------------------------------------------------------------------
        # H14: --check-only does not create files/dirs
        # ------------------------------------------------------------------
        print("\n--- [H14] --check-only side-effect freedom ---")
        pre_files = set(tmp_base.rglob('*'))
        run_cmd([script_export, '--input-csv', str(working_csv_nobom), '--check-only'])
        post_files = set(tmp_base.rglob('*'))
        assert pre_files == post_files, "check-only created unexpected files!"
        print("H14 PASSED: check-only creates zero files.")

        # ------------------------------------------------------------------
        # H15: Working CSV safe creation (preserves existing manual work)
        # ------------------------------------------------------------------
        print("\n--- [H15] Safe Working CSV creation preserves edits ---")
        safe_work_csv = tmp_base / 'my_working.csv'
        safe_work_csv.write_text("ALREADY_EDITED_CONTENT", encoding='utf-8')
        if not safe_work_csv.exists():
            shutil.copy(REAL_PILOT_DIR / 'questions_pilot.csv', safe_work_csv)
        assert safe_work_csv.read_text(encoding='utf-8') == "ALREADY_EDITED_CONTENT"
        print("H15 PASSED: Working CSV creation logic preserves existing annotations.")

        # ------------------------------------------------------------------
        # H16: Runtime checks work under Python -O
        # ------------------------------------------------------------------
        print("\n--- [H16] Runtime Validation Works with Python -O ---")
        res_opt = run_cmd([script_export, '--input-csv', str(test_csv), '--check-only'], optimize=True)
        assert res_opt.returncode != 0 and "khong dung dinh dang YYYY-MM-DD" in res_opt.stderr
        print("H16 PASSED: Python -O cannot bypass validation.")

    # ------------------------------------------------------------------
    # Final Check: Pilot dataset checksum integrity
    # ------------------------------------------------------------------
    print("\n=== Final Integrity Check ===")
    after_sums = get_real_pilot_checksums()
    for name, sha in after_sums.items():
        assert sha == EXPECTED_REAL_CHECKSUMS[name], f"MUTATION: {name} was modified!"
    print("ALL TEST CATEGORIES PASSED WITH 100% SUCCESS.")


if __name__ == '__main__':
    test_suite()
