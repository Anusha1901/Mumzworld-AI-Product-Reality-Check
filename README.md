# 🍼 Mumzworld AI Product Reality Check

1. Track

Track A — AI Engineering Intern

---

2. Summary

This project builds an AI-powered product decision support system for mothers shopping on Mumzworld. It transforms raw product data and customer reviews into structured, decision-ready insights such as fit rating, strengths, drawbacks, and a confidence score. The system is designed for parents who struggle with conflicting reviews and decision fatigue, helping them quickly understand whether a product is suitable for their baby’s needs. It combines deterministic logic (confidence scoring, thresholds) with LLM-based reasoning (evidence extraction and verdict generation) to ensure outputs are both reliable and explainable.

---

3. Loom walkthrough

🎥 Loom Video: [Demo](https://www.loom.com/share/440665f4af46440e934b6c2a48fd25a7)

---

4. AI usage note 
* OpenRouter + poolside/laguna-m.1:free used for structured product analysis and multilingual output
* LLM used for reasoning, evidence extraction, and summarization
* Prompt engineering used to enforce strict JSON outputs and reduce hallucination
* AI assistants (ChatGPT / Claude/ VS code AI agent) used for pair programming, schema design, and refactoring
* Deterministic logic used to override critical decisions (fit rating, confidence)
---

5. Markdown deliverables
* EVALS.md → Evaluation design, test cases, results [Link](https://github.com/Anusha1901/Mumzworld-AI-Product-Reality-Check/blob/main/Evals.md)
* TRADEOFFS.md → Design decisions, architecture tradeoffs  [Link](https://github.com/Anusha1901/Mumzworld-AI-Product-Reality-Check/blob/main/Tradeoffs.md)

---


6. Time log 
* Problem scoping & design: ~2 hour
* Pipeline + LLM integration: ~1.5 hours
* Evaluation framework: ~1 hour
* UI + debugging: ~1.5 hour
* Total: ~6 hours
---

## 🚀 Setup & Run (≤ 5 minutes)

### 1. Clone repo
```bash
git clone https://github.com/Anusha1901/Mumzworld-AI-Product-Reality-Check
```
### 2. Create environment
```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```
### 3. Install dependencies
```bash
pip install -r requirements.txt
```
### 4. Add environment variables
Create .env file:
```bash
OPENROUTER_API_KEY=your_key_here
MODEL_ID=poolside/laguna-m.1:free
```

### 5. Run app
```bash
python -m streamlit run app/main.py
```

## 🧠 System Overview

The system evaluates products using a hybrid AI + rules pipeline:

### Flow:
    1. Load product + reviews
    2. Clean & deduplicate reviews
    3. Compute:
        - Confidence score (deterministic)
        - Fit rating (rule-based logic)
    4. Send structured prompt to LLM
    5. LLM generates:
          - strengths
          - drawbacks
          - verdict
          - evidence
    6. Override critical fields with deterministic logic
    7. Display in Streamlit UI

## 🧱 Architecture
```
    UI (Streamlit)
           ↓
    Pipeline Orchestrator
           ↓
    Review Cleaner
           ↓
    Confidence Scorer (rules)
           ↓
    Fit Rating Engine (rules)
           ↓
    LLM Analyzer (OpenRouter)
           ↓
    Structured Pydantic Output
```

## 🧠 Tooling

### Models / APIs
  1. OpenRouter API
  2. Model: poolside/laguna-m.1:free

Used for:
  * generating structured product analysis (fit, verdict, evidence)
  * multilingual output generation (English + Arabic)
  * extracting reasoning from reviews under strict JSON constraints


### 🔹 How AI tools were used

This project used a hybrid human + AI workflow:

1. Pair coding with LLMs

Used AI to:
* design pipeline architecture
* generate initial Pydantic schema
* draft prompt templates

Human step:
* validated logic consistency
* fixed over-aggressive LLM outputs

2. Iterative prompt engineering

Iterated prompts to:
* reduce hallucinated product claims
* enforce strict JSON output
* improve evidence grounding

3. Eval-driven refinement loop
    * Created 10+ test cases (normal + adversarial)
    * Ran batch evaluation via script
    * Adjusted:
       - confidence scoring weights
       - review cleaning rules
       - fit rating thresholds

4. Manual overrides (critical step)

    I explicitly overrode LLM decisions for:

    * fit_rating (now rule-based)
    * insufficient review cases
    * low-confidence scenarios

This was necessary because:

LLM alone was too optimistic in borderline cases.

## 🔹 What worked well
* OpenRouter integration was stable and fast
* Structured prompting with strict JSON worked reliably
* Pydantic validation prevented malformed outputs
* Rule-based confidence scoring improved consistency significantly
* Streamlit UI made debugging very visual


## 🔹 What did NOT work
* LLM-only fit rating (too optimistic, inconsistent)
* Small review datasets caused hallucinated confidence
* Without strict constraints, model “defaulted to Good Fit”

## 📊 Features
* Product-level AI evaluation
* Multi-language review support (EN + AR)
* Confidence-aware decision system
* Evidence-grounded verdict generation
* Streamlit interactive dashboard
* Eval pipeline for benchmarking outputs

## 📦 Future Improvements
* Sentiment weighting per review intensity (1-star vs 2-star impact scaling)
* Category-specific scoring (diapers ≠ strollers ≠ toys)
* Embedding-based review clustering
* RAG layer for product knowledge expansion
* LLM judge for secondary validation layer

## Note

This system was built as an AI-assisted but human-controlled decision pipeline, where LLMs are constrained rather than trusted blindly.

The goal was: structured, explainable, and reproducible product intelligence.






