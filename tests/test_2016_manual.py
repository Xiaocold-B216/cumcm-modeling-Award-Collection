from pathlib import Path
import json,csv,hashlib
ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'analysis-index'
def j(p): return json.loads(p.read_text(encoding='utf-8'))
def jl(p):
    return [json.loads(x) for x in p.read_text(encoding='utf-8').splitlines() if x.strip()]
def test_required_files():
    req=['01_inventory/2016_carrier_manifest.jsonl','02_documents/logical_documents/2016.csv','03_segments/2016_segments.jsonl','04_relations/2016_representations.jsonl','04_relations/2016_relations.jsonl','04_relations/2016_solution_lineages.jsonl','05_knowledge/methods/2016_methods.jsonl','05_knowledge/expert_feedback/2016_feedback.jsonl','05_knowledge/visualizations/2016_visualizations.jsonl','06_statistics/yearly/2016_statistics.csv','07_reports/yearly/2016_report.md','08_quality/gates/2016_gate.json','09_checkpoints/2016_checkpoint.json','00_control/progress.json','00_control/checkpoint_manifest.json','00_control/processing_log.jsonl','00_control/missing_segment_requests.jsonl','00_control/manual_review_queue.jsonl']
    assert all((A/x).exists() for x in req)
def test_json_files_parse():
    for p in A.rglob('*.json'): j(p)
def test_jsonl_files_parse():
    for p in A.rglob('*.jsonl'): jl(p)
def test_carrier_count_and_hashes():
    c=jl(A/'01_inventory/2016_carrier_manifest.jsonl'); assert len(c)==35
    assert all(len(x['sha256'])==64 and x['sha256_covered'] for x in c)
def test_source_unmodified_flags():
    c=jl(A/'01_inventory/2016_carrier_manifest.jsonl'); assert sum(not x['source_modified'] for x in c)==35
def docs():
    with (A/'02_documents/logical_documents/2016.csv').open(encoding='utf-8-sig') as f:return list(csv.DictReader(f))
def test_logical_document_count(): assert len(docs())==34
def test_representation_count(): assert len(jl(A/'04_relations/2016_representations.jsonl'))==35
def test_solution_lineage_count(): assert len(jl(A/'04_relations/2016_solution_lineages.jsonl'))==14
def test_paper_count(): assert sum(x['role']=='paper' for x in docs())==14
def test_roles_valid(): assert {x['role'] for x in docs()} <= {'problem','paper','commentary','dataset'}
def test_one_preferred_representation():
    reps=jl(A/'04_relations/2016_representations.jsonl'); by={}
    for r in reps: by.setdefault(r['document_id'],[]).append(r)
    assert all(sum(bool(x['is_preferred']) for x in v)==1 for v in by.values())
def test_representation_doc_consistency():
    ds={x['document_id'] for x in docs()}; reps=jl(A/'04_relations/2016_representations.jsonl'); assert all(r['document_id'] in ds for r in reps)
def test_b_duplicate_preserved_and_merged():
    reps=[r for r in jl(A/'04_relations/2016_representations.jsonl') if r['document_id']=='cumcm-2016-B-paper-01']
    assert len(reps)==2 and sum(r['is_preferred'] for r in reps)==1 and len({r['sha256'] for r in reps})==2
def test_six_pack_complete():
    for d in docs():
        p=A/'02_documents/cards/2016'/d['document_id']
        assert {x.name for x in p.iterdir()}=={'metadata.json','problem_summary.md','model_summary.md','validation.md','visualization.md','manual_review.json'}
def test_field_status_enum():
    ok={'present','absent','unknown','not_observed','not_applicable'}
    for p in (A/'02_documents/cards/2016').glob('*/metadata.json'):
        assert set(j(p)['field_status'].values())<=ok
def test_unknown_not_absent():
    for p in (A/'02_documents/cards/2016').glob('*/metadata.json'):
        m=j(p); assert not (m['award_level']=='unknown' and m['field_status']['award_level']=='absent')
def test_segments_unique_and_legal():
    seg=jl(A/'03_segments/2016_segments.jsonl'); assert len(seg)==943
    assert len({s['segment_id'] for s in seg})==len(seg)
    for s in seg:
        if s['bbox'] is not None:
            x0,y0,x1,y1=s['bbox']; assert 0<=x0<x1 and 0<=y0<y1
        else: assert s['segment_type']=='sheet_region' and s['cell_range']
def test_page_boundaries_nonoverlap():
    seg=jl(A/'03_segments/2016_segments.jsonl'); keys=[]
    for s in seg:
        keys.append((s['representation_id'],s['page_number'],s['sheet_name']))
    assert len(keys)==len(set(keys))
def test_problem_distribution():
    ls=jl(A/'04_relations/2016_solution_lineages.jsonl')
    from collections import Counter
    c=Counter(x['problem_id'][-1] for x in ls); assert c=={'A':5,'B':4,'C':2,'D':3}
def test_methods_and_visuals():
    assert len(jl(A/'05_knowledge/methods/2016_methods.jsonl'))==14
    assert len(jl(A/'05_knowledge/visualizations/2016_visualizations.jsonl'))==14
def test_expert_feedback_not_fabricated(): assert jl(A/'05_knowledge/expert_feedback/2016_feedback.jsonl')==[]
def test_statistics_counts():
    with (A/'06_statistics/yearly/2016_statistics.csv').open(encoding='utf-8-sig') as f:r=list(csv.DictReader(f))[0]
    assert r['physical_carriers']=='35' and r['logical_documents']=='34' and r['solution_papers']=='14'
def test_gate_conditional():
    g=j(A/'08_quality/gates/2016_gate.json'); assert g['status']=='conditional_pass' and g['checks']['all_expected_supporting_files_present'] is False
def test_checkpoint_not_remote_verified(): assert j(A/'09_checkpoints/2016_checkpoint.json')['remote_readback_verified'] is False
def test_progress_reconciled():
    p=j(A/'00_control/progress.json'); assert p['last_verified_complete_year']==2009 and p['year_status']['2010']=='conditional_pass' and p['year_status']['2016'].startswith('conditional_pass')
def test_missing_file_precise():
    t=(ROOT/'2016_missing_files.txt').read_text(encoding='utf-8'); assert '4#、16#、24#、33#、49#、57#' in t and 'D题附件2' in t
def test_monthly_data_audit_in_report():
    t=(A/'07_reports/yearly/2016_report.md').read_text(encoding='utf-8'); assert '35040' in t and '10个空白或非数值风速单元格' in t
def test_no_award_inference(): assert all(x['award_level'] in {'unknown','not_applicable'} for x in docs())
