import streamlit as st
from agent import RecommendationAgent
from evaluator import Evaluator

st.set_page_config(page_title="Book & Course Recommender", layout="wide")

st.title("📚 Book & Course Recommendation System")

# 🎯 Input UI
topic = st.text_input("Topic / Skill", "Machine Learning")
level = st.selectbox("Level", ["Beginner", "Intermediate", "Advanced"])
format_type = st.selectbox("Preferred Format", ["Courses", "Books"])
time_commitment = st.selectbox("Time Commitment", ["Few hours a week", "Full time"])

if st.button("Generate Recommendations"):
    with st.spinner("Generating..."):

        try:
            agent = RecommendationAgent()
            evaluator = Evaluator()

            results = agent.get_recommendations(topic, level, format_type, time_commitment)

            st.success("✅ Recommendations Generated!")

            # 📌 Recommendations
            st.subheader("🎯 Top Recommendations")
            st.write(results.get("recommendations", "No recommendations"))

            # 🔍 Search Context
            st.subheader("🔍 Search Data Used")
            if results.get("search_context"):
                st.text(results["search_context"][:2000])
            else:
                st.warning("No search data available")

            # ⚖️ Evaluation
            st.subheader("⚖️ LLM Evaluation")
            feedback = evaluator.evaluate(topic, results.get("recommendations", ""))

            st.write(feedback)

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
