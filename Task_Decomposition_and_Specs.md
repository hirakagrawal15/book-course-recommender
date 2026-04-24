# Deliverable 2: Task Decomposition & Specs

## Step 1: User Input Intake
- **Input:** User provides target Skill (e.g., Python), Level (Beginner), Format (Courses), and Duration (Self-paced).
- **Processing:** Data is formatted into a dictionary and passed to the Recommendation Agent.
- **Output:** A structured `user_inputs` dictionary.

## Step 2: Search Strategy Generation (Agent Reasoning)
- **Input:** `user_inputs` dictionary.
- **Processing:** The Agent passes the context to the Gemini model with instructions to generate specialized, optimized search queries.
- **Output:** A JSON array of 2 string queries (e.g., `["Best beginner Python courses self paced 2024", "Top rated intro to Python online courses"]`).

## Step 3: Information Retrieval (Tool Use)
- **Input:** Generated search queries.
- **Processing:** The Agent uses the `tavily-python` client to perform advanced internet searches for each query, gathering titles, snippets, and URLs.
- **Output:** Concatenated unstructured text context containing the latest web search results.

## Step 4: Recommendation Synthesis (Agent Reasoning)
- **Input:** Raw search context + original `user_inputs`.
- **Processing:** The Gemini model synthesizes the raw data, filtering for relevance and formatting the top 3 recommendations into beautifully structured markdown.
- **Output:** Formatted Markdown text highlighting titles, formats, "why it fits", and direct links.

## Step 5: Quality Evaluation (LLM-as-Judge)
- **Input:** The final generated recommendation text + original `user_inputs`.
- **Processing:** A separate Gemini call acts as an evaluator, grading the output based on a strict rubric (Relevance, Actionability, Formatting).
- **Output:** A JSON object with a score out of 10, brief feedback, and an improvement suggestion. This is displayed to the user alongside the recommendations.
