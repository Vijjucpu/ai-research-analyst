import json, re
from config.models import critic_llm
from langchain.prompts import ChatPromptTemplate

PROMPT = ChatPromptTemplate.from_template("""You are a rigorous research quality critic.

Topic: {original_query}
Summary: {summary}

Score this research summary strictly on:
1. Depth — does it go beyond surface-level facts?
2. Coverage — are multiple angles and perspectives represented?
3. Accuracy — does the information seem reliable?
4. Coherence — is it well-structured and logical?

Give an honest score. Typical first drafts score 4-6. Only excellent research scores 8+.

You MUST respond with ONLY this JSON — no explanation, no markdown:
{{
  "quality_score": 7.5,
  "quality_feedback": "specific gaps identified and what sub-topics to search next to improve",
  "strengths": "what is good about this research"
}}""")

def critic_node(state):
    chain  = PROMPT | critic_llm
    result = chain.invoke({
        "original_query": state["original_query"],
        "summary":        state.get("summary", ""),
    })
    content = result.content.strip()
    match   = re.search(r'\{.*"quality_score".*\}', content, re.DOTALL)
    score   = 5.0
    feedback = "Research needs more depth and diverse sources."
    strengths = "Initial coverage established."
    if match:
        try:
            parsed   = json.loads(match.group())
            score    = float(parsed.get("quality_score", 5.0))
            feedback = parsed.get("quality_feedback", feedback)
            strengths = parsed.get("strengths", strengths)
        except Exception:
            pass
    return {
        **state,
        "quality_score":    score,
        "quality_feedback": feedback,
        "log": state.get("log", []) + [f"Critic scored: {score}/10 — {feedback[:80]}"],
    }
