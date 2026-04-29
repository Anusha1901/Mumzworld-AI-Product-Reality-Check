import json
from pathlib import Path
from typing import Optional, Dict, Any, List

from app.analysis.analyzer import ProductAnalyzer
from app.analysis.schemas import ProductRealityCheck
from app.analysis.confidence import ConfidenceScorer
from app.preprocessing.cleaner import ReviewCleaner


class MumzworldPipeline:
    """
    Central orchestration layer.

    Flow:
    1. Load product data
    2. Clean reviews
    3. Compute deterministic confidence
    4. Compute deterministic fit rating (NEW)
    5. Call LLM analyzer
    6. Override confidence + fit rating
    7. Return validated structured result
    """

    def __init__(self, data_path: str = "data/sample_products.json"):
        self.data_path = Path(data_path)

        self.catalog = self._load_catalog()

        self.cleaner = ReviewCleaner()
        self.confidence_engine = ConfidenceScorer()
        self.analyzer = ProductAnalyzer()

    # -----------------------------------
    # Load Product Catalog
    # -----------------------------------
    def _load_catalog(self) -> Dict[str, Any]:

        if not self.data_path.exists():
            raise FileNotFoundError(
                f"Missing data file: {self.data_path}"
            )

        with open(self.data_path, "r", encoding="utf-8") as f:
            return json.load(f)

    # -----------------------------------
    # List Products
    # -----------------------------------
    def list_products(self) -> List[dict]:
        return self.catalog["products"]

    # -----------------------------------
    # Get Product by ID
    # -----------------------------------
    def get_product_by_id(self, product_id: str) -> Optional[dict]:

        for product in self.catalog["products"]:
            if product["id"] == product_id:
                return product

        return None

    # -----------------------------------
    # Product Preview for UI
    # -----------------------------------
    def get_product_preview(self, product_id: str) -> dict:

        product = self.get_product_by_id(product_id)

        if not product:
            return {}

        return {
            "id": product["id"],
            "title": product["title"],
            "category": product["category"],
            "price_aed": product["price_aed"],
            "rating": product["rating"],
            "review_count": len(product["reviews"])
        }

    # -----------------------------------
    # Main Execution
    # -----------------------------------
    def run(
        self,
        product_id: str,
        output_language: str = "en",
        baby_age: str = "",
        concern: str = ""
    ) -> ProductRealityCheck:

        # ----------------------------
        # Step 1: Fetch Product
        # ----------------------------
        product = self.get_product_by_id(product_id)

        if not product:
            raise ValueError(f"Product not found: {product_id}")

        product = dict(product)

        # ----------------------------
        # Step 2: Clean Reviews
        # ----------------------------
        cleaned_reviews = self.cleaner.clean_reviews(
            product["reviews"]
        )

        product["reviews"] = cleaned_reviews

        # ----------------------------
        # Step 3: Compute Confidence
        # ----------------------------
        confidence_result = self.confidence_engine.score(
            cleaned_reviews
        )

        confidence_label = confidence_result["label"]

        # ----------------------------
        # Step 3.5: Compute Avg Rating
        # ----------------------------
        avg_rating = round(
            sum(r["rating"] for r in cleaned_reviews) / len(cleaned_reviews),
            2
        ) if cleaned_reviews else 0

        # ----------------------------
        # Step 3.6: Deterministic Fit Rating (NEW LOGIC)
        # ----------------------------
        if len(cleaned_reviews) < 5:
            fit_rating = "Insufficient Data"

        elif avg_rating < 2.5 or confidence_label == "Low":
            fit_rating = "Low Fit"

        elif avg_rating < 3.2:
            fit_rating = "Moderate Fit"

        elif avg_rating < 4.2:
            fit_rating = "Good Fit"

        else:
            fit_rating = "Excellent Fit"

        # ----------------------------
        # Step 4: Run AI Analyzer
        # ----------------------------
        result = self.analyzer.analyze_product(
            product=product,
            output_language=output_language,
            baby_age=baby_age,
            concern=concern
        )

        # ----------------------------
        # Step 5: Override LLM Outputs
        # ----------------------------
        result.confidence = confidence_label
        result.fit_rating = fit_rating

        # ----------------------------
        # Step 6: Add Stats
        # ----------------------------
        result.review_summary = {
            "total_reviews": len(cleaned_reviews),
            "avg_rating": avg_rating,
            "confidence_score": confidence_result["score"]
        }

        return result