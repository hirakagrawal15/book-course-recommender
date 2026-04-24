# Deliverable 1: Problem Statement

**Project Title:** Book and Course Recommendation Engine

## Defined Problem
With the constant influx of new content across various learning platforms, professionals and students often struggle to find up-to-date, high-quality, and highly relevant books and courses tailored to their specific goals. Traditional search engines return overwhelming, ad-heavy, and sometimes generic results that do not take into account a learner's specific level or time commitment.

## The Target User
Learners, professionals, and students who want to rapidly upskill in a specific domain but do not have the time to sift through hundreds of reviews and outdated course listings.

## Why an Agentic Approach is Suitable
A standard keyword search simply matches text strings. An **Agentic AI** approach is necessary because:
1. **Tool Use (Tavily):** It can actively search the current web for the latest released courses and books, bypassing outdated LLM training data cut-offs.
2. **Reasoning (Gemini):** It can analyze the user's specific context (Beginner vs. Advanced, time commitment), synthesize the raw search results, and evaluate them to extract only the top 3 highly personalized recommendations.
3. **Evaluation (LLM-as-Judge):** It can self-assess its output to ensure relevance, actionability, and correct formatting before presenting it to the user.
