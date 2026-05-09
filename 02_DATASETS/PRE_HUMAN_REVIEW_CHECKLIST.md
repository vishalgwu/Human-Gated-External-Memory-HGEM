# HGEM Pre-Human-Review Checklist

Date: 2026-05-09

This checklist records the project state immediately before qualified human review of Step 2 constraints and adversarial claims.

## Technical Readiness

- [x] Raw GSM8K download exists locally under `02_DATASETS/raw/gsm8k/`.
- [x] Raw MATH Dataset snapshot exists locally under `02_DATASETS/raw/math_dataset/`.
- [x] Raw SciBench download exists locally under `02_DATASETS/raw/scibench/`.
- [x] Processed JSON schema exists for all three benchmarks.
- [x] Fixed split seed is recorded as `20260509`.
- [x] Pilot split contains 30 total problems: 10 GSM8K, 10 MATH, and 10 SciBench.
- [x] Main split contains 120 total problems: 40 GSM8K, 40 MATH, and 40 SciBench.
- [x] Holdout split contains the remaining 21,833 records.
- [x] Pilot, main, and holdout problem IDs have zero overlap.
- [x] SciBench pilot/main records all include worked solution text.
- [x] Starter constraint JSON files exist for all 150 pilot/main selected problems.
- [x] Draft adversarial false-claim banks contain 50 claims per benchmark.
- [x] Draft adversarial false claims cross-reference selected pilot/main constraints.
- [x] Local review web tool exists under `02_DATASETS/review_tool/`.
- [x] Review web tool can load, cross-check, edit, and save constraint JSON files locally.
- [x] Generated raw/processed/split/constraint/adversarial artifacts remain git-ignored.
- [x] `01_SETUP/credentials/.env` remains git-ignored and must not be committed.

## Pilot Review Load

These are the files/items a human reviewer must inspect before Step 3:

- GSM8K pilot: 10 files, 41 constraint items.
- MATH pilot: 10 files, 32 constraint items.
- SciBench pilot: 10 files, 17 constraint items.
- Total pilot review load: 30 files, 90 constraint items.

## Remaining Human Work

- [ ] Review every pilot constraint file before Step 3.
- [ ] Add `reviewed_by`, `reviewed_at`, `confidence`, and final `review_status` to every reviewed file.
- [ ] Use expert-reviewed official MATH solution steps as the primary MATH constraint source.
- [ ] Review and approve or rewrite draft adversarial false claims.
- [ ] Confirm each approved false claim targets a finalized constraint.
- [ ] Have the research lead spot-check at least 10 finalized constraint sets.
- [ ] Review and finalize all main-set constraints before main experiment use.

## Verification Commands

Run these from the repository root:

```powershell
.\HGEM\Scripts\python.exe 02_DATASETS\audit_step2.py
.\HGEM\Scripts\python.exe -m ruff check 02_DATASETS\prepare_step2.py 02_DATASETS\audit_step2.py 02_DATASETS\review_tool\app.py
.\HGEM\Scripts\python.exe -m compileall 02_DATASETS
```

Run the local review page:

```powershell
.\HGEM\Scripts\python.exe 02_DATASETS\review_tool\app.py
```

Then open:

```text
http://127.0.0.1:8765
```
