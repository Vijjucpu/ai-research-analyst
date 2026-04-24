import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama

load_dotenv()

OLLAMA_BASE = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
MODEL       = os.getenv("OLLAMA_MODEL", "llama3.2")

def get_llm(temperature: float = 0.2):
    return ChatOllama(
        model=MODEL,
        base_url=OLLAMA_BASE,
        temperature=temperature,
        num_predict=2048,
    )

planner_llm    = get_llm(temperature=0.2)
searcher_llm   = get_llm(temperature=0.0)
summarizer_llm = get_llm(temperature=0.3)
critic_llm     = get_llm(temperature=0.0)
optimizer_llm  = get_llm(temperature=0.5)
report_llm     = get_llm(temperature=0.4)
