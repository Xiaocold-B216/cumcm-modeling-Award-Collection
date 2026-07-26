from __future__ import annotations
import csv, hashlib, json, os, re
from collections import Counter, defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
AI=ROOT/'analysis-index'
YEAR=2021
SHA_RE=re.compile(r'^[0-9a-f]{64}$')


def j(path): return json.loads(path.read_text(encoding='utf-8-sig'))
def jl(path):
    text=path.read_text(encoding='utf-8-sig')
    return [json.loads(x) for x in text.splitlines() if x.strip()]

def docs():
    with (AI/'02_documents/logical_documents/2021.csv').open(encoding='utf-8-sig',newline='') as f: return list(csv.DictReader(f))

def test_01_required_files_exist():
    required=['01_inventory/2021_carrier_manifest.jsonl','02_documents/logical_documents/2021.csv','03_segments/2021_segments.jsonl','04_relations/2021_representations.jsonl','04_relations/2021_relations.jsonl','04_relations/2021_solution_lineages.jsonl','05_knowledge/methods/2021_methods.jsonl','05_knowledge/expert_feedback/2021_feedback.jsonl','05_knowledge/visualizations/2021_visualizations.jsonl','06_statistics/yearly/2021_statistics.csv','07_reports/yearly/2021_report.md','08_quality/gates/2021_gate.json','09_checkpoints/2021_checkpoint.json','00_control/progress.json','00_control/checkpoint_manifest.json','00_control/processing_log.jsonl','00_control/missing_segment_requests.jsonl','00_control/manual_review_queue.jsonl']
    assert all((AI/p).exists() for p in required)

def test_02_json_jsonl_parse():
    for p in AI.rglob('*.json'): j(p)
    for p in AI.rglob('*.jsonl'): jl(p)

def test_03_csv_structure():
    ds=docs(); assert len(ds)==37
    with (AI/'06_statistics/yearly/2021_statistics.csv').open(encoding='utf-8-sig',newline='') as f: rows=list(csv.DictReader(f))
    assert len(rows)==6 and rows[0]['scope']=='ALL'

def test_04_sha256_coverage():
    cs=jl(AI/'01_inventory/2021_carrier_manifest.jsonl')
    assert len(cs)==754
    assert all(SHA_RE.match(x['sha256']) for x in cs)
    assert len({x['carrier_id'] for x in cs})==754

def test_05_carrier_layer_counts():
    cs=jl(AI/'01_inventory/2021_carrier_manifest.jsonl')
    c=Counter(x['carrier_layer'] for x in cs)
    assert c=={'archive_member':753,'archive_container':1}
    ext=Counter(x['extension'] for x in cs if x['carrier_layer']=='archive_member')
    assert ext['.jpg']==729 and ext['.xlsx']==15 and ext['.pdf']==5 and ext['.csv']==3 and ext['.doc']==1

def test_06_document_role_counts():
    c=Counter(x['role'] for x in docs())
    assert c=={'paper':17,'problem':5,'dataset':14,'commentary':1}
    assert set(c)<= {'problem','paper','commentary','dataset'}

def test_07_representation_counts_and_preferred():
    rs=jl(AI/'04_relations/2021_representations.jsonl'); ds=docs()
    assert len(rs)==41
    by=defaultdict(list)
    for r in rs: by[r['logical_document_id']].append(r)
    assert set(by)=={d['logical_document_id'] for d in ds}
    assert all(sum(bool(r['preferred']) for r in vals)==1 for vals in by.values())

def test_08_representations_reference_carriers():
    cids={x['carrier_id'] for x in jl(AI/'01_inventory/2021_carrier_manifest.jsonl')}
    for r in jl(AI/'04_relations/2021_representations.jsonl'):
        assert r['carrier_ids'] and set(r['carrier_ids'])<=cids

def test_09_segments_count_and_ids():
    ss=jl(AI/'03_segments/2021_segments.jsonl')
    assert len(ss)==769 and len({s['segment_id'] for s in ss})==769

def test_10_page_boundaries_valid_no_overlap():
    ss=jl(AI/'03_segments/2021_segments.jsonl'); seen=set()
    for s in ss:
        if 'bbox_normalized' in s:
            x0,y0,x1,y1=s['bbox_normalized']; assert 0<=x0<x1<=1 and 0<=y0<y1<=1
            key=(s['representation_id'],s.get('page_number'))
            assert key not in seen; seen.add(key)
        else:
            assert 1<=s['row_start']<=s['row_end'] and 1<=s['column_start']<=s['column_end']

def test_11_paper_page_sequences():
    ss=jl(AI/'03_segments/2021_segments.jsonl'); by=defaultdict(list)
    for s in ss:
        if s['logical_document_id'].startswith('2021-paper-'): by[s['logical_document_id']].append(s['page_number'])
    assert len(by)==17
    for pages in by.values(): assert sorted(pages)==list(range(1,len(pages)+1))

def test_12_six_pack_complete():
    for d in docs():
        p=AI/'02_documents/six_packs/2021'/d['logical_document_id']
        assert {x.name for x in p.iterdir()}=={'metadata.json','problem_summary.md','model_summary.md','validation.md','visualization.md','manual_review.json'}

def test_13_relation_and_lineage_counts():
    rel=jl(AI/'04_relations/2021_relations.jsonl'); lin=jl(AI/'04_relations/2021_solution_lineages.jsonl')
    assert len(lin)==17 and sum(x['relation_type']=='solves' for x in rel)==17 and sum(x['relation_type']=='supports' for x in rel)==14

def test_14_unknown_not_absent_policy():
    for d in docs():
        assert d['award_level'] in {'unknown','not_applicable'}
    text='\n'.join(p.read_text(encoding='utf-8-sig') for p in (AI/'02_documents/six_packs/2021').rglob('*.md'))
    assert '未观察' in text or 'not_observed' in text

def test_15_expert_feedback_not_fabricated():
    rows=jl(AI/'05_knowledge/expert_feedback/2021_feedback.jsonl')
    assert len(rows)==1 and rows[0]['status']=='not_observed' and rows[0]['expert_commentary_documents']==0

def test_16_duplicate_e_datasets_corrected():
    ds={x['logical_document_id']:x for x in docs()}; rs=jl(AI/'04_relations/2021_representations.jsonl')
    for n in range(1,5):
        did=f'2021-dataset-E{n}-'+{1:'mid-ir-types',2:'mid-ir-origins',3:'near-mid-ir-origins',4:'near-ir-types-origins'}[n]
        assert ds[did]['problem_id']=='E' and ds[did]['representation_count']=='2'
        vals=[r for r in rs if r['logical_document_id']==did]
        assert len(vals)==2 and len({r['byte_identical_group'] for r in vals})==1

def test_17_statistics_consistency():
    with (AI/'06_statistics/yearly/2021_statistics.csv').open(encoding='utf-8-sig',newline='') as f: rows=list(csv.DictReader(f))
    allr=rows[0]
    assert int(allr['physical_carriers'])==754 and int(allr['logical_documents'])==37 and int(allr['representations'])==41 and int(allr['segments'])==769
    assert sum(int(r['solution_papers']) for r in rows[1:])==17

def test_18_source_unmodified_evidence():
    gate=j(AI/'08_quality/gates/2021_gate.json'); cp=j(AI/'09_checkpoints/2021_checkpoint.json')
    assert gate['checks']['source_unmodified'] is True and cp['source_files_modified']==0
    p=Path(os.environ.get('YEAR2021_SOURCE_ARCHIVE','/nonexistent'))
    if p.exists():
        h=hashlib.sha256(p.read_bytes()).hexdigest(); assert h==cp['source_archive_sha256']

def test_19_quality_gate_conditional_nonblocking():
    g=j(AI/'08_quality/gates/2021_gate.json')
    assert g['status']=='conditional_pass' and g['blocking_manual_review_items']==0 and g['manual_review_items']==2

def test_20_no_raw_source_in_upload_package():
    forbidden={'.jpg','.jpeg','.pdf','.xlsx','.xls','.doc','.docx','.rar','.zip','.mdb'}
    files=[p for p in ROOT.rglob('*') if p.is_file()]
    assert not [p for p in files if p.suffix.lower() in forbidden]
