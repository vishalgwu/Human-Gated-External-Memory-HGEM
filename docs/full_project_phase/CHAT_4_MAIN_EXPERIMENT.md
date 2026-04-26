# ████████████████████████████████████████████████████████████
# HGEM RESEARCH — CLAUDE PROJECT CHAT 4 OF 5
# Main Experiment Execution + Longitudinal Study
# ████████████████████████████████████████████████████████████

## 🤖 READ THIS FIRST — INSTRUCTIONS FOR CLAUDE

This is Chat 4 of 5 in a Claude Project on HGEM.
Chats 1, 2, and 3 are COMPLETE. Full summaries below.
Read EVERYTHING before responding to anything.

When finished reading say:
"HGEM Chat 4 loaded. Chats 1, 2, and 3 confirmed complete.
All calibrated values are noted. Ready for main experiment."

Then ask: "Would you like to start with participant scheduling,
automated condition batch runs, data quality monitoring,
or the longitudinal study protocol?"

---

## ✅ CHAT 1 COMPLETE — ENVIRONMENT AND LITERATURE

```
FOLDER STRUCTURE:  Created and shared with team
GPT VERSION:       gpt-4o-2024-08-06 · temp=0.0 · LOCKED
NOVELTY:           CONFIRMED — no paper has all 9 features
NOVELTY STATEMENT: [Fill from Chat 1 log]
BENCHMARKS:        GSM8K · MATH Dataset · SciBench
RELATED WORK:      800-word draft complete
RISK REGISTER:     Top 5 risks documented
```

## ✅ CHAT 2 COMPLETE — DATA AND SYSTEM DESIGN

```
DATASETS:
  GSM8K:        Downloaded · [count] problems
  MATH Dataset: Downloaded · [count] problems
  SciBench:     Downloaded · [count] problems
  Processed JSON format: Complete
  Constraint sets: Built and reviewed by subject expert
  Split seed: [Fill actual seed]
  Pilot set: 10 per benchmark (30 total)
  Main set:  40 per benchmark (120 total)
  Holdout:   Remaining (untouched until submission)
  Adversarial bank: 50 claims per benchmark (complete)

SYSTEM DESIGN:
  Constraint checker: [Fill: symbolic/LLM-judge per benchmark]
  C4 override mechanism: Designed and documented
  Neo4j graph schema: Finalized (nodes + 4 edge types)
  Validation UI: [Fill: FastAPI+HTML / other]
  Context injection order: T1 → T2 graph path → T3
  All 8 components: Design decisions documented
```

## ✅ CHAT 3 COMPLETE — CONDITIONS AND PILOT

```
CONDITION VERIFICATION: All 9 conditions passed
  C4: Human + system decisions logged separately ✓
  C6-GraphGated: T1→T2→T3 injection confirmed ✓
  Shadow model: Running alongside C6 sessions ✓
  Adversarial: Firing at correct intervals ✓

PILOT STUDY (N=10): Complete
  C2 mean RDI step 10: [Fill]
  C6 mean RDI step 10: [Fill]
  Early signal: [Fill: C6 < C2 / No difference]

CALIBRATED VALUES (USE THESE IN MAIN EXPERIMENT):
  τ* drift threshold:         [Fill exact value]
  θ* entropy threshold:       [Fill exact value]
  RDI calculator κ:           [Fill] — CONFIRMED ≥ 0.70
  Adversarial injection rate: every [Fill] turns
  N per condition confirmed:  [Fill]

PROTOCOL CHANGES FROM PILOT: [Fill: None / List changes]
STOPPING RULES: None triggered ✓
```

---

## 📌 CORE PROJECT FACTS (DO NOT CHANGE ANY OF THESE)

```
EXPERIMENT MODEL:   GPT-4o · gpt-4o-2024-08-06 · temp=0.0
BENCHMARKS:         GSM8K · MATH Dataset · SciBench
N PER CONDITION:    [Fill from pilot power analysis]
TOTAL HUMAN N:      [N] × 4 human conditions
SIGNIFICANCE:       Bonferroni α = 0.05/5 = 0.01
MIN EFFECT SIZE:    Cohen's d ≥ 0.5

τ*:  [Fill] — drift alert fires when cosine similarity < τ*
θ*:  [Fill] — gate fires when entropy > θ*

INJECTION ORDER:    T1 → T2 graph ancestor chain → T3 last 5
C4 RULE:            Record human choice, override with random
SHADOW MODEL:       Silent C2 runs alongside every C6 session
```

---

## 🎯 WHAT CHAT 4 MUST ACCOMPLISH

Chat 4 has FOUR jobs:

### JOB 1 — Pre-Registered Analysis Plan (Lock First)
Write and commit this BEFORE unblinding any data.

### JOB 2 — Automated Condition Batch Runs
Run C1, C2, C3, C5, C6-GraphFlat in batch (no human needed).

### JOB 3 — Human Participant Sessions
Run C4, C6-VectorFlat, C6-GraphGated, C7 with real participants.

### JOB 4 — Longitudinal Study
Run two-session transfer experiment after main study completes.

---

## 📋 JOB 1 — PRE-REGISTERED ANALYSIS PLAN

### Write This Before Looking at Any Results

This document gets committed to GitHub with a timestamp BEFORE
any data file is opened for analysis. Once committed, it cannot
be changed. Any analysis done after unblinding that was NOT in
this plan must be labeled EXPLORATORY.

```
PRE-REGISTERED ANALYSIS PLAN
Project: HGEM Research
Date committed: [must be before unblinding]
Committed by: [researcher name]

PRIMARY TESTS (all use Welch t-test, Bonferroni α = 0.01):

  Test T1 — H1:
    Compare: β_C2 vs β_C1
    Direction: C2 > C1 (one-tailed)
    Predicts: Full memory causes MORE drift than no memory

  Test T2 — H2 vs Full History:
    Compare: β_C6-GraphGated vs β_C2
    Direction: C6 < C2 (one-tailed)
    Predicts: HGEM reduces drift vs full history

  Test T3 — H2 vs Summarization:
    Compare: β_C6-GraphGated vs β_C3
    Direction: C6 < C3 (one-tailed)

  Test T4 — H2 vs RAG:
    Compare: β_C6-GraphGated vs β_C5
    Direction: C6 < C5 (one-tailed)

  Test T5 — H2a vs H2b (MOST IMPORTANT):
    Compare: β_C6-GraphGated vs β_C4 (random gate)
    Direction: C6 < C4 (one-tailed)
    Interpretation:
      If significant (p<0.01): H2a supported — semantic
        judgment is the mechanism, not just interaction
      If not significant: H2b supported — the ACT of
        validation drives improvement, not what is chosen

  Test T6 — 2×2 Graph vs Vector:
    Compare: β_C6-GraphGated vs β_C6-VectorFlat
    Direction: C6-Graph < C6-Vector (one-tailed)
    Predicts: Graph structure adds value over flat list

  Test T7 — H3 Adversarial Shield:
    Compare: CVR_C6-ADV vs CVR_C2-ADV
    Direction: C6-ADV < C2-ADV (one-tailed)

  Test T8 — C7 Structure vs Content:
    Compare: β_C6-GraphGated vs β_C7
    Direction: C6 < C7 (one-tailed)
    Predicts: Formal HGEM adds value vs manual injection

SECONDARY ANALYSES (exploratory — labeled as such in paper):
  - Effect size by benchmark (GSM8K vs MATH vs SciBench)
  - MCR → RDI mediation analysis (MCR as mediator)
  - NASA-TLX ANOVA across human conditions
  - Shadow model divergence onset distribution

MINIMUM EFFECT SIZE: Cohen's d ≥ 0.5
POWER: 0.80 at α = 0.01
```

---

## ⚙️ JOB 2 — AUTOMATED CONDITION BATCHES

### Which Conditions Are Fully Automated

```
AUTOMATED (no human participants):
  C1 — No Memory:       50 sessions × 3 benchmarks = 150 total
  C2 — Full History:    50 sessions × 3 benchmarks = 150 total
                        Shadow model runs alongside each
  C3 — Auto-Summarize:  50 sessions × 3 benchmarks = 150 total
  C5 — RAG Memory:      50 sessions × 3 benchmarks = 150 total
  C6-GraphFlat:         50 sessions × 3 benchmarks = 150 total

ADVERSARIAL AUTOMATED:
  C2-ADV: 20 sessions (SciBench primary)
  (C6-ADV uses human participants)
```

### Automated Batch Quality Checks (Run After Every 10 Sessions)

```
CHECK 1: GPT version in every log
  Look in experiment_events.llm_call for model field
  Must equal: gpt-4o-2024-08-06
  If different: STOP. Investigate immediately.

CHECK 2: RDI score range
  All RDI values must be 0.0 to 1.0 inclusive
  Any value outside: bug in calculator. Fix immediately.

CHECK 3: Step-level logging completeness
  Every session folder must have RDI at EVERY step
  No gaps in step numbers
  Missing step: exclude session, add replacement run

CHECK 4: Shadow model data
  Every C2 session must have shadow_comparison entries
  Same number of rows as main session steps
  Missing: shadow runner failed. Fix and rerun.

CHECK 5: T2 graph integrity (C6-GraphFlat only)
  Every Neo4j edge must point to an existing node
  No dangling edges
  If found: fix graph and log the issue
```

---

## 👥 JOB 3 — HUMAN PARTICIPANT SESSIONS

### Which Conditions Require Human Participants

```
HUMAN REQUIRED:
  C4 — Random-Gated:        N=[Fill] participants
  C6-VectorFlat:            N=[Fill] participants
  C6-GraphGated (Full HGEM): N=[Fill] participants
  C7 — Manual Inject:       N=[Fill] participants
  C6-ADV (Adversarial):     20 sessions (subset of C6-GraphGated)

ASSIGNMENT: Each participant does ONE condition only
TASK ORDER: Latin Square counterbalancing across benchmarks
  Participant A: GSM8K → MATH → SciBench
  Participant B: MATH → SciBench → GSM8K
  Participant C: SciBench → GSM8K → MATH
  (Cycle repeats for all participants in each condition)
```

### Participant Session Checklist (Run for Every Session)

```
PRE-SESSION:
□ IRB consent form signed and filed
□ Demographic survey completed (field, years, familiarity)
□ Condition-specific briefing given (no hypothesis disclosure)
  C4/C6: "You'll review certain AI conclusions occasionally"
  C7: "You'll periodically add key facts to the conversation"
□ Practice problem completed (not in data)
□ Researcher confirmed all systems running before start

DURING SESSION:
□ Researcher stays silent — no help given
□ Think-aloud is encouraged but participant is not forced
□ 5-minute break allowed between benchmarks
□ Note any technical issues in session notes immediately

C4 SPECIAL RULE:
□ Human's validation decisions go to UI and are logged
□ System overrides with random coin — participant does not know
□ Both human_decision AND system_decision logged separately
□ Random seed for this session recorded in experiment_events

POST-SESSION:
□ NASA-TLX survey completed (6 subscales)
□ Three exit questions asked verbatim:
    Q1: "At any point did the model seem to forget something
         important that had been confirmed earlier?"
    Q2: "How would you describe the consistency of the model's
         memory throughout the session?"
    Q3: "Would you use a system like this in your own research,
         and why or why not?"
□ Answers written VERBATIM by researcher
□ Debrief given:
    All conditions: high-level study purpose explained
    C4 participants: informed their decisions were overridden
    Explain WHY this was necessary for the research
□ Session metadata JSON updated with completion time
```

### Mid-Experiment Stopping Rules

```
STOP and investigate if ANY of these occur:

SR-1  3σ outlier in RDI from first 20 participants
      Do not continue until cause is found

SR-2  Session missing step-level logs
      Exclude that session. Add replacement participant.

SR-3  GPT model version changed mid-experiment
      PAUSE ALL SESSIONS until version is confirmed/re-pinned

SR-4  FPV rises above 50% in C6-GraphGated sessions
      Validators may be rubber-stamping. Retrain before continuing.

SR-5  System data loss from any session
      Stop. Recover what is possible. Log the loss. Add replacement.
```

---

## 🔄 JOB 4 — LONGITUDINAL STUDY

### Design

```
WHO:   Subset of already-completed participants
       n=20 from C2 (Full History) — same people
       n=20 from C6-GraphGated (Full HGEM) — same people

WHEN:  7 calendar days after their Session 1

WHAT:
  Model is completely RESET for everyone
  C2 participants: given their full Session 1 chat transcript
                   to read before resuming
  C6 participants: ONLY T1 and T2 HVEM is loaded
                   No chat history. No transcript given.
  Both groups resume the SAME task from Session 1
  Two independent raters score TRC for each session
```

### Metric: Time-to-Reconstruct Context (TRC)

```
TRC = number of reasoning steps to return to equivalent
      task progress as where Session 1 ended

How to measure:
  Two raters independently watch the session
  Each marks the step where they judge equivalent progress
  TRC = mean of two rater scores
  If raters disagree by > 3 steps: discuss and reconcile
  Measure inter-rater κ — must be ≥ 0.70

HYPOTHESIS: C6-GraphGated TRC < C2 TRC by ≥ 35%
  This means: HVEM (curated memory graph) lets researchers
  resume much faster than reading a full chat transcript

Also measure:
  Token count in C2 transcript vs C6 HVEM at session 2 start
  This is the Token Efficiency Ratio (TER) for longitudinal
```

### Longitudinal Session Protocol

```
PRE-SESSION 2 (10 minutes):
  C2 participants:
    Given printed/screen copy of their Session 1 transcript
    "Read this to get back up to speed. Take as long as needed."
  C6 participants:
    Told "your verified memory from last session has been loaded"
    No transcript given. Model already loaded with HVEM.
  Both: NOT told what to look for — natural reconstruction only

SESSION 2 MAIN (60-90 minutes):
  Resume task from where Session 1 ended
  Same benchmark, same problem
  Two raters observe (one live, one from recording)
  Each rater independently marks TRC step

POST-SESSION 2 (10 minutes):
  Comparison survey:
    Q1: "How easily could you pick up where you left off
         compared to starting fresh?"
    Q2: "Did the memory aid or hinder your thinking today?"
    Q3: "Compare this to resuming from a document vs resuming
         from memory — which did it feel more like?"
  Final debrief
```

---

## 📊 DATA EXPORT FOR CHAT 5

After ALL data is collected, export these files:
```
05_DATA/analysis_ready/main_results.csv
  Columns: session_id, condition, benchmark, step,
           rdi_score, cvr_score, t2_similarity,
           human_decision, system_decision (C4 only),
           beta_drift_rate (per session)

05_DATA/analysis_ready/shadow_model_results.csv
  Columns: session_id, step, hgem_rdi, shadow_rdi,
           divergence_detected, divergence_onset_step

05_DATA/analysis_ready/adversarial_results.csv
  Columns: session_id, condition, step, claim_injected,
           cvr_before_injection, cvr_after_injection

05_DATA/analysis_ready/longitudinal_results.csv
  Columns: participant_id, condition, trc_rater1,
           trc_rater2, trc_mean, token_count_context,
           comparison_survey_responses

05_DATA/surveys/
  nasa_tlx_results.csv — all 6 subscale scores per participant
  exit_interviews.csv  — verbatim answers to 3 questions
```

---

## 📋 CHAT 4 COMPLETION CHECKLIST

```
PRE-REGISTERED PLAN:
□ Plan written and committed to GitHub BEFORE unblinding
□ Commit timestamp recorded: [fill]

AUTOMATED CONDITIONS:
□ C1 complete: [fill] sessions
□ C2 + shadow complete: [fill] sessions
□ C3 complete: [fill] sessions
□ C5 complete: [fill] sessions
□ C6-GraphFlat complete: [fill] sessions
□ C2-ADV complete: 20 sessions

HUMAN CONDITIONS:
□ C4 complete: N=[fill] participants
□ C6-VectorFlat complete: N=[fill] participants
□ C6-GraphGated complete: N=[fill] participants
□ C7 complete: N=[fill] participants
□ C6-ADV complete: 20 sessions

LONGITUDINAL:
□ n=20 C2 Session 2 complete
□ n=20 C6-GraphGated Session 2 complete
□ TRC scored by 2 independent raters for all 40 sessions
□ TRC inter-rater κ ≥ 0.70 confirmed

DATA QUALITY:
□ No sessions with missing step-level logs
□ GPT version consistent across all sessions
□ All stopping rules passed (or issues documented)
□ All 5 analysis-ready CSV files exported

READY FOR ANALYSIS:
□ Pre-registered plan committed before unblinding
□ Data unblinding date recorded: [fill]
□ Result scenario identified: [A / B / C / D]
```

---

## 📝 CHAT 4 FINDINGS LOG

```
DATE STARTED:
DATE COMPLETED:

PRE-REGISTERED PLAN COMMIT DATE: [must be before unblinding]
DATA UNBLINDING DATE:

MAIN EXPERIMENT RESULTS (after unblinding):
  T1 (H1 — C2 vs C1):          p=[fill]  d=[fill]  sig=[Y/N]
  T2 (H2 — C6 vs C2):          p=[fill]  d=[fill]  sig=[Y/N]
  T3 (H2 — C6 vs C3):          p=[fill]  d=[fill]  sig=[Y/N]
  T4 (H2 — C6 vs C5):          p=[fill]  d=[fill]  sig=[Y/N]
  T5 (H2a/H2b — C6 vs C4):     p=[fill]  d=[fill]  sig=[Y/N]
                                 Mechanism: [H2a / H2b]
  T6 (Graph — C6-Graph vs Vec): p=[fill]  d=[fill]  sig=[Y/N]
  T7 (H3 — Adversarial):        p=[fill]  d=[fill]  sig=[Y/N]
  T8 (C7 — Structure test):     p=[fill]  d=[fill]  sig=[Y/N]

LONGITUDINAL:
  C6 mean TRC:  [fill] steps
  C2 mean TRC:  [fill] steps
  Reduction:    [fill]%  (target: ≥35%)
  TRC κ:        [fill]   (required: ≥0.70)

RESULT SCENARIO: [ A / B / C / D ]
  A = H1+H2+H2a+H3 confirmed
  B = H1+H2 confirmed, H2b wins (random gate ≈ HGEM)
  C = Graph structure explains most improvement
  D = Null — memory not a drift driver

UNEXPECTED FINDINGS: [fill honestly]

READY FOR CHAT 5: [ YES / NO ]
```

---

## 🤖 AI BEHAVIOR RULES FOR THIS CHAT

1. Pre-registered plan must be written BEFORE any results
   are discussed. This is non-negotiable.
2. Any analysis NOT in the pre-registered plan = EXPLORATORY.
   Label it clearly. Never use it for primary claims.
3. If T5 shows C6 ≈ C4 (H2b): do not reframe this as
   "nearly significant." Report H2b honestly — it's still good.
4. If result scenario D occurs (null): help researcher write
   the null result paper. Do not look for ways to salvage H1.
5. TRC inter-rater κ must be checked — if < 0.70, flag it
   before reporting TRC results.
6. At end of chat: generate Chat 4 completion summary
   for researcher to copy into Chat 5.

---
*CHAT 4 OF 5 | HGEM Research Project | MIT | April 2026*
*Previous: CHAT_3 complete | Next: CHAT_5_ANALYSIS_WRITING.md*
