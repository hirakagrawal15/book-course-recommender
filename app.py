import streamlit as st
from agent import RecommendationAgent
from evaluator import Evaluator

st.title("📚 Book & Course Recommender")

topic = st.text_input("Topic", "Machine Learning")
level = st.selectbox("Level", ["Beginner", "Intermediate", "Advanced"])
format_type = st.selectbox("Format", ["Courses", "Books"])
time_commitment = st.selectbox("Time", ["Few hours a week", "Full time"])

if st.button("Generate Recommendations"):
    try:
        agent = RecommendationAgent()
        evaluator = Evaluator()

        result = agent.get_recommendations(topic, level, format_type, time_commitment)

        st.success("Recommendations Generated!")

        st.subheader("Top Recommendations")
        st.write(result.get("recommendations", "No data"))

        st.subheader("Search Data Used")
        if result.get("search_context"):
            st.text(result["search_context"][:1500])
        else:
            st.warning("No search data")

        st.subheader("LLM Evaluation")
        feedback = evaluator.evaluate(topic, result.get("recommendations", ""))
        st.write(feedback)

    except Exception as e:
        st.error(str(e))
