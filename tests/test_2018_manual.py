from pathlib import Path
import csv, hashlib, json

ROOT=Path(__file__).resolve().parents[1]
AI=ROOT/'analysis-index'
YEAR='2018'

def read_jsonl(path):
    rows=[]
    for i,line in enumerate(path.read_text(encoding='utf-8').splitlines(),1):
        if line.strip():
            rows.append(json.loads(line))
    return rows

def docs():
    with (AI/'02_documents/logical_documents/2018.csv').open(encoding='utf-8-sig',newline='') as f:
        return list(csv.DictReader(f))

def test_required_files_exist():
    req=[
      AI/'01_inventory/2018_carrier_manifest.jsonl',AI/'02_documents/logical_documents/2018.csv',AI/'03_segments/2018_segments.jsonl',
      AI/'04_relations/2018_representations.jsonl',AI/'04_relations/2018_relations.jsonl',AI/'04_relations/2018_solution_lineages.jsonl',
      AI/'05_knowledge/methods/2018_methods.jsonl',AI/'05_knowledge/expert_feedback/2018_feedback.jsonl',AI/'05_knowledge/visualizations/2018_visualizations.jsonl',
      AI/'06_statistics/yearly/2018_statistics.csv',AI/'07_reports/yearly/2018_report.md',AI/'08_quality/gates/2018_gate.json',AI/'09_checkpoints/2018_checkpoint.json',
      AI/'00_control/progress.json',AI/'00_control/checkpoint_manifest.json',AI/'00_control/processing_log.jsonl',AI/'00_control/missing_segment_requests.jsonl',AI/'00_control/manual_review_queue.jsonl',ROOT/'2018_missing_files.txt']
    assert all(p.exists() for p in req)

def test_json_jsonl_parse():
    for p in AI.rglob('*.json'): json.loads(p.read_text(encoding='utf-8'))
    for p in AI.rglob('*.jsonl'): read_jsonl(p)

def test_counts_and_object_layers():
    carriers=read_jsonl(AI/'01_inventory/2018_carrier_manifest.jsonl'); ds=docs(); reps=read_jsonl(AI/'04_relations/2018_representations.jsonl')
    assert len(carriers)==27 and len(ds)==27 and len(reps)==27
    assert sum(c['physical_carrier_type']=='archive_container' for c in carriers)==1
    represented={r['carrier_id'] for r in reps}
    assert len(represented)==26  # A workbook reused by two docs; RAR container is container-only.

def test_sha256_coverage_and_uniqueness():
    carriers=read_jsonl(AI/'01_inventory/2018_carrier_manifest.jsonl')
    assert all(len(c['sha256'])==64 and all(ch in '0123456789abcdef' for ch in c['sha256']) for c in carriers)
    assert len({c['sha256'] for c in carriers})==27

def test_source_unmodified():
    a=json.loads((AI/'08_quality/evidence/2018_source_hash_audit.json').read_text(encoding='utf-8'))
    assert a['source_modified_count']==0
    assert all(x['initial_sha256']==x['final_sha256'] and not x['modified'] for x in a['hashes'])

def test_one_preferred_representation_per_document():
    reps=read_jsonl(AI/'04_relations/2018_representations.jsonl')
    ds=docs()
    for d in ds:
        rr=[r for r in reps if r['document_id']==d['document_id']]
        assert len(rr)==1 and rr[0]['preferred'] is True

def test_roles_legal_and_solution_scope():
    ds=docs(); legal={'problem','paper','commentary','dataset'}
    assert {d['role'] for d in ds}<=legal
    assert sum(d['role']=='paper' for d in ds)==13
    assert sum(d['role']=='problem' for d in ds)==4
    assert sum(d['role']=='commentary' for d in ds)==2
    assert sum(d['role']=='dataset' for d in ds)==8

def test_problem_distribution_and_filename_correction():
    ds=docs(); papers=[d for d in ds if d['role']=='paper']
    assert {p:sum(d['problem_id']==f'2018-{p}' for d in papers) for p in 'ABCD'}=={'A':3,'B':4,'C':3,'D':3}
    x=[d for d in papers if '多原则比较' in d['title']][0]
    assert x['problem_id']=='2018-B' and x['filename'].startswith('2018A')

def test_unknown_not_absent_policy():
    raw='\n'.join(p.read_text(encoding='utf-8',errors='ignore') for p in AI.rglob('*') if p.is_file() and p.suffix in {'.json','.jsonl','.csv','.md'})
    assert 'award_level,absent' not in raw
    assert all(d['award_level']=='unknown' for d in docs())
    assert all(d['expert_feedback_status']=='not_observed' for d in docs())

def test_segments_have_valid_boundaries():
    segs=read_jsonl(AI/'03_segments/2018_segments.jsonl')
    assert len(segs)==580
    seen=set()
    for s in segs:
        if s['segment_type'] in {'page','derived_render_page'}:
            assert s['page_start']==s['page_end'] and s['page_start']>=1
            assert len(s['bbox'])==4 and s['bbox'][2]>s['bbox'][0] and s['bbox'][3]>s['bbox'][1]
            key=(s['document_id'],s['segment_type'],s['page_start'])
            assert key not in seen; seen.add(key)
        if s['segment_type']=='worksheet_region': assert s['used_range'] is not None

def test_six_pack_complete():
    names={'metadata.json','problem_summary.md','model_summary.md','validation.md','visualization.md','manual_review.json'}
    for d in docs():
        p=AI/'02_documents/document_cards/2018'/d['document_id']
        assert p.is_dir() and names<={x.name for x in p.iterdir()}

def test_lineages_and_relations():
    lin=read_jsonl(AI/'04_relations/2018_solution_lineages.jsonl'); rel=read_jsonl(AI/'04_relations/2018_relations.jsonl')
    assert len(lin)==13 and len({x['solution_document_id'] for x in lin})==13
    assert sum(x['relation_type']=='solves' for x in rel)==13

def test_methods_and_visualizations_nonempty():
    assert len(read_jsonl(AI/'05_knowledge/methods/2018_methods.jsonl'))>=95
    assert len(read_jsonl(AI/'05_knowledge/visualizations/2018_visualizations.jsonl'))>=70

def test_missing_files_are_exact_and_nonblocking():
    req=read_jsonl(AI/'00_control/missing_segment_requests.jsonl')
    assert len(req)==5 and {x['request_id'] for x in req}=={f'2018-MISS-C-0{i}' for i in range(1,6)}
    assert all(x['blocking'] is False for x in req)

def test_gate_is_conditional_pass_not_pass():
    gate=json.loads((AI/'08_quality/gates/2018_gate.json').read_text(encoding='utf-8'))
    assert gate['status']=='conditional_pass'
    assert gate['checks']['supporting_data_complete'] is False
    assert gate['checks']['source_unmodified'] is True
    assert gate['blocking_manual_review_items']==0

def test_progress_reconciliation():
    p=json.loads((AI/'00_control/progress.json').read_text(encoding='utf-8'))
    assert p['last_verified_complete_year']==2009
    assert p['year_status']['2010'].startswith('conditional_pass')
    assert p['year_status']['2011']=='unverified_no_year_evidence'
    assert p['year_status']['2018']=='conditional_pass_pending_remote_readback'
