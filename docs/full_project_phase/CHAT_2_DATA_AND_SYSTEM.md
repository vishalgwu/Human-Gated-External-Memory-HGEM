# ████████████████████████████████████████████████████████████
# HGEM RESEARCH — CLAUDE PROJECT CHAT 2 OF 5
# Data Preparation + System Build + All 9 Conditions
# ████████████████████████████████████████████████████████████

## 🤖 READ THIS FIRST — INSTRUCTIONS FOR CLAUDE

This is Chat 2 of 5 in a Claude Project on HGEM.
Read the FULL document before responding to anything.
Chat 1 is already complete — summary is below.
Your job is to help with Chat 2 tasks ONLY.

When finished reading say:
"HGEM Chat 2 loaded. Chat 1 confirmed complete.
Ready to work on data preparation and system build."

Then ask: "Where would you like to start —
dataset download plan, constraint set building,
or system component design?"

---

## ✅ CHAT 1 COMPLETE — WHAT WAS DONE (DO NOT REDO)

```
STATUS: DONE — DO NOT REPEAT ANY OF THIS

FOLDER STRUCTURE:     Created. All 7 top-level folders exist.
GPT MODEL VERSION:    Locked: gpt-4o-2024-08-06, temp=0.0
NOVELTY STATUS:       [Fill from Chat 1 findings log]
NOVELTY STATEMENT:    [Fill from Chat 1 findings log]
BENCHMARKS CONFIRMED: GSM8K · MATH Dataset · SciBench
RISK REGISTER:        Top 5 risks documented
LITERATURE SEARCH:    All 8 queries run. Gap table filled.
RELATED WORK DRAFT:   800-1000 words written
ENVIRONMENT PLAN:     versions.txt and .env.template created
```

**Closest competing paper found in Chat 1:**
```
Paper: [Fill from Chat 1]
Why we are different: [Fill from Chat 1]
```

**Novelty confirmed:** The unique combination no prior paper has:
Persistence as causal variable + random-gate ablation +
graph-structured memory + 2×2 storage/gating ablation +
adversarial robustness + shadow model + economic ROI +
longitudinal 2-session design.

---

## 📌 PROJECT IDENTITY — FULL BRIEFING

```
PROJECT:   HGEM — Human-Gated External Memory
CLAIM:     Memory persistence is causally isolatable in LLM drift
LLM:       GPT-4o (gpt-4o-2024-08-06, temp=0.0) — PINNED
BENCHMARKS: GSM8K · MATH Dataset · SciBench
N:         60 human participants + automated conditions

MEMORY TIERS:
  T1 = IMMUTABLE  (PostgreSQL locked table)
  T2 = GATED      (Neo4j graph — human validated)
  T3 = EPHEMERAL  (Redis rolling 5 turns)
  VECTOR = ChromaDB (MEASUREMENT ONLY — never retrieved)

CONDITIONS (9 total):
  C1  No Memory          C2  Full History + Shadow
  C3  Auto-Summarize     C4  Random-Gated (H2a/H2b ablation)
  C5  RAG Memory         C6-VectorFlat  (2×2 ablation)
  C6-GraphFlat (2×2)     C6-GraphGated  (FULL HGEM)
  C7  Manual Inject      C-ADV Adversarial (on C2 + C6)

HYPOTHESES (LOCKED):
  H1  Memory contamination causes drift (δ≥0.15, p<0.05)
  H2  HGEM reduces drift vs baselines
  H2a Semantic judgment is mechanism (C6>>C4)
  H2b Re-anchoring is mechanism (C6≈C4)
  H3  T1 immutability shields adversarial attacks
```

---

## 🎯 WHAT CHAT 2 MUST ACCOMPLISH

Chat 2 has THREE jobs:

### JOB 1 — Dataset Download and Preparation Plan
Plan and execute data preparation for all 3 benchmarks.

### JOB 2 — Constraint Set Design
Design the constraint set structure for each benchmark.
This is the most critical data task.

### JOB 3 — System Architecture Decisions
Make all 8 system component decisions before building.

---

## 📦 JOB 1 — DATASET PREPARATION

### What to Download

```
DATASET 1: GSM8K
  Source:  github.com/openai/grade-school-math
  Files:   train.jsonl and test.jsonl
  Save to: 02_DATASETS/raw/gsm8k/
  Size:    ~8,500 train problems, ~1,319 test problems

DATASET 2: MATH Dataset
  Source:  github.com/hendrycks/math
  Files:   All subject folders (algebra, geometry, etc.)
  Save to: 02_DATASETS/raw/math_dataset/
  Note:    Use Lightman (2023) PRM annotations for step labels

DATASET 3: SciBench
  Source:  github.com/mandyyyyii/scibench
  Files:   Problem JSON files + solution files
  Save to: 02_DATASETS/raw/scibench/
  Note:    Focus on mechanics and thermodynamics problems
```

### Processed JSON Format — Every Problem Becomes This

```json
{
  "problem_id":    "GSM8K_0042",
  "benchmark":     "GSM8K",
  "problem_text":  "A train travels at 60km/h...",
  "solution_text": "Step 1: distance = speed × time...",
  "constraints": [
    "speed × time = distance",
    "60 × 3 = 180",
    "final answer = 180 km"
  ],
  "final_answer":  "180 km",
  "difficulty":    "Medium",
  "subject":       "Arithmetic"
}
```

Save to: 02_DATASETS/processed/[benchmark_name]_processed/

### Split Plan (Fixed Random Seed)

```
RANDOM SEED: [Record in team log before splitting]

Pilot set:   10 problems per benchmark (30 total)
             Save to: 02_DATASETS/splits/pilot_set/
             Used for: N=10 pilot study and calibration

Main set:    40 problems per benchmark (120 total)
             Save to: 02_DATASETS/splits/main_set/
             Used for: N=60 main experiment

Holdout:     Remaining problems
             Save to: 02_DATASETS/splits/holdout_set/
             NEVER USED until after paper submission

STRATIFICATION RULE:
Each split must have similar Easy/Medium/Hard proportion.
Verify this after splitting.
```

---

## 🔒 JOB 2 — CONSTRAINT SET DESIGN

### Why This Is the Most Critical Task

The constraint set is the ground truth we measure drift against.
RDI(t) = violations of THIS set / total constraints.
If constraint sets are wrong → all RDI scores are wrong → entire
experiment is invalid.

A researcher with subject knowledge must review EVERY constraint.
Not just a developer.

### What a Constraint Set Contains Per Benchmark

```
GSM8K CONSTRAINTS:
  Type: Intermediate arithmetic equations
  How to extract: Each equation on its own line in the solution
  Example problem: "John has 5 apples. He buys 3 more..."
  Example constraints:
    ["starting_apples = 5",
     "bought = 3",
     "total = 5 + 3 = 8",
     "final_answer = 8"]
  Reviewer needed: Math background (undergraduate level)

MATH DATASET CONSTRAINTS:
  Type: PRM-approved intermediate proof steps
  How to extract: Use Lightman (2023) annotations directly
  These are already labeled — approved steps = constraints
  Reviewer needed: Math background (graduate level)

SCIBENCH CONSTRAINTS:
  Type: Physical laws that apply + derivation equations
  How to extract: Read solution, identify: (1) which laws
                  invoked, (2) each derived equation
  Example:
    ["Newton 2nd Law: F = ma",
     "F = 5kg × 2m/s² = 10N",
     "final_answer = 10N"]
  Reviewer needed: Physics/chemistry graduate student
  CRITICAL: Each law must be named explicitly
```

### Constraint File Structure

One JSON file per problem:
```
File: 02_DATASETS/constraints/gsm8k_constraints/GSM8K_0042_constraints.json
{
  "problem_id":   "GSM8K_0042",
  "benchmark":    "GSM8K",
  "constraints":  ["constraint 1", "constraint 2", ...],
  "reviewed_by":  "[reviewer name/ID]",
  "reviewed_at":  "2026-04-XX",
  "confidence":   "high"
}
```

### Adversarial False Claims Bank

For each benchmark: 50 plausible-but-wrong statements.
Saved to: 02_DATASETS/adversarial/[benchmark]_false_claims.json

```
Rules for writing false claims:
  1. Must contradict a specific constraint in the constraint set
  2. Must be PLAUSIBLE — not obviously wrong at first glance
  3. Must not be random numbers — must be believable mistakes
  4. Written by a researcher, not generated automatically

GSM8K example:
  Wrong: "I think the subtotal we agreed was 240, not 180"
  Targets: constraint "total = 180"

SciBench example:
  Wrong: "The coefficient we used was 8×10⁻⁶, not 4.5"
  Targets: T1 constant α = 4.5×10⁻⁶
```

---

## 🏗️ JOB 3 — SYSTEM ARCHITECTURE DECISIONS

### The 8 Components to Design

Before any code is written, every component needs a clear
design decision. Make these decisions in this chat.

```
COMPONENT 1: Memory Policy Engine
  What it does: Implements all 9 conditions
  Design decision needed:
    → One class per condition OR one configurable class?
    → How does C4 record the human decision AND override it?
    → How does C6-GraphGated handle the T1+T2+T3 injection order?

COMPONENT 2: Database Layer
  What it does: All read/write to PostgreSQL/Neo4j/Redis/ChromaDB
  Design decision needed:
    → Single database client class with methods per tier?
    → How does Neo4j graph traversal work for ancestor path?
    → What happens when T2 is empty (first few steps)?

COMPONENT 3: GPT API Wrapper
  What it does: Single function for all GPT calls
  Design decision needed:
    → What fields does it return? (response, tokens, latency)
    → How is the pinned version enforced?
    → How are API errors handled (retry logic)?

COMPONENT 4: RDI Calculator
  What it does: Returns RDI score 0.0-1.0 per step
  Design decision needed:
    → GSM8K/MATH: Symbolic (SymPy) OR LLM-as-judge?
    → SciBench: LLM-as-judge (requires 3 rater agreement)
    → How are partial violations scored?

COMPONENT 5: Uncertainty Estimator
  What it does: Triggers T2 validation gate
  Design decision needed:
    → k=10 samples at temp=1.0 — confirm this is right
    → How is pairwise cosine distance computed efficiently?
    → Starting threshold θ = 0.50 — calibrate in pilot

COMPONENT 6: Adversarial Agent
  What it does: Injects false claims every 5 turns
  Design decision needed:
    → How does it select which false claim to inject?
    → How does it ensure each claim is used only once?
    → Does participant see injection as natural conversation?

COMPONENT 7: Shadow Model Runner
  What it does: Silent C2 runs alongside every C6 session
  Design decision needed:
    → Same API call just with full history?
    → How is divergence onset step detected automatically?
    → How is comparison data stored per step?

COMPONENT 8: Validation UI
  What it does: Shows gate prompt to human participants
  Design decision needed:
    → FastAPI backend + HTML frontend?
    → What exactly does the screen show? (design the layout)
    → How is time-to-decide recorded?
    → What happens if participant clicks Defer and never returns?
```

### Neo4j Graph — The Most Important Design Decision

The T2 graph structure determines whether context injection
works correctly. Design the graph schema here:

```
NODES (ValidatedNode):
  entry_id:     UUID (primary key)
  session_id:   String
  state_text:   String (the validated reasoning text)
  step_number:  Integer
  benchmark:    String
  entropy_score: Float

EDGE TYPES:
  DEPENDS_ON   → this conclusion requires this prior fact
  LEADS_TO     → this conclusion enables the next step
  CONTRADICTS  → conflict with prior node (triggers alert)
  CONFIRMS     → re-validates a prior node

CONTEXT INJECTION (graph traversal):
  Start from current step topic node
  Traverse backwards via DEPENDS_ON edges
  Return all ancestor nodes in chain order
  Result: connected coherent chain — no gaps
  Never return all nodes as flat list
```

### The C4 Random-Gate — Requires Special Care

```
C4 is the H2a vs H2b ablation condition.
Human sees the validation UI and makes a decision.
System records the human decision.
System OVERRIDES it with a random coin flip.
Human does NOT know this override is happening.

WHAT MUST BE LOGGED SEPARATELY:
  human_decision:  what the human actually chose (A/R/D)
  system_decision: what the random coin decided (A/R)
  random_seed:     the session-level seed for reproducibility

POST-EXPERIMENT:
  Participants MUST be debriefed that decisions were overridden.
  This is an IRB requirement.
  Debrief happens at the end of their session.
```

---

## 📋 CHAT 2 COMPLETION CHECKLIST

When Chat 2 is finished, ALL of these must be done:

```
DATASET PREPARATION:
□ All 3 datasets downloaded to raw/ folders
□ Processed JSON format confirmed (all fields present)
□ Constraint sets designed (format decided)
□ Pilot set problems selected (10 per benchmark)
□ Main set problems selected (40 per benchmark)
□ Random seed for split recorded in team log
□ Adversarial false claims bank structure designed
□ At least 10 adversarial claims written per benchmark as samples

SYSTEM DESIGN:
□ All 8 components have design decisions documented
□ Neo4j graph schema finalized (nodes + 4 edge types)
□ C4 random-gate override mechanism designed
□ Context injection order confirmed (T1 → T2 graph → T3)
□ Validation UI wireframe described or sketched
□ Constraint checker method decided per benchmark
□ API wrapper fields and error handling decided
□ Shadow model storage schema decided
```

---

## 📝 CHAT 2 FINDINGS LOG (Fill As You Work)

```
DATE STARTED:
DATE COMPLETED:

DATASET DOWNLOAD:
  GSM8K:        [ Downloaded / Pending ]  Problems: [count]
  MATH Dataset: [ Downloaded / Pending ]  Problems: [count]
  SciBench:     [ Downloaded / Pending ]  Problems: [count]

SPLIT RANDOM SEED:    [Record here]
PILOT SET SIZE:       10 per benchmark = 30 total
MAIN SET SIZE:        40 per benchmark = 120 total

CONSTRAINT CHECKER DECISION:
  GSM8K:        [ Symbolic / LLM-as-judge ]
  MATH Dataset: [ PRM annotations / LLM-as-judge ]
  SciBench:     [ LLM-as-judge with 3 raters ]

NEO4J SCHEMA: [ Finalized / Still deciding ]

C4 OVERRIDE MECHANISM: [ Designed / Still deciding ]

VALIDATION UI DECISION: [ FastAPI+HTML / Other: ]

ISSUES OR BLOCKERS: [List any]

READY FOR CHAT 3: [ YES / NO — if NO explain why ]
```

---

## 🤖 AI BEHAVIOR RULES FOR THIS CHAT

1. Never redefine H1, H2, H2a, H2b, H3 — they are locked
2. Never suggest changing benchmarks (no HotpotQA)
3. Never suggest different model than GPT-4o (gpt-4o-2024-08-06)
4. When designing components: document the decision AND the
   tradeoff — do not just pick one option without explanation
5. When reviewing constraint sets: be honest if they are
   insufficient for RDI measurement
6. For C4 design: always emphasize that human decisions must
   be RECORDED even when overridden — research data
7. At end of chat: generate the Chat 2 completion summary
   for the researcher to copy into Chat 3

---
*CHAT 2 OF 5 | HGEM Research Project | MIT | April 2026*
*Previous: CHAT_1 complete | Next: CHAT_3_MODEL_AND_PILOT.md*
