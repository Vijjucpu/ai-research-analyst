# 🔬 AI Research Analyst Agent
### Multi-Agent · LangGraph · Ollama · No OpenAI Key Required

---

## 1. 🧩 Business Problem

Researching any topic thoroughly is time-consuming and requires visiting multiple sources, synthesizing information, evaluating quality, and writing structured reports. Manual research can take hours and is often inconsistent in depth and coverage.

**Key pain points:**
- Too many sources to read and compare manually
- No consistent way to evaluate research quality
- Report writing is repetitive and slow
- Requires expensive cloud AI APIs (OpenAI, Anthropic)

---

## 2. 💡 Possible Solution

Build an **automated multi-agent AI research pipeline** that:
- Breaks any query into parallel sub-topics
- Searches the web simultaneously using multiple agents
- Evaluates and scores research quality automatically
- Refines the query if quality is low and retries
- Generates a full structured Markdown report
- Runs **100% locally** — no paid API keys required

---

## 3. ✅ Implemented Solution

A **7-agent AI pipeline** built with LangGraph and Ollama that researches any topic end-to-end and produces a professional report via a web dashboard.

| Agent | Role |
|---|---|
| 🧠 **Planner** | Breaks your query into 3 parallel sub-topics |
| 🔍 **Search A / B / C** | Searches the web in parallel (Serper or mock fallback) |
| 📝 **Summarizer** | Synthesizes and deduplicates all findings |
| ⭐ **Critic** | Scores research quality from 0 to 10 |
| 🔄 **Optimizer** | Refines the query if score < 6 (max 3 retries) |
| 📄 **Report Writer** | Generates a full structured Markdown report |
| 🔔 **Notifier** | Sends a Pushover push notification when done |

---

## 4. 🛠️ Tech Stack Used

| Technology | Purpose |
|---|---|
| **Python 3.10+** | Core programming language |
| **LangGraph 0.2.73** | Stateful multi-agent graph orchestration |
| **LangChain 0.3.25** | Prompt templates and chains |
| **Ollama** | Local LLM inference — no API key needed |
| **llama3.2** | Default AI model (runs locally) |
| **FastAPI** | Backend REST API server |
| **Uvicorn** | ASGI web server |
| **Serper API** | Live web search tool (optional) |
| **Pushover** | Push notification on completion (optional) |
| **Python-dotenv** | Environment variable management |

---

## 5. 🏗️ Architecture

### Agent Pipeline Architecture

```
User Query
    ↓
Planner Agent
(Breaks into 3 sub-topics)
    ↓
┌──────────────────────────────────┐
│  parallel search — 3 at once    │
│  Search A  │ Search B │ Search C │
│       (Serper web search)        │
└──────────────────────────────────┘
    ↓
Summarizer Agent
(Condense + deduplicate)
    ↓
Critic / Evaluator
(Score quality 0-10)
    ↓
Score Router
├── score < 6  → Optimizer → (retry loop, max 3 passes)
└── score >= 6 → Report Writer (Markdown + citations)
                      ↓
              Pushover Notification Sent
```

### Slide 1 — architecture
![Architecture](https://raw.githubusercontent.com/Vijjucpu/ai-research-analyst/main/ai_research_analyst/screenshots/architecture.png)

### Slide 2 — optimizer loop
![Optimizer Loop](https://raw.githubusercontent.com/Vijjucpu/ai-research-analyst/main/ai_research_analyst/screenshots/optimizer_loop.png)
### Slide 3 — langraph
![LangGraph](https://raw.githubusercontent.com/Vijjucpu/ai-research-analyst/main/ai_research_analyst/screenshots/langgraph.png)


---

## 6. 🚀 How to Run Locally

### Prerequisites
- Python 3.10+
- [Ollama](https://ollama.com/download) installed

---

### Step 1 — Install Ollama and pull model
```bash
ollama serve
ollama pull llama3.2
```

### Step 2 — Clone the repository
```bash
git clone  https://github.com/Vijjucpu/ai-research-analyst.git
cd ai-research-analyst
```

### Step 3 — Create and activate virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### Step 4 — Install dependencies
```bash
pip install langchain==0.3.25 langchain-core==0.3.84 langchain-community==0.3.24 langchain-ollama==0.2.3 langgraph==0.2.73 langsmith==0.3.45 langgraph-prebuilt==0.2.2 fastapi uvicorn httpx python-dotenv jinja2 aiofiles pydantic --force-reinstall
```

### Step 5 — Configure environment
Open `.env` file and set:
```
OLLAMA_MODEL=llama3.2
OLLAMA_BASE_URL=http://localhost:11434
```

### Step 6 — Run the app
```bash
python main.py
```
Open browser: **http://localhost:8080** 🎉

---

### ⚡ Quick Reference — Every Time You Run

| Step | Terminal | Command |
|---|---|---|
| 1 | Terminal 1 | `ollama serve` |
| 2 | Terminal 2 | `venv\Scripts\activate` |
| 3 | Terminal 2 | `python main.py` |
| 4 | Browser | `http://localhost:8080` |

---

### CLI Mode (no browser needed)
```bash
python main.py cli "Impact of AI on healthcare in 2025"
```

---

## 7. 📚 References and Resources

| Resource | Link |
|---|---|
| LangGraph Documentation | https://langchain-ai.github.io/langgraph |
| LangChain Documentation | https://python.langchain.com |
| Ollama Official Site | https://ollama.com |
| Ollama Model Library | https://ollama.com/library |
| FastAPI Documentation | https://fastapi.tiangolo.com |
| Serper API (web search) | https://serper.dev |
| Pushover Notifications | https://pushover.net |
| LangSmith Tracing | https://smith.langchain.com |

## 8. 📸 Output Screenshots


**Dashboard UI:**

![dashboard](https://raw.githubusercontent.com/Vijjucpu/ai-research-analyst/main/ai_research_analyst/screenshots/dashboard.png)

**Research Running — Live Log:**

![live_log](https://raw.githubusercontent.com/Vijjucpu/ai-research-analyst/main/ai_research_analyst/screenshots/live_log.png)

**Final Report Output:**

![report_output](https://raw.githubusercontent.com/Vijjucpu/ai-research-analyst/main/ai_research_analyst/screenshots/report_output.png)
---

## 9. ⚠️ Problems Faced and Solutions

### ❌ Problem 1 — `ModuleNotFoundError: No module named 'langchain.prompts'`

**Cause:** Newer version of langchain (1.x) installed but project uses 0.3.x syntax.

**Solution:**
```bash
pip install langchain==0.3.25 langchain-core==0.3.84 langchain-community==0.3.24 langchain-ollama==0.2.3 langgraph==0.2.73 --force-reinstall
```

---

### ❌ Problem 2 — `ModuleNotFoundError: No module named 'langchain_ollama'`

**Cause:** Virtual environment not activated — packages were missing.

**Solution:** Always activate venv first:
```bash
venv\Scripts\activate
```

---

### ❌ Problem 3 — `AttributeError: module 'langchain' has no attribute 'verbose'`

**Cause:** Version conflict between langchain and langchain-core.

**Solution:**
```bash
pip install langchain==0.3.25 langchain-core==0.3.84 --force-reinstall
```

---

### ❌ Problem 4 — `[Errno 10048] only one usage of each socket address permitted`

**Cause:** Port 8080 already in use — app was already running in another terminal.

**Solution:** Press `Ctrl + C` in the old terminal, then run again:
```bash
python main.py
```

---

### ❌ Problem 5 — `Research failed: Failed to fetch` on browser

**Cause:** `llama3.2` is slow on CPU and browser request timed out.

**Solution:** After clicking Research, wait **8-10 minutes** without refreshing. For faster results switch to `phi3` in `.env`:
```
OLLAMA_MODEL=phi3
```

---

### ❌ Problem 6 — Dependency conflicts warning with `langchain-openai`

**Cause:** `langchain-openai` requires a different `langchain-core` version.

**Solution:** This is just a warning, not a blocking error. The project does not use `langchain-openai` so safely ignore it. The app runs fine.

---

## 📄 License

MIT License — free to use, modify, and distribute.

---
