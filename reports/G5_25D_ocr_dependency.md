# G5-25D OCR Language-Data Dependency Provisioning & Smoke-Test Gate

STAGE=G5-25D
STATUS=PASS
BRANCH=library-refactor-v1
HEAD=a042ecf898feaba6fc81d543a10e0188db8b2b12
PYTHON_EXECUTABLE=D:\python\python.exe
PYTHON_VERSION=3.13.15
OCR_ENGINE=tesseract.js
OCR_ENGINE_VERSION=7.0.0
PDF_BACKEND=Poppler/pdfinfo
PDF_BACKEND_VERSION=26.05.0
PDF_INSPECTOR_RUN=0
PDF_INSPECTOR_MODIFIED=0
POPPLER_MODIFIED=0
OCR_REQUIRED_LANGUAGES=chi_sim+eng
TESSERACT_LANG_LOADING_MODE=explicit local filesystem traineddata.gz via langPath; gzip=true; cacheMethod=none
TESSERACT_LANG_PATH_MODE=local directory
TRAINEDDATA_FILES_REQUIRED=2
TRAINEDDATA_FILES_PRESENT=2
TRAINEDDATA_SHA256_VERIFIED=1
TRAINEDDATA_SOURCE=jsDelivr npm package @tesseract.js-data
TRAINEDDATA_SOURCE_REVISION=4.0.0_best_int
TRAINEDDATA_LOCAL_PATH=.bootstrap/ocr/tesseract-data
RUNTIME_NETWORK_REQUIRED_FOR_LANG_DATA=0
OCR_WORKER_CREATE_SUCCESS=1
LANGUAGE_MODEL_LOAD_SUCCESS=1
OCR_SMOKE_TEST_RUN=1
OCR_SMOKE_RECOGNITION_SUCCESS=1
OCR_SMOKE_TEXT_CHARS=1907
OCR_SMOKE_TEXT_SHA256=8618C3D959AA466EEF9AE4994A21BBBCC09E282F52C9C4E8C201577664314CBA
FORMAL_OCR_RUN=0
Q2_REPAIR_ATTEMPTED=0
Q2_REPAIR_SUCCEEDED=0
OCR_OUTPUT_FILES=0
REPAIR_MANIFEST_ENTRIES_ADDED=0
TRAINEDDATA_CACHE_REUSED=2
DUPLICATE_TRAINEDDATA_FILES=0
IDEMPOTENCY_PASS=1
G5_25_OCR_RUNNER_MODIFIED=1
SOURCE_SHA_MISMATCH=0
ORIGINAL_SHA_CHANGED_AFTER_G5_25D=0
G1_CATALOG_MODIFIED=0
G2_CATALOG_MODIFIED=0
G3_CATALOG_MODIFIED=0
G4_OUTPUT_MODIFIED=0
G5_00_QUALITY_CATALOG_MODIFIED=0
G5_00_ROUTING_CATALOG_MODIFIED=0
ORIGINAL_FILES_MODIFIED=0
ORIGINAL_FILES_DELETED=0
ORIGINAL_FILES_MOVED_OR_RENAMED=0
TEMP_SMOKE_ARTIFACTS_REMAINING=0

DEPENDENCY_SUMMARY=
- language: chi_sim
- local path: .bootstrap/ocr/tesseract-data/chi_sim.traineddata.gz
- source: https://cdn.jsdelivr.net/npm/@tesseract.js-data/chi_sim/4.0.0_best_int/chi_sim.traineddata.gz
- SHA256: B8A23F10C7DE500891EB458A8ADC9CC58AB7F242F08B7D149F5E9AEA4AD5DB7C
- size: 1718768 bytes
- language: eng
- local path: .bootstrap/ocr/tesseract-data/eng.traineddata.gz
- source: https://cdn.jsdelivr.net/npm/@tesseract.js-data/eng/4.0.0_best_int/eng.traineddata.gz
- SHA256: 45B4CB346724AC1774F1C36F42F182B887BCDB28EBE63E6FFF90AC41F3FCFF91
- size: 2952873 bytes

SMOKE_TEST_SUMMARY=
- One page from the frozen A066 Q2 PDF was rendered to a temporary PNG.
- Offline tesseract.js worker loaded chi_sim+eng from explicit local langPath and recognized 1907 characters.
- No readable.pdf and no repair manifest success entry were created.

VALIDATION=
- Frozen G5-25-OCR routing and source SHA were checked; no G4/G5-00 catalog was modified.
- Smoke temporary directory was removed; TEMP_SMOKE_ARTIFACTS_REMAINING=0.
- Second dependency check reused the two local models without downloading duplicates; IDEMPOTENCY_PASS=1.
- API_CHANGE=NONE; MIGRATION_OWNERSHIP=NONE.

ISSUES=NONE
BLOCKER=NONE
APPROVAL=OCR language-data dependency provisioned and offline smoke-tested
NEXT=rerun G5-25-OCR
