from tools.pushover_tool import send_pushover_alert

def notifier_node(state):
    topic   = state["original_query"]
    score   = state.get("quality_score", 0.0)
    retries = state.get("retry_count", 0)
    preview = (state.get("final_report", "")[:200]).replace("\n", " ")
    send_pushover_alert.invoke({
        "title":   f"Research done: {topic[:40]}",
        "message": f"Quality {score}/10 | {retries} retries\n{preview}...",
    })
    return {**state, "log": state.get("log", []) + ["Notification sent"]}
