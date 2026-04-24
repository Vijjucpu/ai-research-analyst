from config.models import optimizer_llm
from langchain.prompts import ChatPromptTemplate

PROMPT = ChatPromptTemplate.from_template("""The critic rated this research {quality_score}/10.

Feedback: {quality_feedback}
Original query: {original_query}

Generate a refined, more specific version of the research query that directly addresses the identified gaps.
Focus on: specificity, missing angles, deeper sub-topics.

Respond with ONLY the refined query string — nothing else.""")

def optimizer_node(state):
    chain  = PROMPT | optimizer_llm
    result = chain.invoke({
        "quality_score":    state.get("quality_score", 5.0),
        "quality_feedback": state.get("quality_feedback", ""),
        "original_query":   state["original_query"],
    })
    refined = result.content.strip().strip('"').strip("'")
    return {
        **state,
        "refined_query": refined,
        "retry_count":   state.get("retry_count", 0) + 1,
        "log": state.get("log", []) + [f"Optimizer refined query (retry {state.get('retry_count',0)+1}): {refined[:80]}"],
    }
