import json, re
from config.models import planner_llm
from langchain.prompts import ChatPromptTemplate

PROMPT = ChatPromptTemplate.from_template("""You are a research planning expert.

Original query: {original_query}
Critic feedback (if any): {quality_feedback}
Refined focus (if any): {refined_query}

Break this into exactly 3 distinct sub-topics for parallel web research.
Each sub-topic should be a specific, searchable query string.

You MUST respond with ONLY this JSON — no explanation, no markdown, no code block:
{{"sub_topics": ["specific query 1", "specific query 2", "specific query 3"]}}""")

def planner_node(state):
    chain  = PROMPT | planner_llm
    result = chain.invoke({
        "original_query":   state["original_query"],
        "quality_feedback": state.get("quality_feedback", "none"),
        "refined_query":    state.get("refined_query", ""),
    })
    content = result.content.strip()
    match = re.search(r'\{.*"sub_topics".*\}', content, re.DOTALL)
    sub_topics = []
    if match:
        try:
            parsed = json.loads(match.group())
            sub_topics = parsed.get("sub_topics", [])
        except Exception:
            pass

    if len(sub_topics) < 3:
        q = state.get("refined_query") or state["original_query"]
        sub_topics = [
            f"{q} overview and fundamentals",
            f"{q} recent developments 2024 2025",
            f"{q} applications and future trends",
        ]

    # Only return non-Annotated keys here — no raw_results reset
    return {
        "sub_topics":  sub_topics[:3],
        "log": [f"Planner created {len(sub_topics[:3])} sub-topics"],
    }
