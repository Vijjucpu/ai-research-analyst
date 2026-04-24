from config.models import summarizer_llm
from langchain.prompts import ChatPromptTemplate

PROMPT = ChatPromptTemplate.from_template("""You are a research synthesizer.

Topic: {original_query}

All collected facts:
{raw_results}

Synthesize these into a coherent, deduplicated research summary.
- Remove duplicate information
- Group related facts by theme
- Keep source URLs where available
- Write 400-600 words minimum
- Be comprehensive and analytical""")

def summarizer_node(state):
    facts_text = "\n".join([
        f"- {f.get('fact','')}" + (f" (source: {f.get('source','')})" if f.get('source') else "")
        for f in state.get("raw_results", [])
    ])
    if not facts_text:
        facts_text = "No facts collected yet — summarize what is generally known about this topic."

    chain  = PROMPT | summarizer_llm
    result = chain.invoke({
        "original_query": state["original_query"],
        "raw_results":    facts_text,
    })
    return {
        **state,
        "summary": result.content,
        "log": state.get("log", []) + ["Summarizer condensed all search results"],
    }
