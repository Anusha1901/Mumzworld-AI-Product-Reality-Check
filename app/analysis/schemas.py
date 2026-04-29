# app/analysis/schemas.py

from typing import List, Literal, Optional
from pydantic import BaseModel, Field, field_validator


# -----------------------------
# Final AI Output Schema
# -----------------------------
class ProductRealityCheck(BaseModel):
    """
    Structured response returned by the LLM after analyzing
    product details + reviews.
    """

    product_id: str = Field(..., description="Unique product ID")
    product_title: str = Field(..., description="Product title")

    language: Literal["en", "ar"] = Field(
        ..., description="Output language: English or Arabic"
    )

    fit_rating: Literal[
        "Excellent Fit",
        "Good Fit",
        "Moderate Fit",
        "Low Fit",
        "Insufficient Data"
    ] = Field(..., description="Overall suitability score")

    best_for: List[str] = Field(
        ..., min_length=1,
        description="Who / what use-case this product is best suited for"
    )

    avoid_if: List[str] = Field(
        ..., description="Who should avoid or reconsider this product"
    )

    strengths: List[str] = Field(
        ..., min_length=1,
        description="Most common positives found in reviews"
    )

    key_drawbacks: List[str] = Field(
        ..., description="Most common negatives or limitations"
    )

    verdict: str = Field(
        ..., min_length=10,
        description="Short balanced summary with recommendation"
    )

    confidence: Literal[
        "High",
        "Medium",
        "Low"
    ] = Field(..., description="Confidence based on review volume + consistency")

    evidence: List[str] = Field(
        ..., min_length=1,
        description="Grounded evidence pulled from review patterns"
    )

    review_summary: Optional[dict] = Field(
        default=None,
        description="Optional review stats like counts by rating"
    )


    # -----------------------------
    # Validators
    # -----------------------------
    @field_validator("best_for", "strengths", "evidence")
    @classmethod
    def must_not_be_empty(cls, v):
        if not v or len(v) == 0:
            raise ValueError("Field cannot be empty")
        return v

    @field_validator("verdict")
    @classmethod
    def clean_verdict(cls, v):
        if not v.strip():
            raise ValueError("Verdict cannot be blank")
        return v.strip()


# -----------------------------
# Raw Input Product Schema
# (for loading sample_products.json)
# -----------------------------
class Review(BaseModel):
    id: str
    lang: Literal["en", "ar"]
    rating: int = Field(..., ge=1, le=5)
    text: str


class Product(BaseModel):
    id: str
    title: str
    category: str
    price_aed: float
    rating: float = Field(..., ge=0, le=5)
    description: str
    features: List[str]
    reviews: List[Review]


class ProductCatalog(BaseModel):
    products: List[Product]