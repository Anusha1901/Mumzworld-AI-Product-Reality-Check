# app/analysis/confidence.py

from typing import List, Dict


class ConfidenceScorer:
    """
    Computes confidence score using:
    1. Review volume
    2. Rating consistency
    3. Review text coverage
    """

    def __init__(self):
        pass

    # -----------------------------------
    # Public Method
    # -----------------------------------
    def score(self, reviews: List[Dict]) -> Dict:
        """
        Returns:
        {
            "score": 0.82,
            "label": "High"
        }
        """

        if not reviews or len(reviews) == 0:
            return {
                "score": 0.10,
                "label": "Low"
            }

        volume_score = self._volume_score(reviews)
        consistency_score = self._consistency_score(reviews)
        coverage_score = self._coverage_score(reviews)

        # weighted final score
        final_score = (
            (volume_score * 0.40) +
            (consistency_score * 0.35) +
            (coverage_score * 0.25)
        )

        label = self._label(final_score)

        return {
            "score": round(final_score, 2),
            "label": label
        }

    # -----------------------------------
    # Review Count Strength
    # -----------------------------------
    def _volume_score(self, reviews: List[Dict]) -> float:
        count = len(reviews)

        if count >= 20:
            return 1.0
        elif count >= 10:
            return 0.8
        elif count >= 5:
            return 0.6
        elif count >= 3:
            return 0.4
        else:
            return 0.2

    # -----------------------------------
    # Rating Agreement
    # Lower variance = higher confidence
    # -----------------------------------
    def _consistency_score(self, reviews: List[Dict]) -> float:

        ratings = [
            r.get("rating", 0)
            for r in reviews
            if r.get("rating", 0) > 0
        ]

        if not ratings:
            return 0.4

        mean = sum(ratings) / len(ratings)

        variance = sum(
            (r - mean) ** 2 for r in ratings
        ) / len(ratings)

        # lower variance better
        if variance <= 0.5:
            return 1.0
        elif variance <= 1.0:
            return 0.8
        elif variance <= 1.5:
            return 0.6
        elif variance <= 2.0:
            return 0.4
        else:
            return 0.2

    # -----------------------------------
    # Review Quality Coverage
    # Longer useful text = more signal
    # -----------------------------------
    def _coverage_score(self, reviews: List[Dict]) -> float:

        texts = [
            r.get("text", "").strip()
            for r in reviews
        ]

        if not texts:
            return 0.3

        avg_len = sum(len(t) for t in texts) / len(texts)

        if avg_len >= 120:
            return 1.0
        elif avg_len >= 80:
            return 0.8
        elif avg_len >= 50:
            return 0.6
        elif avg_len >= 25:
            return 0.4
        else:
            return 0.2

    # -----------------------------------
    # Convert Score to Label
    # -----------------------------------
    def _label(self, score: float) -> str:

        if score >= 0.75:
            return "High"
        elif score >= 0.50:
            return "Medium"
        else:
            return "Low"