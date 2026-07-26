from __future__ import annotations
import csv, hashlib, json
from collections import defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
YEAR='2017'

def j(path): return json.loads((ROOT/path).read_text(encoding='utf-8-sig'))
def jl(path):
    p=ROOT/path
    if not p.read_text(encoding='utf-8-sig').strip(): return []
    return [json.loads(x) for x in p.read_text(encoding='utf-8-sig').splitlines() if x.strip()]

def test_01_required_annual_files_exist():
    req=['analysis-index/01_inventory/2017_carrier_manifest.jsonl','analysis-index/02_documents/logical_documents/2017.csv','analysis-index/03_segments/2017_segments.jsonl','analysis-index/04_relations/2017_representations.jsonl','analysis-index/04_relations/2017_relations.jsonl','analysis-index/04_relations/2017_solution_lineages.jsonl','analysis-index/05_knowledge/methods/2017_methods.jsonl','analysis-index/05_knowledge/expert_feedback/2017_feedback.jsonl','analysis-index/05_knowledge/visualizations/2017_visualizations.jsonl','analysis-index/06_statistics/yearly/2017_statistics.csv','analysis-index/07_reports/yearly/2017_report.md','analysis-index/08_quality/gates/2017_gate.json','analysis-index/09_checkpoints/2017_checkpoint.json','2017_missing_files.txt']
    assert all((ROOT/x).exists() for x in req)

def test_02_required_control_files_exist():
    req=['analysis-index/00_control/progress.json','analysis-index/00_control/checkpoint_manifest.json','analysis-index/00_control/processing_log.jsonl','analysis-index/00_control/missing_segment_requests.jsonl','analysis-index/00_control/manual_review_queue.jsonl']
    assert all((ROOT/x).exists() for x in req)

def test_03_json_and_jsonl_parse():
    for p in ROOT.rglob('*.json'): json.loads(p.read_text(encoding='utf-8-sig'))
    for p in ROOT.rglob('*.jsonl'):
        for line in p.read_text(encoding='utf-8-sig').splitlines():
            if line.strip(): json.loads(line)

def test_04_csv_schema():
    with (ROOT/'analysis-index/02_documents/logical_documents/2017.csv').open(encoding='utf-8-sig') as f:
        rows=list(csv.DictReader(f))
    assert len(rows)==19
    assert {'logical_document_id','role','preferred_representation_id','representation_count'} <= set(rows[0])

def test_05_carrier_count(): assert len(jl('analysis-index/01_inventory/2017_carrier_manifest.jsonl'))==20

def test_06_sha256_coverage_and_format():
    rows=jl('analysis-index/01_inventory/2017_carrier_manifest.jsonl')
    assert all(len(r['sha256'])==64 and set(r['sha256'])<=set('0123456789abcdef') for r in rows)
    assert len({r['sha256'] for r in rows})==20

def test_07_trusted_baseline_blob_match():
    rows=jl('analysis-index/01_inventory/2017_carrier_manifest.jsonl')
    assert all(r['baseline_match'] and r['git_blob_sha1']==r['baseline_git_blob_sha1'] for r in rows)

def test_08_source_unmodified():
    x=j('analysis-index/01_inventory/2017_source_integrity.json')
    assert x['all_unchanged'] is True and x['source_modified_count']==0 and x['pre_hash_count']==20

def test_09_roles_legal():
    with (ROOT/'analysis-index/02_documents/logical_documents/2017.csv').open(encoding='utf-8-sig') as f: rows=list(csv.DictReader(f))
    assert {r['role'] for r in rows} <= {'problem','paper','commentary','dataset'}

def test_10_counts_consistent():
    reps=jl('analysis-index/04_relations/2017_representations.jsonl'); cars=jl('analysis-index/01_inventory/2017_carrier_manifest.jsonl')
    with (ROOT/'analysis-index/02_documents/logical_documents/2017.csv').open(encoding='utf-8-sig') as f: docs=list(csv.DictReader(f))
    assert len(cars)==20 and len(reps)==20 and len(docs)==19
    assert sum(int(d['representation_count']) for d in docs)==20

def test_11_one_preferred_representation():
    reps=jl('analysis-index/04_relations/2017_representations.jsonl'); g=defaultdict(list)
    for r in reps: g[r['logical_document_id']].append(r)
    assert len(g)==19 and all(sum(bool(x['is_preferred']) for x in xs)==1 for xs in g.values())

def test_12_format_spec_merged():
    reps=[r for r in jl('analysis-index/04_relations/2017_representations.jsonl') if r['logical_document_id']=='2017_reference_format_spec']
    assert len(reps)==2 and {r['format'] for r in reps}=={'doc','pdf'} and [r for r in reps if r['is_preferred']][0]['format']=='pdf'

def test_13_solution_lineages():
    l=jl('analysis-index/04_relations/2017_solution_lineages.jsonl')
    assert len(l)==6 and all(x['lineage_status']=='distinct_solution' for x in l)

def test_14_paper_problem_distribution():
    with (ROOT/'analysis-index/02_documents/logical_documents/2017.csv').open(encoding='utf-8-sig') as f: rows=list(csv.DictReader(f))
    papers=[r for r in rows if r['role']=='paper']
    assert len(papers)==6 and sum(r['problem_id']=='A' for r in papers)==5 and sum(r['problem_id']=='B' for r in papers)==1

def test_15_six_pack_complete():
    with (ROOT/'analysis-index/02_documents/logical_documents/2017.csv').open(encoding='utf-8-sig') as f: ids=[r['logical_document_id'] for r in csv.DictReader(f)]
    names={'metadata.json','problem_summary.md','model_summary.md','validation.md','visualization.md','manual_review.json'}
    for did in ids:
        p=ROOT/'analysis-index/02_documents/document_cards/2017'/did
        assert {x.name for x in p.iterdir()}==names

def test_16_segments_reference_valid_representations():
    reps={r['representation_id'] for r in jl('analysis-index/04_relations/2017_representations.jsonl')}
    segs=jl('analysis-index/03_segments/2017_segments.jsonl')
    assert len(segs)==223 and all(s['representation_id'] in reps for s in segs)

def test_17_page_bbox_legal():
    for s in jl('analysis-index/03_segments/2017_segments.jsonl'):
        if s['bbox'] is not None:
            x0,y0,x1,y1=s['bbox']; assert x0>=0 and y0>=0 and x1>x0 and y1>y0

def test_18_page_regions_nonoverlap():
    groups=defaultdict(list)
    for s in jl('analysis-index/03_segments/2017_segments.jsonl'):
        if s['page_number'] is not None: groups[(s['representation_id'],s['page_number'])].append(s)
    assert all(len(v)==1 for v in groups.values())

def test_19_solution_paper_pages():
    reps=jl('analysis-index/04_relations/2017_representations.jsonl')
    assert sum(r['page_count'] or 0 for r in reps if r['logical_document_id'].startswith('2017_paper_'))==190

def test_20_unknown_not_absent():
    corpus='\n'.join(p.read_text(encoding='utf-8-sig',errors='ignore') for p in ROOT.rglob('*') if p.is_file() and p.suffix in {'.json','.jsonl','.csv'})
    assert '"absent"' not in corpus and ',absent,' not in corpus

def test_21_missing_requests_exact():
    req=jl('analysis-index/00_control/missing_segment_requests.jsonl'); q=jl('analysis-index/00_control/manual_review_queue.jsonl')
    assert len(req)==12 and len(q)==12 and all(x['severity']=='blocking' for x in req)
    assert sum('2017B：' in x['requested_repository_path'] for x in req)==6
    assert sum('2017C：' in x['requested_repository_path'] for x in req)==3
    assert sum('2017D：' in x['requested_repository_path'] for x in req)==3

def test_22_gate_conditional_not_pass():
    g=j('analysis-index/08_quality/gates/2017_gate.json')
    assert g['status']=='conditional_pass' and g['blocking_manual_review_items']==12
    assert g['checks']['manual_verification_complete_for_full_year'] is False

def test_23_progress_conservative():
    p=j('analysis-index/00_control/progress.json')
    assert p['last_verified_complete_year']==2009
    assert p['year_status']['2017']=='conditional_pass_missing_source_carriers'
    assert 2017 not in p['completed_years']

def test_24_no_expert_commentary_fabrication():
    assert jl('analysis-index/05_knowledge/expert_feedback/2017_feedback.jsonl')==[]
    with (ROOT/'analysis-index/02_documents/logical_documents/2017.csv').open(encoding='utf-8-sig') as f: rows=list(csv.DictReader(f))
    assert not any(r['role']=='commentary' for r in rows)
