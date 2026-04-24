# AI Research Analyst Agent
### Multi-Agent · LangGraph · Ollama · No OpenAI Key Required

---

## What it does

Researches any topic end-to-end using 7 specialized AI agents:

| Agent | Role |
|---|---|
| Planner | Breaks your query into 3 parallel sub-topics |
| Search A/B/C | Searches the web in parallel (Serper or mock fallback) |
| Summarizer | Synthesizes and deduplicates all findings |
| Critic | Scores research quality 0-10 |
| Optimizer | Refines query if score < 6 (max 2 retries) |
| Report Writer | Generates a full structured Markdown report |
| Notifier | Sends Pushover push notification when done |

---

## Quick Start (3 steps)

### Step 1 — Make sure Ollama is running
```bash
ollama serve
ollama pull llama3.2
```

### Step 2 — Configure your model (optional)
Edit `.env`:
```
OLLAMA_MODEL=llama3.2        # or: mistral, llama3.1, gemma2, phi3
OLLAMA_BASE_URL=http://localhost:11434
```

### Step 3 — Run
```bash
./run.sh
```
Then open: **http://localhost:8080**

---

## Manual install (without run.sh)
```bash
pip install -r requirements.txt
python main.py
```

---

## CLI mode (no browser needed)
```bash
python main.py cli "Impact of AI on healthcare in 2025"
```

---

## Docker mode
```bash
docker-compose up --build
```
> Note: Docker uses `network_mode: host` so it can reach Ollama on localhost.

---

## Optional API keys (project still works without them)

| Key | Purpose | Get it |
|---|---|---|
| `SERPER_API_KEY` | Real web search | serper.dev (free tier) |
| `PUSHOVER_USER_KEY` + `PUSHOVER_APP_TOKEN` | Push notifications | pushover.net |

Without Serper, the project uses mock search results — great for testing.

---

## Recommended Ollama models

| Model | Speed | Quality | RAM needed |
|---|---|---|---|
| `llama3.2` | Fast | Good | 4 GB |
| `llama3.1` | Medium | Better | 8 GB |
| `mistral` | Fast | Good | 4 GB |
| `gemma2` | Fast | Good | 5 GB |
| `phi3` | Very fast | Decent | 3 GB |

---

## Course concepts demonstrated

- Docker · Containerised deployment
- LLMs / Transformers · Ollama local models
- Tokenization · Prompt input processing
- MCP pattern · Tools as callable functions (Serper, Pushover)
- LangGraph · Stateful multi-agent graph
- LangChain · Prompt templates, chains
- Agents · 7 specialized agents with distinct roles
- Handoffs · Orchestrator → workers → evaluator
- Parallelization · 3 search agents run simultaneously
- Orchestrator-Worker · Planner + 3 search workers
- Evaluator-Optimizer · Critic scores → Optimizer refines → loop
- Prompt Chaining · Query → topics → search → summary → report
- Routing · route_after_critic() conditional edge
- Multi-model · Different temperatures per agent role
- Serper · Live web search tool
- Pushover · Push notification on completion
