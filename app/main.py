# app/main.py

import streamlit as st
from app.pipeline import MumzworldPipeline

# -----------------------------------
# Page Config
# -----------------------------------
st.set_page_config(
    page_title="Mumzworld AI Product Advisor",
    page_icon="🍼",
    layout="wide"
)

# -----------------------------------
# Init Pipeline
# -----------------------------------
@st.cache_resource
def load_pipeline():
    return MumzworldPipeline()

pipeline = load_pipeline()

# -----------------------------------
# Header
# -----------------------------------
st.title("🍼 Mumzworld AI Product Reality Check")
st.caption(
    "AI-powered product guidance for mothers using reviews + product data"
)

st.divider()

# -----------------------------------
# Sidebar Inputs
# -----------------------------------
st.sidebar.header("🔍 Product Inputs")

products = pipeline.list_products()

product_map = {
    f"{p['title']} ({p['id']})": p["id"]
    for p in products
}

selected_label = st.sidebar.selectbox(
    "Choose Product",
    list(product_map.keys())
)

selected_id = product_map[selected_label]

language = st.sidebar.selectbox(
    "Output Language",
    ["en", "ar"]
)

baby_age = st.sidebar.text_input(
    "Baby Age (optional)",
    placeholder="e.g. 6 months, 1 year, toddler"
)

concern = st.sidebar.text_input(
    "Concern (optional)",
    placeholder="e.g. sensitive skin"
)

analyze_btn = st.sidebar.button("✨ Analyze Product")

# -----------------------------------
# Product Preview
# -----------------------------------
preview = pipeline.get_product_preview(selected_id)

st.subheader("📦 Product Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Product ID", preview["id"])

with col2:
    st.metric("Category", preview["category"])

with col3:
    st.metric("Price", f"{preview['price_aed']} AED")

with col4:
    st.metric("Rating", preview["rating"])

st.caption(f"Based on {preview['review_count']} reviews")

st.divider()

# -----------------------------------
# Run Analysis
# -----------------------------------
if analyze_btn:

    with st.spinner("Analyzing product reviews and generating insights..."):

        try:
            result = pipeline.run(
                product_id=selected_id,
                output_language=language,
                baby_age=baby_age,
                concern=concern
            )

            # ----------------------------
            # Header Summary
            # ----------------------------
            st.subheader("🧠 AI-Powered Product Assessment")

            colA, colB = st.columns(2)

            with colA:
                st.success(f"Fit Rating: {result.fit_rating}")

            with colB:
                st.info(f"Confidence: {result.confidence}")

            # ----------------------------
            # Best For / Avoid If
            # ----------------------------
            c1, c2 = st.columns(2)

            with c1:
                st.markdown("### ⭐ Best For")
                for item in result.best_for:
                    st.write(f"• {item}")

            with c2:
                st.markdown("### ⚠️ Avoid If")
                for item in result.avoid_if:
                    st.write(f"• {item}")

            # ----------------------------
            # Strengths / Drawbacks
            # ----------------------------
            c3, c4 = st.columns(2)

            with c3:
                st.markdown("### ✅ Strengths")
                for item in result.strengths:
                    st.write(f"• {item}")

            with c4:
                st.markdown("### ❌ Drawbacks")
                for item in result.key_drawbacks:
                    st.write(f"• {item}")

            # ----------------------------
            # Verdict
            # ----------------------------
            st.markdown("### 📌 Final Verdict")
            st.write(result.verdict)

            # ----------------------------
            # Evidence
            # ----------------------------
            st.markdown("### 🧾 Evidence From Reviews")
            for item in result.evidence:
                st.write(f"• {item}")

            # ----------------------------
            # Review Summary
            # ----------------------------
            if result.review_summary:
                st.markdown("### 📊 Review Stats")

                colx, coly = st.columns(2)

                with colx:
                    st.metric(
                        "Total Reviews",
                        result.review_summary.get("total_reviews", 0)
                    )

                with coly:
                    st.metric(
                        "Average Rating",
                        result.review_summary.get("avg_rating", 0)
                    )

        except Exception as e:
            st.error(f"Error: {str(e)}")

# -----------------------------------
# Footer
# -----------------------------------
st.divider()

st.caption(
    "Built for Mumzworld Track A Assessment | Structured AI outputs with confidence-aware reasoning"
)