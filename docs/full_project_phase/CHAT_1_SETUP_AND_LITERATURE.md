# ████████████████████████████████████████████████████████████
# HGEM RESEARCH — CLAUDE PROJECT CHAT 1 OF 5
# Environment Setup + Literature Review + Novelty Lock
# ████████████████████████████████████████████████████████████

## 🤖 READ THIS FIRST — INSTRUCTIONS FOR CLAUDE

You are working on a PhD-level research project called HGEM.
This is Chat 1 of 5 in a Claude Project.
This document contains everything you need to start.
There is NO prior chat history to reference — this is the beginning.

When you finish reading this document say exactly:
"HGEM Chat 1 loaded. I understand the full project. Ready to begin Step 1 work."

Then ask: "Which part of Chat 1 would you like to start with — environment
setup checklist, literature search, or novelty gap table?"

---

## 📌 PROJECT IDENTITY — MEMORIZE THIS

```
PROJECT NAME:    Human-Gated External Memory (HGEM)

FULL TITLE:      Mitigating Parametric Drift in LLM Agent Systems
                 using Human-Gated External Memory with Tiered
                 Persistence, Graph Memory, and Adversarial Robustness

RESEARCHER:      [Your Name] — PhD Candidate — MIT

CORE CLAIM:      Memory persistence is a causally isolatable variable
                 in LLM parametric drift. Restricting persistence to
                 human-validated graph-structured states measurably
                 reduces drift in long-horizon tasks.

EXPERIMENT LLM:  GPT-4o — version gpt-4o-2024-08-06 — PINNED
                 Temperature = 0.0 for ALL conditions
                 Claude is used for research assistance only

BENCHMARKS:      GSM8K · MATH Dataset · SciBench
                 (HotpotQA was considered and REMOVED)
```

---

## 🧠 THE PROBLEM IN PLAIN ENGLISH

When an AI works on a long engineering task (e.g. designing a
propulsion system over 50 steps), it gradually gives wrong answers.
By step 40, the model may contradict facts it confirmed at step 3.

Why? Because ALL content in the session — confirmed formulas,
discarded ideas, casual chat, wrong guesses — is treated equally
when the AI generates its next response.

**HGEM's solution:**
Only human-validated reasoning states are allowed to persist in
long-term memory. Memory is stored in a graph database (Neo4j)
so validated facts are connected — not fragmented.

---

## 🏗️ THE THREE-TIER MEMORY ARCHITECTURE

```
T1 — IMMUTABLE
  Physics laws + absolute constants
  Set ONCE at session start
  CANNOT be changed by AI or anyone
  Example: F=ma · T_melt(W)=3422°C · α=4.5×10⁻⁶/°C

T2 — GATED (stored in Neo4j graph)
  Human-validated design conclusions
  Each entry = a NODE in the graph
  Relationships between entries = EDGES (DEPENDS_ON, LEADS_TO,
  CONTRADICTS, CONFIRMS)
  Triggered by uncertainty estimator (semantic entropy > θ*)

T3 — EPHEMERAL
  Last 5 turns only — auto-deleted on rolling basis
  No human action needed
  Captures: tangents, greetings, discarded ideas
```

**Why Graph DB (Neo4j) for T2, NOT Vector DB?**
If validated facts are stored as a flat list, the AI sees GAPS
between them and halluccinates bridging assumptions — causing new
drift. Graph traversal returns a CONNECTED CHAIN of facts.
No gaps. No hallucination needed.

**The 2×2 Ablation (critical for reviewers):**
A reviewer will say "your improvement comes from graph structure,
not human gating." We defend with a 2×2 design:

```
                  VECTOR DB       GRAPH DB
AUTO-PERSIST  |  C2 baseline  |  C6-GraphFlat  |
HUMAN-GATED   |  C6-VectorFlat|  C6-GraphGated | ← FULL HGEM
```

---

## 🔬 ALL 5 HYPOTHESES (LOCKED — DO NOT CHANGE)

```
H1  Contamination: Memory contamination contributes to drift
    (δ ≥ 0.15 in CVR at p < 0.05, Cohen's d ≥ 0.5)

H2  Intervention: HGEM reduces β (drift growth rate) vs baselines

H2a Mechanism A: Drift reduction = exclusion of bad states
    (C6-GraphGated >> C4 random-gate → H2a supported)

H2b Mechanism B: Drift reduction = act of human validation itself
    (C6-GraphGated ≈ C4 random-gate → H2b supported)
    NOTE: H2b is still publishable — different scientific question

H3  Shield: T1 immutability blocks adversarial corruption
    (C6 CVR < 20% under adversarial · C2 CVR > 40%)
```

---

## 🧪 ALL 9 EXPERIMENTAL CONDITIONS

```
C1  No Memory          No persistence. Lower bound.
C2  Full History       All turns. Upper contamination bound.
                       Also runs as SHADOW MODEL silently.
C3  Auto-Summarize     GPT-4o sliding window summary.
C4  Random-Gated       Human sees UI but system overrides with
                       random 50%. H2a vs H2b ablation.
                       HUMAN DOES NOT KNOW DECISIONS ARE OVERRIDDEN.
C5  RAG Memory         Top-k vector retrieval. SOTA comparison.
C6-VectorFlat          Human-gated + flat vector. 2×2 ablation.
C6-GraphFlat           Auto-persist + Neo4j graph. 2×2 ablation.
C6-GraphGated          FULL HGEM. Human-gated + Neo4j graph.
C7  Manual Inject      Human pastes formulas every 10 turns.
C-ADV Adversarial      Secondary AI injects false claims every
                       5 turns. Applied to C2 and C6-GraphGated.
```

---

## 💾 STORAGE STACK

```
PostgreSQL  → T1 immutable store (locked — no UPDATE/DELETE)
             + experiment event log
             + conflict log
Neo4j       → T2 validated memory GRAPH (nodes + typed edges)
Redis       → T3 ephemeral buffer (rolling 5 turns, auto-TTL)
ChromaDB    → Drift MEASUREMENT ONLY — NOT used for retrieval
             Embeds T2 nodes, measures cosine similarity
             to compute RDI. NEVER injected into GPT context.
```

---

## 📐 KEY FORMULAS

```
RDI(t) = |{ci violated by r_t}| / |C|
β      = OLS slope of RDI(t) over steps
CVR    = violations / total constraint checks
Similarity(t) = cos(embed(r_t), Centroid(T2_t))
Entropy(s_t)  = mean pairwise cosine distance of
                k=10 GPT samples at temperature=1.0
HGEM_ROI = G* / G   where G*=3600×P(failure)×T_debug
           (at G=5s, T_debug=60min, P=0.10 → ROI=72×)
```

---

## 📚 PRIOR WORK DIFFERENTIATIONS (MEMORIZE)

```
MemGPT (2023)    → Manages WHERE memory lives. HGEM controls
                   WHETHER it persists. Different question.

Voyager (2023)   → Stores executable SKILLS. HGEM stores
                   REASONING CHAINS. Different content type.

RLHF (2022)      → Human feedback → WEIGHT updates at training.
                   HGEM → memory structure at INFERENCE. Different layer.

PRMs (2023)      → Verify steps WITHIN one session.
                   HGEM persists facts ACROSS sessions (weeks).
                   Categorical distinction.

LangGraph HITL   → Engineering workflow checkpoints.
                   HGEM treats validation as research variable.
```

---

## 🎯 WHAT THIS CHAT (CHAT 1) MUST ACCOMPLISH

Chat 1 has TWO jobs:

### JOB 1 — Environment Setup Checklist
Help the researcher create and verify the complete environment.
Work through this list item by item:

```
□ 1.1  Create master folder structure (see structure below)
□ 1.2  Record tool installation checklist format
□ 1.3  Create versions.txt template
□ 1.4  Create .env.template (key names only, no values)
□ 1.5  Create change_log.md template
□ 1.6  Confirm GPT model version string is documented:
        MODEL_VERSION = gpt-4o-2024-08-06
□ 1.7  Confirm all 4 databases are in setup plan:
        PostgreSQL · Neo4j · Redis · ChromaDB
```

### JOB 2 — Literature Review
Search for papers that could threaten the novelty claim.
Run these searches in order and fill the novelty gap table:

```
Search 1: "memory persistence causal LLM reasoning"
Search 2: "human-gated memory language model agent"
Search 3: "long-horizon reasoning drift LLM"
Search 4: "parametric drift language model"
Search 5: "episodic memory working memory LLM agent"
Search 6: "tiered memory LLM validation"
Search 7: "graph memory LLM reasoning"
Search 8: "adversarial memory injection language model"
```

**Novelty Gap Table to Fill:**

| Feature | HGEM | Paper 1 | Paper 2 | Paper 3 | Paper 4 |
|---------|------|---------|---------|---------|---------|
| Persistence as causal variable | ✅ | | | | |
| Random-gate ablation | ✅ | | | | |
| Human semantic gating at inference | ✅ | | | | |
| Graph-structured validated memory | ✅ | | | | |
| 2×2 storage vs gating ablation | ✅ | | | | |
| Adversarial robustness test | ✅ | | | | |
| Shadow model protocol | ✅ | | | | |
| Economic ROI analysis | ✅ | | | | |
| Longitudinal 2-session design | ✅ | | | | |

**STOP RULE:** If any paper has 6+ matching features, report
immediately: "NOVELTY AT RISK — needs professor consultation."

---

## 📁 MASTER FOLDER STRUCTURE TO CREATE

```
HGEM_RESEARCH/
│
├── 00_PROJECT_DOCS/
│   ├── proposal/
│   ├── workflow/
│   ├── meeting_notes/
│   └── change_log.md
│
├── 01_SETUP/
│   ├── environment/
│   │   ├── versions.txt
│   │   └── install_checklist.md
│   ├── credentials/
│   │   └── .env.template
│   └── neo4j_config/
│
├── 02_DATASETS/
│   ├── raw/
│   │   ├── gsm8k/
│   │   ├── math_dataset/
│   │   └── scibench/
│   ├── processed/
│   ├── splits/
│   │   ├── pilot_set/
│   │   ├── main_set/
│   │   └── holdout_set/
│   ├── constraints/
│   └── adversarial/
│
├── 03_SYSTEM/
│   ├── memory_policies/
│   ├── database/
│   │   ├── postgresql/
│   │   ├── neo4j/
│   │   └── chromadb/
│   ├── api_layer/
│   ├── drift_engine/
│   ├── uncertainty_estimator/
│   ├── adversarial_agent/
│   ├── shadow_model/
│   └── validation_ui/
│
├── 04_EXPERIMENT/
│   ├── pilot/
│   ├── main/
│   ├── longitudinal/
│   └── adversarial/
│
├── 05_DATA/
│   ├── raw_logs/
│   ├── cleaned/
│   ├── analysis_ready/
│   └── surveys/
│
├── 06_ANALYSIS/
│   ├── pre_registered_plan.md
│   ├── primary_tests/
│   ├── mediation/
│   ├── figures/
│   └── exploratory/
│
└── 07_PAPER/
    ├── drafts/
    ├── submission/
    └── reviewer_responses/
```

---

## ✅ CHAT 1 COMPLETION — WHAT MUST BE DONE BEFORE CHAT 2

When Chat 1 is finished, confirm ALL of these are done:

```
□ Folder structure created and shared with team
□ versions.txt template created
□ .env.template created (names only, no values)
□ GPT model version documented: gpt-4o-2024-08-06
□ Literature search completed (all 8 queries)
□ Novelty gap table filled with real papers
□ No STOP RULE triggered (no paper with 6+ matches)
□ 3-sentence novelty lock statement written
□ Related work section drafted (800-1000 words)
□ Benchmark validation confirmed for GSM8K/MATH/SciBench
□ Risk register filled (top 5 risks)
```

**At the end of Chat 1, ask Claude:**
"Generate the Chat 1 completion summary for Chat 2"
Save that summary — it goes at the top of Chat 2.

---

## 📝 CHAT 1 FINDINGS LOG (Fill As You Work)

```
DATE STARTED:
DATE COMPLETED:

NOVELTY STATUS:         [ CONFIRMED / AT RISK ]
CLOSEST COMPETING PAPER:
WHY WE ARE DIFFERENT:

NOVELTY LOCK STATEMENT (3 sentences):
  Sentence 1:
  Sentence 2:
  Sentence 3:

BENCHMARK CHANGES:
  GSM8K:        [ Keep ]
  MATH Dataset: [ Keep ]
  SciBench:     [ Keep ]

TOP 3 RISKS:
  1.
  2.
  3.

FOLDER STRUCTURE: [ Created / Not yet ]
GPT VERSION LOCKED: [ gpt-4o-2024-08-06 / different: ]
```

---
*CHAT 1 OF 5 | HGEM Research Project | MIT | April 2026*
*Next: Upload CHAT_2_SYSTEM_BUILD.md to continue*
