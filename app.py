import os
import streamlit as st
from dotenv import load_dotenv
from agent import RecommendationAgent
from evaluator import LLMJudge

# Load env variables if a .env file exists
load_dotenv()

# UI Setup
st.set_page_config(page_title="AI Learning Agent", page_icon="🤖", layout="wide")
st.title("📚 Book & Course Recommendation Engine")
st.markdown("Powered by **Gemini** & **Tavily Search**")

# Sidebar for Setup
with st.sidebar:
    st.header("⚙️ Configuration")
    st.markdown("API Keys are now securely loaded from your `.env` file or deployment environment!")
    
    st.markdown("---")
    st.markdown("### How it works:")
    st.markdown("1. Agent generates optimal search queries.")
    st.markdown("2. Agent fetches latest data using Tavily.")
    st.markdown("3. Agent synthesizes tailored recommendations.")
    st.markdown("4. LLM-as-Judge scores the output.")

# Main Form
st.subheader("Your Profile")
col1, col2 = st.columns(2)

with col1:
    skill = st.text_input("Topic / Skill (e.g., Advanced Python, Marketing)", value="Machine Learning")
    level = st.selectbox("Current Level", ["Beginner", "Intermediate", "Advanced"])

with col2:
    format_pref = st.selectbox("Preferred Format", ["Courses", "Books", "Both"])
    duration = st.selectbox("Time Commitment", ["Few hours a week", "Bootcamp style (intensive)", "Self-paced over months"])

if st.button("Generate Recommendations", type="primary"):
    gemini_key = os.environ.get("GEMINI_API_KEY")
    tavily_key = os.environ.get("TAVILY_API_KEY")
    
    if not gemini_key or not tavily_key:
        st.error("Please provide both GEMINI_API_KEY and TAVILY_API_KEY in your `.env` file.")
    else:
        user_inputs = {
            "skill": skill,
            "level": level,
            "format": format_pref,
            "duration": duration
        }
        
        with st.spinner("🤖 Agent is thinking and searching..."):
            agent = RecommendationAgent(gemini_api_key=gemini_key, tavily_api_key=tavily_key)
            results = agent.run(user_inputs)
            
            st.success("Analysis Complete!")
            
            with st.expander("🔍 View Agent Internal Reasoning (Queries & Data)"):
                st.markdown("**Generated Search Queries:**")
                st.write(results["queries"])
                st.markdown("**Raw Search Data from Tavily:**")
                st.text(results.get("search_context", "No search context available")[:2000] + "\n...[truncated]...")
                
            st.markdown("---")
            st.subheader("🎯 Top Recommendations")
            st.markdown(results["recommendation"])
            
            st.markdown("---")
        
        with st.spinner("⚖️ Judging the output..."):
            judge = LLMJudge(gemini_api_key=gemini_key)
            evaluation = judge.evaluate(results["recommendation"], user_inputs)
            
            st.subheader("⚖️ LLM-as-Judge Evaluation")
            st.metric("Overall Score", f"{evaluation.get('score', 'N/A')}/10")
            st.markdown(f"**Feedback:** {evaluation.get('feedback', '')}")
            st.markdown(f"**Improvement Area:** {evaluation.get('improvements', '')}")
