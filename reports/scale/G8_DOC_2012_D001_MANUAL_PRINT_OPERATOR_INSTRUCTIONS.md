# G8 DOC Manual Print-to-PDF Operator Instructions

1. Run the preflight command below. Proceed only if `PREFLIGHT_PASS=1`.
2. In a normal Windows desktop session, open `D:\cumcm-modeling-Award-Collection\tmp\g8_doc_2012_d001_docx_intermediate\CUMCM-2012-D-001\source_rebuilt.docx` in Microsoft Word.
3. Do not edit or save the document. Use **File → Print**, choose **Microsoft Print to PDF**, select **Print All Pages**, and retain **1 Page Per Sheet** with the document's existing paper, orientation, margins, and default page settings.
4. Do not enable Print Markup, scaling, custom page ranges, or multiple pages per sheet. If preview is visibly abnormal, cancel and stop.
5. Click Print once only. In the Windows save dialog enter exactly: `D:\cumcm-modeling-Award-Collection\tmp\g8_doc_2012_d001_manual_print_to_pdf\CUMCM-2012-D-001\manual_print_candidate.pdf`. If overwrite is offered, cancel and stop.
6. Close Word and choose **Don't Save** if prompted.
7. Run the postflight command. Do not print again, even if it reports failure.

```powershell
Set-Location 'D:\cumcm-modeling-Award-Collection'
powershell.exe -NoProfile -ExecutionPolicy Bypass -File '.\tools\62_g8_doc_2012_d001_manual_print_preflight.ps1'
python '.\tools\62_g8_doc_2012_d001_manual_print_postflight.py'
```
