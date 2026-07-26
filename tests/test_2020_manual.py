from pathlib import Path
import csv,json,re,hashlib
ROOT=Path(__file__).resolve().parents[1]
def jl(p): return [json.loads(x) for x in (ROOT/p).read_text(encoding='utf-8').splitlines() if x.strip()]
def docs():
    with (ROOT/'analysis-index/02_documents/logical_documents/2020.csv').open(encoding='utf-8-sig') as f:return list(csv.DictReader(f))
def test_json_control_files_parse():
    for p in ['analysis-index/00_control/progress.json','analysis-index/00_control/checkpoint_manifest.json','analysis-index/08_quality/gates/2020_gate.json','analysis-index/09_checkpoints/2020_checkpoint.json','analysis-index/08_quality/evidence/2020_source_integrity.json','analysis-index/08_quality/evidence/2020_data_audit.json']: json.loads((ROOT/p).read_text())
def test_jsonl_files_parse():
    for p in ['analysis-index/01_inventory/2020_carrier_manifest.jsonl','analysis-index/03_segments/2020_segments.jsonl','analysis-index/04_relations/2020_representations.jsonl','analysis-index/04_relations/2020_relations.jsonl','analysis-index/04_relations/2020_solution_lineages.jsonl','analysis-index/05_knowledge/methods/2020_methods.jsonl','analysis-index/05_knowledge/expert_feedback/2020_feedback.jsonl','analysis-index/05_knowledge/visualizations/2020_visualizations.jsonl','analysis-index/00_control/processing_log.jsonl','analysis-index/00_control/missing_segment_requests.jsonl','analysis-index/00_control/manual_review_queue.jsonl']: jl(p)
def test_csv_structure():
    for p in ['analysis-index/02_documents/logical_documents/2020.csv','analysis-index/06_statistics/yearly/2020_statistics.csv']:
        with (ROOT/p).open(encoding='utf-8-sig') as f: assert list(csv.DictReader(f))
def test_counts():
    assert len(jl('analysis-index/01_inventory/2020_carrier_manifest.jsonl'))==39
    assert len(docs())==39
    assert len(jl('analysis-index/04_relations/2020_representations.jsonl'))==39
def test_role_counts():
    d=docs(); assert sum(x['role']=='paper' for x in d)==17; assert sum(x['role']=='problem' for x in d)==5; assert sum(x['role']=='dataset' for x in d)==17; assert sum(x['role']=='commentary' for x in d)==0
def test_paper_problem_counts():
    d=docs(); expected={'2020-A':3,'2020-B':4,'2020-C':5,'2020-D':3,'2020-E':2}
    assert {k:sum(x['role']=='paper' and x['problem_id']==k for x in d) for k in expected}==expected
def test_sha_coverage():
    c=jl('analysis-index/01_inventory/2020_carrier_manifest.jsonl'); assert all(re.fullmatch('[0-9a-f]{64}',x['sha256']) for x in c); assert len({x['original_filename'] for x in c})==39
def test_no_byte_duplicates():
    c=jl('analysis-index/01_inventory/2020_carrier_manifest.jsonl'); assert len({x['sha256'] for x in c})==39
def test_source_unmodified():
    x=json.loads((ROOT/'analysis-index/08_quality/evidence/2020_source_integrity.json').read_text()); assert x['file_count']==39 and x['modification_count']==0 and x['all_sources_unmodified']
def test_exactly_one_preferred_representation():
    g={}
    for x in jl('analysis-index/04_relations/2020_representations.jsonl'):g.setdefault(x['logical_document_id'],[]).append(x)
    assert all(sum(y['preferred'] for y in ys)==1 for ys in g.values())
def test_ids_consistent():
    c=jl('analysis-index/01_inventory/2020_carrier_manifest.jsonl'); r=jl('analysis-index/04_relations/2020_representations.jsonl'); d=docs()
    assert {x['logical_document_id'] for x in c}=={x['logical_document_id'] for x in r}=={x['logical_document_id'] for x in d}
def test_misnamed_credit_paper_corrected():
    c=[x for x in jl('analysis-index/01_inventory/2020_carrier_manifest.jsonl') if '梯度下降' in x['original_filename']][0]; assert c['associated_problem']=='C' and c['logical_document_id'].startswith('2020-C-PAPER')
def test_e_q4_present():
    d=docs(); assert any(x['logical_document_id']=='2020-E-DATA-005' for x in d); g=json.loads((ROOT/'analysis-index/08_quality/gates/2020_gate.json').read_text()); assert g['checks']['four_quarters_present_for_problem_E']
def test_solution_lineages(): assert len(jl('analysis-index/04_relations/2020_solution_lineages.jsonl'))==17
def test_observed_methods():
    m=jl('analysis-index/05_knowledge/methods/2020_methods.jsonl'); assert sum(x.get('paper_observed',False) for x in m)>=80
def test_feedback_not_observed(): assert jl('analysis-index/05_knowledge/expert_feedback/2020_feedback.jsonl')==[]
def test_observed_visualizations():
    v=jl('analysis-index/05_knowledge/visualizations/2020_visualizations.jsonl'); assert sum(x.get('paper_observed',False) for x in v)==68
def test_segments_page_coordinates():
    for x in jl('analysis-index/03_segments/2020_segments.jsonl'):
        if x['segment_type']=='page':
            a,b,c,d=x['region']; assert 0<=a<c<=1 and 0<=b<d<=1
def test_page_boundaries_unique():
    p=[x for x in jl('analysis-index/03_segments/2020_segments.jsonl') if x['segment_type']=='page']; keys=[(x['representation_id'],x['page_number']) for x in p]; assert len(keys)==len(set(keys))
def test_tabular_boundaries():
    for x in jl('analysis-index/03_segments/2020_segments.jsonl'):
        if x['segment_type']!='page': assert x['row_start']>=1 and x['row_end']>=x['row_start'] and x['column_start']>=1 and x['column_end']>=x['column_start']
def test_six_pack_complete():
    names={'metadata.json','problem_summary.md','model_summary.md','validation.md','visualization.md','manual_review.json'}; base=ROOT/'analysis-index/02_documents/six_pack/2020'
    for d in docs(): assert names<={x.name for x in (base/d['logical_document_id']).iterdir()}
def test_six_pack_count(): assert len(list((ROOT/'analysis-index/02_documents/six_pack/2020').iterdir()))==39
def test_metadata_status_semantics():
    txt='\n'.join((p/'metadata.json').read_text() for p in (ROOT/'analysis-index/02_documents/six_pack/2020').iterdir()); assert '"status": "unknown"' in txt and '"status": "not_observed"' in txt and '"status": "absent"' not in txt
def test_gate_conditional_pass():
    g=json.loads((ROOT/'analysis-index/08_quality/gates/2020_gate.json').read_text()); assert g['status']=='conditional_pass' and g['blocking_items']==0 and g['checks']['solution_paper_corpus_present'] and not g['checks']['remote_readback_verified']
def test_checkpoint_counts_match_gate():
    g=json.loads((ROOT/'analysis-index/08_quality/gates/2020_gate.json').read_text()); c=json.loads((ROOT/'analysis-index/09_checkpoints/2020_checkpoint.json').read_text());
    for k in ['carriers','documents','solution_papers','problem_statements','supporting_objects','representations','segments']: assert g[k]==c[k]
def test_progress_pending_remote_readback():
    p=json.loads((ROOT/'analysis-index/00_control/progress.json').read_text()); assert 2020 not in p['completed_years'] and p['year_status']['2020']=='conditional_pass_pending_remote_readback' and p['next_recommended_year']==2020
def test_no_blocking_missing_requests(): assert all(not x['blocking'] for x in jl('analysis-index/00_control/missing_segment_requests.jsonl'))
def test_missing_files_txt_precise():
    t=(ROOT/'analysis-index/00_control/2020_missing_files.txt').read_text(); assert '没有阻塞性缺失文件' in t and '0~3' in t and '10~100万元' in t
def test_report_exists_and_has_corrections():
    t=(ROOT/'analysis-index/07_reports/yearly/2020_report.md').read_text(); assert '39个物理载体' in t and '17篇参赛论文' in t and 'conditional_pass' in t
def test_original_role_enum(): assert {x['role'] for x in docs()}<={'problem','paper','commentary','dataset'}
def test_format_spec_present(): assert any(x['logical_document_id']=='2020-GLOBAL-RULE-001' for x in docs())
def test_q4_audit_rows():
    a=json.loads((ROOT/'analysis-index/08_quality/evidence/2020_data_audit.json').read_text()); q=a['2020年国赛E题附件 (5).xlsx']; assert q['rows']==787466 and q['unique_water_meters']==91
