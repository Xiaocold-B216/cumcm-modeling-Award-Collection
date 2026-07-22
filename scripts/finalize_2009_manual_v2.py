#!/usr/bin/env python3
from pathlib import Path

source = Path(__file__).with_name("finalize_2009_manual.py")
text = source.read_text(encoding="utf-8")
insert = '''    ("2009C：卫星和飞船的跟踪测控模型.pdf", "dff5ff5a382813fe9b15e55fc9b5f1756872b7d61f16378b576ce763ebe6d867", 11, "award_paper", "solution_paper", "C", "scanned_solution"),
    ("2009C：卫星和飞船的跟踪测控 (2).pdf", "dc2e5948119ebd38e43cbcaa23e9169d4c218ea34129f5a5a459875b71275c5f", 17, "award_paper", "solution_paper", "C", "none"),
    ("2009C：卫星和飞船的跟踪测控.pdf", "3d1d1c7dd22ce32c427c9d8446f36cdb9791113c8b8ec7b3c9ce847a17dab09b", 18, "award_paper", "solution_paper", "C", "none"),
    ("2009D：会议筹备的优化方案.pdf", "07902d575163c83148dbbe3c4066f249f401945aaddc9b6e8d1fd1aec52a89d5", 16, "award_paper", "solution_paper", "D", "none"),
    ("2009D：会议筹备方案的优化设计模型.pdf", "cdad73c32b35b9553c785ff7d0b3179cbcfd545a584b24a43a85916d0fc86ef5", 21, "award_paper", "solution_paper", "D", "none"),
    ("2009D：会议筹备优化方案.pdf", "2d6d5edb040baa995c172e3cebf7ca2de80c8c8e12b9cb3646bf68ed674ae864", 15, "award_paper", "solution_paper", "D", "none"),
    ("2009D：会议筹备优化模型.pdf", "7b84c9546d60db3aa68edd490b7a5ea3f133c3252063338e7cc541bff4434f57", 18, "award_paper", "solution_paper", "D", "none"),
'''
marker = '    ("2009年国赛A题data.xls", "e3bdc80d72f54cc90f24d4a83f255191dc92aef9ef246fbdaf69e5bb0f3e3a30", None, "other_related", "supporting_object", "A", "official_data"),\n]'
if marker not in text:
    raise RuntimeError("2009 EXPECTED insertion target not found")
text = text.replace(marker, marker[:-2] + insert + "]", 1)
replacements = {
    'if len(sources) != 20: raise RuntimeError("expected 20 audited carriers")': 'if len(sources) != 27: raise RuntimeError("expected 27 audited carriers")',
    'if total_pages != 277: raise RuntimeError(f"expected 277 PDF pages, got {total_pages}")': 'if total_pages != 393: raise RuntimeError(f"expected 393 PDF pages, got {total_pages}")',
    '"pdf_count":15,"page_count":total_pages': '"pdf_count":22,"page_count":total_pages',
    'len(carriers)==20': 'len(carriers)==27',
    'sum(c["carrier_type"]=="pdf" for c in carriers)==15': 'sum(c["carrier_type"]=="pdf" for c in carriers)==22',
    'total_pages==277': 'total_pages==393',
    'kinds["solution_paper"]==14': 'kinds["solution_paper"]==21',
    'len(lineages)==14': 'len(lineages)==21',
    'len(reps)==20': 'len(reps)==27',
    '15个PDF的277页': '22个PDF的393页',
}
for old, new in replacements.items():
    if old not in text:
        raise RuntimeError(f"2009 patch target not found: {old}")
    text = text.replace(old, new)
namespace = {"__name__": "__main__", "__file__": str(source)}
exec(compile(text, str(source), "exec"), namespace)
