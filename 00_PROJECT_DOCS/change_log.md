# HGEM Change Log

Project: Human-Gated External Memory (HGEM)

## 2026-05-03

- Created master project folder structure from `HGEM_Execution_Workflow_v1.docx`.
- Added Step 1 environment setup templates.
- Created setup plan for Python virtual environment `HGEM`.
- Created local ignored `.env` file from `.env.template`.
- Expanded `.gitignore` for HGEM local secrets, virtual environment, datasets, logs, generated experiment outputs, and ChromaDB local store.
- Installed PostgreSQL 15, Neo4j 5, and Redis 7 as Docker services.
- Verified PostgreSQL schema, Neo4j constraints, Redis ping, and ChromaDB local client.
- Confirmed local ignored `.env` contains an OpenAI API key and verified OpenAI authentication through the models endpoint.

## 2026-05-09

- Read the Step 2 instructions from the project docs and added `02_DATASETS/STEP_2_WORKFLOW.md`.
- Added `02_DATASETS/prepare_step2.py` to reproduce dataset download, normalization, fixed-seed splitting, and starter constraint generation.
- Downloaded local raw snapshots for GSM8K, MATH, and SciBench into git-ignored `02_DATASETS/raw/` folders.
- Converted GSM8K, MATH, and SciBench into the standard processed JSON schema under git-ignored `02_DATASETS/processed/`.
- Created fixed-seed splits with seed `20260509`: 10 pilot problems per benchmark, 40 main problems per benchmark, and all remaining records as holdout.
- Generated starter constraint files for pilot and main selected problems only; all are marked `needs_subject_matter_review`.
- Created empty adversarial false-claim bank skeletons; claims are intentionally not auto-filled because the project docs require researcher-written plausible false claims.
- Recorded source revisions, local file sizes, processed counts, split counts, and remaining review blockers in `02_DATASETS/step2_manifest.json`.
