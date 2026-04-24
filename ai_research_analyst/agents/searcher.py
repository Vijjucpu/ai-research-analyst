import json, re
from config.models import searcher_llm
from tools.serper_tool import web_search
from langchain.prompts import ChatPromptTemplate

PROMPT = ChatPromptTemplate.from_template("""You searched for: {query}

Raw search results:
{results}

Extract the 3 most relevant facts with their source URLs.
You MUST respond with ONLY this JSON — no explanation, no markdown:
{{"facts": [{{"fact": "concise fact here", "source": "url here"}}]}}""")

def _make_search_node(topic_index: int):
    label = ["A", "B", "C"][topic_index]
    def search_node(state):
        sub_topics = state.get("sub_topics", [])
        if topic_index >= len(sub_topics):
            return {"raw_results": [], "log": []}
        query   = sub_topics[topic_index]
        results = web_search.invoke({"query": query})
        results_text = "\n".join([
            f"- {r['title']}: {r['snippet']} ({r['link']})"
            for r in results[:6]
        ])
        chain   = PROMPT | searcher_llm
        out     = chain.invoke({"query": query, "results": results_text})
        content = out.content.strip()
        match   = re.search(r'\{.*"facts".*\}', content, re.DOTALL)
        facts   = []
        if match:
            try:
                parsed = json.loads(match.group())
                facts  = parsed.get("facts", [])
            except Exception:
                pass
        if not facts:
            facts = [
                {"fact": r["snippet"], "source": r["link"]}
                for r in results[:3] if r.get("snippet")
            ]
        # IMPORTANT: only return Annotated keys (raw_results, log)
        # Do NOT return original_query or other non-annotated keys
        return {
            "raw_results": facts,
            "log": [f"Search {label} found {len(facts)} facts for: {query[:60]}"],
        }
    return search_node

search_A_node = _make_search_node(0)
search_B_node = _make_search_node(1)
search_C_node = _make_search_node(2)
