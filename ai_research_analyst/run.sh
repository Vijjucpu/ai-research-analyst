#!/bin/bash
set -e

echo ""
echo "  ============================================"
echo "   AI Research Analyst Agent"
echo "   Powered by Ollama (No OpenAI key needed)"
echo "  ============================================"
echo ""

# Check Ollama is running
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
  echo "  [ERROR] Ollama is not running."
  echo "  Start it with:  ollama serve"
  echo "  Then run this script again."
  exit 1
fi

MODEL=${OLLAMA_MODEL:-llama3.2}
echo "  Ollama is running."

# Pull model if not present
if ! ollama list 2>/dev/null | grep -q "$MODEL"; then
  echo "  Pulling model: $MODEL ..."
  ollama pull "$MODEL"
fi

echo "  Model ready: $MODEL"
echo ""

# Install Python deps if needed
if ! python3 -c "import langgraph" 2>/dev/null; then
  echo "  Installing Python dependencies..."
  pip install -r requirements.txt -q
fi

echo "  Starting server at http://localhost:8080"
echo ""
python3 main.py
