# app/analysis/analyzer.py

import os
import json
import requests
from dotenv import load_dotenv

from app.analysis.schemas import ProductRealityCheck

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL_ID = os.getenv("MODEL_ID", "poolside/laguna-m.1:free")

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


class ProductAnalyzer:
    def __init__(self):
        if not OPENROUTER_API_KEY:
            raise ValueError("OPENROUTER_API_KEY missing in .env")

        self.headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }

    # -----------------------------------
    # Main Public Method
    # -----------------------------------
    def analyze_product(
        self,
        product: dict,
        output_language: str = "en",
        baby_age: str = "",
        concern: str = ""
    ) -> ProductRealityCheck:

        prompt = self._build_prompt(
            product=product,
            output_language=output_language,
            baby_age=baby_age,
            concern=concern
        )

        raw_response = self._call_llm(prompt)

        parsed_json = self._extract_json(raw_response)

        # validate through pydantic schema
        validated = ProductRealityCheck(**parsed_json)

        return validated

    # -----------------------------------
    # Prompt Builder
    # -----------------------------------
    def _build_prompt(
        self,
        product: dict,
        output_language: str,
        baby_age: str,
        concern: str
    ) -> str:

        reviews_text = "\n".join(
            [
                f"- ({r['lang']}, {r['rating']}/5) {r['text']}"
                for r in product["reviews"]
            ]
        )

        return f"""
You are an honest AI shopping advisor for mothers buying baby and family products on an e-commerce platform.

Your goal:
Convert product descriptions + customer reviews into balanced, decision-ready buying guidance.

STRICT RULES:
1. Use ONLY information explicitly supported by the provided product data or reviews.
2. Do NOT invent facts, specs, ages, certifications, or benefits.
3. If reviews conflict, mention mixed evidence.
4. If evidence is weak or sparse, reduce confidence.
5. Prefer concise, non-overlapping bullet points.
6. Mention limitations clearly, not just positives.
7. Return ONLY valid JSON. No markdown. No extra text.
8. If a claim is not directly supported by reviews, DO NOT include it.

OUTPUT LANGUAGE: {output_language}

USER CONTEXT:
Baby Age: {baby_age if baby_age else "Not Provided"}
Concern: {concern if concern else "Not Provided"}

PRODUCT:
ID: {product["id"]}
Title: {product["title"]}
Category: {product["category"]}
Price AED: {product["price_aed"]}
Rating: {product["rating"]}

Description:
{product["description"]}

Features:
{json.dumps(product["features"], ensure_ascii=False)}

Reviews:
{reviews_text}

Return JSON with EXACT schema:

{{
  "product_id": "",
  "product_title": "",
  "language": "",
  "fit_rating": "",
  "best_for": [],
  "avoid_if": [],
  "strengths": [],
  "key_drawbacks": [],
  "verdict": "",
  "confidence": "",
  "evidence": [],
  "review_summary": {{
    "total_reviews": 0,
    "avg_rating": 0
  }}
}}

Allowed fit_rating:
Excellent Fit, Good Fit, Moderate Fit, Low Fit, Insufficient Data

Allowed confidence:
High, Medium, Low

QUALITY BAR:
- best_for max 4 bullets
- avoid_if max 4 bullets
- strengths max 6 bullets
- drawbacks max 5 bullets
- evidence must cite recurring review themes
- verdict should be practical and trustworthy
"""

    # -----------------------------------
    # LLM API Call
    # -----------------------------------
    def _call_llm(self, prompt: str) -> str:

        payload = {
        "model": MODEL_ID,
        "messages": [
            {
                "role": "system",
                "content": "You return structured JSON only."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.2
        }

        response = requests.post(
            OPENROUTER_URL,
            headers=self.headers,
            json=payload,
            timeout=60
        )

        response.raise_for_status()

        data = response.json()

        try:
            content = data["choices"][0]["message"]["content"]
        except Exception:
            raise ValueError(f"Unexpected API response:\n{json.dumps(data, indent=2)}")

        if content is None or str(content).strip() == "":
            raise ValueError(
                f"Model returned empty content.\nFull Response:\n{json.dumps(data, indent=2)}"
         )

        return content

    # -----------------------------------
    # Extract JSON Safely
    # -----------------------------------
    def _extract_json(self, raw_text: str) -> dict:

        raw_text = (raw_text or "").strip()

        # remove markdown code fences if model adds them
        raw_text = raw_text.replace("```json", "").replace("```", "").strip()

        try:
            return json.loads(raw_text)

        except Exception as e:
            raise ValueError(
                f"Model did not return valid JSON.\nRaw Output:\n{raw_text}"
            ) from e