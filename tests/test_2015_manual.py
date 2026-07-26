from __future__ import annotations
import csv, hashlib, json, re
from collections import Counter, defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; AN=ROOT/'analysis-index'; YEAR=2015

def read_jsonl(p): return [json.loads(x) for x in p.read_text(encoding='utf-8').splitlines() if x.strip()]
def docs():
 with (AN/'02_documents/logical_documents/2015.csv').open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))

def test_01_required_files_exist():
 required=[AN/'01_inventory/2015_carrier_manifest.jsonl',AN/'02_documents/logical_documents/2015.csv',AN/'03_segments/2015_segments.jsonl',AN/'04_relations/2015_representations.jsonl',AN/'04_relations/2015_relations.jsonl',AN/'04_relations/2015_solution_lineages.jsonl',AN/'05_knowledge/methods/2015_methods.jsonl',AN/'05_knowledge/expert_feedback/2015_feedback.jsonl',AN/'05_knowledge/visualizations/2015_visualizations.jsonl',AN/'06_statistics/yearly/2015_statistics.csv',AN/'07_reports/yearly/2015_report.md',AN/'08_quality/gates/2015_gate.json',AN/'09_checkpoints/2015_checkpoint.json',AN/'00_control/progress.json',AN/'00_control/checkpoint_manifest.json',AN/'00_control/processing_log.jsonl',AN/'00_control/missing_segment_requests.jsonl',AN/'00_control/manual_review_queue.jsonl']
 assert all(p.is_file() for p in required)
def test_02_json_jsonl_structures():
 for p in ROOT.rglob('*.json'): json.loads(p.read_text(encoding='utf-8'))
 for p in ROOT.rglob('*.jsonl'): read_jsonl(p)
def test_03_csv_structures():
 for p in ROOT.rglob('*.csv'):
  with p.open(encoding='utf-8',newline='') as f: rows=list(csv.DictReader(f))
  assert rows
def test_04_sha256_coverage_and_format():
 c=read_jsonl(AN/'01_inventory/2015_carrier_manifest.jsonl'); assert len(c)==29 and len({x['carrier_id'] for x in c})==29
 assert all(re.fullmatch(r'[0-9a-f]{64}',x['sha256']) for x in c)
def test_05_source_snapshot_unmodified():
 s=json.loads((AN/'00_control/2015_source_hash_snapshot.json').read_text()); assert s['source_modified_count']==0 and len(s['files'])==29
 assert all(x['pre_sha256']==x['post_sha256'] and not x['modified'] for x in s['files'])
def test_06_logical_document_count_and_ids(): assert len(docs())==28 and len({x['logical_document_id'] for x in docs()})==28
def test_07_roles_legal_and_counts(): assert Counter(x['role'] for x in docs())==Counter({'paper':18,'dataset':6,'problem':4})
def test_08_problem_distribution(): assert Counter(x['problem_id'] for x in docs() if x['role']=='paper')==Counter({'2015_A':6,'2015_B':5,'2015_C':4,'2015_D':3})
def test_09_unknown_not_absent_policy():
 assert all(x['award_level']=='unknown' and x['authors_status']=='not_observed' for x in docs())
def test_10_representation_count_and_references():
 r=read_jsonl(AN/'04_relations/2015_representations.jsonl'); c=read_jsonl(AN/'01_inventory/2015_carrier_manifest.jsonl')
 assert len(r)==29 and {x['carrier_id'] for x in r}=={x['carrier_id'] for x in c}
def test_11_exactly_one_preferred_representation():
 by=defaultdict(list)
 for x in read_jsonl(AN/'04_relations/2015_representations.jsonl'):by[x['logical_document_id']].append(x)
 assert len(by)==28 and all(sum(bool(r['is_preferred']) for r in rs)==1 for rs in by.values())
def test_12_duplicate_representation_resolution():
 g=[x for x in read_jsonl(AN/'04_relations/2015_representations.jsonl') if x.get('duplicate_group_id')=='2015_DUP_A_PAPER_005']
 assert len(g)==2 and len({x['file_sha256'] for x in g})==2 and len({x['normalized_text_or_data_sha256'] for x in g})==1 and len({x['render_sequence_sha256'] for x in g})==1
def test_13_no_other_duplicate_group():
 r=read_jsonl(AN/'04_relations/2015_representations.jsonl'); assert sum(x.get('duplicate_group_id') is not None for x in r)==2
def test_14_lineage_counts_and_links():
 l=read_jsonl(AN/'04_relations/2015_solution_lineages.jsonl'); assert len(l)==18 and len({x['solution_lineage_id'] for x in l})==18
 assert all(len(x['logical_document_ids'])==1 for x in l)
def test_15_problem_paper_relations():
 s=[x for x in read_jsonl(AN/'04_relations/2015_relations.jsonl') if x['relation_type']=='solves']; assert len(s)==18
 assert Counter(x['target_document_id'] for x in s)==Counter({'2015_PROBLEM_A':6,'2015_PROBLEM_B':5,'2015_PROBLEM_C':4,'2015_PROBLEM_D':3})
def test_16_segment_count_consistency():
 s=read_jsonl(AN/'03_segments/2015_segments.jsonl'); r=read_jsonl(AN/'04_relations/2015_representations.jsonl'); assert len(s)==625
 c=Counter(x['representation_id'] for x in s); assert all(c[x['representation_id']]==x['segment_count'] for x in r)
def test_17_preferred_segment_count():
 s=read_jsonl(AN/'03_segments/2015_segments.jsonl'); r=read_jsonl(AN/'04_relations/2015_representations.jsonl'); p={x['representation_id'] for x in r if x['is_preferred']}
 assert sum(x['representation_id'] in p for x in s)==599
def test_18_page_bounds_valid():
 for s in read_jsonl(AN/'03_segments/2015_segments.jsonl'):
  b=s['bounds']
  if s['segment_type']=='page': assert b['x0']==0 and b['y0']==0 and b['x1']>0 and b['y1']>0 and s['page_number']>=1
def test_19_sheet_bounds_valid():
 ss=[s for s in read_jsonl(AN/'03_segments/2015_segments.jsonl') if s['segment_type']=='sheet_region']; assert len(ss)==3
 assert all(1<=s['bounds']['row_start']<=s['bounds']['row_end'] and 1<=s['bounds']['col_start']<=s['bounds']['col_end'] for s in ss)
def test_20_no_duplicate_page_segments():
 s=[x for x in read_jsonl(AN/'03_segments/2015_segments.jsonl') if x['segment_type']=='page']; k=[(x['representation_id'],x['page_number']) for x in s]; assert len(k)==len(set(k))
def test_21_six_pack_complete():
 c=AN/'02_documents/document_cards/2015'; req={'metadata.json','problem_summary.md','model_summary.md','validation.md','visualization.md','manual_review.json'}; ds=[p for p in c.iterdir() if p.is_dir()]
 assert len(ds)==28 and all(req<={x.name for x in d.iterdir() if x.is_file()} for d in ds)
def test_22_six_pack_metadata_matches_csv():
 for r in docs():
  m=json.loads((AN/'02_documents/document_cards/2015'/r['logical_document_id']/'metadata.json').read_text()); assert m['logical_document_id']==r['logical_document_id'] and m['role']==r['role']
def test_23_card_preferred_rep_matches_relation():
 r=read_jsonl(AN/'04_relations/2015_representations.jsonl'); p={x['logical_document_id']:x['representation_id'] for x in r if x['is_preferred']}
 for d,i in p.items(): assert json.loads((AN/'02_documents/document_cards/2015'/d/'metadata.json').read_text())['preferred_representation_id']==i
def test_24_methods_have_valid_documents_and_pages():
 m=read_jsonl(AN/'05_knowledge/methods/2015_methods.jsonl'); d={x['logical_document_id']:int(x['page_or_region_count']) for x in docs()}; assert len(m)>=100
 assert all(x['logical_document_id'] in d and x['evidence_pages'] and min(x['evidence_pages'])>=1 and max(x['evidence_pages'])<=d[x['logical_document_id']] for x in m)
def test_25_methods_cover_all_papers():
 m=read_jsonl(AN/'05_knowledge/methods/2015_methods.jsonl'); assert {x['logical_document_id'] for x in m}>={x['logical_document_id'] for x in docs() if x['role']=='paper'}
def test_26_expert_feedback_not_fabricated():
 r=read_jsonl(AN/'05_knowledge/expert_feedback/2015_feedback.jsonl'); assert len(r)==1 and r[0]['feedback_status']=='not_observed'
def test_27_visualization_records():
 r=read_jsonl(AN/'05_knowledge/visualizations/2015_visualizations.jsonl'); assert len(r)>=20 and all(x['documents'] for x in r)
def test_28_statistics_consistent():
 with (AN/'06_statistics/yearly/2015_statistics.csv').open(encoding='utf-8',newline='') as f:s=next(csv.DictReader(f))
 assert (int(s['physical_carriers']),int(s['logical_documents']),int(s['representations']))==(29,28,29)
 assert (int(s['solution_papers']),int(s['problem_statements']),int(s['datasets_supporting']))==(18,4,6)
 assert (int(s['representation_segments']),int(s['logical_preferred_segments']))==(625,599)
def test_29_quality_gate_conditional_and_blocked():
 g=json.loads((AN/'08_quality/gates/2015_gate.json').read_text()); assert g['status']=='conditional_pass' and g['blocking_manual_review_items']==2
 assert not g['checks']['raw_bundle_completeness_verified'] and not g['checks']['all_referenced_attachments_present']
def test_30_missing_file_is_specific():
 t=(AN/'00_control/2015_missing_files.txt').read_text(); assert 'A题附件4原始视频文件' in t and '2015-07-13 08:54:06' in t and '09:34:36' in t and '2015_raw_bundle.zip' in t
def test_31_manual_queue_consistency():
 q=read_jsonl(AN/'00_control/manual_review_queue.jsonl'); assert len(q)==2 and all(x['status']=='open' and x['severity']=='blocking' for x in q)
def test_32_progress_reconciliation():
 p=json.loads((AN/'00_control/progress.json').read_text()); assert p['last_verified_complete_year']==2009 and p['year_status']['2010']=='conditional_pass' and p['year_status']['2015'].startswith('conditional_pass') and p['stop_after_year']==2015 and p['next_recommended_year'] is None
def test_33_original_file_modified_count_zero(): assert json.loads((AN/'00_control/2015_source_hash_snapshot.json').read_text())['source_modified_count']==0
def test_34_all_carrier_hashes_link_to_representations():
 c={x['carrier_id']:x for x in read_jsonl(AN/'01_inventory/2015_carrier_manifest.jsonl')}
 for r in read_jsonl(AN/'04_relations/2015_representations.jsonl'): assert r['file_sha256']==c[r['carrier_id']]['sha256']
def test_35_late_uploaded_files_included():
 names={x['source_filename'] for x in read_jsonl(AN/'01_inventory/2015_carrier_manifest.jsonl')}
 assert all(f'2015B：互联网+_时代的出租车资源配置 ({i}).pdf' in names for i in range(1,6))
 assert all(any(n.startswith(f'2015C：月上柳梢头，人约黄昏后 ({i}).') for n in names) for i in range(1,5))
 assert all(any(n.startswith(f'2015D：众筹筑屋规划方案设计 ({i}).') for n in names) for i in range(1,4))
def test_36_no_cache_or_compiled_files(): assert not any(p.name=='__pycache__' or p.suffix in {'.pyc','.pyo'} or p.name=='.pytest_cache' for p in ROOT.rglob('*'))
