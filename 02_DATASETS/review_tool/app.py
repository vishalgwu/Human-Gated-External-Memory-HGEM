"""Local HGEM constraint review web app.

Run from the repository root:
    .\HGEM\Scripts\python.exe 02_DATASETS\review_tool\app.py
"""

from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path
from typing import Any, Literal

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
import uvicorn


REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_ROOT = REPO_ROOT / "02_DATASETS"
APP_DIR = Path(__file__).resolve().parent
PROBLEM_ID_PATTERN = re.compile(r"^(GSM8K|MATH|SCIBENCH)_\d{5}$")

CONSTRAINT_DIRS = {
    "GSM8K": DATA_ROOT / "constraints" / "gsm8k_constraints",
    "MATH": DATA_ROOT / "constraints" / "math_dataset_constraints",
    "SCIBENCH": DATA_ROOT / "constraints" / "scibench_constraints",
}

SPLIT_FILES = {
    "pilot": DATA_ROOT / "splits" / "pilot_set" / "all_pilot.json",
    "main": DATA_ROOT / "splits" / "main_set" / "all_main.json",
}


class ConstraintSaveRequest(BaseModel):
    constraints: list[str] = Field(default_factory=list)
    reviewed_by: str | None = None
    reviewed_at: str | None = None
    confidence: Literal["unreviewed", "low", "medium", "high"] = "unreviewed"
    review_status: Literal["needs_subject_matter_review", "needs_revision", "finalized"] = (
        "needs_subject_matter_review"
    )
    review_notes: list[str] = Field(default_factory=list)


class UploadedConstraintRequest(BaseModel):
    payload: dict[str, Any]


app = FastAPI(title="HGEM Constraint Review Tool")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def load_split_records() -> dict[str, dict[str, Any]]:
    records: dict[str, dict[str, Any]] = {}
    for split_name, path in SPLIT_FILES.items():
        if not path.exists():
            continue
        for record in read_json(path):
            merged = dict(record)
            merged["hgem_split"] = split_name
            records[record["problem_id"]] = merged
    return records


def constraint_path(problem_id: str, benchmark: str | None = None) -> Path:
    if not PROBLEM_ID_PATTERN.fullmatch(problem_id):
        raise HTTPException(status_code=400, detail=f"Invalid problem_id: {problem_id}")
    if benchmark and benchmark in CONSTRAINT_DIRS:
        path = CONSTRAINT_DIRS[benchmark] / f"{problem_id}_constraints.json"
        if path.exists():
            return path
    for folder in CONSTRAINT_DIRS.values():
        path = folder / f"{problem_id}_constraints.json"
        if path.exists():
            return path
    raise HTTPException(status_code=404, detail=f"Constraint file not found for {problem_id}")


def load_constraint(problem_id: str, benchmark: str | None = None) -> tuple[Path, dict[str, Any]]:
    path = constraint_path(problem_id, benchmark)
    return path, read_json(path)


def all_constraint_files() -> list[Path]:
    files: list[Path] = []
    for folder in CONSTRAINT_DIRS.values():
        files.extend(sorted(folder.glob("*_constraints.json")))
    return sorted(files)


def load_adversarial_claims() -> dict[str, list[dict[str, Any]]]:
    by_problem: dict[str, list[dict[str, Any]]] = {}
    for path in (DATA_ROOT / "adversarial").glob("*_false_claims.json"):
        data = read_json(path)
        for claim in data.get("claims", []):
            by_problem.setdefault(claim.get("target_problem_id", ""), []).append(claim)
    return by_problem


def summarize_status() -> dict[str, Any]:
    split_records = load_split_records()
    counts: dict[str, Any] = {
        "total_files": 0,
        "by_benchmark": {},
        "by_status": {},
        "pilot_files": 0,
        "main_files": 0,
    }
    for path in all_constraint_files():
        data = read_json(path)
        pid = data.get("problem_id")
        benchmark = data.get("benchmark", "UNKNOWN")
        status = data.get("review_status", "unknown")
        split = split_records.get(pid, {}).get("hgem_split", data.get("source_split", "unknown"))
        counts["total_files"] += 1
        counts["by_benchmark"][benchmark] = counts["by_benchmark"].get(benchmark, 0) + 1
        counts["by_status"][status] = counts["by_status"].get(status, 0) + 1
        if split == "pilot":
            counts["pilot_files"] += 1
        if split == "main":
            counts["main_files"] += 1
    return counts


@app.get("/")
def index() -> FileResponse:
    return FileResponse(APP_DIR / "index.html")


@app.get("/api/summary")
def summary() -> dict[str, Any]:
    return summarize_status()


@app.get("/api/constraints")
def list_constraints(
    split: str = "pilot",
    benchmark: str = "ALL",
    status: str = "ALL",
) -> dict[str, Any]:
    split_records = load_split_records()
    items = []
    for path in all_constraint_files():
        data = read_json(path)
        pid = data.get("problem_id")
        record = split_records.get(pid, {})
        item_split = record.get("hgem_split", data.get("source_split", "unknown"))
        item_benchmark = data.get("benchmark", "UNKNOWN")
        item_status = data.get("review_status", "unknown")
        if split != "all" and item_split != split:
            continue
        if benchmark != "ALL" and item_benchmark != benchmark:
            continue
        if status != "ALL" and item_status != status:
            continue
        items.append(
            {
                "problem_id": pid,
                "benchmark": item_benchmark,
                "split": item_split,
                "status": item_status,
                "confidence": data.get("confidence"),
                "reviewed_by": data.get("reviewed_by"),
                "constraint_count": len(data.get("constraints", [])),
                "subject": record.get("subject"),
                "difficulty": record.get("difficulty"),
                "path": str(path.relative_to(REPO_ROOT)),
            }
        )
    return {"items": items, "count": len(items)}


@app.get("/api/constraint/{problem_id}")
def get_constraint(problem_id: str) -> dict[str, Any]:
    split_records = load_split_records()
    claims = load_adversarial_claims()
    path, constraint = load_constraint(problem_id)
    problem = split_records.get(problem_id)
    if problem is None:
        raise HTTPException(status_code=404, detail=f"Problem record not found for {problem_id}")
    return {
        "constraint_path": str(path.relative_to(REPO_ROOT)),
        "constraint": constraint,
        "problem": problem,
        "adversarial_claims": claims.get(problem_id, []),
        "today": date.today().isoformat(),
    }


@app.post("/api/constraint/{problem_id}/save")
def save_constraint(problem_id: str, request: ConstraintSaveRequest) -> dict[str, Any]:
    path, data = load_constraint(problem_id)
    clean_constraints = [item.strip() for item in request.constraints if item.strip()]
    if not clean_constraints:
        raise HTTPException(status_code=400, detail="At least one constraint is required.")
    data["constraints"] = clean_constraints
    data["reviewed_by"] = request.reviewed_by.strip() if request.reviewed_by else None
    data["reviewed_at"] = request.reviewed_at.strip() if request.reviewed_at else None
    data["confidence"] = request.confidence
    data["review_status"] = request.review_status
    data["review_notes"] = [item.strip() for item in request.review_notes if item.strip()]
    write_json(path, data)
    return {
        "saved": True,
        "problem_id": problem_id,
        "path": str(path.relative_to(REPO_ROOT)),
        "constraint": data,
        "summary": summarize_status(),
    }


@app.post("/api/uploaded-constraint")
def match_uploaded_constraint(request: UploadedConstraintRequest) -> dict[str, Any]:
    uploaded = request.payload
    problem_id = uploaded.get("problem_id")
    benchmark = uploaded.get("benchmark")
    if not problem_id:
        raise HTTPException(status_code=400, detail="Uploaded JSON does not include problem_id.")
    split_records = load_split_records()
    problem = split_records.get(problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail=f"No matching pilot/main split record for {problem_id}.")
    path, stored = load_constraint(problem_id, benchmark)
    return {
        "constraint_path": str(path.relative_to(REPO_ROOT)),
        "uploaded": uploaded,
        "stored": stored,
        "problem": problem,
        "today": date.today().isoformat(),
    }


if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8765, reload=False, app_dir=str(APP_DIR))
