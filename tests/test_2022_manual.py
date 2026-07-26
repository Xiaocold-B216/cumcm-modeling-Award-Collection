from __future__ import annotations
from pathlib import Path
import csv, hashlib, json, os, re
import pytest

ROOT = Path(__file__).resolve().parents[1]
YEAR = 2022

def read_jsonl(path):
    text=path.read_text(encoding='utf-8-sig')
    return [json.loads(line) for line in text.splitlines() if line.strip()]

def sha256(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):
            h.update(chunk)
    return h.hexdigest()

def test_required_paths_exist():
    required=[
      'analysis-index/01_inventory/2022_carrier_manifest.jsonl',
      'analysis-index/02_documents/logical_documents/2022.csv',
      'analysis-index/03_segments/2022_segments.jsonl',
      'analysis-index/04_relations/2022_representations.jsonl',
      'analysis-index/04_relations/2022_relations.jsonl',
      'analysis-index/04_relations/2022_solution_lineages.jsonl',
      'analysis-index/05_knowledge/methods/2022_methods.jsonl',
      'analysis-index/05_knowledge/expert_feedback/2022_feedback.jsonl',
      'analysis-index/05_knowledge/visualizations/2022_visualizations.jsonl',
      'analysis-index/06_statistics/yearly/2022_statistics.csv',
      'analysis-index/07_reports/yearly/2022_report.md',
      'analysis-index/08_quality/gates/2022_gate.json',
      'analysis-index/09_checkpoints/2022_checkpoint.json',
      'analysis-index/00_control/progress.json',
      'analysis-index/00_control/checkpoint_manifest.json',
      'analysis-index/00_control/processing_log.jsonl',
      'analysis-index/00_control/missing_segment_requests.jsonl',
      'analysis-index/00_control/manual_review_queue.jsonl',
      '2022_missing_files.txt',
    ]
    assert all((ROOT/p).is_file() for p in required)

def test_json_files_parse():
    for p in ROOT.rglob('*.json'):
        json.loads(p.read_text(encoding='utf-8-sig'))

def test_jsonl_files_parse():
    for p in ROOT.rglob('*.jsonl'):
        read_jsonl(p)

def test_csv_files_parse_and_have_rows():
    for p in ROOT.rglob('*.csv'):
        with p.open(encoding='utf-8-sig',newline='') as f:
            rows=list(csv.DictReader(f))
        assert rows

def test_inventory_sha256_coverage_and_uniqueness():
    rows=read_jsonl(ROOT/'analysis-index/01_inventory/2022_carrier_manifest.jsonl')
    assert len(rows)==260
    pages=[r for r in rows if r['carrier_scope']=='source_page_image']
    assert len(pages)==259
    assert all(re.fullmatch(r'[0-9a-f]{64}',r['sha256']) for r in rows)
    assert len({r['sha256'] for r in pages})==259

def test_object_count_consistency():
    with (ROOT/'analysis-index/02_documents/logical_documents/2022.csv').open(encoding='utf-8-sig',newline='') as f:
        docs=list(csv.DictReader(f))
    reps=read_jsonl(ROOT/'analysis-index/04_relations/2022_representations.jsonl')
    segs=read_jsonl(ROOT/'analysis-index/03_segments/2022_segments.jsonl')
    inv=read_jsonl(ROOT/'analysis-index/01_inventory/2022_carrier_manifest.jsonl')
    pages=[r for r in inv if r['carrier_scope']=='source_page_image']
    assert len(docs)==7 and len(reps)==7 and len(segs)==259 and len(pages)==259
    assert sum(int(d['page_count']) for d in docs)==259
    assert sum(r['page_count'] for r in reps)==259

def test_one_preferred_representation_per_document():
    reps=read_jsonl(ROOT/'analysis-index/04_relations/2022_representations.jsonl')
    grouped={}
    for r in reps: grouped.setdefault(r['logical_document_id'],[]).append(r)
    assert all(sum(1 for r in rs if r['preferred'])==1 for rs in grouped.values())

def test_representation_carriers_and_segments_resolve():
    inv=read_jsonl(ROOT/'analysis-index/01_inventory/2022_carrier_manifest.jsonl')
    pages={r['carrier_id']:r for r in inv if r['carrier_scope']=='source_page_image'}
    reps=read_jsonl(ROOT/'analysis-index/04_relations/2022_representations.jsonl')
    segs=read_jsonl(ROOT/'analysis-index/03_segments/2022_segments.jsonl')
    assert all(cid in pages for r in reps for cid in r['carrier_ids'])
    assert {s['carrier_id'] for s in segs}==set(pages)
    assert all(len(r['carrier_ids'])==r['page_count'] for r in reps)

def test_legal_document_roles():
    legal={'problem','paper','commentary','dataset'}
    with (ROOT/'analysis-index/02_documents/logical_documents/2022.csv').open(encoding='utf-8-sig',newline='') as f:
        docs=list(csv.DictReader(f))
    assert {d['document_role'] for d in docs} <= legal
    assert {d['document_role'] for d in docs} == {'paper'}

def test_unknown_is_not_absent():
    for p in ROOT.glob('analysis-index/02_documents/logical_documents/2022/*/metadata.json'):
        m=json.loads(p.read_text(encoding='utf-8-sig'))
        assert 'absent' not in set(m['feature_status'].values())
        assert m['award_level']=='unknown'
        assert m['authors']=='not_observed'

def test_page_boundaries_valid_and_non_overlapping():
    segs=read_jsonl(ROOT/'analysis-index/03_segments/2022_segments.jsonl')
    by_carrier={}
    for s in segs:
        b=s['normalized_bbox']
        assert 0<=b['x0']<b['x1']<=1 and 0<=b['y0']<b['y1']<=1
        by_carrier.setdefault(s['carrier_id'],[]).append(b)
    assert all(len(v)==1 for v in by_carrier.values())

def test_page_indices_are_contiguous():
    segs=read_jsonl(ROOT/'analysis-index/03_segments/2022_segments.jsonl')
    by_doc={}
    for s in segs: by_doc.setdefault(s['logical_document_id'],[]).append(s['page_index'])
    assert all(sorted(v)==list(range(1,len(v)+1)) for v in by_doc.values())

def test_six_pack_exactly_present_for_each_document():
    base=ROOT/'analysis-index/02_documents/logical_documents/2022'
    dirs=[p for p in base.iterdir() if p.is_dir()]
    required={'metadata.json','problem_summary.md','model_summary.md','validation.md','visualization.md','manual_review.json'}
    assert len(dirs)==7
    assert all({p.name for p in d.iterdir() if p.is_file()}==required for d in dirs)

def test_lineage_and_method_document_ids_resolve():
    with (ROOT/'analysis-index/02_documents/logical_documents/2022.csv').open(encoding='utf-8-sig',newline='') as f:
        docs={r['logical_document_id'] for r in csv.DictReader(f)}
    lineages=read_jsonl(ROOT/'analysis-index/04_relations/2022_solution_lineages.jsonl')
    methods=read_jsonl(ROOT/'analysis-index/05_knowledge/methods/2022_methods.jsonl')
    assert {r['logical_document_id'] for r in lineages}==docs
    assert {r['logical_document_id'] for r in methods}<=docs

def test_visualization_page_references_resolve():
    segs={s['segment_id'] for s in read_jsonl(ROOT/'analysis-index/03_segments/2022_segments.jsonl')}
    viz=read_jsonl(ROOT/'analysis-index/05_knowledge/visualizations/2022_visualizations.jsonl')
    assert viz and all(v['segment_id'] in segs for v in viz)

def test_expert_feedback_empty_because_not_observed():
    assert read_jsonl(ROOT/'analysis-index/05_knowledge/expert_feedback/2022_feedback.jsonl')==[]

def test_confirmed_content_duplicates_are_retained_not_merged():
    rels=read_jsonl(ROOT/'analysis-index/04_relations/2022_relations.jsonl')
    dup=[r for r in rels if r['relation_type']=='same_visible_content_different_physical_page']
    assert len(dup)==2
    inv=read_jsonl(ROOT/'analysis-index/01_inventory/2022_carrier_manifest.jsonl')
    flagged=[r for r in inv if r.get('content_duplicate_group')]
    assert len(flagged)==4 and len({r['sha256'] for r in flagged})==4

def test_statistics_match_counts():
    with (ROOT/'analysis-index/06_statistics/yearly/2022_statistics.csv').open(encoding='utf-8-sig',newline='') as f:
        rows=list(csv.DictReader(f))
    y=next(r for r in rows if r['scope']=='year')
    assert int(y['source_carriers'])==259 and int(y['logical_documents'])==7 and int(y['representations'])==7 and int(y['page_segments'])==259

def test_gate_is_conditional_not_pass():
    g=json.loads((ROOT/'analysis-index/08_quality/gates/2022_gate.json').read_text(encoding='utf-8-sig'))
    assert g['status']=='conditional_pass'
    assert g['checks']['full_year_source_complete'] is False
    assert g['checks']['official_problem_statements_present'] is False

def test_missing_file_requests_are_precise():
    rows=read_jsonl(ROOT/'analysis-index/00_control/missing_segment_requests.jsonl')
    assert len(rows)==7
    assert all(r['expected_name_or_role'] and r['recognition_features'] for r in rows)

def test_progress_stops_at_2022_without_claiming_gap_years():
    p=json.loads((ROOT/'analysis-index/00_control/progress.json').read_text(encoding='utf-8-sig'))
    assert p['stop_after_year']==2022 and p['next_recommended_year'] is None
    assert p['year_status']['2012']=='not_observed' and p['year_status']['2021']=='not_observed'
    assert p['year_status']['2022']=='conditional_pass_pending_remote_readback'

def test_checkpoint_pending_remote_readback():
    c=json.loads((ROOT/'analysis-index/09_checkpoints/2022_checkpoint.json').read_text(encoding='utf-8-sig'))
    assert c['remote_readback_verified'] is False and c['stop_after_year']==2022

def test_source_files_unmodified_when_raw_root_available():
    raw=os.environ.get('CUMCM_2022_RAW_ROOT')
    if not raw:
        pytest.skip('Set CUMCM_2022_RAW_ROOT for source read-only verification')
    raw=Path(raw)
    rows=read_jsonl(ROOT/'analysis-index/01_inventory/2022_carrier_manifest.jsonl')
    pages=[r for r in rows if r['carrier_scope']=='source_page_image']
    mismatches=[]
    for r in pages:
        p=raw/r['source_relative_path']
        if not p.is_file() or sha256(p)!=r['sha256']:
            mismatches.append(r['source_relative_path'])
    assert mismatches==[]

def test_transport_bundle_hash_when_available():
    path=os.environ.get('CUMCM_2022_BUNDLE')
    if not path:
        pytest.skip('Set CUMCM_2022_BUNDLE for bundle hash verification')
    rows=read_jsonl(ROOT/'analysis-index/01_inventory/2022_carrier_manifest.jsonl')
    b=next(r for r in rows if r['carrier_scope']=='transport_bundle')
    assert sha256(Path(path))==b['sha256']
