import json
import time
import sys
import os
import traceback

sys.path.append(os.path.abspath("."))

from app.pipeline import MumzworldPipeline

pipeline = MumzworldPipeline()

# -----------------------------------
# Load Test Cases
# -----------------------------------
with open("evals/test_cases.json", "r", encoding="utf-8") as f:
    test_cases = json.load(f)

# Allow running specific test IDs
selected_ids = sys.argv[1:]
if selected_ids:
    test_cases = [t for t in test_cases if t["test_id"] in selected_ids]

# -----------------------------------
# Ranking Maps
# -----------------------------------
fit_rank = {
    "Excellent Fit": 5,
    "Good Fit": 4,
    "Moderate Fit": 3,
    "Low Fit": 2,
    "Insufficient Data": 1
}

conf_rank = {
    "High": 3,
    "Medium": 2,
    "Low": 1
}

# -----------------------------------
# Counters
# -----------------------------------
exact = 0
near = 0
fail = 0

# -----------------------------------
# Run Evaluations
# -----------------------------------
for case in test_cases:
    print(f"\n==============================")
    print(f"Running {case['test_id']}...")
    print(f"==============================")

    try:
        result = pipeline.run(
            product_id=case["product_id"],
            output_language=case["language"],
            baby_age=case["baby_age"],
            concern=case["concern"]
        )

        # -----------------------------------
        # Expected vs Actual
        # -----------------------------------
        expected_fit = case["expected_fit_rating"]
        actual_fit = result.fit_rating

        expected_conf = case["expected_confidence"]
        actual_conf = result.confidence

        fit_diff = abs(fit_rank[expected_fit] - fit_rank[actual_fit])
        conf_diff = abs(conf_rank[expected_conf] - conf_rank[actual_conf])

        # -----------------------------------
        # Check 1: Output Completeness
        # -----------------------------------
        completeness_fail = False

        if not result.best_for or len(result.best_for) == 0:
            completeness_fail = True

        if not result.strengths or len(result.strengths) == 0:
            completeness_fail = True

        if not result.evidence or len(result.evidence) == 0:
            completeness_fail = True

        if not result.verdict or len(result.verdict.strip()) < 10:
            completeness_fail = True

        # -----------------------------------
        # Check 2: Grounding (Hallucination)
        # -----------------------------------
        grounding_fail = False

        original_product = pipeline.get_product_by_id(case["product_id"])

        review_text_blob = " ".join(
            [r["text"].lower() for r in original_product["reviews"]]
        )

        match_count = 0

        for ev in result.evidence:
            ev_words = ev.lower().split()

            # check if at least 50% words appear
            match_words = sum(
                1 for w in ev_words if w in review_text_blob
            )

            if len(ev_words) > 0 and (match_words / len(ev_words)) >= 0.5:
                match_count += 1

        if len(result.evidence) > 0:
            if match_count / len(result.evidence) < 0.5:
                grounding_fail = True

        # -----------------------------------
        # Final Evaluation Logic
        # -----------------------------------
        if (
            fit_diff == 0 and
            conf_diff == 0 and
            not completeness_fail and
            not grounding_fail
        ):
            status = "PASS"
            exact += 1

        elif fit_diff <= 1 and conf_diff <= 1:
            status = "NEAR MATCH"
            near += 1

        else:
            status = "FAIL"
            fail += 1

        # -----------------------------------
        # Debug Output
        # -----------------------------------
        print("Expected Fit:", expected_fit)
        print("Actual Fit:", actual_fit)
        print("Expected Confidence:", expected_conf)
        print("Actual Confidence:", actual_conf)
        print("Fit Diff:", fit_diff)
        print("Confidence Diff:", conf_diff)

        print("Completeness Fail:", completeness_fail)
        print("Grounding Fail:", grounding_fail)

        print("Final Status:", status)

    except Exception as e:
        print("ERROR OCCURRED:")
        traceback.print_exc()
        fail += 1

    time.sleep(2)

# -----------------------------------
# Summary
# -----------------------------------
print("\n========== FINAL SUMMARY ==========")
print("Exact Pass:", exact)
print("Near Match:", near)
print("Fail:", fail)
print("Total:", len(test_cases))