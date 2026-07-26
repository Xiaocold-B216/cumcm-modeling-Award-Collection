from __future__ import annotations
import csv, hashlib, json, re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AI = ROOT / "analysis-index"
YEAR = 2025

def read_jsonl(path: Path):
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]

def test_required_files_exist():
    required = [
      AI/'01_inventory/2025_carrier_manifest.jsonl', AI/'02_documents/logical_documents/2025.csv',
      AI/'03_segments/2025_segments.jsonl', AI/'04_relations/2025_representations.jsonl',
      AI/'04_relations/2025_relations.jsonl', AI/'04_relations/2025_solution_lineages.jsonl',
      AI/'05_knowledge/methods/2025_methods.jsonl', AI/'05_knowledge/expert_feedback/2025_feedback.jsonl',
      AI/'05_knowledge/visualizations/2025_visualizations.jsonl', AI/'06_statistics/yearly/2025_statistics.csv',
      AI/'07_reports/yearly/2025_report.md', AI/'08_quality/gates/2025_gate.json',
      AI/'09_checkpoints/2025_checkpoint.json', AI/'00_control/progress.json',
      AI/'00_control/checkpoint_manifest.json', AI/'00_control/processing_log.jsonl',
      AI/'00_control/missing_segment_requests.jsonl', AI/'00_control/manual_review_queue.jsonl']
    assert all(p.exists() for p in required)

def test_json_files_parse():
    for p in ROOT.rglob('*.json'): json.loads(p.read_text(encoding='utf-8'))

def test_jsonl_files_parse():
    for p in ROOT.rglob('*.jsonl'):
        for line in p.read_text(encoding='utf-8').splitlines():
            if line.strip(): json.loads(line)

def test_csv_files_parse():
    for p in ROOT.rglob('*.csv'):
        with p.open(encoding='utf-8-sig',newline='') as f: list(csv.DictReader(f))

def test_carrier_sha_coverage():
    rows=read_jsonl(AI/'01_inventory/2025_carrier_manifest.jsonl')
    assert len(rows)==107
    assert len({r['carrier_id'] for r in rows})==107
    assert len({r['source_path'] for r in rows})==107
    assert all(re.fullmatch(r'[0-9a-f]{64}',r['sha256']) for r in rows)
    assert all(r['read_only_verified'] for r in rows)

def test_object_counts_and_roles():
    with (AI/'02_documents/logical_documents/2025.csv').open(encoding='utf-8-sig') as f: docs=list(csv.DictReader(f))
    assert len(docs)==106
    c=Counter(d['role'] for d in docs)
    assert c=={'dataset':94,'paper':7,'problem':5}
    assert all(d['role'] in {'problem','paper','commentary','dataset'} for d in docs)

def test_representation_consistency():
    reps=read_jsonl(AI/'04_relations/2025_representations.jsonl')
    with (AI/'02_documents/logical_documents/2025.csv').open(encoding='utf-8-sig') as f: docs=list(csv.DictReader(f))
    assert len(reps)==107
    by=defaultdict(list)
    for r in reps: by[r['logical_document_id']].append(r)
    assert set(by)=={d['document_id'] for d in docs}
    assert all(sum(1 for r in rs if r['preferred'])==1 for rs in by.values())
    assert sum(1 for r in reps if r['logical_document_id']=='2025-PAPER-C023')==2

def test_carrier_representation_one_to_one():
    carriers=read_jsonl(AI/'01_inventory/2025_carrier_manifest.jsonl')
    reps=read_jsonl(AI/'04_relations/2025_representations.jsonl')
    assert {c['carrier_id'] for c in carriers}=={r['carrier_id'] for r in reps}

def test_every_document_has_exact_six_pack():
    with (AI/'02_documents/logical_documents/2025.csv').open(encoding='utf-8-sig') as f: docs=list(csv.DictReader(f))
    expected={'metadata.json','problem_summary.md','model_summary.md','validation.md','visualization.md','manual_review.json'}
    for d in docs:
        folder=AI/'02_documents/six_pack/2025'/d['document_id']
        assert folder.is_dir()
        assert {p.name for p in folder.iterdir() if p.is_file()}==expected

def test_segment_coordinates_valid_and_nonoverlap():
    segs=read_jsonl(AI/'03_segments/2025_segments.jsonl')
    assert len(segs)==745
    page_keys=set()
    for s in segs:
        assert s['coordinate_valid'] is True
        if s['segment_type']=='page':
            x0,y0,x1,y1=s['bbox_pdf_points']; assert x1>x0 and y1>y0
            key=(s['representation_id'],s['page_number']); assert key not in page_keys; page_keys.add(key)
        else:
            assert s['bbox_pdf_points'] is None

def test_unknown_not_absent_policy():
    text='\n'.join(p.read_text(encoding='utf-8',errors='ignore') for p in AI.rglob('*') if p.is_file() and p.suffix in {'.json','.jsonl','.csv','.md'})
    assert 'field_status_policy' in text
    # No machine field marks an unobserved feature as absent.
    assert '"status": "absent"' not in text and '"status":"absent"' not in text

def test_problem_paper_distribution():
    lines=read_jsonl(AI/'04_relations/2025_solution_lineages.jsonl')
    assert Counter(x['problem_id'] for x in lines)=={'A':2,'B':1,'C':2,'D':1,'E':1}

def test_no_expert_commentary_fabricated():
    assert read_jsonl(AI/'05_knowledge/expert_feedback/2025_feedback.jsonl')==[]

def test_duplicate_relations_retained():
    rel=read_jsonl(AI/'04_relations/2025_relations.jsonl')
    dup=[r for r in rel if r['relation_type']=='byte_identical_but_semantically_distinct']
    assert len(dup)>=4
    assert any(r.get('duplicate_semantics')=='cross_label_duplicate_requires_source_confirmation' for r in dup)

def test_manual_review_is_nonblocking():
    q=read_jsonl(AI/'00_control/manual_review_queue.jsonl')
    assert len(q)==1 and q[0]['severity']=='nonblocking' and q[0]['status']=='open'

def test_missing_segment_requests_empty():
    assert read_jsonl(AI/'00_control/missing_segment_requests.jsonl')==[]

def test_source_unmodified_evidence():
    e=json.loads((AI/'08_quality/evidence/2025_source_hash_verification.json').read_text(encoding='utf-8'))
    assert e['source_file_count']==107 and e['modified_file_count']==0 and e['all_hashes_match'] is True
    assert all(x['match'] for x in e['files'])

def test_gate_conditional_pass_without_blockers():
    g=json.loads((AI/'08_quality/gates/2025_gate.json').read_text(encoding='utf-8'))
    assert g['status']=='conditional_pass'
    assert g['blocking_manual_review_items']==0
    assert g['manual_review_items']==1
    assert g['upload_ready'] is True

def test_progress_reconciled_not_blindly_advanced():
    p=json.loads((AI/'00_control/progress.json').read_text(encoding='utf-8'))
    assert p['last_verified_complete_year']==2009
    assert 2010 not in p['completed_years'] and 2011 not in p['completed_years'] and 2025 not in p['completed_years']
    assert p['year_status']['2025']=='conditional_pass_pending_remote_readback'

def test_checkpoint_counts_match():
    c=json.loads((AI/'09_checkpoints/2025_checkpoint.json').read_text(encoding='utf-8'))
    assert (c['carriers'],c['documents'],c['representations'])==(107,106,107)
    assert c['solution_papers']==7 and c['problem_statements']==5 and c['expert_commentaries']==0

def test_statistics_key_counts():
    with (AI/'06_statistics/yearly/2025_statistics.csv').open(encoding='utf-8-sig') as f: rows=list(csv.DictReader(f))
    d={(r['metric'],r['scope']):r['value'] for r in rows}
    assert d[('physical_carriers','all')]=='107'
    assert d[('logical_documents','all')]=='106'
    assert d[('solution_papers','all')]=='7'
    assert d[('source_modified_files','all')]=='0'

def test_all_representation_page_counts_nonnegative():
    reps=read_jsonl(AI/'04_relations/2025_representations.jsonl')
    assert all(isinstance(r['page_count'],int) and r['page_count']>=0 for r in reps)
    assert sum(r['page_count'] for r in reps if r['format']=='pdf')==524

def test_c023_representation_pair():
    reps=[r for r in read_jsonl(AI/'04_relations/2025_representations.jsonl') if r['logical_document_id']=='2025-PAPER-C023']
    assert sorted(r['page_count'] for r in reps)==[122,122]
    assert {r['format'] for r in reps}=={'pdf','docx'}

def test_report_contains_required_sections():
    text=(AI/'07_reports/yearly/2025_report.md').read_text(encoding='utf-8')
    for s in ['年度对象统计','关键纠错','模型与算法谱系','专家评审知识','高价值可视化模式','数据质量限制','测试与质量门']:
        assert s in text
