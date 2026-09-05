"""Bind the existing TeX Live Poppler 25.02.0 runtime and replay G8 evidence."""
from __future__ import annotations
import csv, hashlib, importlib.metadata, json, os, re, subprocess, sys, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; SCALE=ROOT/'catalog/scale'; BIN=Path(r'D:\texlive\2026\bin\windows')
PDFINFO=BIN/'pdfinfo.exe'; PDFTOTEXT=BIN/'pdftotext.exe'; PDFTOPPM=BIN/'pdftoppm.exe'; PDFTOCAIRO=BIN/'pdftocairo.exe'; PY=Path(r'D:\python\python.exe')
REF=SCALE/'g8_doc_effective_pdf_closure_manifest.csv'; PAGES=SCALE/'g8_doc_effective_pdf_page_audit.csv'; EX=SCALE/'g8_doc_effective_pdf_extraction_manifest.csv'; BIND=SCALE/'g8_q3_poppler_runtime_binding.json'; OUTR=SCALE/'g8_poppler_25_02_0_reference_replay.csv'; OUTP=SCALE/'g8_poppler_25_02_0_page_validation.csv'; OUTB=SCALE/'g8_poppler_25_02_0_body_validation.csv'; RESULT=SCALE/'g8_poppler_25_02_0_local_bind_validation_result.json'; REPORT=ROOT/'reports/scale/G8_Q3_POPPLER_25_02_0_LOCAL_BIND_AND_VALIDATE.md'
def rows(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def wc(p,rs):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rs[0]) if rs else ['paper_id']);w.writeheader();w.writerows(rs)
def norm(s):return re.sub(r'\s+',' ',s.replace('\x00','')).strip()
def st(s):return hashlib.sha256(s.encode('utf-8')).hexdigest().upper()
def sf(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest().upper()
def ver(p):
 x=subprocess.run([str(p),'-v'],capture_output=True,text=True,encoding='utf-8',errors='replace');line=(x.stdout+x.stderr).splitlines()[0] if (x.stdout+x.stderr).splitlines() else ''
 m=re.search(r'version\s+(\S+)',line);return (m.group(1) if m else 'UNKNOWN'),x.returncode
def pagecount(p):
 x=subprocess.run([str(PDFINFO),str(p)],capture_output=True,text=True,encoding='utf-8',errors='replace');m=re.search(r'^Pages:\s*(\d+)',x.stdout,re.M)
 if x.returncode or not m:raise RuntimeError('PDFINFO_FAILED')
 return int(m.group(1))
def pop(p,n):
 a=[]
 for i in range(1,n+1):
  x=subprocess.run([str(PDFTOTEXT),'-f',str(i),'-l',str(i),'-layout','-enc','UTF-8',str(p),'-'],capture_output=True)
  if x.returncode:raise RuntimeError('PDFTOTEXT_FAILED:'+str(i))
  a.append(norm(x.stdout.decode('utf-8',errors='replace')))
 return a
def insp(p,n):
 rel=os.path.relpath(p,ROOT).replace('\\','/'); code="""import json,sys,pdf_inspector
p=sys.argv[1];n=int(sys.argv[2]);x=pdf_inspector.extract_text_in_regions(p,[(i,[[0,0,100000,100000]]) for i in range(n)]);print(json.dumps([r.regions[0].text for r in x],ensure_ascii=False))"""; env=dict(os.environ);env['PYTHONIOENCODING']='utf-8';x=subprocess.run([str(PY),'-c',code,rel,str(n)],cwd=ROOT,env=env,capture_output=True)
 if x.returncode:raise RuntimeError('PDF_INSPECTOR_FAILED')
 return [norm(t) for t in json.loads(x.stdout.decode('utf-8'))]
def counts():
 a=rows(SCALE/'g8_artifact_manifest.csv');b=rows(SCALE/'g8_manual_backlog.csv');e=rows(SCALE/'g8_artifact_eligibility.csv');return {'ARTIFACT_SETS':len(a)//3,'PRIMARY_ARTIFACTS':len(a),'DOC_MANUAL_BACKLOG':sum(x.get('category')=='DOC_REPAIR_MANUAL' for x in b),'Q3_MANUAL_BACKLOG':sum(x.get('category')=='Q3_REPAIR_MANUAL' for x in b),'ELIGIBLE':sum(x.get('artifact_eligible')=='1' for x in e),'INELIGIBLE':sum(x.get('artifact_eligible')!='1' for x in e)}
def main():
 ref=sorted(rows(REF),key=lambda x:x['paper_id']); pg=rows(PAGES); ex={x['paper_id']:x for x in rows(EX)}; by={}
 for x in pg:by.setdefault(x['paper_id'],[]).append(x)
 tools={'PDFINFO':PDFINFO,'PDFTOTEXT':PDFTOTEXT,'PDFTOPPM':PDFTOPPM,'PDFTOCAIRO':PDFTOCAIRO};vs={k:ver(v) for k,v in tools.items()}; mismatch=sum(v[0]!='25.02.0' for v in vs.values());loads=sum(v[1]!=0 for v in vs.values())
 r={'STAGE':'G8-Q3-POPPLER-25-02-0-LOCAL-BIND-AND-VALIDATE','STATUS':'BLOCKED','BRANCH':subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip(),'HEAD':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'POPPLER_ROOT':str(BIN),**{k+'_PATH':str(v) for k,v in tools.items()},**{k+'_VERSION':vs[k][0] for k in tools},'POPPLER_TOOL_VERSION_MISMATCH_COUNT':mismatch,'POPPLER_TOOL_LOAD_FAILURE_COUNT':loads,'POPPLER_RUNTIME_COPIED':0,'TEXLIVE_MODIFIED':0,'REFERENCE_IDENTITY_COUNT':len(ref),'REFERENCE_PAGE_COUNT':sum(int(x['page_count']) for x in ex.values()),'REFERENCE_PDF_MISSING_COUNT':0,'REFERENCE_PDF_SHA_MISMATCH_COUNT':0,'REPLAY_PAGE_COUNT':0,'PAGE_COUNT_MATCH_COUNT':0,'PAGE_COUNT_MISMATCH_COUNT':0,'PAGE_HASH_MATCH_COUNT':0,'PAGE_HASH_MISMATCH_COUNT':0,'BODY_HASH_MATCH_COUNT':0,'BODY_HASH_MISMATCH_COUNT':0,'BODY_CHAR_COUNT_MATCH_COUNT':0,'BODY_CHAR_COUNT_MISMATCH_COUNT':0,'PAGE_SEQUENCE_MISMATCH_COUNT':0,'PAGE_TEXT_PRESENCE_CLASS_MISMATCH_COUNT':0,'RENDER_SMOKE_PAGE_COUNT':0,'RENDER_SMOKE_FAILURE_COUNT':0,'RENDER_OUTPUT_ZERO_BYTE_COUNT':0,'POPPLER_RUNTIME_BINDING_PREPARED':0,'POPPLER_RUNTIME_BINDING_VALIDATED':0,'ACTIVE_POPPLER_VERSION':'','Q3_PILOT_RUNNER_RUNTIME_GATE_UPDATED':0,'POPPLER_26_05_0_COMPATIBILITY_STATUS':'UNTESTABLE_INCOMPLETE_RUNTIME','OCR_RUN':0,'Q3_OCR_RUN':0,'Q3_OCR_PAGE_COUNT':0,'OCR_WORKER_INITIALIZATION_RUN':0,'PILOT_TARGET_COUNT':0,'FULL_Q3_BATCH_RUN':0,'FORMAL_ARTIFACTS_GENERATED':0,'EXISTING_ARTIFACT_MODIFICATION_COUNT':0,'NETWORK_ACCESS_USED':0,'DOWNLOAD_RUN':0,'NEW_DEPENDENCY_INSTALLED':0,'WORD_RUN':0,'WORD_COM_RUN':0,'DOC_CONVERSION_RUN':0,'PRINT_JOB_RUN':0,'G9_RUN':0,'G10_RUN':0,'GIT_OPERATIONS':0,'MISMATCH_PAPER_IDS':'','MISMATCH_PAGE_IDS':''};r.update(counts());rr=[];pr=[];br=[];mp=set();mi=[]
 try:
  if mismatch or loads or importlib.metadata.version('pdf-inspector')!='1.15.0':raise RuntimeError('POPPLER_OR_PDF_INSPECTOR_GATE_FAILED')
  for x in ref:
   pid=x['paper_id'];p=ROOT/x['effective_pdf_path'];hist=sorted(by[pid],key=lambda q:int(q['logical_page_number']));expected=ex[pid]
   if not p.is_file():r['REFERENCE_PDF_MISSING_COUNT']+=1;mp.add(pid);continue
   if sf(p)!=x['effective_pdf_sha256']:r['REFERENCE_PDF_SHA_MISMATCH_COUNT']+=1;mp.add(pid);continue
   n=pagecount(p);ok=n==int(expected['page_count']);r['PAGE_COUNT_MATCH_COUNT']+=ok;r['PAGE_COUNT_MISMATCH_COUNT']+=not ok
   if not ok:mp.add(pid);continue
   it=insp(p,n);pt=pop(p,n);chosen=[a or b for a,b in zip(it,pt)];seq=len(chosen)==n==len(hist) and [int(q['logical_page_number']) for q in hist]==list(range(1,n+1));r['PAGE_SEQUENCE_MISMATCH_COUNT']+=not seq;r['REPLAY_PAGE_COUNT']+=n
   for i,(h,t,z) in enumerate(zip(hist,chosen,pt),1):
    hok=st(t)==h['text_sha256'];pok=(bool(z)==(int(h.get('poppler_text_chars','0')or 0)>0) and len(z)==int(h.get('poppler_text_chars','0')or 0));r['PAGE_HASH_MATCH_COUNT']+=hok;r['PAGE_HASH_MISMATCH_COUNT']+=not hok;r['PAGE_TEXT_PRESENCE_CLASS_MISMATCH_COUNT']+=not pok
    if not hok or not pok:mp.add(pid);mi.append(f'{pid}:{i}')
    pr.append({'paper_id':pid,'page_number':i,'effective_pdf_sha256':x['effective_pdf_sha256'],'pdf_inspector_text_chars':len(it[i-1]),'poppler_text_chars':len(z),'selected_authoritative_source':'PDF_INSPECTOR' if it[i-1] else 'POPPLER_FALLBACK','normalized_page_chars':len(t),'normalized_page_sha256':st(t),'historical_page_sha256':h['text_sha256'],'hash_match':int(hok)})
   body=norm(' '.join(chosen));bh=st(body)==expected['normalized_text_sha256'];ch=len(body)==int(expected['normalized_text_chars']);r['BODY_HASH_MATCH_COUNT']+=bh;r['BODY_HASH_MISMATCH_COUNT']+=not bh;r['BODY_CHAR_COUNT_MATCH_COUNT']+=ch;r['BODY_CHAR_COUNT_MISMATCH_COUNT']+=not ch
   if not bh or not ch or not seq:mp.add(pid)
   br.append({'paper_id':pid,'historical_body_sha256':expected['normalized_text_sha256'],'candidate_body_sha256':st(body),'historical_chars':expected['normalized_text_chars'],'candidate_chars':len(body),'hash_match':int(bh),'char_match':int(ch)});rr.append({'paper_id':pid,'effective_pdf_path':x['effective_pdf_path'],'effective_pdf_sha256':x['effective_pdf_sha256'],'historical_page_count':expected['page_count'],'candidate_page_count':n,'page_count_match':int(ok)})
  smoke=[]
  for q in sorted(pr,key=lambda x:(-int(x['normalized_page_chars']),x['paper_id'],int(x['page_number'])))[:6]:smoke.append((q['paper_id'],int(q['page_number'])))
  with tempfile.TemporaryDirectory(prefix='g8_poppler_smoke_',dir=ROOT/'tmp') as d:
   for pid,num in smoke:
    p=ROOT/next(x['effective_pdf_path'] for x in ref if x['paper_id']==pid);prefix=Path(d)/f'{pid}_{num:04d}';x=subprocess.run([str(PDFTOPPM),'-f',str(num),'-l',str(num),'-singlefile','-r','150','-png',str(p),str(prefix)],capture_output=True);png=Path(str(prefix)+'.png');r['RENDER_SMOKE_FAILURE_COUNT']+=int(x.returncode!=0 or not png.is_file());r['RENDER_OUTPUT_ZERO_BYTE_COUNT']+=int(png.is_file() and png.stat().st_size==0)
  r['RENDER_SMOKE_PAGE_COUNT']=len(smoke)
  strict=not any(r[k] for k in ['REFERENCE_PDF_MISSING_COUNT','REFERENCE_PDF_SHA_MISMATCH_COUNT','PAGE_COUNT_MISMATCH_COUNT','PAGE_HASH_MISMATCH_COUNT','BODY_HASH_MISMATCH_COUNT','BODY_CHAR_COUNT_MISMATCH_COUNT','PAGE_SEQUENCE_MISMATCH_COUNT','PAGE_TEXT_PRESENCE_CLASS_MISMATCH_COUNT','RENDER_SMOKE_FAILURE_COUNT','RENDER_OUTPUT_ZERO_BYTE_COUNT']) and r['REPLAY_PAGE_COUNT']==606
  if not strict:raise RuntimeError('HISTORICAL_SEMANTIC_REPLAY_FAILED')
  bind={'runtime_type':'historical_local','runtime_root':str(BIN),'baseline_version':'25.02.0','active_version':'25.02.0','pdfinfo':str(PDFINFO),'pdftotext':str(PDFTOTEXT),'pdftoppm':str(PDFTOPPM),'pdftocairo':str(PDFTOCAIRO),'tool_versions':{k:vs[k][0] for k in vs},'historical_provenance_reference':'catalog/scale/g8_poppler_historical_provenance.json','reference_validation':{'identities':17,'pages':606,'page_hash_matches':606,'body_hash_matches':17},'validation_status':'PASS'};BIND.write_text(json.dumps(bind,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');r.update({'STATUS':'PASS','POPPLER_RUNTIME_BINDING_PREPARED':1,'POPPLER_RUNTIME_BINDING_VALIDATED':1,'ACTIVE_POPPLER_VERSION':'25.02.0','Q3_PILOT_RUNNER_RUNTIME_GATE_UPDATED':int('g8_q3_poppler_runtime_binding.json' in (ROOT/'tools/72_g8_q3_contract_pilot_resume.py').read_text(encoding='utf-8')),'BLOCKER':'NONE','NEXT':'G8-Q3-CONTRACT-PILOT-RESUME'})
 except Exception as e:r.update({'BLOCKER':str(e),'NEXT':'RESOLVE_POPPLER_BINDING_OR_REPLAY_BLOCKER'})
 r['MISMATCH_PAPER_IDS']=','.join(sorted(mp));r['MISMATCH_PAGE_IDS']=','.join(mi);wc(OUTR,rr);wc(OUTP,pr);wc(OUTB,br);RESULT.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');REPORT.parent.mkdir(parents=True,exist_ok=True);REPORT.write_text('# G8 Q3 Poppler Local Bind and Validate\n\n'+'\n'.join(f'{k}={v}' for k,v in r.items())+'\n',encoding='utf-8');print('\n'.join(f'{k}={v}' for k,v in r.items()));print(f'OUTPUTS={BIND}; {OUTR}; {OUTP}; {OUTB}; {RESULT}; {REPORT}');return 0 if r['STATUS']=='PASS' else 2
if __name__=='__main__':sys.exit(main())
