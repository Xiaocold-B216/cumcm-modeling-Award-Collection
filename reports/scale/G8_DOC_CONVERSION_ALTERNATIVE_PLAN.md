# G8 DOC Conversion Alternative Plan

Stage: `G8-DOC-CONVERSION-ALTERNATIVE-PLAN`

Status: `PASS`

## Baseline and source integrity

- DOC targets: 18 unique; duplicate IDs: 0; unknown identities: 0.
- Missing sources: 0; source SHA/size mismatches: 0; OLE format drift: 0.
- Eligibility remains resolved and unchanged. DOC backlog remains 18; Q3 backlog remains 128.

## Capability discovery

- Microsoft Word executable and Wordconv.exe are installed at the existing Office location, version `16.0.20228.20190`.
- Current Word COM blocker remains `0x80070520 LOGIN_SESSION_NOT_FOUND`; this stage performed no COM retry and created no Word instance.
- antiword, catdoc, wvText, wvWare, LibreOffice, relevant Python DOC modules, and project Node parser modules are absent.
- Existing project utilities provide OLE/signature inventory and PDF extraction contracts, but no binary-DOC body extractor.
- Office filter DLLs exist but are not a governed standalone extractor with page/provenance fidelity.

## Strategy decision

- Autonomous local DOC path: `NO_AUTONOMOUS_LOCAL_DOC_PATH=1`.
- Recommended strategy: rank 3, `C_INTERACTIVE_MICROSOFT_WORD_PILOT`.
- Feasibility is conditional: a user must run the existing 3-sample controlled pilot from a normal Windows desktop login session. This stage does not trigger that action.
- New tooling remains a user-authorized fallback only; nothing was installed or downloaded.

## Protection and closure

- DOC conversion, read-only probe, batch extraction, and formal Artifact generation: 0.
- Existing 308 Artifact Sets and 924 primary Artifacts were hash-checked with drift 0.
- Image, Q3, Eligibility, G3, frozen Pilot outputs, originals, system configuration, and network state were unchanged.

Next: `G8-DOC-INTERACTIVE-WORD-PILOT`.
