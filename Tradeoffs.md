# ⚖️ Tradeoffs & Design Decisions

🎯 Why this problem?

Mothers shopping on Mumzworld face a high-friction decision problem:

* Hundreds of similar products per category
* Conflicting reviews (5★ vs 1★ with no clear conclusion)
* Hidden drawbacks only visible after purchase
* High stakes decisions (health, safety, comfort of the baby)

This leads to:

* decision fatigue
* low trust in product selection
* higher return rates

---

## 💡 Why this is a high-leverage AI problem

This problem is not solvable with:

* filters (too generic)
* ratings (too shallow)
* manual curation (not scalable)

Because:

the signal is buried inside unstructured, messy reviews

AI is required to:

* synthesize large volumes of text
* extract consistent patterns
* highlight both strengths and drawbacks
* adapt output to user context (baby age, concern)
---

## 🧠 Model Choice

### Selected:
- OpenRouter + `poolside/laguna-m.1:free`

### Why:
- Fast iteration
- Cheap/free experimentation
- Good structured JSON compliance

---

## 🏗️ Architecture Choice

### Hybrid system:

| Component | Type |
|----------|------|
| Confidence | Deterministic |
| Fit rating | Rule-based |
| Explanation | LLM |

### Why not full LLM?

Because:
- LLM is inconsistent on borderline cases
- Tends to overestimate product quality
- Hard to reproduce outputs reliably

---

## ⚖️ Key Tradeoff #1: Deterministic vs LLM decisions

### Option A (Rejected):
- LLM decides everything

❌ Issues:
- hallucinated confidence
- unstable fit ratings
- poor reproducibility

### Option B (Chosen):
- Rules decide critical fields
- LLM explains results

✅ Benefits:
- predictable outputs
- easier evaluation
- production-safe behavior

---

## ⚖️ Key Tradeoff #2: Simplicity vs realism

We avoided:
- embedding models
- sentiment transformers
- complex NLP pipelines

Instead used:
- clean rules
- structured prompts

Reason:
clarity > complexity for assessment context

---

## ⚖️ Key Tradeoff #3: Review aggregation logic

We simplified:
- no per-sentence sentiment parsing
- no topic modeling

Instead:
- rating + length + count heuristics

This improves:
- speed
- interpretability
- debugging

---

## 🧠 Handling Uncertainty

We explicitly model uncertainty via:

- ConfidenceScorer
- review count thresholds
- fallback "Insufficient Data" state

If:
- reviews < 5 → system refuses strong opinion

---

## ✂️ What we cut intentionally

- real-time web scraping
- multi-model ensemble
- vector database / RAG layer
- sentiment transformer models

Reason:
focus was structured reasoning, not infrastructure complexity

---

## 🚀 What we would build next

- sentiment weighting per review severity (1★ > 2★ impact scaling)
- category-aware scoring system
- embedding-based clustering of review themes
- second-pass LLM verifier (“AI judge layer”)
- explainability heatmap (why fit rating was assigned)

---

## 🧑‍💻 Final philosophy

LLMs are used for interpretation, not authority.

All critical decisions are:
- deterministic
- testable
- reproducible
- deterministic
- testable
- reproducible
