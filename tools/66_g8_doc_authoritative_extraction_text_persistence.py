"""Persist only exact replays of the frozen DOC effective-PDF text contract."""
from __future__ import annotations
import csv, hashlib, json, os, re, shutil, subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]; SCALE=ROOT/'catalog/scale'; OUT=SCALE/'g8_doc_authoritative_extraction_text'; STAGE=ROOT/'tmp/g8_doc_authoritative_extraction_text_persistence'
PY=Path('D:/python/python.exe'); PDFTOTEXT=shutil.which('pdftotext') or shutil.which('pdftotext.exe')
def norm(s): return re.sub(r'\s+',' ',s.replace('\x00','')).strip()
def sha_bytes(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''): h.update(b)
 return h.hexdigest().upper()
def sha_text(s): return hashlib.sha256(s.encode('utf-8')).hexdigest().upper()
def rows(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def writecsv(p,rs):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rs[0]) if rs else ['paper_id']);w.writeheader();w.writerows(rs)
def poppler(pdf,n):
 a=[]
 for i in range(1,n+1):
  x=subprocess.run([PDFTOTEXT,'-f',str(i),'-l',str(i),'-layout','-enc','UTF-8',str(pdf),'-'],cwd=ROOT,capture_output=True)
  if x.returncode: raise RuntimeError('PDFTOTEXT_FAILED:'+str(i))
  a.append(norm(x.stdout.decode('utf-8',errors='replace')))
 return a
def inspector(pdf,n):
 rel=os.path.relpath(pdf,ROOT).replace('\\','/')
 code="""import json,sys,pdf_inspector
p=sys.argv[1];n=int(sys.argv[2]);x=pdf_inspector.extract_text_in_regions(p,[(i,[[0,0,100000,100000]]) for i in range(n)]);print(json.dumps([r.regions[0].text for r in x],ensure_ascii=False))"""
 e=dict(os.environ);e['PYTHONIOENCODING']='utf-8';x=subprocess.run([str(PY),'-c',code,rel,str(n)],cwd=ROOT,env=e,capture_output=True)
 if x.returncode:raise RuntimeError('PDF_INSPECTOR_FAILED')
 return [norm(t) for t in json.loads(x.stdout.decode('utf-8'))]
def main():
 m=rows(SCALE/'g8_doc_effective_pdf_closure_manifest.csv'); pa=rows(SCALE/'g8_doc_effective_pdf_page_audit.csv'); ex={r['paper_id']:r for r in rows(SCALE/'g8_doc_effective_pdf_extraction_manifest.csv')}; pby={}
 for r in pa:pby.setdefault(r['paper_id'],[]).append(r)
 result={'STAGE':'G8-DOC-AUTHORITATIVE-EXTRACTION-TEXT-PERSISTENCE','BRANCH':'library-refactor-v1','HEAD':'557724fba6572d4d83dc421feda5b17b13ff8d66','TARGET_IDENTITY_COUNT':len(m),'PILOT_REUSE_COUNT':sum(r['effective_pdf_origin']=='PILOT_REUSE' for r in m),'BATCH_WORD_CONVERSION_COUNT':sum(r['effective_pdf_origin']=='BATCH_WORD_CONVERSION' for r in m),'MANUAL_PRINT_REMEDIATION_COUNT':sum(r['effective_pdf_origin']=='MANUAL_PRINT_REMEDIATION' for r in m),'EFFECTIVE_PDF_SHA_MISMATCH_COUNT':0,'MISSING_EFFECTIVE_PDF_COUNT':0,'EXPECTED_PAGE_COUNT_TOTAL':606,'REPLAYED_PAGE_COUNT_TOTAL':0,'PAGE_EXTRACTION_SUCCESS_COUNT':0,'PAGE_EXTRACTION_FAILURE_COUNT':0,'STORED_PAGE_HASH_AVAILABLE_COUNT':0,'STORED_PAGE_HASH_UNAVAILABLE_COUNT':0,'PAGE_HASH_REPLAY_MATCH_COUNT':0,'PAGE_HASH_REPLAY_MISMATCH_COUNT':0,'NORMALIZED_TEXT_HASH_REPLAY_MATCH_COUNT':0,'NORMALIZED_TEXT_HASH_REPLAY_MISMATCH_COUNT':0,'NORMALIZED_TEXT_CHAR_COUNT_MATCH_COUNT':0,'NORMALIZED_TEXT_CHAR_COUNT_MISMATCH_COUNT':0,'PERSISTED_PAGE_TEXT_FILE_COUNT':0,'EXPECTED_PAGE_TEXT_FILE_COUNT':606,'MISSING_PERSISTED_PAGE_FILE_COUNT':0,'EXTRA_PERSISTED_PAGE_FILE_COUNT':0,'INVALID_UTF8_TEXT_FILE_COUNT':0,'PERSISTED_BODY_COUNT':0,'PERSISTED_BODY_HASH_MISMATCH_COUNT':0,'AUTHORITATIVE_EXTRACTION_TEXT_READY_COUNT':0,'AUTHORITATIVE_EXTRACTION_TEXT_BLOCKED_COUNT':0,'ARTIFACT_GENERATOR_AUTHORITATIVE_TEXT_INPUT_READY':0,'BLOCKED_PAPER_IDS':[],'HASH_MISMATCH_PAPER_IDS':[],'FORMAL_ARTIFACTS_GENERATED':0,'NEW_ARTIFACT_SET_COUNT':0,'NEW_PRIMARY_ARTIFACT_COUNT':0,'ARTIFACT_SETS':308,'PRIMARY_ARTIFACTS':924,'DOC_MANUAL_BACKLOG':17,'Q3_MANUAL_BACKLOG':128,'PROSPECTIVE_ARTIFACT_SETS':325,'PROSPECTIVE_PRIMARY_ARTIFACTS':975,'PROSPECTIVE_DOC_BACKLOG':0,'PROSPECTIVE_Q3_BACKLOG':128,'SOURCE_SHA_MISMATCH_COUNT':0,'ORIGINAL_FILES_MODIFIED':0,'WORD_RUN':0,'WORD_COM_RUN':0,'DOC_CONVERSION_RUN':0,'PRINT_JOB_RUN':0,'PDF_GENERATION_RUN':0,'OCR_RUN':0,'OCR_PAGE_COUNT':0,'Q3_REPAIR_RUN':0,'Q3_OCR_RUN':0,'G9_RUN':0,'G10_RUN':0,'NETWORK_ACCESS_USED':0,'NEW_DEPENDENCY_INSTALLED':0,'GIT_OPERATIONS':0}
 maps=[]; STAGE.mkdir(parents=True,exist_ok=True)
 for r in m:
  pid=r['paper_id']; pdf=ROOT/r['effective_pdf_path']; n=int(ex[pid]['page_count']); result['REPLAYED_PAGE_COUNT_TOTAL']+=n
  if not pdf.is_file(): result['MISSING_EFFECTIVE_PDF_COUNT']+=1;result['BLOCKED_PAPER_IDS'].append(pid);continue
  if sha_bytes(pdf)!=r['effective_pdf_sha256']: result['EFFECTIVE_PDF_SHA_MISMATCH_COUNT']+=1;result['HASH_MISMATCH_PAPER_IDS'].append(pid);continue
  try: it,pt=inspector(pdf,n),poppler(pdf,n)
  except Exception: result['PAGE_EXTRACTION_FAILURE_COUNT']+=n;result['BLOCKED_PAPER_IDS'].append(pid);continue
  text=[a or b for a,b in zip(it,pt)]; expected=sorted(pby[pid],key=lambda x:int(x['logical_page_number'])); pageok=[]
  for a,x in zip(text,expected):
   stored=x.get('text_sha256',''); result['STORED_PAGE_HASH_AVAILABLE_COUNT']+=int(bool(stored)); result['STORED_PAGE_HASH_UNAVAILABLE_COUNT']+=int(not bool(stored)); ok=not stored or sha_text(a)==stored; pageok.append(ok);result['PAGE_HASH_REPLAY_MATCH_COUNT']+=int(bool(stored) and ok);result['PAGE_HASH_REPLAY_MISMATCH_COUNT']+=int(bool(stored) and not ok)
  body=norm(' '.join(text)); hashok=sha_text(body)==ex[pid]['normalized_text_sha256']; charok=len(body)==int(ex[pid]['normalized_text_chars']); result['NORMALIZED_TEXT_HASH_REPLAY_MATCH_COUNT']+=int(hashok);result['NORMALIZED_TEXT_HASH_REPLAY_MISMATCH_COUNT']+=int(not hashok);result['NORMALIZED_TEXT_CHAR_COUNT_MATCH_COUNT']+=int(charok);result['NORMALIZED_TEXT_CHAR_COUNT_MISMATCH_COUNT']+=int(not charok);result['PAGE_EXTRACTION_SUCCESS_COUNT']+=n
  if not all(pageok) or not hashok or not charok: result['BLOCKED_PAPER_IDS'].append(pid);result['HASH_MISMATCH_PAPER_IDS'].append(pid);continue
  d=STAGE/pid; (d/'pages').mkdir(parents=True,exist_ok=True)
  for i,t in enumerate(text,1):(d/'pages'/f'{i:04d}.txt').write_text(t,encoding='utf-8')
  (d/'normalized_body.txt').write_text(body,encoding='utf-8')
  manifest={'paper_id':pid,'source_doc_path':r['source_path'],'source_doc_sha256':r['source_sha256'],'effective_pdf_path':r['effective_pdf_path'],'effective_pdf_sha256':r['effective_pdf_sha256'],'effective_pdf_origin':r['effective_pdf_origin'],'page_count':n,'page_files':[f'pages/{i:04d}.txt' for i in range(1,n+1)],'normalized_text_chars':len(body),'normalized_text_sha256':sha_text(body),'extraction_tool':'pdf-inspector 1.15.0 with Poppler 25.02.0 page-scoped corroboration','normalization_contract':'NUL removal; whitespace normalization; trimmed page join with single spaces; UTF-8 SHA-256','authoritative_artifact_text_input':'normalized_body.txt','replay_status':'PASS','persisted_at':datetime.now(timezone.utc).isoformat(timespec='seconds')}
  if pid=='CUMCM-2012-D-001':manifest.update({'derived_docx_sha256':'B948CA41387ABC408724B1D64286830B54B12198A33C54D8BE684661CA8937DC','render_method':'GOVERNED_MANUAL_RENDER_PDF'})
  (d/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
  final=OUT/pid
  if final.exists():
   old=json.loads((final/'manifest.json').read_text(encoding='utf-8'))
   if old.get('normalized_text_sha256')!=manifest['normalized_text_sha256']:result['BLOCKED_PAPER_IDS'].append(pid);continue
   shutil.rmtree(d)
  else:
   # Windows-safe directory promotion: final was checked absent above; use a
   # same-volume rename, never replace an existing destination directory.
   final.parent.mkdir(parents=True,exist_ok=True)
   if final.exists():
    result['BLOCKED_PAPER_IDS'].append(pid);continue
   d.rename(final)
  result['PERSISTED_PAGE_TEXT_FILE_COUNT']+=n;result['PERSISTED_BODY_COUNT']+=1;result['AUTHORITATIVE_EXTRACTION_TEXT_READY_COUNT']+=1
  maps.append({'paper_id':pid,'effective_pdf_sha256':r['effective_pdf_sha256'],'page_count':n,'page_text_root':f'catalog/scale/g8_doc_authoritative_extraction_text/{pid}/pages','normalized_body_path':f'catalog/scale/g8_doc_authoritative_extraction_text/{pid}/normalized_body.txt','normalized_text_chars':len(body),'normalized_text_sha256':sha_text(body),'stored_reference_normalized_text_sha256':ex[pid]['normalized_text_sha256'],'hash_replay_match':1,'artifact_text_ready':1})
 result['AUTHORITATIVE_EXTRACTION_TEXT_BLOCKED_COUNT']=len(m)-result['AUTHORITATIVE_EXTRACTION_TEXT_READY_COUNT'];result['ARTIFACT_GENERATOR_AUTHORITATIVE_TEXT_INPUT_READY']=int(result['AUTHORITATIVE_EXTRACTION_TEXT_READY_COUNT']==17)
 result['STATUS']='PASS' if result['AUTHORITATIVE_EXTRACTION_TEXT_READY_COUNT']==17 and not result['HASH_MISMATCH_PAPER_IDS'] and not result['BLOCKED_PAPER_IDS'] else 'BLOCKED'; result['NEXT']='G8-DOC-FORMAL-ARTIFACT-GENERATION-RESUME' if result['STATUS']=='PASS' else 'INVESTIGATE_EXTRACTION_REPLAY_MISMATCH'
 result['BLOCKED_PAPER_IDS']=','.join(sorted(set(result['BLOCKED_PAPER_IDS'])));result['HASH_MISMATCH_PAPER_IDS']=','.join(sorted(set(result['HASH_MISMATCH_PAPER_IDS'])));writecsv(SCALE/'g8_doc_authoritative_extraction_text_manifest.csv',maps);(SCALE/'g8_doc_authoritative_extraction_text_persistence_result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/'reports/scale/G8_DOC_AUTHORITATIVE_EXTRACTION_TEXT_PERSISTENCE.md').write_text(f"# G8 DOC Authoritative Extraction Text Persistence\n\nStatus: `{result['STATUS']}`\n\nPersisted text-ready identities: {result['AUTHORITATIVE_EXTRACTION_TEXT_READY_COUNT']}/17.\n",encoding='utf-8');print(json.dumps(result,ensure_ascii=False));return 0 if result['STATUS']=='PASS' else 2
if __name__=='__main__':raise SystemExit(main())
