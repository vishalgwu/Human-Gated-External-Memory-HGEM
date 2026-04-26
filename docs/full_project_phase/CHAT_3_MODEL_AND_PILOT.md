# ████████████████████████████████████████████████████████████
# HGEM RESEARCH — CLAUDE PROJECT CHAT 3 OF 5
# Model Integration + All 9 Conditions + Pilot Study (N=10)
# ████████████████████████████████████████████████████████████

## 🤖 READ THIS FIRST — INSTRUCTIONS FOR CLAUDE

This is Chat 3 of 5 in a Claude Project on HGEM.
Chats 1 and 2 are COMPLETE. Full summaries are below.
Read EVERYTHING before responding to anything.

When finished reading say:
"HGEM Chat 3 loaded. Chats 1 and 2 confirmed complete.
I understand what was done and what is left.
Ready to work on model integration and pilot study."

Then ask: "Would you like to start with condition verification,
pilot study planning, or calibration analysis?"

---

## ✅ CHAT 1 COMPLETE — ENVIRONMENT AND LITERATURE

```
FOLDER STRUCTURE:  Created. 7 top-level folders + all subfolders
GPT VERSION:       Locked: gpt-4o-2024-08-06 · temp=0.0
NOVELTY STATUS:    [Fill: CONFIRMED / AT RISK]
NOVELTY STATEMENT: [Fill from Chat 1 log — 3 sentences]
BENCHMARKS:        GSM8K · MATH Dataset · SciBench (confirmed)
RELATED WORK:      800-word draft written
RISK REGISTER:     Top 5 risks documented
LITERATURE:        All 8 queries done · gap table filled
```

## ✅ CHAT 2 COMPLETE — DATA AND SYSTEM DESIGN

```
DATASETS:
  GSM8K downloaded:        [Fill: Yes/No] · [count] problems
  MATH Dataset downloaded: [Fill: Yes/No] · [count] problems
  SciBench downloaded:     [Fill: Yes/No] · [count] problems

DATA PROCESSING:
  Processed JSON format:   [Fill: Done/Pending]
  Constraint sets built:   [Fill: Done/Pending]
  Pilot set (10 each):     [Fill: Done/Pending]
  Main set (40 each):      [Fill: Done/Pending]
  Random split seed:       [Fill: actual seed number]
  Adversarial bank:        [Fill: Done/Pending · how many written]

SYSTEM DESIGN DECISIONS:
  Constraint checker GSM8K:     [Fill: Symbolic/LLM-judge]
  Constraint checker SciBench:  [Fill: LLM-judge 3 raters]
  Context injection order:      T1 → T2 graph path → T3 last 5
  C4 override mechanism:        [Fill: Designed/Pending]
  Validation UI decision:       [Fill: FastAPI+HTML/Other]
  Neo4j graph schema:           [Fill: Finalized/Pending]
  Validation UI wireframe:      [Fill: Described/Pending]
```

---

## 📌 FULL PROJECT BRIEFING (For Context)

```
PROJECT:   HGEM — Human-Gated External Memory
CORE CLAIM: Memory persistence is causally isolatable in LLM drift

MEMORY ARCHITECTURE:
  T1 = Immutable (PostgreSQL locked) — physics laws
  T2 = Gated (Neo4j graph) — human-validated
  T3 = Ephemeral (Redis) — rolling 5 turns
  ChromaDB = Drift measurement ONLY (never retrieved)

WHY GRAPH DB (critical to remember):
  Flat list injection → AI sees GAPS → hallucinates bridges
  Graph traversal → returns CONNECTED ANCESTOR CHAIN
  No gaps = no hallucinated bridging = less drift

2×2 ABLATION (defends against reviewer confound):
  C6-VectorFlat  = human-gated + vector (no graph)
  C6-GraphFlat   = auto-persist + graph (no human)
  C6-GraphGated  = human-gated + graph = FULL HGEM

KEY FORMULAS:
  RDI(t) = |{ci violated}| / |C|
  β      = OLS slope of RDI(t) over steps
  ROI    = 72× (G=5s vs G*=360s at P=0.10, T_debug=60min)
```

---

## 🎯 WHAT CHAT 3 MUST ACCOMPLISH

Chat 3 has THREE jobs:

### JOB 1 — All 9 Conditions Verification
Verify each condition produces EXACTLY the right GPT context.
This is the core experiment — getting this wrong invalidates everything.

### JOB 2 — Pilot Study Planning and Execution (N=10)
Plan the N=10 pilot, run it, and calibrate all thresholds.

### JOB 3 — Calibration Analysis
Analyze pilot results to get τ*, θ*, κ, and confirm N for main study.

---

## 🔍 JOB 1 — CONDITION VERIFICATION

### What Each Condition Sends to GPT

This is the ONLY difference between conditions.
GPT model, version, temperature are IDENTICAL everywhere.

```
C1 — No Memory:
  API call contains:
    [System prompt]
    [Current question]
  NOTHING from previous turns
  ─────────────────────────────────────────
C2 — Full History + Shadow:
  API call contains:
    [System prompt]
    [Turn 1 user + Turn 1 AI]
    [Turn 2 user + Turn 2 AI]
    ... all previous turns ...
    [Current question]
  Shadow model runs same call simultaneously, logged separately
  ─────────────────────────────────────────
C3 — Auto-Summarize:
  API call contains:
    [System prompt]
    [GPT-4o summary of turns 1 through (t-5)]
    [Turn t-4 user + AI]
    [Turn t-3 user + AI]
    [Turn t-2 user + AI]
    [Turn t-1 user + AI]
    [Turn t-4 user + AI] (raw last 5)
    [Current question]
  ─────────────────────────────────────────
C4 — Random-Gated (CRITICAL):
  Human sees validation UI → makes A/R/D decision
  System SECRETLY flips coin → overrides with random result
  API call uses SYSTEM'S random result, not human's choice
  BOTH human decision AND system decision logged separately
  API call contains: same as C6-VectorFlat but entries
  are random 50% not semantic
  ─────────────────────────────────────────
C5 — RAG Memory:
  API call contains:
    [System prompt]
    [Top-5 most similar past turns by cosine similarity]
    [Current question]
  Retrieved by: ChromaDB query on past turn embeddings
  ─────────────────────────────────────────
C6-VectorFlat — 2×2 Ablation:
  API call contains:
    [System prompt]
    [Flat list of human-validated T2 entries in ChromaDB]
    [T3: last 5 turns]
    [Current question]
  No graph structure — just a flat list
  ─────────────────────────────────────────
C6-GraphFlat — 2×2 Ablation:
  API call contains:
    [System prompt]
    [Neo4j graph traversal → ancestor chain, auto-persisted]
    [T3: last 5 turns]
    [Current question]
  No human validation — graph without gating
  ─────────────────────────────────────────
C6-GraphGated — FULL HGEM:
  API call contains:
    [System prompt]
    === VERIFIED MEMORY ===
    T1: [All T1 immutable constants for this session]
    T2: [Neo4j graph traversal → ancestor path of
         validated nodes connected to current step]
    ===
    T3: [Last 5 turns]
    [Current question]
  T1 injected FIRST always
  Gate triggered when entropy(current_step) > θ*
  ─────────────────────────────────────────
C7 — Manual Inject:
  API call contains:
    [System prompt]
    [Manually-pasted formulas (at turns 10, 20, 30...)]
    [Last 5 turns]
    [Current question]
  No database. Human types key facts every 10 turns.
  ─────────────────────────────────────────
C-ADV — Adversarial (applied to C2 and C6):
  Same as base condition PLUS:
  At turns 5, 10, 15, 20...: inject one false claim from bank
  False claim appears as part of the conversation context
  Adversarial agent blind to T1/T2 contents
```

### Verification Test for Each Condition

For each condition, run one test problem and check:

```
□ C1: Prompt contains ONLY system prompt + question. Zero prior context.
□ C2: Prompt contains ALL prior turns in order. Grows each turn.
□ C3: Prompt contains one summary paragraph + last 5 raw turns.
□ C4: Both human_decision AND system_decision logged separately.
      System override (random) is what appears in the prompt.
□ C5: ChromaDB returns top-5 by cosine. Correct turns retrieved.
□ C6-VectorFlat: T2 appears as flat list. ChromaDB source.
□ C6-GraphFlat: Neo4j traversal returns chain. Not flat list.
□ C6-GraphGated: T1 appears first, then T2 chain, then T3 last 5.
□ C7: Injected formulas appear at correct 10-turn intervals.
□ C-ADV: False claim injection appears at turn 5, 10, 15...
```

---

## 🧪 JOB 2 — PILOT STUDY PLAN

### Who Participates in the Pilot

```
N = 10 participants total
  5 assigned to C2 (Full History)
  5 assigned to C6-GraphGated (Full HGEM)

Eligibility: STEM graduate students
Recruitment: Internal lab network or department mailing list

Note: C4, C6-VectorFlat, C6-GraphFlat, C7 are NOT in pilot
They are automated conditions (pilot tests C2 and C6 only)
```

### Pilot Session Protocol

```
PRE-SESSION (10 minutes):
  1. Participant reads and signs consent form
  2. Completes demographic survey:
     - Field of study
     - Years of graduate study
     - Familiarity with physics/math problems (1-5 scale)
  3. Receives briefing (NO hypothesis disclosure):
     C2: "You'll work with an AI assistant on problems"
     C6: "You'll work with an AI and occasionally review
          certain conclusions it makes"
  4. Completes ONE practice problem (not included in data)
     to learn the interface

MAIN SESSION (90-120 minutes):
  Problems: 5 from GSM8K pilot set + 5 from SciBench pilot set
  Order: counterbalanced across participants
  Rules: Researcher is SILENT during task
         Participant can think aloud (encouraged, not required)
         5-minute break allowed between the two benchmarks
         All interactions logged automatically

POST-SESSION (15 minutes):
  NASA-TLX survey (6 subscales — takes about 5 minutes)
  Three exit questions (researcher writes answers verbatim):
    Q1: "At any point did the model seem to forget something
         important that had been confirmed earlier?"
    Q2: "How would you describe the consistency of the
         model's memory throughout the session?"
    Q3: "Would you use a system like this in your own
         research work, and why?"
  Debrief: explain high-level study purpose
```

---

## 📐 JOB 3 — CALIBRATION ANALYSIS

### 5 Values to Calibrate From Pilot Data

```
═══════════════════════════════════════════════════════
CALIBRATION 1 — τ* (Drift Alert Threshold)
  Starting value: τ = 0.70
  Method: ROC curve analysis on pilot session data
  Input: Similarity(t) scores + ground truth drift labels
         (drift label = True if RDI(t) > 0.30)
  Output: τ* = threshold that maximizes F1 score
  Acceptable range: 0.60 ≤ τ* ≤ 0.80
  Record: τ*, AUC score, F1 at τ*

═══════════════════════════════════════════════════════
CALIBRATION 2 — θ* (Entropy Gate Threshold)
  Starting value: explore range 0.30 to 0.70
  Method: Find value where validation triggers for 20-30% of steps
  Too low: validator interrupted constantly → fatigue
  Too high: gate never fires → defeats purpose
  Acceptable range: 20-30% of steps trigger validation
  Record: θ*, actual trigger rate at θ*

═══════════════════════════════════════════════════════
CALIBRATION 3 — RDI Calculator Reliability (κ)
  This is the most critical calibration.
  If κ < 0.70: STOP. Do not run main experiment.
  Method:
    Take 20 random reasoning steps from pilot data
    Have 2 independent human raters score each step:
      For each constraint: violated (1) or satisfied (0)
    Compare: human rater 1 vs human rater 2 (inter-rater κ)
    Compare: calculator vs human rater 1
    Compare: calculator vs human rater 2
  Required: κ ≥ 0.70 on all three comparisons
  Record: κ values for all 3 comparisons

═══════════════════════════════════════════════════════
CALIBRATION 4 — Adversarial Noise Level
  Target: C2 shows CVR 40-60% under adversarial injection
           C6 shows CVR < 20% under adversarial injection
  Method: Run 5 test sessions with adversarial injection
  If C2 adversarial CVR < 30%: injection too weak → increase
  If C2 adversarial CVR > 80%: injection too strong → reduce
  Record: Calibrated injection frequency (every N turns)

═══════════════════════════════════════════════════════
CALIBRATION 5 — N for Main Study (Power Analysis)
  From pilot: collect β values for C2 and C6
  Compute Cohen's d from pilot: d = |β_C2 - β_C6| / pooled_SD
  Required N for power=0.80 and α=0.01 (Bonferroni adjusted)
  If required N ≤ 30: original plan is fine
  If required N > 30: increase before recruiting participants
  Record: pilot Cohen's d, required N, final confirmed N
```

### Pilot Stopping Rules

```
STOP immediately if ANY of these occur:

SR-1  RDI Calculator κ < 0.50
      The core metric is unreliable. Fix before anything.

SR-2  FPV (False-Positive Validation Rate) > 60%
      Validators are rubber-stamping. Retrain them.
      Define FPV = T2 entries approved that later found wrong.

SR-3  Zero RDI difference between C2 and C6 pilot sessions
      Possible early null signal. Consult professor before
      spending resources on N=60 main experiment.

SR-4  Participants cannot finish in 3 hours
      Reduce problem count. 5+5 becomes 3+3.

SR-5  System crashes or data loss
      Fix before running more sessions.

SR-6  τ* calibration falls outside [0.55, 0.85]
      Embedding model may be inadequate. Review ChromaDB setup.
```

---

## 📋 CHAT 3 COMPLETION CHECKLIST

```
CONDITION VERIFICATION:
□ All 9 conditions verified with test problem
□ C4 logs both human_decision AND system_decision separately
□ C6-GraphGated shows T1 → T2 chain → T3 in prompt
□ Shadow model runs alongside C6-GraphGated and logs separately
□ Adversarial injection fires at correct intervals

PILOT STUDY:
□ N=10 participants recruited (5 C2, 5 C6-GraphGated)
□ Consent forms signed and filed
□ All 10 sessions completed without system crashes
□ NASA-TLX surveys collected from all 10 participants
□ Exit interview notes written verbatim

CALIBRATION:
□ τ* calibrated (value: [fill])  Acceptable range: 0.60-0.80
□ θ* calibrated (value: [fill])  Trigger rate: 20-30%
□ RDI κ confirmed (value: [fill])  Required: ≥ 0.70
□ Adversarial injection frequency set (every [fill] turns)
□ N for main study confirmed (value: [fill])

NO STOPPING RULES TRIGGERED:
□ κ ≥ 0.70 confirmed
□ FPV < 60% confirmed
□ Pilot shows some RDI difference C2 vs C6
□ All participants finished within 3 hours
□ No data loss during pilot
```

---

## 📝 CHAT 3 FINDINGS LOG (Fill As You Work)

```
DATE STARTED:
DATE COMPLETED:

CONDITION VERIFICATION:
  All 9 conditions passed: [ YES / NO — issues: ]

PILOT RESULTS:
  N completed:        10
  C2 mean RDI at step 10:  [fill]
  C6 mean RDI at step 10:  [fill]
  Early signal:       [ C6 < C2 / No difference / C6 > C2 ]

CALIBRATED VALUES:
  τ* (drift threshold):       [fill]
  θ* (entropy threshold):     [fill]
  RDI calculator κ:           [fill]  PASS: ≥0.70 / FAIL: <0.70
  Adversarial frequency:      every [fill] turns
  Confirmed N per condition:  [fill]

FPV in C6 pilot:    [fill]%
HIL in C6 pilot:    [fill] decisions/step

STOPPING RULES:     [ None triggered / List which triggered ]

PROTOCOL CHANGES:   [ None / List changes made after pilot ]

READY FOR CHAT 4:   [ YES / NO — explain if NO ]
```

---

## 🤖 AI BEHAVIOR RULES FOR THIS CHAT

1. Context injection is the core of the experiment —
   get every condition exactly right
2. Never change the model version or temperature
3. C4 is the most sensitive condition — human decisions
   must be RECORDED even though overridden
4. Calibration is not optional — if κ < 0.70, stop and fix
5. If pilot shows no C2 vs C6 difference: do not dismiss it.
   Report honestly and help researcher decide next step.
6. At end of chat: generate the Chat 3 completion summary
   for researcher to copy into Chat 4

---
*CHAT 3 OF 5 | HGEM Research Project | MIT | April 2026*
*Previous: CHAT_2 complete | Next: CHAT_4_MAIN_EXPERIMENT.md*
