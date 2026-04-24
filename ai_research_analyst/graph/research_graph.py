from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Annotated
import operator

class ResearchState(TypedDict):
    original_query:   str
    sub_topics:       List[str]
    refined_query:    str
    raw_results:      Annotated[List[dict], operator.add]
    summary:          str
    quality_score:    float
    quality_feedback: str
    retry_count:      int
    final_report:     str
    log:              Annotated[List[str], operator.add]

def route_after_critic(state: ResearchState) -> str:
    if state.get("retry_count", 0) >= 2:
        return "write_report"
    if state.get("quality_score", 0) < 6.0:
        return "optimize"
    return "write_report"

def build_graph():
    from agents.planner       import planner_node
    from agents.searcher      import search_A_node, search_B_node, search_C_node
    from agents.summarizer    import summarizer_node
    from agents.critic        import critic_node
    from agents.optimizer     import optimizer_node
    from agents.report_writer import report_writer_node
    from agents.notifier      import notifier_node

    g = StateGraph(ResearchState)

    g.add_node("planner",       planner_node)
    g.add_node("search_A",      search_A_node)
    g.add_node("search_B",      search_B_node)
    g.add_node("search_C",      search_C_node)
    g.add_node("summarizer",    summarizer_node)
    g.add_node("critic",        critic_node)
    g.add_node("optimizer",     optimizer_node)
    g.add_node("report_writer", report_writer_node)
    g.add_node("notify",        notifier_node)

    g.set_entry_point("planner")

    # Fan-out: planner -> 3 search agents in parallel
    g.add_edge("planner",  "search_A")
    g.add_edge("planner",  "search_B")
    g.add_edge("planner",  "search_C")

    # Fan-in: all 3 search agents -> summarizer
    g.add_edge("search_A", "summarizer")
    g.add_edge("search_B", "summarizer")
    g.add_edge("search_C", "summarizer")

    g.add_edge("summarizer", "critic")

    g.add_conditional_edges("critic", route_after_critic, {
        "optimize":     "optimizer",
        "write_report": "report_writer",
    })

    g.add_edge("optimizer",     "planner")
    g.add_edge("report_writer", "notify")
    g.add_edge("notify",        END)

    return g.compile()
