import httpx, os
from langchain.tools import tool

@tool
def send_pushover_alert(title: str, message: str) -> dict:
    """Send a push notification to the user via Pushover."""
    user_key  = os.getenv("PUSHOVER_USER_KEY", "")
    app_token = os.getenv("PUSHOVER_APP_TOKEN", "")
    if not user_key or user_key == "your_pushover_user_key_here":
        print(f"\n[PUSHOVER SKIPPED - no key] {title}: {message[:100]}")
        return {"status": "skipped", "reason": "no Pushover credentials configured"}
    try:
        resp = httpx.post("https://api.pushover.net/1/messages.json", data={
            "token":   app_token,
            "user":    user_key,
            "title":   title,
            "message": message,
        }, timeout=10.0)
        return resp.json()
    except Exception as e:
        return {"status": "error", "reason": str(e)}
