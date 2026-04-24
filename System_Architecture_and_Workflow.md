# System Architecture & Detailed Workflow

This document explains exactly how the **Book and Course Recommendation Engine** functions under the hood. It is designed to help you completely understand the data flow, which is crucial for your project Viva (oral exam).

## 1. The Core Components

The system is broken down into three main Python files that interact with each other:
1. **`app.py` (The Frontend):** The Streamlit user interface where the user inputs their preferences and views the final output.
2. **`agent.py` (The Brain & Hands):** Contains the `RecommendationAgent` class. It manages prompting the Gemini API and calling the Tavily Search API. 
3. **`evaluator.py` (The Judge):** Contains the `LLMJudge` class. It reviews the work produced by `agent.py`.

---

## 2. Step-by-Step Data Flow

When a user clicks **"Generate Recommendations"** on the frontend, a highly structured sequence of events is triggered:

### Phase 1: Intake & Orchestration
1. **Data Collection:** `app.py` gathers the `Skill`, `Level`, `Format`, and `Time Commitment` into a `user_inputs` dictionary.
2. **Initialization:** The `RecommendationAgent` is initialized using the API keys provided in the sidebar.
3. **Execution Run:** `app.py` calls `agent.run(user_inputs)`. This single function acts as the orchestrator for the rest of the agent's tasks.

### Phase 2: Agent Tool Preparation (Reasoning)
*(Inside `agent.py` -> `generate_search_queries`)*
- The agent doesn't just blindly search "books on Python". It uses the **Gemini model** to *reason* about what the best search queries would be.
- It is prompted to act as an expert consultant, looks at the specific `user_inputs`, and returns exactly two highly optimized string queries as a JSON array (e.g., `["Top rated self-paced advanced Python courses 2024", "Best advanced Python bootcamps"]`).

### Phase 3: Information Retrieval (Tool Use)
*(Inside `agent.py` -> `perform_search`)*
- The agent iterates over the queries generated in Phase 2.
- For each query, it makes a live API call to **Tavily Search** (`self.tavily_client.search`).
- Tavily browses the internet and returns raw data (Titles, URLs, and text snippets from websites).
- The agent compiles all this retrieved data into a single, massive string of "search context". 

### Phase 4: Synthesis & Formatting (Reasoning)
*(Inside `agent.py` -> `synthesize_recommendations`)*
- Now the agent has the user's specific goals AND the latest web data.
- It sends a massive prompt to Gemini-2.5-Pro. The prompt includes the `user_inputs` and the `search_context`.
- Gemini reads the web search snippets, filters out the irrelevant ones, and formats the top 3 best matching results into beautiful Markdown, including the direct URLs retrieved from Tavily.
- This markdown text is returned to the frontend.

### Phase 5: Quality Assurance (LLM-as-Judge)
*(Inside `evaluator.py` -> `evaluate`)*
- Before the user simply reads the output, the system evaluates itself.
- `app.py` passes the final Markdown text and the `user_inputs` into the `LLMJudge`.
- The judge sends this data to Gemini with a **strict scoring Rubric**:
  - *Relevance:* Did it meet the user's criteria?
  - *Actionability:* Are the links real and clickable based on the output?
  - *Formatting:* Is it structured well?
- The Judge returns a JSON dictionary containing a score out of 10, positive feedback, and areas for improvement.

### Phase 6: Final Presentation
- `app.py` unpackages all this data.
- It displays the final Markdown recommendation.
- It displays the Judge's score.
- It also uses an expander ("View Agent Internal Reasoning") to allow the user to peek behind the curtain and see exactly what queries were generated (Phase 2) and what raw data came back from Tavily (Phase 3). 

---

## 3. Why This is "Agentic" (Viva Talking Points)
If asked why this is an AI Agent and not just a standard LLM chatbot, explain the following:
- **Autonomous Tool Use:** The system actively decides *what* to search and utilizes an external API tool (Tavily) to fetch data outside of its fixed training set.
- **Multi-Step Reasoning:** It breaks the problem into discrete steps (Search Generation -> Data Gathering -> Synthesis) rather than trying to answer in one shot.
- **Self-Reflection:** By employing an LLM-as-a-Judge, the system has a built-in mechanism to evaluate the quality of its own outputs against a predetermined rubric.
