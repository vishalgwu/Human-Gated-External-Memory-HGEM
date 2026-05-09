# Human-Gated External Memory (HGEM)

HGEM is a research project studying whether long-term memory persistence is a causal driver of reasoning drift in LLM agent systems. The central claim is that restricting long-term memory to human-validated reasoning states should reduce Constraint Violation Rate (CVR), Reasoning Drift Index (RDI), and drift growth rate in multi-step scientific and engineering tasks.

This README is the current project control summary. It separates completed repository work from planned research work so the project status stays honest.

## Source Documents

The current project plan comes from these documents:

- `docs/HGEM_Complete_Research_Document_v4.docx`
- `docs/HGEM_Execution_Workflow_v1.docx`
- `docs/HGEM_Researcher_Step_Guide_v1.docx`
- `docs/full_project_phase/CHAT_1_SETUP_AND_LITERATURE.md`
- `docs/full_project_phase/CHAT_2_DATA_AND_SYSTEM.md`
- `docs/full_project_phase/CHAT_3_MODEL_AND_PILOT.md`
- `docs/full_project_phase/CHAT_4_MAIN_EXPERIMENT.md`
- `docs/full_project_phase/CHAT_5_ANALYSIS_WRITING.md`

There are also two prototype/demo files:

- `Prototype/hgem_professor_demo.html`
- `docs/full_project_phase/hgem_ui_prototype.html`

## Research Idea

In long LLM-assisted tasks, the conversation context can mix verified facts, wrong guesses, tangents, discarded options, and casual text. HGEM proposes that this unfiltered persistence causes reasoning drift over time.

HGEM separates memory into three tiers:

- T1 Immutable: fixed laws and constants. These are locked and cannot be changed by the model.
- T2 Human-gated: human-approved reasoning states stored as graph nodes with dependency edges.
- T3 Ephemeral: recent working context, limited to the last five turns.

The full HGEM condition should inject context in this order:

```text
T1 immutable constants -> T2 Neo4j graph traversal -> T3 last five turns
```

The model should not receive the full raw conversation history in the HGEM condition.

## Planned Experimental Conditions

The documents define the following experimental conditions:

- C1: No Memory
- C2: Full History
- C3: Auto-Summarize
- C4: Random-Gated
- C5: RAG Memory
- C6-VectorFlat: human-gated flat vector memory
- C6-GraphFlat: auto-persisted graph memory
- C6-GraphGated: full HGEM
- C7: Manual Inject
- C-ADV: adversarial false-memory injection

Important methodological controls:

- Random-gate ablation separates semantic judgment from the act of validation.
- 2x2 graph-vs-gating ablation separates storage structure from human gating.
- Shadow model protocol compares HGEM against full-history memory step by step.
- Adversarial condition tests whether T1 immutability protects against false claims.

## Current Repository Status

Current project stage:

```text
Step 1 environment setup: functionally complete
Step 2 dataset preparation: starter pipeline complete locally
Step 2 scientific review: in progress / not complete
System implementation: not started
Experiments: not started
Analysis/paper: not started
```

The repo is on `main`. Dataset artifacts are intentionally local-only and ignored by Git; GitHub stores the reproducible pipeline and metadata, not raw/generated benchmark payloads.

Latest relevant prior setup commit:

```text
9a4d576 folder structure
```

## What Has Been Done

### 1. Project Structure Created

The master folder structure from `HGEM_Execution_Workflow_v1.docx` has been created:

```text
00_PROJECT_DOCS/
01_SETUP/
02_DATASETS/
03_SYSTEM/
04_EXPERIMENT/
05_DATA/
06_ANALYSIS/
07_PAPER/
```

Empty folders include `.gitkeep` files so Git preserves the structure.

### 2. Step 1 Setup Files Created

Created:

- `00_PROJECT_DOCS/change_log.md`
- `01_SETUP/environment/install_checklist.md`
- `01_SETUP/environment/versions.txt`
- `01_SETUP/environment/requirements.txt`
- `01_SETUP/environment/requirements.freeze.txt`
- `01_SETUP/credentials/.env.template`
- `01_SETUP/credentials/.env` local only, ignored by Git
- `01_SETUP/docker-compose.services.yml`
- `01_SETUP/environment/check_services.py`

The local `.env` contains credentials and is intentionally ignored by Git.

### 3. Python Environment Created

Created local virtual environment:

```text
HGEM/
```

Activation:

```powershell
.\HGEM\Scripts\Activate.ps1
```

Installed Python package groups:

- OpenAI SDK
- FastAPI and Uvicorn
- PostgreSQL, Neo4j, Redis, and ChromaDB clients
- datasets, pandas, numpy, scipy, scikit-learn
- statsmodels, pingouin, sympy
- sentence-transformers
- matplotlib, seaborn, jupyterlab
- pytest, ruff, black

Exact installed versions are recorded in:

```text
01_SETUP/environment/requirements.freeze.txt
01_SETUP/environment/versions.txt
```

### 4. Local Services Installed Through Docker

Installed and started:

```text
PostgreSQL 15.17          container: hgem_postgres
Neo4j 5.26.25 Community   container: hgem_neo4j
Redis 7.4.8               container: hgem_redis
```

Current Docker service command:

```powershell
docker compose --env-file 01_SETUP\credentials\.env -f 01_SETUP\docker-compose.services.yml up -d
```

Current verification command:

```powershell
.\HGEM\Scripts\python.exe 01_SETUP\environment\check_services.py
```

Verified output:

```text
OpenAI auth OK: model=gpt-4o-2024-08-06, models endpoint reachable
PostgreSQL OK: PostgreSQL 15.17
PostgreSQL tables: conflict_log, experiment_events, tier1_immutable
Neo4j OK: Neo4j Kernel 5.26.25 (community)
Neo4j constraints: validated_node_entry_id
Redis OK: 7.4.8 ping=True
ChromaDB OK
```

### 5. Database Bootstrap Added

PostgreSQL schema:

```text
03_SYSTEM/database/postgresql/schema.sql
```

Created tables:

- `tier1_immutable`
- `experiment_events`
- `conflict_log`

Neo4j initialization:

```text
01_SETUP/neo4j_config/init.cypher
```

Created constraint:

- `validated_node_entry_id`

Database notes:

- `03_SYSTEM/database/README.md`
- `03_SYSTEM/database/postgresql/README.md`
- `03_SYSTEM/database/neo4j/README.md`
- `03_SYSTEM/database/chromadb/README.md`
- `03_SYSTEM/database/redis.md`

### 6. Git Ignore Rules Updated

`.gitignore` now prevents accidental commits of:

- local `.env`
- `HGEM/` virtual environment
- raw datasets
- processed datasets
- experiment logs
- generated analysis-ready data
- generated figures
- ChromaDB local store
- SQLite/local database files

### 7. Step 2 Dataset Pipeline Started

Added:

- `02_DATASETS/STEP_2_WORKFLOW.md`
- `02_DATASETS/prepare_step2.py`
- `02_DATASETS/step2_manifest.json`
- `02_DATASETS/audit_step2.py`
- `02_DATASETS/HUMAN_REVIEW_GUIDE.md`
- `02_DATASETS/PRE_HUMAN_REVIEW_CHECKLIST.md`
- `02_DATASETS/STEP_2_AUDIT_REPORT.md`
- `02_DATASETS/review_tool/`

Local ignored artifacts generated by the pipeline:

- raw GSM8K, MATH, and SciBench snapshots under `02_DATASETS/raw/`
- processed standard JSON files under `02_DATASETS/processed/`
- fixed-seed split files under `02_DATASETS/splits/`
- starter constraint files under `02_DATASETS/constraints/`
- adversarial false-claim bank skeletons under `02_DATASETS/adversarial/`

Local review tool:

```powershell
.\HGEM\Scripts\python.exe 02_DATASETS\review_tool\app.py
```

Then open:

```text
http://127.0.0.1:8765
```

The review tool lets a researcher cross-check a generated constraint JSON file against the matching split problem and solution, edit constraints, add reviewer/date/confidence/status metadata, and save the JSON back to the same local constraint folder.

Step 2 run details:

```text
Download date: 2026-05-09
Split seed:    20260509

Processed problems:
  GSM8K:        8,792
  MATH Dataset: 12,500
  SciBench:       691

Splits:
  Pilot:   10 per benchmark = 30 total
  Main:    40 per benchmark = 120 total
  Holdout: remaining 21,833 total

Starter constraints:
  GSM8K:        50 files
  MATH Dataset: 50 files
  SciBench:     50 files

Draft adversarial claims:
  GSM8K:        50 claims
  MATH Dataset: 50 claims
  SciBench:     50 claims
```

Important status note: the generated constraint files and adversarial claims are review seeds only. They are marked for subject-matter or researcher review and must not be treated as validated RDI/CVR ground truth yet.

## Current Folder Structure

```text
00_PROJECT_DOCS/
  proposal/
  workflow/
  meeting_notes/
  change_log.md

01_SETUP/
  credentials/
    .env              local only, ignored
    .env.template     tracked reference
  environment/
    check_services.py
    install_checklist.md
    requirements.txt
    requirements.freeze.txt
    versions.txt
  neo4j_config/
    init.cypher
  docker-compose.services.yml

02_DATASETS/
  raw/
    gsm8k/
    math_dataset/
    scibench/
  processed/
    gsm8k_processed/
    math_dataset_processed/
    scibench_processed/
  splits/
    pilot_set/
    main_set/
    holdout_set/
  constraints/
    gsm8k_constraints/
    math_dataset_constraints/
    scibench_constraints/
  adversarial/
  review_tool/

03_SYSTEM/
  memory_policies/
  database/
    postgresql/
    neo4j/
    chromadb/
    redis.md
  api_layer/
  drift_engine/
  uncertainty_estimator/
  adversarial_agent/
  shadow_model/
  validation_ui/

04_EXPERIMENT/
  pilot/
  main/
  longitudinal/
  adversarial/
  sessions/

05_DATA/
  raw_logs/
  cleaned/
  analysis_ready/
  surveys/

06_ANALYSIS/
  primary_tests/
  mediation/
  figures/
  exploratory/
  pre_registered_plan.md

07_PAPER/
  drafts/
  submission/
  reviewer_responses/
```

## What Is Left In Step 1

Step 1 infrastructure is complete.

One Step 1 rule remains for later implementation:

- Every GPT API call must log the exact model version and temperature.

This cannot be fully completed until the GPT API wrapper is implemented in:

```text
03_SYSTEM/api_layer/
```

## What Is Left In The Whole Project

### Phase 1: Literature And Novelty Lock

Status: not completed in this repository.

Remaining:

- Run the documented literature searches.
- Fill the novelty gap table with real papers.
- Confirm whether any prior work matches six or more HGEM features.
- Write the final three-sentence novelty lock.
- Draft or update the related work section.
- Record the closest competing papers.

Important note: the docs contain planned references and novelty claims, but this repository has not yet recorded a completed systematic literature review.

### Phase 2: Dataset Download And Preparation

Status: starter pipeline complete locally; generated data remains ignored by Git.

Done:

- Downloaded GSM8K.
- Downloaded MATH Dataset payload.
- Downloaded SciBench.
- Stored raw files under `02_DATASETS/raw/`.
- Converted each benchmark into the standard processed JSON format.
- Recorded source, date, file sizes, revisions, and problem counts.
- Kept raw/generated artifacts out of Git.
- Re-audited SciBench and corrected pilot/main selection to use only records with worked solution text.

Remaining:

- Treat raw files as read-only from this point.
- Use expert-reviewed official MATH solution steps as the primary constraint path; PRM800K is optional secondary reference only unless exact alignment is implemented.
- Have a researcher read example problems from each dataset and sign off that the processed schema preserves required fields.

### Phase 3: Constraint Set Construction

Status: starter constraint files generated for pilot/main selected problems; scientific validation not complete.

Done:

- Generated 50 GSM8K starter constraint files.
- Generated 50 MATH starter constraint files.
- Generated 50 SciBench starter constraint files.
- Marked all starter constraints as `needs_subject_matter_review`.

Remaining:

- Have subject-matter review for every pilot constraint before Step 3.
- Review and finalize all main-set constraints before main experiment use.
- Create confidence/reviewer metadata.
- Validate that RDI can be computed from these constraints.
- For SciBench, explicitly name physical laws in every finalized constraint set.

This is a critical scientific task. If the constraints are wrong, the RDI and CVR measurements become unreliable.

### Phase 4: Dataset Splits

Status: fixed-seed splits created locally; metadata recorded.

Done:

- Chosen and recorded fixed random seed: `20260509`.
- Created pilot split: 10 problems per benchmark.
- Created main split: 40 problems per benchmark.
- Created holdout split from remaining problems.
- Verified pilot/main/holdout problem IDs have zero overlap.
- Recorded split metadata in `02_DATASETS/step2_manifest.json`.

Remaining:

- Preserve the split seed and do not change selected pilot/main problems without a documented methodological reason.
- Keep holdout untouched until after submission or explicit replication/reviewer challenge.

### Phase 5: Adversarial False Claims Bank

Status: draft claims generated; researcher review still required.

Done:

- Created 50 draft adversarial claims for GSM8K.
- Created 50 draft adversarial claims for MATH.
- Created 50 draft adversarial claims for SciBench.
- Cross-referenced each draft claim to a selected pilot/main constraint.

Remaining:

- Researcher must review, rewrite where needed, and approve the draft claims.
- Ensure each approved false claim targets a finalized constraint, not a draft one.
- Ensure false claims are plausible, not random obvious errors.

### Phase 6: System Build

Status: not started.

Remaining components:

- Memory policy engine for all conditions.
- Database access layer for PostgreSQL, Neo4j, Redis, and ChromaDB.
- GPT API wrapper with pinned model and full call logging.
- RDI/CVR calculator.
- Uncertainty estimator.
- Adversarial agent.
- Shadow model runner.
- Validation UI.
- Experiment logger.

Important implementation rule:

```text
All conditions must use identical model settings unless a documented experiment intentionally changes them.
```

### Phase 7: Condition Verification

Status: not started.

Remaining:

- Verify C1 prompt contains no memory.
- Verify C2 prompt contains full history.
- Verify C3 prompt contains summary plus recent turns.
- Verify C4 records human decision and random system decision separately.
- Verify C5 retrieves top-k vector memories.
- Verify C6-VectorFlat injects flat validated memory.
- Verify C6-GraphFlat injects graph traversal without human gating.
- Verify C6-GraphGated injects T1, T2 graph path, then T3.
- Verify C7 manual injection works at required intervals.
- Verify C-ADV false claims inject at required intervals.

### Phase 8: Pilot Study

Status: not started.

Remaining:

- Recruit pilot participants.
- Run C2 and C6-GraphGated pilot sessions.
- Calibrate drift threshold.
- Calibrate entropy gate threshold.
- Validate RDI calculator reliability.
- Calibrate adversarial injection strength.
- Run power analysis.
- Apply stopping rules before main experiment.

### Phase 9: Main Experiment

Status: not started.

Remaining:

- Lock pre-registered analysis plan before unblinding.
- Run automated conditions.
- Run human participant conditions.
- Run adversarial sessions.
- Collect NASA-TLX surveys.
- Collect exit interviews.
- Maintain complete step-level logs.
- Export analysis-ready CSV files.

### Phase 10: Longitudinal Study

Status: not started.

Remaining:

- Run two-session 7-day transfer study.
- Compare full transcript recovery against HGEM memory recovery.
- Measure Time-to-Reconstruct Context.
- Measure token efficiency.
- Score with independent raters.

### Phase 11: Statistical Analysis

Status: not started.

Remaining:

- Run all pre-registered tests.
- Compute t-statistics, p-values, confidence intervals, and Cohen's d.
- Run mediation analysis if appropriate.
- Analyze shadow model divergence.
- Analyze adversarial robustness.
- Analyze longitudinal TRC.
- Label any non-pre-registered analysis as exploratory.

### Phase 12: Figures, Paper, And Submission

Status: not started.

Remaining:

- Generate architecture figure.
- Generate RDI curves.
- Generate beta comparison figure.
- Generate H2a vs H2b mechanism figure.
- Generate shadow model figure.
- Generate adversarial robustness figure.
- Generate longitudinal TRC figure.
- Write paper according to the result scenario.
- Prepare reviewer objection responses.
- Submit to selected venue.

## Immediate Next Action

The next concrete task is to finish the researcher-owned part of Step 2:

```text
Validate pilot/main constraint sets and approve adversarial false-claim banks.
```

Raw and generated benchmark files are currently local-only. Current `.gitignore` keeps them out of normal Git commits; move to Git LFS or external storage only if the team explicitly decides to share large dataset artifacts.

## Research Safety Notes

- Do not commit `.env`.
- Do not commit raw participant data.
- Do not treat proposal claims as completed results.
- Do not use ChromaDB as the retrieval source for full HGEM context.
- Do not change model version or temperature without documenting the methodological impact.
- Pre-register the analysis plan before looking at experiment results.
