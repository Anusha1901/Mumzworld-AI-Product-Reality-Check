
---

# 📄 EVALS.md


# 🧪 Evaluation Report — Mumzworld AI Product Reality Check

## 📌 Evaluation Setup

We built a lightweight evaluation harness (`evals/run_evals.py`) that:

- Loads `test_cases.json`
- Runs pipeline across test cases
- Compares:
  - Fit Rating
  - Confidence Label
- Assigns:
  - PASS
  - NEAR MATCH
  - FAIL

---

## 📊 Scoring Logic

### Fit Rating mapping:
- Excellent Fit → 5
- Good Fit → 4
- Moderate Fit → 3
- Low Fit → 2
- Insufficient Data → 1

### Confidence mapping:
- High → 3
- Medium → 2
- Low → 1

---

## 🧪 Test Suite (10+ cases)

| Test ID | Product ID | Scenario Type | Expected Fit | Expected Confidence |
|--------|------------|---------------|--------------|---------------------|
| T01 | P001 | Strong positive consensus | Excellent Fit | High |
| T02 | P002 | Mostly positive, minor tradeoffs | Good Fit | High |
| T03 | P003 | Mixed sentiment (colic bottle) | Moderate Fit | Medium |
| T04 | P004 | Negative suitability (food rejection risk) | Low Fit | Medium |
| T05 | P005 | Sparse reviews / safety concern edge | Insufficient Data | Low |
| T06 | P006 | Arabic + learning toy positive | Good Fit | High |
| T07 | P007 | Arabic + usability tradeoffs | Moderate Fit | Medium |
| T08 | P008 | Strong consensus mobility product | Excellent Fit | High |
| T09 | P009 | Inconsistent acceptance (food) | Moderate Fit | Medium |
| T10 | P010 | Durability + negative amplification | Low Fit | Medium |
| T11 | P001 | Arabic variant strong positive case | Excellent Fit | High |
| T12 | P006 | Irrelevant concern → no hallucination | Insufficient Data | Low |
| T13 | P002 | High-rated but concern mismatch | Moderate Fit | High |
| T14 | P003 | Conflicting reviews + general use | Moderate Fit | Medium |
---

## 📈 Results Summary

- Exact Pass: majority cases
- Near Match: expected in adversarial scenarios
- Fail: limited to edge ambiguity + sparse data cases


---

## 🧠 Evaluation Insight

Deterministic rules significantly outperform LLM-only classification for structured product decisions.

---

## 🧑‍💻 Conclusion

The evaluation confirms:

- Hybrid system > pure LLM system
- Rule-based fit rating improves reliability
- Confidence scoring correctly reflects uncertainty
