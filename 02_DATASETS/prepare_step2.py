"""Download and prepare HGEM Step 2 datasets.

The generated dataset artifacts live under git-ignored folders:
02_DATASETS/raw, processed, splits, constraints, and adversarial.

Tracked metadata is written to 02_DATASETS/step2_manifest.json.
"""

from __future__ import annotations

import argparse
import json
import random
import re
import shutil
import time
import urllib.request
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable
from zipfile import ZipFile


REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = REPO_ROOT / "02_DATASETS"

SPLIT_SEED = 20260509

GSM8K_SHA = "3101c7d5072418e28b9008a6636bde82a006892c"
MATH_HF_REPO = "EleutherAI/hendrycks_math"
MATH_HF_SHA = "21a5633873b6a120296cce3e2df9d5550074f4a3"
MATH_OFFICIAL_REPO_SHA = "985bdc1696e88e8643f081a0ff4719da39f2ae2a"
SCIBENCH_SHA = "e14e0ca3d3db0f02928a18d435b9c3d15656a7c5"

MATH_CONFIGS = [
    "algebra",
    "counting_and_probability",
    "geometry",
    "intermediate_algebra",
    "number_theory",
    "prealgebra",
    "precalculus",
]

SCIBENCH_SPLIT_FOCUS = {"class", "thermo"}


@dataclass(frozen=True)
class SourceSpec:
    name: str
    url: str
    revision: str
    raw_dir: Path


SOURCES = {
    "gsm8k": SourceSpec(
        name="GSM8K",
        url=f"https://github.com/openai/grade-school-math/archive/{GSM8K_SHA}.zip",
        revision=GSM8K_SHA,
        raw_dir=DATA_ROOT / "raw" / "gsm8k",
    ),
    "scibench": SourceSpec(
        name="SciBench",
        url=f"https://github.com/mandyyyyii/scibench/archive/{SCIBENCH_SHA}.zip",
        revision=SCIBENCH_SHA,
        raw_dir=DATA_ROOT / "raw" / "scibench",
    ),
}


def ensure_dirs() -> None:
    for path in [
        DATA_ROOT / "raw" / "gsm8k",
        DATA_ROOT / "raw" / "math_dataset",
        DATA_ROOT / "raw" / "scibench",
        DATA_ROOT / "processed" / "gsm8k_processed",
        DATA_ROOT / "processed" / "math_dataset_processed",
        DATA_ROOT / "processed" / "scibench_processed",
        DATA_ROOT / "splits" / "pilot_set",
        DATA_ROOT / "splits" / "main_set",
        DATA_ROOT / "splits" / "holdout_set",
        DATA_ROOT / "constraints" / "gsm8k_constraints",
        DATA_ROOT / "constraints" / "math_dataset_constraints",
        DATA_ROOT / "constraints" / "scibench_constraints",
        DATA_ROOT / "adversarial",
    ]:
        path.mkdir(parents=True, exist_ok=True)


def download_with_retries(url: str, destination: Path, retries: int = 4) -> None:
    if destination.exists() and destination.stat().st_size > 0:
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    temp = destination.with_suffix(destination.suffix + ".part")
    for attempt in range(1, retries + 1):
        try:
            with urllib.request.urlopen(url, timeout=120) as response:
                with temp.open("wb") as handle:
                    shutil.copyfileobj(response, handle)
            temp.replace(destination)
            return
        except Exception:
            if temp.exists():
                temp.unlink()
            if attempt == retries:
                raise
            time.sleep(2 * attempt)


def extract_zip_once(zip_path: Path, output_dir: Path) -> Path:
    marker = output_dir / ".extract_complete.json"
    if marker.exists():
        data = json.loads(marker.read_text(encoding="utf-8"))
        root = output_dir / data["root"]
        if root.exists():
            return root

    before = {p.name for p in output_dir.iterdir()} if output_dir.exists() else set()
    with ZipFile(zip_path) as archive:
        bad_member = archive.testzip()
        if bad_member:
            raise RuntimeError(f"Bad zip member in {zip_path}: {bad_member}")
        archive.extractall(output_dir)
    after = {p.name for p in output_dir.iterdir()}
    new_dirs = [output_dir / name for name in sorted(after - before) if (output_dir / name).is_dir()]
    if not new_dirs:
        raise RuntimeError(f"Could not identify extracted root for {zip_path}")
    root = new_dirs[0]
    marker.write_text(json.dumps({"root": root.name}, indent=2), encoding="utf-8")
    return root


def download_github_sources() -> dict:
    details = {}
    for key, source in SOURCES.items():
        zip_path = source.raw_dir / f"{key}_{source.revision[:12]}.zip"
        download_with_retries(source.url, zip_path)
        extracted_root = extract_zip_once(zip_path, source.raw_dir)
        details[key] = {
            "name": source.name,
            "source_url": source.url,
            "revision": source.revision,
            "zip_path": str(zip_path.relative_to(REPO_ROOT)),
            "extracted_root": str(extracted_root.relative_to(REPO_ROOT)),
        }
    return details


def copy_math_snapshot() -> dict:
    from huggingface_hub import snapshot_download

    raw_dir = DATA_ROOT / "raw" / "math_dataset"
    local_dir = raw_dir / "EleutherAI_hendrycks_math_snapshot"
    if not (local_dir / "README.md").exists():
        try:
            snapshot_download(
                repo_id=MATH_HF_REPO,
                repo_type="dataset",
                revision=MATH_HF_SHA,
                allow_patterns=["README.md", "**/*.parquet"],
                local_dir=str(local_dir),
                local_dir_use_symlinks=False,
            )
        except Exception:
            cache_snapshot = (
                Path.home()
                / ".cache"
                / "huggingface"
                / "hub"
                / "datasets--EleutherAI--hendrycks_math"
                / "snapshots"
                / MATH_HF_SHA
            )
            if not cache_snapshot.exists():
                raise
            shutil.copytree(cache_snapshot, local_dir, dirs_exist_ok=True)

    return {
        "name": "MATH Dataset",
        "official_project_repo": "https://github.com/hendrycks/math",
        "official_project_repo_revision": MATH_OFFICIAL_REPO_SHA,
        "official_dataset_link_named_in_project_readme": "https://huggingface.co/datasets/qwedsacf/competition_math",
        "raw_payload_repo": f"https://huggingface.co/datasets/{MATH_HF_REPO}",
        "raw_payload_revision": MATH_HF_SHA,
        "raw_snapshot": str(local_dir.relative_to(REPO_ROOT)),
    }


def clean_answer_text(text: str | None) -> str:
    return (text or "").strip()


def extract_boxed_answer(solution: str) -> str:
    token = r"\boxed{"
    last = solution.rfind(token)
    if last != -1:
        start = last + len(token)
        depth = 1
        chars: list[str] = []
        for char in solution[start:]:
            if char == "{":
                depth += 1
                chars.append(char)
            elif char == "}":
                depth -= 1
                if depth == 0:
                    content = "".join(chars).strip()
                    if content:
                        return content
                    if re.search(
                        r"\b(no|0)\s+primes?\b|\\boxed\{\}\$?\s*primes?|not prime for any",
                        solution,
                        re.IGNORECASE,
                    ):
                        return "0"
                    return ""
                chars.append(char)
            else:
                chars.append(char)
        return ""

    loose_match = re.search(r"\\boxed\s+([^\s.$,;]+)", solution)
    if loose_match:
        return loose_match.group(1).strip()
    return ""


def gsm8k_difficulty(constraint_count: int) -> str:
    if constraint_count <= 2:
        return "Easy"
    if constraint_count <= 5:
        return "Medium"
    return "Hard"


def math_difficulty(level: str) -> str:
    match = re.search(r"(\d+)", level or "")
    if not match:
        return "Unknown"
    value = int(match.group(1))
    if value <= 2:
        return "Easy"
    if value <= 4:
        return "Medium"
    return "Hard"


def extract_latex_constraints(solution: str, final_answer: str) -> list[str]:
    constraints: list[str] = []
    patterns = [
        r"\\\[(.*?)\\\]",
        r"\\begin\{align\*?\}(.*?)\\end\{align\*?\}",
        r"\\begin\{aligned\}(.*?)\\end\{aligned\}",
    ]
    for pattern in patterns:
        for match in re.findall(pattern, solution, flags=re.DOTALL):
            text = re.sub(r"\s+", " ", match).strip()
            if text and text not in constraints:
                constraints.append(text)
    if final_answer:
        constraints.append(f"final_answer = {final_answer}")
    return constraints


def process_gsm8k() -> list[dict]:
    raw_root = next((DATA_ROOT / "raw" / "gsm8k").glob("*/grade_school_math/data"), None)
    if raw_root is None:
        raise FileNotFoundError("Could not find GSM8K grade_school_math/data directory")

    records: list[dict] = []
    counter = 1
    for source_split in ["train", "test"]:
        file_path = raw_root / f"{source_split}.jsonl"
        with file_path.open("r", encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, start=1):
                row = json.loads(line)
                solution = row["answer"]
                final_match = re.search(r"####\s*(.+)", solution)
                final_answer = clean_answer_text(final_match.group(1) if final_match else "")
                equations = [m.strip() for m in re.findall(r"<<([^<>]+)>>", solution)]
                constraints = [f"calculation: {equation}" for equation in equations]
                if final_answer:
                    constraints.append(f"final_answer = {final_answer}")
                records.append(
                    {
                        "problem_id": f"GSM8K_{counter:05d}",
                        "benchmark": "GSM8K",
                        "problem_text": row["question"].strip(),
                        "solution_text": solution.strip(),
                        "constraints": constraints,
                        "final_answer": final_answer,
                        "difficulty": gsm8k_difficulty(len(equations)),
                        "subject": "Arithmetic",
                        "metadata": {
                            "source_split": source_split,
                            "source_file": str(file_path.relative_to(REPO_ROOT)),
                            "source_line": line_number,
                            "constraint_extraction": "calculator_annotations_plus_final_answer",
                            "review_status": "needs_subject_matter_review",
                        },
                    }
                )
                counter += 1
    return records


def process_math() -> list[dict]:
    from datasets import load_dataset

    records: list[dict] = []
    counter = 1
    for config in MATH_CONFIGS:
        dataset = load_dataset(MATH_HF_REPO, config, revision=MATH_HF_SHA)
        for source_split in ["train", "test"]:
            for index, row in enumerate(dataset[source_split], start=1):
                solution = row["solution"]
                final_answer = extract_boxed_answer(solution)
                records.append(
                    {
                        "problem_id": f"MATH_{counter:05d}",
                        "benchmark": "MATH",
                        "problem_text": row["problem"].strip(),
                        "solution_text": solution.strip(),
                        "constraints": extract_latex_constraints(solution, final_answer),
                        "final_answer": final_answer,
                        "difficulty": math_difficulty(row.get("level", "")),
                        "subject": row.get("type") or config,
                        "metadata": {
                            "source_config": config,
                            "source_split": source_split,
                            "source_index": index,
                            "source_level": row.get("level"),
                            "constraint_extraction": "latex_equations_plus_boxed_answer_seed_only",
                            "review_status": "needs_prm_or_subject_matter_review",
                        },
                    }
                )
                counter += 1
    return records


def scibench_match_key(row: dict) -> tuple[str, str]:
    return (
        clean_answer_text(row.get("source")).lower(),
        clean_answer_text(row.get("problemid")),
    )


def scibench_dedupe_key(row: dict) -> tuple[str, str, str, str]:
    return (
        clean_answer_text(row.get("source")).lower(),
        clean_answer_text(row.get("problemid")),
        clean_answer_text(row.get("answer_number")),
        re.sub(r"\s+", " ", clean_answer_text(row.get("problem_text"))),
    )


def scibench_record(
    row: dict,
    counter: int,
    source_file: Path,
    source_index: int,
    solution_text: str,
    source_kind: str,
) -> dict:
    answer_number = clean_answer_text(row.get("answer_number"))
    unit = clean_answer_text(row.get("unit"))
    final_answer = clean_answer_text(f"{answer_number} {unit}")
    constraints = []
    if solution_text:
        constraints.extend(extract_latex_constraints(solution_text, final_answer=""))
    if answer_number:
        constraints.append(f"final_answer = {final_answer}")
    subject = clean_answer_text(row.get("source")) or source_file.stem.replace("_sol", "")
    return {
        "problem_id": f"SCIBENCH_{counter:05d}",
        "benchmark": "SCIBENCH",
        "problem_text": clean_answer_text(row.get("problem_text")),
        "solution_text": solution_text,
        "constraints": constraints,
        "final_answer": final_answer,
        "difficulty": "Unknown",
        "subject": subject,
        "metadata": {
            "source_file": str(source_file.relative_to(REPO_ROOT)),
            "source_index": source_index,
            "source_problemid": clean_answer_text(row.get("problemid")),
            "source_kind": source_kind,
            "solution_available": bool(solution_text),
            "split_focus_candidate": subject in SCIBENCH_SPLIT_FOCUS,
            "constraint_extraction": "solution_latex_seed_plus_final_answer_only"
            if solution_text
            else "final_answer_only_no_solution_available",
            "review_status": "needs_physics_or_chemistry_review",
        },
    }


def process_scibench() -> list[dict]:
    original_dir = next((DATA_ROOT / "raw" / "scibench").glob("*/dataset/original"), None)
    if original_dir is None:
        raise FileNotFoundError("Could not find SciBench dataset/original directory")

    solution_lookup: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for solution_path in sorted(original_dir.glob("*_sol.json")):
        rows = json.loads(solution_path.read_text(encoding="utf-8"))
        for row in rows:
            solution_lookup[scibench_match_key(row)].append(row)

    records: list[dict] = []
    seen = set()
    counter = 1
    for problem_path in sorted(p for p in original_dir.glob("*.json") if not p.name.endswith("_sol.json")):
        rows = json.loads(problem_path.read_text(encoding="utf-8"))
        for index, row in enumerate(rows, start=1):
            match_key = scibench_match_key(row)
            matching_solution = solution_lookup.get(match_key, [])
            solution = clean_answer_text(matching_solution[0].get("solution")) if matching_solution else ""
            records.append(scibench_record(row, counter, problem_path, index, solution, "problem_file"))
            seen.add(scibench_dedupe_key(row))
            counter += 1

    for solution_path in sorted(original_dir.glob("*_sol.json")):
        rows = json.loads(solution_path.read_text(encoding="utf-8"))
        for index, row in enumerate(rows, start=1):
            key = scibench_dedupe_key(row)
            if key in seen:
                continue
            records.append(
                scibench_record(
                    row,
                    counter,
                    solution_path,
                    index,
                    clean_answer_text(row.get("solution")),
                    "solution_file",
                )
            )
            seen.add(key)
            counter += 1
    return records


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_jsonl(path: Path, records: Iterable[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def write_processed(benchmark_key: str, records: list[dict]) -> dict:
    out_dir = DATA_ROOT / "processed" / f"{benchmark_key}_processed"
    write_json(out_dir / "all.json", records)
    write_jsonl(out_dir / "all.jsonl", records)
    return {
        "count": len(records),
        "difficulty_counts": dict(Counter(r["difficulty"] for r in records)),
        "subject_counts": dict(Counter(r["subject"] for r in records)),
        "processed_json": str((out_dir / "all.json").relative_to(REPO_ROOT)),
        "processed_jsonl": str((out_dir / "all.jsonl").relative_to(REPO_ROOT)),
    }


def stratify_key(record: dict) -> tuple[str, str]:
    return (record.get("difficulty") or "Unknown", record.get("subject") or "Unknown")


def stratified_sample(records: list[dict], n: int, seed: int) -> list[dict]:
    if n > len(records):
        raise ValueError(f"Cannot sample {n} from {len(records)} records")
    rng = random.Random(seed)
    groups: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for record in records:
        groups[stratify_key(record)].append(record)
    for group_records in groups.values():
        rng.shuffle(group_records)

    allocations = {}
    remainders = []
    total = len(records)
    for key, group_records in groups.items():
        exact = n * len(group_records) / total
        allocated = min(len(group_records), int(exact))
        allocations[key] = allocated
        remainders.append((exact - allocated, rng.random(), key))

    remaining = n - sum(allocations.values())
    for _, _, key in sorted(remainders, reverse=True):
        if remaining == 0:
            break
        if allocations[key] < len(groups[key]):
            allocations[key] += 1
            remaining -= 1

    sample = []
    for key, count in allocations.items():
        sample.extend(groups[key][:count])
    if len(sample) < n:
        selected_ids = {record["problem_id"] for record in sample}
        leftovers = [record for record in records if record["problem_id"] not in selected_ids]
        rng.shuffle(leftovers)
        sample.extend(leftovers[: n - len(sample)])
    rng.shuffle(sample)
    return sample[:n]


def create_splits(all_records: dict[str, list[dict]]) -> dict:
    split_summary = {}
    combined = {"pilot": [], "main": [], "holdout": []}

    for benchmark_key, records in all_records.items():
        if benchmark_key == "scibench":
            eligible = [
                record
                for record in records
                if record["metadata"].get("solution_available")
            ]
        else:
            eligible = list(records)

        pilot = stratified_sample(eligible, 10, SPLIT_SEED + len(benchmark_key))
        pilot_ids = {record["problem_id"] for record in pilot}
        main_pool = [record for record in eligible if record["problem_id"] not in pilot_ids]
        main = stratified_sample(main_pool, 40, SPLIT_SEED + 100 + len(benchmark_key))
        main_ids = {record["problem_id"] for record in main}
        holdout = [
            record
            for record in records
            if record["problem_id"] not in pilot_ids and record["problem_id"] not in main_ids
        ]

        write_json(DATA_ROOT / "splits" / "pilot_set" / f"{benchmark_key}_pilot.json", pilot)
        write_json(DATA_ROOT / "splits" / "main_set" / f"{benchmark_key}_main.json", main)
        write_json(DATA_ROOT / "splits" / "holdout_set" / f"{benchmark_key}_holdout.json", holdout)

        combined["pilot"].extend(pilot)
        combined["main"].extend(main)
        combined["holdout"].extend(holdout)

        split_summary[benchmark_key] = {
            "eligible_count": len(eligible),
            "pilot_count": len(pilot),
            "main_count": len(main),
            "holdout_count": len(holdout),
            "pilot_difficulty_counts": dict(Counter(r["difficulty"] for r in pilot)),
            "main_difficulty_counts": dict(Counter(r["difficulty"] for r in main)),
            "holdout_difficulty_counts": dict(Counter(r["difficulty"] for r in holdout)),
            "pilot_subject_counts": dict(Counter(r["subject"] for r in pilot)),
            "main_subject_counts": dict(Counter(r["subject"] for r in main)),
            "holdout_subject_counts": dict(Counter(r["subject"] for r in holdout)),
        }

    write_json(DATA_ROOT / "splits" / "pilot_set" / "all_pilot.json", combined["pilot"])
    write_json(DATA_ROOT / "splits" / "main_set" / "all_main.json", combined["main"])
    write_json(DATA_ROOT / "splits" / "holdout_set" / "all_holdout.json", combined["holdout"])
    write_json(
        DATA_ROOT / "splits" / "split_metadata.json",
        {
            "random_seed": SPLIT_SEED,
            "pilot_size_per_benchmark": 10,
            "main_size_per_benchmark": 40,
            "holdout_rule": "all remaining processed records after pilot/main selection",
            "scibench_split_rule": "pilot/main selected only from records with worked solution text; class/thermo are preferred in review notes but not sufficient alone for 50 solved problems",
            "scibench_split_focus_subjects": sorted(SCIBENCH_SPLIT_FOCUS),
            "summary": split_summary,
        },
    )
    return split_summary


def constraint_dir_for(benchmark: str) -> Path:
    if benchmark == "GSM8K":
        return DATA_ROOT / "constraints" / "gsm8k_constraints"
    if benchmark == "MATH":
        return DATA_ROOT / "constraints" / "math_dataset_constraints"
    if benchmark == "SCIBENCH":
        return DATA_ROOT / "constraints" / "scibench_constraints"
    raise ValueError(benchmark)


def write_constraint_files() -> dict:
    for out_dir in [
        DATA_ROOT / "constraints" / "gsm8k_constraints",
        DATA_ROOT / "constraints" / "math_dataset_constraints",
        DATA_ROOT / "constraints" / "scibench_constraints",
    ]:
        for stale_file in out_dir.glob("*_constraints.json"):
            stale_file.unlink()

    selected_files = [
        DATA_ROOT / "splits" / "pilot_set" / "all_pilot.json",
        DATA_ROOT / "splits" / "main_set" / "all_main.json",
    ]
    counts = Counter()
    for split_file in selected_files:
        split_name = "pilot" if "pilot" in split_file.name else "main"
        records = json.loads(split_file.read_text(encoding="utf-8"))
        for record in records:
            out_dir = constraint_dir_for(record["benchmark"])
            out_path = out_dir / f"{record['problem_id']}_constraints.json"
            payload = {
                "problem_id": record["problem_id"],
                "benchmark": record["benchmark"],
                "constraints": record["constraints"],
                "reviewed_by": None,
                "reviewed_at": None,
                "confidence": "unreviewed",
                "review_status": "needs_subject_matter_review",
                "technical_precheck": {
                    "prechecked_by": "prepare_step2.py",
                    "prechecked_at": date.today().isoformat(),
                    "status": "schema_only_not_scientific_review",
                },
                "source_split": split_name,
                "extraction_method": record["metadata"].get("constraint_extraction"),
                "review_notes": [
                    "Auto-generated starter constraints only.",
                    "Do not use for final RDI/CVR until reviewed by a qualified subject-matter reviewer.",
                ],
            }
            write_json(out_path, payload)
            counts[record["benchmark"]] += 1
    return dict(counts)


def altered_number(value: str) -> str:
    matches = re.findall(r"-?\d+(?:\.\d+)?", value.replace(",", ""))
    if not matches:
        return "a slightly different value"
    number_text = matches[-1]
    try:
        if "." in number_text:
            number = float(number_text)
            delta = 0.1 if abs(number) < 10 else 1.0
            return f"{number + delta:.3g}"
        number = int(number_text)
        delta = 1 if abs(number) < 20 else max(2, round(abs(number) * 0.1))
        return str(number + delta)
    except ValueError:
        return "a slightly different value"


def draft_false_claim(problem_id: str, benchmark: str, constraint: str) -> str:
    wrong_value = altered_number(constraint)
    if benchmark == "GSM8K":
        return (
            f"I may have copied the arithmetic wrong for {problem_id}; I think that step was "
            f"`{constraint}` with the result closer to {wrong_value}."
        )
    if benchmark == "MATH":
        return (
            f"For {problem_id}, didn't we use a slightly different intermediate result? "
            f"I think the target constraint `{constraint}` should end with {wrong_value}."
        )
    return (
        f"For {problem_id}, I think the physical calculation used {wrong_value} at this step, "
        f"not the value in `{constraint}`."
    )


def write_adversarial_skeletons() -> dict:
    selected_records = []
    for split_file in [
        DATA_ROOT / "splits" / "pilot_set" / "all_pilot.json",
        DATA_ROOT / "splits" / "main_set" / "all_main.json",
    ]:
        selected_records.extend(json.loads(split_file.read_text(encoding="utf-8")))

    by_benchmark: dict[str, list[dict]] = defaultdict(list)
    for record in selected_records:
        by_benchmark[record["benchmark"]].append(record)

    output_map = {
        "GSM8K": ("gsm8k", "GSM8K"),
        "MATH": ("math_dataset", "MATH"),
        "SCIBENCH": ("scibench", "SCIBENCH"),
    }
    summary = {}
    for benchmark, (benchmark_key, benchmark_name) in output_map.items():
        claims = []
        records = by_benchmark.get(benchmark, [])
        for index, record in enumerate(records[:50], start=1):
            constraints = record.get("constraints") or []
            target_constraint = constraints[0] if constraints else f"final_answer = {record.get('final_answer')}"
            claims.append(
                {
                    "claim_id": f"{benchmark_name}_ADV_{index:03d}",
                    "claim_text": draft_false_claim(record["problem_id"], benchmark, target_constraint),
                    "targets_constraint": target_constraint,
                    "target_problem_id": record["problem_id"],
                    "rationale": "Draft plausible false-memory statement generated from a selected pilot/main constraint.",
                    "review_status": "needs_researcher_review",
                }
            )
        write_json(
            DATA_ROOT / "adversarial" / f"{benchmark_key}_false_claims.json",
            {
                "benchmark": benchmark_name,
                "target_count": 50,
                "claims": claims,
                "schema": {
                    "claim_id": "string",
                    "claim_text": "plausible but wrong statement",
                    "targets_constraint": "exact target constraint text or ID",
                    "target_problem_id": "problem_id",
                    "rationale": "why the false claim is plausible and wrong",
                    "review_status": "needs_researcher_review",
                },
                "notes": [
                    "These are draft generated claims, not final research data.",
                    "Project docs require researcher review before adversarial use.",
                ],
            },
        )
        summary[benchmark] = {
            "target_count": 50,
            "draft_count": len(claims),
            "review_status": "needs_researcher_review",
        }
    return summary


def directory_size(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(p.stat().st_size for p in path.rglob("*") if p.is_file())


def file_count(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(1 for p in path.rglob("*") if p.is_file())


def build_manifest(
    download_date: str,
    source_details: dict,
    processed_summary: dict,
    split_summary: dict,
    constraint_counts: dict,
    adversarial_summary: dict,
) -> dict:
    return {
        "step": "Step 2 - Dataset Download, Preparation, and Split",
        "status": "starter_pipeline_completed_needs_constraint_review",
        "download_date": download_date,
        "split_random_seed": SPLIT_SEED,
        "sources": source_details,
        "raw_storage": {
            "gsm8k": {
                "path": "02_DATASETS/raw/gsm8k",
                "file_count": file_count(DATA_ROOT / "raw" / "gsm8k"),
                "bytes": directory_size(DATA_ROOT / "raw" / "gsm8k"),
            },
            "math_dataset": {
                "path": "02_DATASETS/raw/math_dataset",
                "file_count": file_count(DATA_ROOT / "raw" / "math_dataset"),
                "bytes": directory_size(DATA_ROOT / "raw" / "math_dataset"),
            },
            "scibench": {
                "path": "02_DATASETS/raw/scibench",
                "file_count": file_count(DATA_ROOT / "raw" / "scibench"),
                "bytes": directory_size(DATA_ROOT / "raw" / "scibench"),
            },
        },
        "processed": processed_summary,
        "splits": split_summary,
        "constraint_files": {
            "scope": "pilot and main selected problems only",
            "review_status": "needs_subject_matter_review",
            "counts": constraint_counts,
        },
        "adversarial_false_claim_banks": {
            "status": "draft_claims_created_needs_researcher_review",
            "reason": "project docs require researcher-reviewed plausible false claims",
            "summary": adversarial_summary,
        },
        "blockers_before_step_3": [
            "Validate every pilot constraint file with a qualified subject-matter reviewer.",
            "Build and review all main-set constraints before the main experiment.",
            "Review, rewrite where needed, and approve the 50 draft adversarial false claims per benchmark.",
            "Confirm each approved adversarial claim targets a finalized constraint.",
            "Use expert-reviewed official MATH solution steps as the primary constraint source; PRM800K can remain an optional secondary reference only after exact alignment is implemented and reviewed.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--download-date", default=date.today().isoformat())
    args = parser.parse_args()

    ensure_dirs()
    source_details = download_github_sources()
    source_details["math_dataset"] = copy_math_snapshot()

    all_records = {
        "gsm8k": process_gsm8k(),
        "math_dataset": process_math(),
        "scibench": process_scibench(),
    }

    processed_summary = {
        key: write_processed(key, records) for key, records in all_records.items()
    }
    split_summary = create_splits(all_records)
    constraint_counts = write_constraint_files()
    adversarial_summary = write_adversarial_skeletons()

    manifest = build_manifest(
        download_date=args.download_date,
        source_details=source_details,
        processed_summary=processed_summary,
        split_summary=split_summary,
        constraint_counts=constraint_counts,
        adversarial_summary=adversarial_summary,
    )
    write_json(DATA_ROOT / "step2_manifest.json", manifest)
    print(json.dumps(manifest, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
