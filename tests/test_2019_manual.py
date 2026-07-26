from __future__ import annotations
import csv, hashlib, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
AN=ROOT/'analysis-index'
YEAR=2019

def read_jsonl(p):
    rows=[]
    for line in p.read_text(encoding='utf-8-sig').splitlines():
        if line.strip(): rows.append(json.loads(line))
    return rows

def test_required_files_exist():
    required=[
      AN/'01_inventory/2019_carrier_manifest.jsonl',AN/'02_documents/logical_documents/2019.csv',AN/'03_segments/2019_segments.jsonl',
      AN/'04_relations/2019_representations.jsonl',AN/'04_relations/2019_relations.jsonl',AN/'04_relations/2019_solution_lineages.jsonl',
      AN/'05_knowledge/methods/2019_methods.jsonl',AN/'05_knowledge/expert_feedback/2019_feedback.jsonl',AN/'05_knowledge/visualizations/2019_visualizations.jsonl',
      AN/'06_statistics/yearly/2019_statistics.csv',AN/'07_reports/yearly/2019_report.md',AN/'08_quality/gates/2019_gate.json',AN/'09_checkpoints/2019_checkpoint.json',
      AN/'00_control/progress.json',AN/'00_control/checkpoint_manifest.json',AN/'00_control/processing_log.jsonl',AN/'00_control/missing_segment_requests.jsonl',AN/'00_control/manual_review_queue.jsonl']
    assert all(p.exists() for p in required)

def test_json_jsonl_csv_structures():
    for p in ROOT.rglob('*.json'):
        json.loads(p.read_text(encoding='utf-8-sig'))
    for p in ROOT.rglob('*.jsonl'):
        read_jsonl(p)
    for p in ROOT.rglob('*.csv'):
        try:
            with p.open(encoding='utf-8-sig',newline='') as f: list(csv.DictReader(f))
        except UnicodeDecodeError:
            with p.open(encoding='gbk',newline='') as f: list(csv.DictReader(f))

def test_counts_and_hash_coverage():
    carriers=read_jsonl(AN/'01_inventory/2019_carrier_manifest.jsonl')
    with (AN/'02_documents/logical_documents/2019.csv').open(encoding='utf-8-sig',newline='') as f: docs=list(csv.DictReader(f))
    reps=read_jsonl(AN/'04_relations/2019_representations.jsonl')
    assert len(carriers)==34
    assert len(docs)==34
    assert len(reps)==34
    assert all(len(x['sha256'])==64 for x in carriers)
    assert len({x['carrier_id'] for x in carriers})==34
    assert len({x['logical_document_id'] for x in docs})==34

def test_roles_and_solution_counts():
    with (AN/'02_documents/logical_documents/2019.csv').open(encoding='utf-8-sig',newline='') as f: docs=list(csv.DictReader(f))
    valid={'problem','paper','commentary','dataset'}
    assert all(x['document_role'] in valid for x in docs)
    assert sum(x['document_role']=='paper' for x in docs)==17
    assert sum(x['document_role']=='problem' for x in docs)==5
    assert sum(x['document_role']=='dataset' for x in docs)==12

def test_one_preferred_representation():
    reps=read_jsonl(AN/'04_relations/2019_representations.jsonl')
    by={}
    for r in reps: by.setdefault(r['logical_document_id'],[]).append(r)
    assert all(sum(bool(x['is_preferred']) for x in arr)==1 for arr in by.values())

def test_six_pack_exactly_once_per_document():
    with (AN/'02_documents/logical_documents/2019.csv').open(encoding='utf-8-sig',newline='') as f: docs=list(csv.DictReader(f))
    required={'metadata.json','problem_summary.md','model_summary.md','validation.md','visualization.md','manual_review.json'}
    for d in docs:
        path=AN/'02_documents/dossiers'/d['logical_document_id']
        assert path.is_dir()
        assert required.issubset({p.name for p in path.iterdir()})

def test_page_boundaries_and_coordinates():
    segs=read_jsonl(AN/'03_segments/2019_segments.jsonl')
    seen=set()
    for s in segs:
        if s['segment_type']=='page_region':
            assert s['page_start']==s['page_end'] and s['page_start']>=1
            x0,y0,x1,y1=s['bbox_normalized']
            assert 0<=x0<x1<=1 and 0<=y0<y1<=1
            key=(s['representation_id'],s['page_start'])
            assert key not in seen
            seen.add(key)
    assert len(seen)==562

def test_solution_lineages():
    ls=read_jsonl(AN/'04_relations/2019_solution_lineages.jsonl')
    assert len(ls)==17
    assert all(len(x['solution_document_ids'])==1 for x in ls)
    assert all(x['lineage_status']=='verified' for x in ls)

def test_unknown_not_absent_and_no_award_inference():
    with (AN/'02_documents/logical_documents/2019.csv').open(encoding='utf-8-sig',newline='') as f: docs=list(csv.DictReader(f))
    assert all(x['award_level']=='unknown' for x in docs)
    corpus='\n'.join(p.read_text(encoding='utf-8-sig',errors='ignore') for p in (AN/'02_documents/dossiers').rglob('*') if p.is_file())
    assert 'award_level": "absent"' not in corpus

def test_source_modification_count_zero():
    with (AN/'06_statistics/yearly/2019_statistics.csv').open(encoding='utf-8-sig',newline='') as f: row=next(csv.DictReader(f))
    assert int(row['source_modifications'])==0
    assert int(row['physical_carriers'])==34

def test_gate_is_nonblocking_conditional_pass():
    gate=json.loads((AN/'08_quality/gates/2019_gate.json').read_text(encoding='utf-8-sig'))
    assert gate['status']=='conditional_pass'
    assert gate['blocking_manual_review_items']==0
    assert gate['checks']['local_tests_passed'] is True
