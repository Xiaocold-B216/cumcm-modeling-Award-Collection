from pathlib import Path
import csv, json, hashlib, os, zipfile

ROOT=Path(__file__).resolve().parents[1]
Y=2024

def read_jsonl(p):
    rows=[]
    for i,line in enumerate(p.read_text(encoding='utf-8-sig').splitlines(),1):
        if line.strip():
            rows.append(json.loads(line))
    return rows

def test_required_paths_exist():
    req=[
      'analysis-index/01_inventory/2024_carrier_manifest.jsonl',
      'analysis-index/02_documents/logical_documents/2024.csv',
      'analysis-index/03_segments/2024_segments.jsonl',
      'analysis-index/04_relations/2024_representations.jsonl',
      'analysis-index/04_relations/2024_relations.jsonl',
      'analysis-index/04_relations/2024_solution_lineages.jsonl',
      'analysis-index/05_knowledge/methods/2024_methods.jsonl',
      'analysis-index/05_knowledge/expert_feedback/2024_feedback.jsonl',
      'analysis-index/05_knowledge/visualizations/2024_visualizations.jsonl',
      'analysis-index/06_statistics/yearly/2024_statistics.csv',
      'analysis-index/07_reports/yearly/2024_report.md',
      'analysis-index/08_quality/gates/2024_gate.json',
      'analysis-index/09_checkpoints/2024_checkpoint.json',
      'analysis-index/00_control/progress.json',
      'analysis-index/00_control/checkpoint_manifest.json',
      'analysis-index/00_control/processing_log.jsonl',
      'analysis-index/00_control/missing_segment_requests.jsonl',
      'analysis-index/00_control/manual_review_queue.jsonl',
      '2024_missing_files.txt']
    assert all((ROOT/p).exists() for p in req)

def test_json_jsonl_parse():
    for p in ROOT.rglob('*.json'):
        json.loads(p.read_text(encoding='utf-8-sig'))
    for p in ROOT.rglob('*.jsonl'):
        read_jsonl(p)

def test_csv_parse_and_counts():
    p=ROOT/'analysis-index/02_documents/logical_documents/2024.csv'
    try:
   with p.open(encoding='utf-8-sig',newline='') as f: rows=list(csv.DictReader(f))
  except UnicodeDecodeError:
   with p.open(encoding='gbk',newline='') as f: rows=list(csv.DictReader(f))
    assert len(rows)==29
    assert sum(r['document_role']=='paper' for r in rows)==16
    assert sum(r['document_role']=='problem' for r in rows)==5
    assert sum(r['document_role']=='dataset' for r in rows)==8

def test_sha256_coverage_and_uniqueness():
    rows=read_jsonl(ROOT/'analysis-index/01_inventory/2024_carrier_manifest.jsonl')
    assert len(rows)==820
    assert len({r['carrier_id'] for r in rows})==820
    assert len({r['source_path'] for r in rows})==820
    assert len({r['sha256'] for r in rows})==820
    assert all(len(r['sha256'])==64 and set(r['sha256'])<=set('0123456789abcdef') for r in rows)
    assert all(r['source_unmodified'] for r in rows)

def test_carrier_assignment_consistency():
    carriers=read_jsonl(ROOT/'analysis-index/01_inventory/2024_carrier_manifest.jsonl')
    assigned=[r for r in carriers if r['logical_document_id']]
    archives=[r for r in carriers if r['carrier_kind']=='archive_container']
    assert len(assigned)==818 and len(archives)==2
    docs={}
    with (ROOT/'analysis-index/02_documents/logical_documents/2024.csv').open(encoding='utf-8-sig') as f:
        for r in csv.DictReader(f): docs[r['logical_document_id']]=r
    bydoc={k:0 for k in docs}
    for r in assigned: bydoc[r['logical_document_id']]+=1
    assert all(bydoc[k]==int(v['carrier_count']) for k,v in docs.items())

def test_representations_one_preferred_each():
    reps=read_jsonl(ROOT/'analysis-index/04_relations/2024_representations.jsonl')
    assert len(reps)==29
    by={}
    for r in reps: by.setdefault(r['logical_document_id'],[]).append(r)
    assert len(by)==29
    assert all(sum(x['is_preferred'] is True for x in v)==1 for v in by.values())
    assert sum(r['carrier_count'] for r in reps)==818

def test_roles_legal():
    legal={'problem','paper','commentary','dataset'}
    with (ROOT/'analysis-index/02_documents/logical_documents/2024.csv').open(encoding='utf-8-sig') as f:
        roles={r['document_role'] for r in csv.DictReader(f)}
    assert roles<=legal

def test_unknown_not_absent_policy():
    with (ROOT/'analysis-index/02_documents/logical_documents/2024.csv').open(encoding='utf-8-sig') as f:
        rows=list(csv.DictReader(f))
    assert all(r['award_level'] in {'unknown','not_applicable'} for r in rows)
    assert not any(r['award_level']=='absent' for r in rows)

def test_segments_coordinates_and_unique_pages():
    segs=read_jsonl(ROOT/'analysis-index/03_segments/2024_segments.jsonl')
    assert len(segs)==826
    seen=set()
    for s in segs:
        reg=s.get('region')
        if reg is not None:
            assert 0<=reg['x0']<reg['x1']<=1
            assert 0<=reg['y0']<reg['y1']<=1
        if s['segment_type']=='page':
            key=(s['logical_document_id'],s['page_index'])
            assert key not in seen
            seen.add(key)
    assert sum(s['segment_type']=='page' for s in segs)==815

def test_a242_missing_pages_explicit():
    reps=read_jsonl(ROOT/'analysis-index/04_relations/2024_representations.jsonl')
    r=next(x for x in reps if x['logical_document_id']=='doc_2024_paper_A242')
    assert r['missing_page_indices']==[12,15,16]
    req=read_jsonl(ROOT/'analysis-index/00_control/missing_segment_requests.jsonl')
    paths={x['expected_path'] for x in req}
    assert '2024国赛优秀论文/A题/A242/12.jpg' in paths
    assert '2024国赛优秀论文/A题/A242/15.jpg' in paths
    assert '2024国赛优秀论文/A题/A242/16.jpg' in paths

def test_missing_official_templates_explicit():
    req=read_jsonl(ROOT/'analysis-index/00_control/missing_segment_requests.jsonl')
    paths={x['expected_path'] for x in req}
    assert {'2024真题/A题/附件/result4.xlsx','2024真题/C题/附件3/result1_1.xlsx','2024真题/C题/附件3/result1_2.xlsx','2024真题/C题/附件3/result2.xlsx'}<=paths
    assert len(req)==7 and all(x['blocking'] for x in req)

def test_six_pack_complete():
    with (ROOT/'analysis-index/02_documents/logical_documents/2024.csv').open(encoding='utf-8-sig') as f:
        ids=[r['logical_document_id'] for r in csv.DictReader(f)]
    names={'metadata.json','problem_summary.md','model_summary.md','validation.md','visualization.md','manual_review.json'}
    for did in ids:
        d=ROOT/f'analysis-index/02_documents/cards/2024/{did}'
        assert {p.name for p in d.iterdir()}==names

def test_methods_lineages_visualizations():
    assert len(read_jsonl(ROOT/'analysis-index/05_knowledge/methods/2024_methods.jsonl'))==16
    assert len(read_jsonl(ROOT/'analysis-index/04_relations/2024_solution_lineages.jsonl'))==16
    assert len(read_jsonl(ROOT/'analysis-index/05_knowledge/visualizations/2024_visualizations.jsonl'))==16

def test_expert_feedback_empty_not_fabricated():
    assert read_jsonl(ROOT/'analysis-index/05_knowledge/expert_feedback/2024_feedback.jsonl')==[]

def test_source_integrity_record():
    x=json.loads((ROOT/'analysis-index/08_quality/evidence/2024_source_integrity.json').read_text(encoding='utf-8-sig'))
    assert x['physical_carrier_count']==820
    assert x['unique_sha256_count']==820
    assert x['exact_duplicate_groups']==0
    assert x['modified_files']==0

def test_statistics_match_gate():
    gate=json.loads((ROOT/'analysis-index/08_quality/gates/2024_gate.json').read_text(encoding='utf-8-sig'))
    with (ROOT/'analysis-index/06_statistics/yearly/2024_statistics.csv').open(encoding='utf-8-sig') as f:
        total=next(csv.DictReader(f))
    assert int(total['physical_carriers'])==gate['counts']['physical_carriers']==820
    assert int(total['logical_documents'])==gate['counts']['logical_documents']==29
    assert int(total['solution_papers'])==16
    assert int(total['representations'])==29

def test_gate_is_conditional_not_pass():
    gate=json.loads((ROOT/'analysis-index/08_quality/gates/2024_gate.json').read_text(encoding='utf-8-sig'))
    assert gate['status']=='conditional_pass'
    assert gate['blocking_missing_items']==7
    assert gate['checks']['all_expected_attachments_present'] is False
    assert gate['checks']['all_observed_page_sequences_complete'] is False

def test_checkpoint_consistent():
    gate=json.loads((ROOT/'analysis-index/08_quality/gates/2024_gate.json').read_text(encoding='utf-8-sig'))
    cp=json.loads((ROOT/'analysis-index/09_checkpoints/2024_checkpoint.json').read_text(encoding='utf-8-sig'))
    assert cp['status']==gate['status']=='conditional_pass'
    assert cp['counts']==gate['counts']
    assert cp['remote_readback_verified'] is False

def test_progress_does_not_promote_to_pass():
    p=json.loads((ROOT/'analysis-index/00_control/progress.json').read_text(encoding='utf-8-sig'))
    assert p['year_status']['2024']=='conditional_pass'
    assert 2024 not in p['completed_years']
    assert 2024 in p['processed_years']

def test_no_raw_source_in_upload_tree():
    forbidden={'.jpg','.jpeg','.pdf','.xlsx','.csv','.doc','.zip','.rar','.mdb'}
    # upload package contains analysis artifacts only; .csv statistics is allowed, so only check source-like locations
    assert not (ROOT/'raw').exists()
    assert not (ROOT/'2024国赛优秀论文').exists()
    assert not (ROOT/'2024真题').exists()

def test_local_actual_hashes_when_sources_available():
    papers=Path('/mnt/data/2024国赛优秀论文.zip'); probs=Path('/mnt/data/2024真题.zip')
    if not papers.exists() or not probs.exists():
        return
    rows=read_jsonl(ROOT/'analysis-index/01_inventory/2024_carrier_manifest.jsonl')
    arc={r['source_path']:r['sha256'] for r in rows if r['carrier_kind']=='archive_container'}
    def h(p):
        x=hashlib.sha256()
        with p.open('rb') as f:
            for b in iter(lambda:f.read(8*1024*1024),b''): x.update(b)
        return x.hexdigest()
    assert h(papers)==arc['2024国赛优秀论文.zip']
    assert h(probs)==arc['2024真题.zip']

def test_relation_endpoints_and_ids_valid():
    with (ROOT/'analysis-index/02_documents/logical_documents/2024.csv').open(encoding='utf-8-sig') as f:
        docs={r['logical_document_id'] for r in csv.DictReader(f)}
    reps=read_jsonl(ROOT/'analysis-index/04_relations/2024_representations.jsonl')
    repids={r['representation_id'] for r in reps}
    known=docs|repids
    rels=read_jsonl(ROOT/'analysis-index/04_relations/2024_relations.jsonl')
    assert len({r['relation_id'] for r in rels})==len(rels)
    assert all(r['source_id'] in known and r['target_id'] in known for r in rels)

def test_segment_references_are_resolvable():
    carriers={r['carrier_id'] for r in read_jsonl(ROOT/'analysis-index/01_inventory/2024_carrier_manifest.jsonl')}
    reps={r['representation_id'] for r in read_jsonl(ROOT/'analysis-index/04_relations/2024_representations.jsonl')}
    with (ROOT/'analysis-index/02_documents/logical_documents/2024.csv').open(encoding='utf-8-sig') as f:
        docs={r['logical_document_id'] for r in csv.DictReader(f)}
    segs=read_jsonl(ROOT/'analysis-index/03_segments/2024_segments.jsonl')
    assert len({s['segment_id'] for s in segs})==len(segs)
    assert all(s['logical_document_id'] in docs for s in segs)
    assert all(s['representation_id'] in reps for s in segs)
    assert all(not s.get('carrier_id') or s['carrier_id'] in carriers for s in segs)

def test_final_control_readback_provenance():
    p=json.loads((ROOT/'analysis-index/00_control/progress.json').read_text(encoding='utf-8-sig'))
    prov=p['control_merge_provenance']
    assert prov['remote_progress_blob_sha']=='1ac6896e9a80eab95a9b50ad5eb5be54b2648659'
    assert len(prov['remote_absent_at_readback'])==4
    integrity=json.loads((ROOT/'analysis-index/08_quality/evidence/2024_source_integrity.json').read_text(encoding='utf-8-sig'))
    assert integrity['rehash_checked_carriers']==820
    assert integrity['rehash_mismatches']==0
