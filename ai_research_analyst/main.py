import os, sys, time
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
import httpx

from graph.research_graph import build_graph

app   = FastAPI(title="AI Research Analyst Agent")
graph = build_graph()

OLLAMA_BASE = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
MODEL       = os.getenv("OLLAMA_MODEL", "llama3.2")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root():
    return FileResponse("static/dashboard.html")

@app.get("/health")
async def health():
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            r = await client.get(f"{OLLAMA_BASE}/api/tags")
            if r.status_code == 200:
                models = [m["name"] for m in r.json().get("models", [])]
                matched = next((m for m in models if MODEL.split(":")[0] in m), None)
                return {"ollama": "ok", "model": matched or MODEL, "available_models": models}
    except Exception:
        pass
    return {"ollama": "offline", "model": MODEL}

class ResearchRequest(BaseModel):
    query: str

@app.post("/research")
async def run_research(req: ResearchRequest):
    if not req.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    # Annotated keys (raw_results, log) MUST start as empty lists
    # Non-annotated keys can be set normally
    initial_state = {
        "original_query":   req.query.strip(),
        "sub_topics":       [],
        "refined_query":    "",
        "raw_results":      [],   # Annotated[List, operator.add] — starts empty
        "summary":          "",
        "quality_score":    0.0,
        "quality_feedback": "",
        "retry_count":      0,
        "final_report":     "",
        "log":              [],   # Annotated[List, operator.add] — starts empty
    }

    try:
        result = graph.invoke(initial_state)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent pipeline error: {str(e)}")

    return JSONResponse({
        "report":        result.get("final_report", ""),
        "quality_score": round(float(result.get("quality_score", 0.0)), 1),
        "retries":       result.get("retry_count", 0),
        "model":         MODEL,
        "log":           result.get("log", []),
    })


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "cli":
        query = " ".join(sys.argv[2:]) or "Impact of AI on software engineering 2025"
        print(f"\n{'='*60}\n  AI Research Analyst Agent\n  Model: {MODEL}\n{'='*60}")
        print(f"\nResearching: {query}\n")
        initial_state = {
            "original_query": query, "sub_topics": [], "refined_query": "",
            "raw_results": [], "summary": "", "quality_score": 0.0,
            "quality_feedback": "", "retry_count": 0, "final_report": "", "log": [],
        }
        start  = time.time()
        result = graph.invoke(initial_state)
        duration = round(time.time() - start, 1)
        print("\n" + "="*60)
        print(result.get("final_report", "No report generated"))
        print(f"\nQuality: {result.get('quality_score',0)}/10 | Retries: {result.get('retry_count',0)} | Time: {duration}s")
    else:
        import uvicorn
        print(f"\n  AI Research Analyst Agent")
        print(f"  Model  : {MODEL}")
        print(f"  Ollama : {OLLAMA_BASE}")
        print(f"  Open   : http://localhost:8080\n")
        uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=False)
