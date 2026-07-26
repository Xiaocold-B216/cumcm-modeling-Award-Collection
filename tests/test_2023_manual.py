from __future__ import annotations

import csv
import hashlib
import json
import os
from collections import Counter, defaultdict
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = Path(os.environ.get('CUMCM_SOURCE_ROOT', ROOT))
AI = ROOT / 'analysis-index'


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding='utf-8-sig').splitlines() if line.strip()]


def sha256(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


@pytest.fixture(scope='module')
def carriers():
    return read_jsonl(AI / '01_inventory/2023_carrier_manifest.jsonl')


@pytest.fixture(scope='module')
def documents():
    with (AI / '02_documents/logical_documents/2023.csv').open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))


@pytest.fixture(scope='module')
def reps():
    return read_jsonl(AI / '04_relations/2023_representations.jsonl')


@pytest.fixture(scope='module')
def segs():
    return read_jsonl(AI / '03_segments/2023_segments.jsonl')


def test_required_annual_files_exist():
    required = [
        '01_inventory/2023_carrier_manifest.jsonl',
        '02_documents/logical_documents/2023.csv',
        '03_segments/2023_segments.jsonl',
        '04_relations/2023_representations.jsonl',
        '04_relations/2023_relations.jsonl',
        '04_relations/2023_solution_lineages.jsonl',
        '05_knowledge/methods/2023_methods.jsonl',
        '05_knowledge/expert_feedback/2023_feedback.jsonl',
        '05_knowledge/visualizations/2023_visualizations.jsonl',
        '06_statistics/yearly/2023_statistics.csv',
        '07_reports/yearly/2023_report.md',
        '08_quality/gates/2023_gate.json',
        '09_checkpoints/2023_checkpoint.json',
        '00_control/progress.json',
        '00_control/checkpoint_manifest.json',
        '00_control/processing_log.jsonl',
        '00_control/missing_segment_requests.jsonl',
        '00_control/manual_review_queue.jsonl',
    ]
    assert all((AI / p).is_file() for p in required)


def test_json_and_jsonl_parse():
    for p in AI.rglob('*.json'):
        read_json(p)
    for p in AI.rglob('*.jsonl'):
        read_jsonl(p)


def test_csv_parse():
    for p in AI.rglob('*.csv'):
        with p.open(encoding='utf-8-sig', newline='') as f:
            assert list(csv.reader(f))


def test_expected_counts(carriers, documents, reps, segs):
    assert len(carriers) == 32
    assert len(documents) == 32
    assert len(reps) == 32
    assert len(segs) == 761


def test_roles_and_subtypes(documents):
    role_counts = Counter(d['role'] for d in documents)
    assert role_counts == {'paper': 14, 'problem': 5, 'dataset': 13}
    assert set(d['role'] for d in documents) <= {'paper', 'problem', 'commentary', 'dataset'}
    assert Counter(d['subtype'] for d in documents)['submission_template'] == 4


def test_problem_distribution(documents):
    counts = Counter(d['problem_code'] for d in documents if d['role'] == 'paper')
    assert counts == {'A': 4, 'B': 3, 'C': 4, 'D': 1, 'E': 2}


def test_sha256_coverage_and_source_bytes(carriers):
    assert len({c['source_relative_path'] for c in carriers}) == 32
    for c in carriers:
        p = SOURCE_ROOT / c['source_relative_path']
        assert p.is_file(), p
        assert sha256(p) == c['sha256']
        assert c['source_modified'] is False


def test_readonly_flags(carriers):
    assert all(c['readonly_verified'] for c in carriers)


def test_byte_duplicate_preserved(carriers):
    groups = defaultdict(list)
    for c in carriers:
        if c['byte_duplicate_group']:
            groups[c['byte_duplicate_group']].append(c)
    assert len(groups) == 1
    values = next(iter(groups.values()))
    assert len(values) == 2
    assert {Path(v['source_relative_path']).name for v in values} == {'result2.xlsx', 'result3.xlsx'}
    assert len({v['logical_document_id'] for v in values}) == 2


def test_one_preferred_representation_per_document(documents, reps):
    by_doc = defaultdict(list)
    for r in reps:
        by_doc[r['logical_document_id']].append(r)
    for d in documents:
        rs = by_doc[d['logical_document_id']]
        assert len(rs) == 1
        assert sum(bool(r['preferred']) for r in rs) == 1
        assert d['preferred_representation_id'] == rs[0]['representation_id']


def test_carrier_document_representation_consistency(carriers, documents, reps):
    doc_ids = {d['logical_document_id'] for d in documents}
    carrier_ids = {c['carrier_id'] for c in carriers}
    assert {c['logical_document_id'] for c in carriers} == doc_ids
    assert {r['logical_document_id'] for r in reps} == doc_ids
    assert {r['carrier_id'] for r in reps} == carrier_ids


def test_pdf_page_and_xlsx_sheet_segment_counts(segs):
    assert sum(s['segment_type'] == 'page' for s in segs) == 742
    assert sum(s['segment_type'] == 'worksheet' for s in segs) == 19


def test_pdf_regions_legal_and_unique(segs):
    seen = set()
    for s in segs:
        if s['segment_type'] != 'page':
            continue
        r = s['region']
        assert 0 <= r['x0'] < r['x1']
        assert 0 <= r['y0'] < r['y1']
        key = (s['representation_id'], s['page_number'])
        assert key not in seen
        seen.add(key)
        assert s['boundary_status'] == 'verified'


def test_worksheet_regions_legal_and_unique(segs):
    seen = set()
    for s in segs:
        if s['segment_type'] != 'worksheet':
            continue
        r = s['region']
        assert 1 <= r['row_start'] <= r['row_end']
        assert 1 <= r['column_start'] <= r['column_end']
        key = (s['representation_id'], s['sheet_name'])
        assert key not in seen
        seen.add(key)


def test_no_blank_or_missing_segments(segs):
    assert all(s.get('blank_status', 'not_applicable') != 'blank' for s in segs)
    requests = read_jsonl(AI / '00_control/missing_segment_requests.jsonl')
    assert requests[0]['request_count'] == 0


def test_six_pack_complete(documents):
    expected = {'metadata.json', 'problem_summary.md', 'model_summary.md', 'validation.md', 'visualization.md', 'manual_review.json'}
    root = AI / '02_documents/six_packs/2023'
    assert len([p for p in root.iterdir() if p.is_dir()]) == 32
    for d in documents:
        folder = root / d['logical_document_id']
        assert {p.name for p in folder.iterdir() if p.is_file()} == expected


def test_six_pack_manual_reviews_closed(documents):
    root = AI / '02_documents/six_packs/2023'
    for d in documents:
        mr = read_json(root / d['logical_document_id'] / 'manual_review.json')
        assert mr['review_status'] == 'complete'
        assert mr['open_review_items'] == 0
        assert mr['preferred_representation_count'] == 1
        assert mr['award_level_inferred'] is False


def test_relations_referential_integrity(documents):
    ids = {d['logical_document_id'] for d in documents}
    rels = read_jsonl(AI / '04_relations/2023_relations.jsonl')
    assert rels
    for r in rels:
        assert r['subject_id'] in ids
        assert r['object_id'] in ids
    assert any(r['predicate'] == 'byte_identical_to' for r in rels)


def test_solution_lineages_complete(documents):
    papers = {d['logical_document_id'] for d in documents if d['role'] == 'paper'}
    rows = read_jsonl(AI / '04_relations/2023_solution_lineages.jsonl')
    assert len(rows) == 14
    assert {r['paper_document_id'] for r in rows} == papers
    assert all(r['sequence'] and r['algorithms'] and r['validation_modes'] for r in rows)


def test_methods_and_visualizations_cover_papers(documents):
    papers = {d['logical_document_id'] for d in documents if d['role'] == 'paper'}
    methods = read_jsonl(AI / '05_knowledge/methods/2023_methods.jsonl')
    visuals = read_jsonl(AI / '05_knowledge/visualizations/2023_visualizations.jsonl')
    assert {r['paper_document_id'] for r in methods} == papers
    assert {r['paper_document_id'] for r in visuals} == papers


def test_expert_feedback_not_fabricated():
    feedback = read_jsonl(AI / '05_knowledge/expert_feedback/2023_feedback.jsonl')
    assert len(feedback) == 1
    assert feedback[0]['status'] == 'not_observed'
    assert feedback[0]['expert_commentary_documents'] == 0


def test_unknown_not_counted_as_absent(documents):
    allowed = {'present', 'absent', 'unknown', 'not_observed', 'not_applicable'}
    assert set(d['field_status'] for d in documents) <= allowed
    assert all(d['award_level'] == 'unknown' and d['award_level_status'] == 'not_observed' for d in documents)
    assert not any(d['award_level_status'] == 'absent' for d in documents)


def test_statistics_consistent(carriers, documents, reps, segs):
    with (AI / '06_statistics/yearly/2023_statistics.csv').open(encoding='utf-8-sig', newline='') as f:
        row = next(csv.DictReader(f))
    assert int(row['physical_carriers']) == len(carriers)
    assert int(row['logical_documents']) == len(documents)
    assert int(row['representations']) == len(reps)
    assert int(row['segments']) == len(segs)
    assert int(row['source_modified_files']) == 0


def test_quality_gate_pass():
    gate = read_json(AI / '08_quality/gates/2023_gate.json')
    assert gate['status'] == 'pass'
    assert all(gate['checks'].values())
    assert gate['manual_review_items'] == 0
    assert gate['blocking_manual_review_items'] == 0


def test_checkpoint_pending_remote_readback():
    cp = read_json(AI / '09_checkpoints/2023_checkpoint.json')
    assert cp['status'] == 'pass_pending_remote_readback'
    assert cp['manual_review_complete'] is True
    assert cp['remote_readback_verified'] is False


def test_progress_reconciled_conservatively():
    p = read_json(AI / '00_control/progress.json')
    assert p['last_verified_complete_year'] == 2009
    assert p['year_status']['2010'] == 'conditional_pass'
    assert p['year_status']['2011'] == 'not_verified'
    assert p['year_status']['2023'] == 'pass_pending_remote_readback'
    assert 2023 not in p['completed_years']


def test_manual_review_queue_closed():
    q = read_jsonl(AI / '00_control/manual_review_queue.jsonl')
    assert q[0]['open_items'] == 0
    assert q[0]['blocking_items'] == 0


def test_source_file_count_and_extensions(carriers):
    assert Counter(c['extension'] for c in carriers) == {'.pdf': 19, '.xlsx': 13}
