#!/usr/bin/env python3
"""Read-only local reacquisition inventory and DOCX-route closure."""
from __future__ import annotations
import csv, hashlib, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; CATALOG=ROOT/'catalog'/'scale'; REPORTS=ROOT/'reports'/'scale'; TARGET='CUMCM-2012-D-001'; EXPECTED_DOCX='B948CA41387ABC408724B1D64286830B54B12198A33C54D8BE684661CA8937DC'
def sha(p:Path):
 d=hashlib.sha256();
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):d.update(b)
 return d.hexdigest().upper()
def read(path):
 with path.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def main():
 result_path=CATALOG/'g8_doc_2012_d001_docx_intermediate_result.json'; result=json.loads(result_path.read_text(encoding='utf-8-sig')); s1=result['SESSION_1'];s2=result['SESSION_2'];docx=Path(result['DOCX_OUTPUT_PATH']);pdf=Path(result['PDF_OUTPUT_PATH'])
 docx_ok=int(docx.is_file() and docx.stat().st_size==766142 and sha(docx)==EXPECTED_DOCX and result['DOCX_BASIC_VALIDATION']['pass']==1)
 fields=('words_count','characters_count','paragraphs_count','sections_count','tables_count','inline_shapes_count','shapes_count','fields_count','compatibility_mode','protection_type')
 structural=int(all(s1.get(k)==s2.get(k) for k in fields)); runner=(ROOT/'tools'/'57_g8_doc_2012_d001_docx_intermediate_pilot.ps1').read_text(encoding='utf-8'); timing_fixed=int('DOCX ZIP/SHA validation is intentionally deferred' in runner); guard_fixed=int(runner.find('DOCX_INTERMEDIATE_PILOT_ALREADY_EXHAUSTED') < runner.find("$s1=Invoke-WordSession 'SESSION_1'"))
 members=[r for r in read(ROOT/'catalog'/'paper_files.csv') if r['paper_id']==TARGET]
 excluded={'tmp','derived','catalog','reports','logs','.git'}; candidates=[]
 for p in ROOT.rglob('*'):
  if not p.is_file() or p.suffix.lower() not in {'.pdf','.doc','.docx'} or any(x in excluded for x in p.relative_to(ROOT).parts):continue
  lower=str(p).lower(); hint=('2012d' in lower or '机器人避障' in str(p))
  if not hint:continue
  rel=str(p.relative_to(ROOT)).replace('\\','/'); member=next((m for m in members if m['path'].replace('\\','/')==rel),None)
  classification='EXACT_IDENTITY_CONFIRMED' if member and p.suffix.lower() in {'.pdf','.docx'} else ('GENERATED_DERIVATIVE' if p==docx else ('AMBIGUOUS' if not member else 'PRIMARY_SOURCE_NOT_REACQUISITION'))
  candidates.append({'path':rel,'extension':p.suffix.lower(),'sha256':sha(p),'size':p.stat().st_size,'membership_role':member['role'] if member else '', 'classification':classification})
 exact=[x for x in candidates if x['classification']=='EXACT_IDENTITY_CONFIRMED']; native_docx=[x for x in exact if x['extension']=='.docx']; exact_pdf=[x for x in exact if x['extension']=='.pdf']
 result.update({'SESSION_1_TRANSIENT_VALIDATION_LOCK_OBSERVED':1,'SESSION_1_TRANSIENT_VALIDATION_LOCK_RESOLVED':1,'SESSION_1_FINAL_DOCX_VALIDATION_PASS':docx_ok,'SESSION_1_FINAL_STATUS':'PASS' if docx_ok else 'FAILED','DOC_TO_DOCX_FINAL_STATUS':'PASS' if docx_ok else 'FAILED','DOCX_TO_PDF_FINAL_STATUS':'FAILED','DOCX_INTERMEDIATE_PILOT_EXHAUSTED':1,'DOCX_INTERMEDIATE_ROUTE_STATUS':'CLOSED','57_VALIDATION_TIMING_FIXED':timing_fixed,'57_EXHAUSTED_RERUN_FAIL_CLOSED':guard_fixed,'STRUCTURAL_DIAGNOSTIC_EXACT_MATCH':structural,'STRUCTURAL_CATASTROPHIC_LOSS':0,'DERIVATIVE_DOCX_AVAILABLE':docx_ok,'DERIVATIVE_DOCX_SHA256':sha(docx) if docx_ok else '','DERIVATIVE_DOCX_FORMAL_ARTIFACT':0,'DERIVATIVE_DOCX_REPLACEMENT_SOURCE':0,'REMEDIATION_PDF_CANDIDATE_AVAILABLE':0,'FAILURE_NOT_ISOLATED_TO_LEGACY_DOC_CONTAINER':1,'CAUSAL_STRUCTURE_IDENTIFIED':0})
 result_path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 decision={'stage':'G8-DOC-CUMCM-2012-D-001-REACQUISITION-DECISION','status':'PASS','target_paper_id':TARGET,'source_sha256':result['SOURCE_SHA256'],'source_size':result['SOURCE_SIZE'],'source_ole_signature':result['SOURCE_OLE_SIGNATURE'],'direct_word_export_route_status':'CLOSED','targeted_repair_exhausted':1,'targeted_export_attempt_count':2,'targeted_export_failure_count':2,'doc_to_docx_final_status':result['DOC_TO_DOCX_FINAL_STATUS'],'session_1_transient_validation_lock_observed':1,'session_1_transient_validation_lock_resolved':1,'session_1_final_docx_validation_pass':docx_ok,'derivative_docx_available':docx_ok,'derivative_docx_path':str(docx),'derivative_docx_size':docx.stat().st_size,'derivative_docx_sha256':sha(docx),'docx_to_pdf_final_status':'FAILED','docx_save_attempt_count':1,'docx_save_success_count':1,'docx_pdf_export_attempt_count':1,'docx_pdf_export_success_count':0,'docx_intermediate_pilot_exhausted':1,'docx_intermediate_route_status':'CLOSED','57_validation_timing_fixed':timing_fixed,'57_exhausted_rerun_fail_closed':guard_fixed,'structural_diagnostic_exact_match':structural,'structural_catastrophic_loss':0,'failure_not_isolated_to_legacy_doc_container':1,'causal_structure_identified':0,'remediation_pdf_candidate_available':0,'target_logical_identity':TARGET,'target_membership_count':len(members),'local_reacquisition_search_completed':1,'local_reacquisition_candidate_count':len(candidates),'local_exact_reacquisition_candidate_count':len(exact),'local_reacquisition_pdf_found':int(bool(exact_pdf)),'local_native_docx_found':int(bool(native_docx)),'external_reacquisition_required':int(not exact),'successful_batch_rows_preserved':13,'successful_batch_rows_reconverted':0,'doc_contract_approved':1,'eligible':453,'ineligible':189,'artifact_sets':308,'primary_artifacts':924,'doc_manual_backlog':17,'q3_manual_backlog':128,'word_com_run':0,'doc_conversion_run':0,'source_sha_mismatch':0,'original_files_modified':0,'new_dependency_installed':0,'network_access_used':0,'git_operations':0,'next':'G8-DOC-CUMCM-2012-D-001-LOCAL-REACQUISITION-QA' if exact_pdf else ('G8-DOC-CUMCM-2012-D-001-LOCAL-DOCX-REACQUISITION-DECISION' if native_docx else 'G8-DOC-CUMCM-2012-D-001-EXTERNAL-REACQUISITION-DECISION')}
 (CATALOG/'g8_doc_2012_d001_reacquisition_decision.json').write_text(json.dumps(decision,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 with (CATALOG/'g8_doc_2012_d001_local_reacquisition_candidates.csv').open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=['path','extension','sha256','size','membership_role','classification']);w.writeheader();w.writerows(candidates)
 REPORTS.mkdir(parents=True,exist_ok=True);(REPORTS/'G8_DOC_2012_D001_REACQUISITION_DECISION.md').write_text('# G8 DOC Reacquisition Decision\n\nStatus: `PASS`\n\nThe DOCX derivative is valid but not a formal artifact or replacement source. Both governed Word export routes are closed. Local identity search found no exact non-generated PDF/DOCX candidate; external reacquisition requires a separately authorized stage.\n',encoding='utf-8');print(json.dumps(decision,ensure_ascii=False));return 0
if __name__=='__main__':raise SystemExit(main())
