# G8 Q3 Runner Durability Closure

STATUS=PASS
STAGE=G8-Q3-CONTRACT-REFINEMENT-DURABILITY-EVIDENCE-CLOSURE

The previous refinement result was stale: it reported that attempt
checkpoints and the always-current result were still missing. The runner now
creates a unique attempt identifier and atomically persists attempt state and
the current result at phase boundaries, including blocked and timeout paths.

Child processes use one bounded wrapper with UTF-8 transport, a 180-second
timeout, bounded stderr capture, and no automatic retry. A timeout produces a
`CHILD_PROCESS_TIMEOUT` blocker. The wrapper records the diagnostic row before
returning, including success and timeout cleanup fields. The durable CSV uses
the exact frozen schema and global monotonic sequence numbers per audit file;
invalid existing state blocks as `CHILD_PROCESS_AUDIT_STATE_INVALID`, while a
deterministic write failure blocks as
`CHILD_PROCESS_AUDIT_PERSISTENCE_FAILURE`.

The implementation check executed a temp-only synthetic suite. It wrote three
rows for one attempt with statuses SUCCESS, FAILED, and TIMED_OUT; reopened the
file and appended the fourth row for the same attempt; then verified a fifth
row for a second attempt without loss or header duplication. It also exercised
schema rejection and a non-directory parent failure. All synthetic checks
passed and temporary fixtures were removed.

The metadata-only preflight and implementation-check remain side-effect free
with respect to formal Pilot evidence: no real attempt, inventory, selection,
render, OCR, batch, formal artifact, network, dependency, Word, or Git action
was run. This report does not assert completion of the Q3 Pilot.

REFINEMENT_CONTRACT_UPDATED=1
REFINEMENT_CONTRACT_SHA256=CAED643919AD35E2CD67938E116AE5BCA008C9FB05CC243E28DE2930A38723DB
REFINEMENT_EVIDENCE_FINGERPRINT=3235CCCE44CC467414DE6C4344B1A4C220342E2DCF6A18A2B19235E794D97AC1
DURABILITY_EVIDENCE_UPDATED=1
REFINEMENT_RESULT_UPDATED=1
REFINEMENT_REPORT_UPDATED=1
FORMAL_CHILD_PROCESS_AUDIT_EXISTS=0
PRECHECK_FORMAL_PILOT_EVIDENCE_MUTATION_COUNT=0
IMPLEMENTATION_CHECK_FORMAL_EVIDENCE_MUTATION_COUNT=0

NEXT=G8-Q3-CONTRACT-PILOT-RESUME
