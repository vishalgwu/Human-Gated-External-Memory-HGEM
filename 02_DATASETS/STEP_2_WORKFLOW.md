# HGEM Step 2 Workflow

Status: technical audit passed locally; scientific human review remains

This workflow is based on the project documents in `docs/`, especially `HGEM_Execution_Workflow_v1.docx` and `CHAT_2_DATA_AND_SYSTEM.md`.

## Scope

Step 2 prepares the three benchmark datasets used by HGEM:

- GSM8K
- MATH Dataset
- SciBench

The raw data folders are local-only and git-ignored. Tracked files should contain workflow, provenance, and reproducibility metadata, not the large/generated datasets themselves.

## Workflow

1. Download raw data into `02_DATASETS/raw/`.
   - GSM8K: official OpenAI GitHub repository snapshot.
   - MATH: official Hendrycks project repository plus the Hugging Face dataset snapshot preserving subject/split folders.
   - SciBench: official GitHub repository snapshot.
2. Treat `02_DATASETS/raw/` as read-only after download.
3. Convert every problem to the standard processed JSON schema:
   - `problem_id`
   - `benchmark`
   - `problem_text`
   - `solution_text`
   - `constraints`
   - `final_answer`
   - `difficulty`
   - `subject`
4. Write processed benchmark JSON files under `02_DATASETS/processed/`.
5. Use fixed split seed `20260509`.
6. Create split files:
   - pilot: 10 problems per benchmark
   - main: 40 problems per benchmark
   - holdout: all remaining problems
7. Generate starter constraint files for pilot and main problems.
   - These files are not scientifically validated yet.
   - Every generated file must remain marked `needs_subject_matter_review` until a qualified reviewer checks it.
   - Review can be done with the local web tool in `02_DATASETS/review_tool/`.
8. Create adversarial false-claim bank skeletons.
   - Claims should be written and reviewed by a researcher, not auto-filled as final data.
9. Record source URLs, revisions, download date, file sizes, and problem counts in `02_DATASETS/step2_manifest.json` and `01_SETUP/environment/versions.txt`.

## Current Outputs

The Step 2 pipeline was run on 2026-05-09 with split seed `20260509`.

Processed problem counts:

- GSM8K: 8,792
- MATH Dataset: 12,500
- SciBench: 691

Split counts:

- Pilot: 10 per benchmark, 30 total
- Main: 40 per benchmark, 120 total
- Holdout: 21,833 total

Starter constraint files:

- GSM8K: 50
- MATH Dataset: 50
- SciBench: 50

The generated raw, processed, split, constraint, and adversarial files are ignored by Git. The reproducible script and manifest are tracked.

Correction made during audit:

- SciBench pilot/main selection now uses only records with worked solution text.
- SciBench records without worked solutions remain in holdout/reference data.
- Draft adversarial false claims now contain 50 cross-referenced claims per benchmark, but they still require researcher review.

## Remaining Step 2 Work

- Review and finalize every pilot constraint file before Step 3.
- Review and finalize all main-set constraint files before main experiment use.
- Add reviewer metadata: `reviewed_by`, `reviewed_at`, and confidence.
- Use expert-reviewed official MATH solution steps as the primary constraint path; Lightman/PRM800K annotations remain optional secondary references unless exact alignment is implemented and reviewed.
- Review, rewrite where needed, and approve 50 draft adversarial false claims per benchmark.
- Confirm each false claim targets a finalized constraint.
- Have the research lead spot-check at least 10 finalized constraint sets.

## Local Constraint Review Tool

Run:

```powershell
.\HGEM\Scripts\python.exe 02_DATASETS\review_tool\app.py
```

Then open:

```text
http://127.0.0.1:8765
```

The tool lists pilot, main, or all generated constraint JSON files; cross-checks the selected file against the matching split problem and solution; shows linked draft adversarial claims; lets a reviewer edit constraints and metadata; and saves the JSON back into the original local constraint folder.

## Scientific Cautions

- Raw files must not be edited in place.
- Auto-extracted constraints are only a starting pass.
- GSM8K constraints can be seeded from calculator annotations and final answers.
- MATH constraints use expert-reviewed official solution steps before use in RDI; PRM800K remains an optional secondary reference only after exact alignment is implemented and reviewed.
- SciBench constraints require explicit physical-law naming by a physics/chemistry reviewer.
- Holdout data should not be used until after submission or an explicit replication/reviewer challenge.
