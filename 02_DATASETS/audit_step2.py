"""Audit HGEM Step 2 local dataset artifacts.

This script checks raw download presence, processed schema integrity,
split separation, selected SciBench solution availability, constraint
metadata, and adversarial draft cross-references.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = REPO_ROOT / "02_DATASETS"

REQUIRED_FIELDS = {
    "problem_id",
    "benchmark",
    "problem_text",
    "solution_text",
    "constraints",
    "final_answer",
    "difficulty",
    "subject",
}


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def fail(message: str) -> None:
    raise SystemExit(f"STEP 2 AUDIT FAILED: {message}")


def audit_raw() -> dict:
    checks = {}
    raw_expectations = {
        "gsm8k": DATA_ROOT / "raw" / "gsm8k",
        "math_dataset": DATA_ROOT / "raw" / "math_dataset",
        "scibench": DATA_ROOT / "raw" / "scibench",
    }
    for name, path in raw_expectations.items():
        if not path.exists():
            fail(f"Missing raw directory: {path}")
        files = [p for p in path.rglob("*") if p.is_file()]
        if not files:
            fail(f"Raw directory has no files: {path}")
        checks[name] = {"file_count": len(files), "bytes": sum(p.stat().st_size for p in files)}

    gsm_train = list((DATA_ROOT / "raw" / "gsm8k").rglob("train.jsonl"))
    gsm_test = list((DATA_ROOT / "raw" / "gsm8k").rglob("test.jsonl"))
    if not gsm_train or not gsm_test:
        fail("GSM8K raw train.jsonl/test.jsonl not found")

    math_parquet = list((DATA_ROOT / "raw" / "math_dataset").rglob("*.parquet"))
    if len(math_parquet) < 14:
        fail("MATH raw snapshot should contain subject train/test parquet files")

    scibench_original = list((DATA_ROOT / "raw" / "scibench").rglob("dataset/original/*.json"))
    if len(scibench_original) < 20:
        fail("SciBench raw original JSON files not found")
    return checks


def audit_processed() -> dict:
    processed_paths = {
        "gsm8k": DATA_ROOT / "processed" / "gsm8k_processed" / "all.json",
        "math_dataset": DATA_ROOT / "processed" / "math_dataset_processed" / "all.json",
        "scibench": DATA_ROOT / "processed" / "scibench_processed" / "all.json",
    }
    summary = {}
    all_ids = set()
    for name, path in processed_paths.items():
        data = load_json(path)
        if not data:
            fail(f"No processed records in {path}")
        bad_schema = [r.get("problem_id", "<missing>") for r in data if not REQUIRED_FIELDS <= set(r)]
        if bad_schema:
            fail(f"Processed schema missing fields in {path}: {bad_schema[:5]}")
        ids = [r["problem_id"] for r in data]
        duplicate_ids = [pid for pid, count in Counter(ids).items() if count > 1]
        if duplicate_ids:
            fail(f"Duplicate processed problem IDs in {path}: {duplicate_ids[:5]}")
        all_ids.update(ids)
        summary[name] = {
            "count": len(data),
            "missing_solution_text": sum(1 for r in data if not r["solution_text"]),
            "missing_constraints": sum(1 for r in data if not r["constraints"]),
            "missing_final_answer": sum(1 for r in data if not r["final_answer"]),
            "subject_counts": dict(Counter(r["subject"] for r in data)),
        }
    summary["total_unique_ids"] = len(all_ids)
    return summary


def audit_splits() -> dict:
    split_paths = {
        "pilot": DATA_ROOT / "splits" / "pilot_set" / "all_pilot.json",
        "main": DATA_ROOT / "splits" / "main_set" / "all_main.json",
        "holdout": DATA_ROOT / "splits" / "holdout_set" / "all_holdout.json",
    }
    splits = {name: load_json(path) for name, path in split_paths.items()}
    expected_counts = {"pilot": 30, "main": 120}
    for name, expected in expected_counts.items():
        if len(splits[name]) != expected:
            fail(f"{name} split count is {len(splits[name])}, expected {expected}")

    ids = {name: {r["problem_id"] for r in rows} for name, rows in splits.items()}
    for left in ids:
        for right in ids:
            if left >= right:
                continue
            overlap = ids[left] & ids[right]
            if overlap:
                fail(f"Split overlap {left}/{right}: {sorted(overlap)[:5]}")

    per_benchmark = {}
    for name in ["pilot", "main"]:
        expected_each = 10 if name == "pilot" else 40
        counts = Counter(r["benchmark"] for r in splits[name])
        if counts != {"GSM8K": expected_each, "MATH": expected_each, "SCIBENCH": expected_each}:
            fail(f"Unexpected {name} benchmark counts: {counts}")
        per_benchmark[name] = dict(counts)

    selected_scibench_without_solution = [
        r["problem_id"]
        for r in splits["pilot"] + splits["main"]
        if r["benchmark"] == "SCIBENCH" and not r["solution_text"]
    ]
    if selected_scibench_without_solution:
        fail(f"Selected SciBench records without solution text: {selected_scibench_without_solution[:5]}")

    return {
        "counts": {name: len(rows) for name, rows in splits.items()},
        "benchmark_counts": per_benchmark,
        "selected_scibench_without_solution": 0,
    }


def audit_constraints() -> dict:
    constraints = list((DATA_ROOT / "constraints").rglob("*_constraints.json"))
    if len(constraints) != 150:
        fail(f"Expected 150 starter constraint files, found {len(constraints)}")

    summary = Counter()
    missing_metadata = []
    empty_constraints = []
    for path in constraints:
        data = load_json(path)
        summary[data.get("benchmark", "UNKNOWN")] += 1
        for key in ["problem_id", "benchmark", "constraints", "reviewed_by", "reviewed_at", "confidence", "review_status"]:
            if key not in data:
                missing_metadata.append(path.name)
                break
        if not data.get("constraints"):
            empty_constraints.append(path.name)
    if missing_metadata:
        fail(f"Constraint files missing metadata: {missing_metadata[:5]}")
    if empty_constraints:
        fail(f"Constraint files with empty constraints: {empty_constraints[:5]}")
    return dict(summary)


def audit_adversarial() -> dict:
    output = {}
    for rel in [
        "gsm8k_false_claims.json",
        "math_dataset_false_claims.json",
        "scibench_false_claims.json",
    ]:
        path = DATA_ROOT / "adversarial" / rel
        data = load_json(path)
        claims = data.get("claims", [])
        if len(claims) != 50:
            fail(f"{path} has {len(claims)} claims, expected 50")
        for claim in claims:
            for key in ["claim_id", "claim_text", "targets_constraint", "target_problem_id", "review_status"]:
                if not claim.get(key):
                    fail(f"Adversarial claim missing {key}: {claim}")
            if claim.get("review_status") != "needs_researcher_review":
                fail(f"Draft claim should remain needs_researcher_review: {claim['claim_id']}")
        output[rel] = {"claim_count": len(claims), "target_count": data.get("target_count")}
    return output


def main() -> None:
    report = {
        "raw": audit_raw(),
        "processed": audit_processed(),
        "splits": audit_splits(),
        "constraints": audit_constraints(),
        "adversarial": audit_adversarial(),
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
