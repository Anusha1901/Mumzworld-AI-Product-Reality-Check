# app/preprocessing/cleaner.py

import re
from typing import List, Dict


class ReviewCleaner:
    """
    Cleans and normalizes review text before LLM analysis.

    Goals:
    - remove duplicate reviews
    - trim whitespace
    - normalize spacing
    - remove noisy symbols
    - discard empty reviews
    """

    def __init__(self):
        pass

    # -----------------------------------
    # Public Method
    # -----------------------------------
    def clean_reviews(self, reviews: List[Dict]) -> List[Dict]:
        """
        Input:
            list of review dicts

        Output:
            cleaned list of review dicts
        """

        cleaned_reviews = []
        seen_texts = set()

        for review in reviews:

            raw_text = review.get("text", "")

            cleaned_text = self._clean_text(raw_text)

            # skip empty
            if not cleaned_text:
                continue

            # deduplicate based on normalized lowercase text
            dedupe_key = cleaned_text.lower()

            if dedupe_key in seen_texts:
                continue

            seen_texts.add(dedupe_key)

            cleaned_reviews.append(
                {
                    "id": review.get("id", ""),
                    "lang": review.get("lang", "en"),
                    "rating": review.get("rating", 0),
                    "text": cleaned_text
                }
            )

        return cleaned_reviews

    # -----------------------------------
    # Internal Text Cleaner
    # -----------------------------------
    def _clean_text(self, text: str) -> str:

        if not text:
            return ""

        # strip spaces
        text = text.strip()

        # remove repeated spaces
        text = re.sub(r"\s+", " ", text)

        # remove strange repeated punctuation
        text = re.sub(r"[!]{2,}", "!", text)
        text = re.sub(r"[?]{2,}", "?", text)
        text = re.sub(r"[.]{3,}", "...", text)

        # remove emojis / non-basic symbols (optional lightweight)
        text = re.sub(
            r"[^\w\s\u0600-\u06FF.,!?;:'\"()\-\n]",
            "",
            text
        )

        # final trim
        text = text.strip()

        return text

    # -----------------------------------
    # Optional Stats
    # -----------------------------------
    def get_cleaning_stats(
        self,
        original_reviews: List[Dict],
        cleaned_reviews: List[Dict]
    ) -> Dict:

        return {
            "original_count": len(original_reviews),
            "cleaned_count": len(cleaned_reviews),
            "removed_count": len(original_reviews) - len(cleaned_reviews)
        }