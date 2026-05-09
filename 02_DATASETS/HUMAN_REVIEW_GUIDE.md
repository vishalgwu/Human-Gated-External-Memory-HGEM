# Beginner Guide: Finishing HGEM Step 2 Review

This guide explains the remaining human review work in plain language.

The scripts have prepared the data. A human reviewer now needs to confirm that the constraints and adversarial claims are scientifically valid.

For the verified pre-review project state, also read `02_DATASETS/PRE_HUMAN_REVIEW_CHECKLIST.md`.

## Why This Matters

HGEM measures drift by checking whether model reasoning violates a problem's constraint set.

If a constraint is wrong, vague, or missing, then the RDI and CVR scores will be wrong. This can invalidate the experiment.

## Files To Review

Pilot constraint files:

- `02_DATASETS/constraints/gsm8k_constraints/`
- `02_DATASETS/constraints/math_dataset_constraints/`
- `02_DATASETS/constraints/scibench_constraints/`

Adversarial claim files:

- `02_DATASETS/adversarial/gsm8k_false_claims.json`
- `02_DATASETS/adversarial/math_dataset_false_claims.json`
- `02_DATASETS/adversarial/scibench_false_claims.json`

These files are git-ignored because they are generated research artifacts. They exist locally after running `prepare_step2.py`.

## Easier Review Option: Local Web Tool

A local HTML review page is available at:

```text
02_DATASETS/review_tool/index.html
```

Start it from the repository root:

```powershell
.\HGEM\Scripts\python.exe 02_DATASETS\review_tool\app.py
```

Then open:

```text
http://127.0.0.1:8765
```

Use this page to load pilot or main constraint files, compare each file against the matching split problem and solution, edit the constraint list, add reviewer metadata, set confidence, set review status, and save the JSON back to the same local constraint folder.

## How To Review One Constraint File

1. Open one `*_constraints.json` file.
2. Read `problem_id` and `benchmark`.
3. Find the same `problem_id` in the matching split file:
   - `02_DATASETS/splits/pilot_set/all_pilot.json`
   - `02_DATASETS/splits/main_set/all_main.json`
4. Read the problem text and solution text.
5. Check every item in `constraints`.
6. Ask: "If the model violates this item, would the solution become wrong or drift away from the verified reasoning?"
7. Remove constraints that are not necessary.
8. Add missing constraints that are necessary.
9. For SciBench, name the physical law explicitly when possible.

Good SciBench example:

```text
Newton 2nd Law: F = ma
```

Weak SciBench example:

```text
F = ma
```

The weak example lacks the named law and is less useful for conflict detection.

## How To Mark A Constraint File Final

Only do this after reviewing the file carefully.

Change:

```json
"reviewed_by": null,
"reviewed_at": null,
"confidence": "unreviewed",
"review_status": "needs_subject_matter_review"
```

To:

```json
"reviewed_by": "reviewer_id_or_name",
"reviewed_at": "2026-05-09",
"confidence": "high",
"review_status": "finalized"
```

Use `confidence = "medium"` if the constraint is probably valid but should be revisited.

Do not use `confidence = "high"` unless you would be comfortable using the constraint as ground truth in the paper.

## Review Rules By Benchmark

GSM8K:

- Check arithmetic equations.
- Confirm the final answer is correct.
- Prefer one constraint per necessary arithmetic step.

MATH:

- Check algebra, proof, or derivation steps.
- The project decision is to use expert-reviewed official solution steps as the primary constraint source.
- PRM800K can be used later as a secondary reference, but do not auto-import PRM labels without exact alignment.

SciBench:

- Check physical laws, constants, units, and derived equations.
- Name laws explicitly.
- If a solution step depends on a law, include the law and the derived equation.

## How To Review Adversarial Claims

Open each false-claim bank and inspect every claim.

A valid adversarial claim must be:

- plausible;
- specific;
- wrong;
- linked to one exact target constraint;
- natural enough to appear in conversation.

Bad claim:

```text
The answer is 999.
```

Better claim:

```text
I think we used 110 for that subtotal, not 100.
```

The better claim targets a specific prior arithmetic result and sounds like a plausible memory error.

## Research Lead Spot Check

After reviewers finalize the files:

1. Randomly choose at least 10 finalized constraint files.
2. Re-check them against the source problem and solution.
3. Record any corrections.
4. If more than 3 of 10 have serious issues, pause Step 3 and review the full constraint process.

## Final Step 2 Checklist

Before Step 3, confirm:

- all 30 pilot constraint files are finalized;
- all 120 main constraint files are finalized before main experiment use;
- every finalized file has reviewer metadata;
- every SciBench finalized file names physical laws where possible;
- every adversarial claim is approved or rewritten;
- at least 10 finalized constraint sets are spot-checked by the research lead;
- `audit_step2.py` passes.
