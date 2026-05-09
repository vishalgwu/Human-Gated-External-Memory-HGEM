# HGEM Step 2 Audit Report

Date: 2026-05-09

This report records the technical audit performed before moving toward Step 3. It separates what has been verified by code from what still requires a qualified human reviewer.

## Audit Commands

Run these from the repository root:

```powershell
.\HGEM\Scripts\python.exe 02_DATASETS\prepare_step2.py --download-date 2026-05-09
.\HGEM\Scripts\python.exe 02_DATASETS\audit_step2.py
.\HGEM\Scripts\python.exe -m ruff check 02_DATASETS\prepare_step2.py 02_DATASETS\audit_step2.py
```

## Technical Verdict

The local Step 2 dataset artifacts pass the technical audit.

Verified:

- Raw GSM8K files exist and include `train.jsonl` and `test.jsonl`.
- Raw MATH files exist and include subject-level train/test parquet files.
- Raw SciBench files exist and include `dataset/original/*.json` files.
- Processed records use the required standard schema.
- Pilot split contains 10 problems per benchmark.
- Main split contains 40 problems per benchmark.
- Pilot, main, and holdout problem IDs have zero overlap.
- Selected SciBench pilot/main records all have worked solution text.
- Starter constraint files exist for all pilot and main selected records.
- Draft adversarial false-claim banks contain 50 claims per benchmark.
- Draft adversarial claims cross-reference selected pilot/main constraints.

## Current Counts

Processed records:

- GSM8K: 8,792
- MATH Dataset: 12,500
- SciBench: 691

Split counts:

- Pilot: 30 total, 10 per benchmark
- Main: 120 total, 40 per benchmark
- Holdout: 21,833 total

Constraint files:

- GSM8K: 50
- MATH Dataset: 50
- SciBench: 50

Adversarial draft claims:

- GSM8K: 50
- MATH Dataset: 50
- SciBench: 50

## Important SciBench Correction

The first pipeline pass selected SciBench records from the full problem files, but most full problem records do not include worked solution text. That would have made constraint review fragile.

The corrected pipeline now selects SciBench pilot/main records only from records with worked solution text. The remaining unsolved SciBench records stay in holdout/reference data and are not selected for pilot or main experiment use.

## MATH Constraint Decision

Decision for Step 2: use expert-reviewed official MATH solution steps as the primary HGEM constraint source.

Reason:

- The current MATH payload has official problem text, solution text, subject, level, and final answer data.
- PRM800K is useful, but its labels are step-level correctness labels on model-generated solutions, not direct finalized constraints for the official solution path.
- OpenAI's PRM800K README also notes a nonstandard MATH split, so automatic merging would need careful matching and review.

PRM800K can be used later as a secondary validation/reference source, but it should not replace human review of the selected HGEM constraint files unless exact problem/step alignment is implemented and verified.

Reference: https://github.com/openai/prm800k

## What Is Still Not Scientifically Complete

The following cannot be honestly marked complete by code alone:

- Qualified subject-matter review of every pilot constraint file.
- Qualified subject-matter review of every main-set constraint file.
- Research lead spot-check of at least 10 finalized constraint sets.
- Final approval of adversarial false claims.

The local JSON files contain the needed metadata fields (`reviewed_by`, `reviewed_at`, `confidence`, `review_status`), but they intentionally remain marked as requiring review until a qualified human reviewer signs off.

## Step 3 Gate

Do not begin Step 3 condition/system verification until:

- every pilot constraint file has `review_status = finalized`;
- every pilot constraint file has non-empty `reviewed_by` and `reviewed_at`;
- the research lead has spot-checked at least 10 finalized constraint sets;
- the adversarial claim banks have been reviewed and approved for plausibility.
