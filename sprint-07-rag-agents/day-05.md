# Sprint 7 · Day 5

## 🚀 Capstone: AI Support Agent with RAG + Enterprise Data

`90 min` · `The final project` · `Everything you've built, in one system`

---

&nbsp;

## Today's Big Picture

> This is the project that ties your entire journey together.
> An AI support agent that can search your docs (RAG), query a database,
> and check service health — deployed as an API. This goes on your resume.

By the end of today, you'll have:

- ✅ Combined RAG + Agent + Enterprise Connectors into one system
- ✅ Wrapped it in a FastAPI server with endpoints
- ✅ Written a killer README with architecture diagram
- ✅ The capstone project pushed to GitHub 🎉

&nbsp;

---

&nbsp;

## The Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  AI SUPPORT AGENT — CAPSTONE                                │
│                                                             │
│  User                                                       │
│    │                                                        │
│    ▼                                                        │
│  ┌────────────────────────────────┐                         │
│  │  FastAPI Server (:8000)       │                         │
│  │  POST /ask                    │                         │
│  │  GET  /health                 │                         │
│  └──────────────┬─────────────────┘                         │
│                 │                                           │
│                 ▼                                           │
│  ┌────────────────────────────────┐                         │
│  │  LLM AGENT (Ollama + Tools)   │                         │
│  │  Decides which tool to call   │                         │
│  └──────────┬─────────┬──────────┘                         │
│             │         │         │                           │
│    ┌────────▼──┐ ┌────▼─────┐ ┌▼───────────┐              │
│    │ RAG       │ │ DATABASE │ │ API HEALTH │              │
│    │           │ │          │ │            │              │
│    │ ChromaDB  │ │ SQLite   │ │ requests   │              │
│    │ + Ollama  │ │ tickets  │ │ GET check  │              │
│    │ embeddings│ │ customers│ │            │              │
│    │           │ │          │ │            │              │
│    │ K8s docs  │ │ Runbooks │ │ Any URL    │              │
│    └───────────┘ └──────────┘ └────────────┘              │
└─────────────────────────────────────────────────────────────┘
```

&nbsp;

---

&nbsp;

## Part 1 — Build the Capstone `50 min`

&nbsp;

### Do This

**1 →** Create the project

```bash
mkdir -p ~/projects/ai-mlops-journey/projects/07-capstone-agent/docs
mkdir -p ~/projects/ai-mlops-journey/projects/07-capstone-agent/runbooks
cd ~/projects/ai-mlops-journey/projects/07-capstone-agent
python3 -m venv .venv
source .venv/bin/activate
pip install fastapi uvicorn chromadb requests langchain langchain-ollama langchain-core
```

&nbsp;

**2 →** Copy your docs and runbooks from earlier sprints

```bash
cp ~/projects/ai-mlops-journey/projects/04-rag-pipeline/docs/*.md docs/
cp ~/projects/ai-mlops-journey/projects/06-enterprise-agent/runbooks/*.md runbooks/
cp ~/projects/ai-mlops-journey/projects/06-enterprise-agent/setup_db.py .
python3 setup_db.py
```

&nbsp;

**3 →** Create `capstone.py`

```python
import os
import json
import sqlite3
import chromadb
import requests
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage

# ─── CONFIG ───

OLLAMA_URL = "http://localhost:11434"
EMBED_MODEL = "nomic-embed-text"
CHAT_MODEL = "llama3.2"

app = FastAPI(title="AI Support Agent", version="1.0")


# ─── HELPERS ───

def get_embedding(text):
    r = requests.post(f"{OLLAMA_URL}/api/embed", json={
        "model": EMBED_MODEL, "input": text
    })
    return r.json()["embeddings"][0]


# ─── RAG INDEX (built at startup) ───

def build_rag_index():
    client = chromadb.Client()
    try:
        client.delete_collection("docs")
    except Exception:
        pass
    collection = client.create_collection("docs")

    for filename in os.listdir("docs"):
        if not filename.endswith(".md"):
            continue
        with open(os.path.join("docs", filename)) as f:
            text = f.read()
        sections = text.split("\n## ")
        for i, section in enumerate(sections):
            section = section.strip()
            if not section:
                continue
            embedding = get_embedding(section)
            collection.add(
                ids=[f"{filename}_{i}"],
                embeddings=[embedding],
                documents=[section],
                metadatas=[{"source": filename}]
            )
    return collection


print("📦 Building RAG index...")
rag_collection = build_rag_index()
print("✅ RAG index ready\n")


# ─── TOOLS ───

@tool
def search_knowledge_base(query: str) -> str:
    """Search the Kubernetes documentation for answers about K8s concepts,
    architecture, troubleshooting, and best practices.
    Use this when the user asks about Kubernetes topics."""
    query_emb = get_embedding(query)
    results = rag_collection.query(query_embeddings=[query_emb], n_results=3)
    if results["documents"][0]:
        chunks = "\n\n---\n\n".join(results["documents"][0])
        sources = [m["source"] for m in results["metadatas"][0]]
        return f"Sources: {sources}\n\nContent:\n{chunks}"
    return "No relevant documentation found."


@tool
def query_database(sql: str) -> str:
    """Execute a read-only SQL query on the support database.
    Tables: tickets (id, customer, subject, status, priority, created_at),
    customers (id, name, plan, pods_limit, region).
    Use for customer lookups, ticket searches, and support data."""
    if not sql.strip().upper().startswith("SELECT"):
        return "Error: Only SELECT queries allowed."
    try:
        conn = sqlite3.connect("support.db")
        cur = conn.cursor()
        cur.execute(sql)
        cols = [d[0] for d in cur.description]
        rows = [dict(zip(cols, r)) for r in cur.fetchall()]
        conn.close()
        return json.dumps(rows, indent=2)
    except Exception as e:
        return f"SQL Error: {e}"


@tool
def read_runbook(filename: str) -> str:
    """Read a troubleshooting runbook. Available: pod-pending.md,
    deployment-failing.md, monitoring-setup.md.
    Use when the user needs step-by-step troubleshooting instructions."""
    path = os.path.join("runbooks", os.path.basename(filename))
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        available = os.listdir("runbooks") if os.path.exists("runbooks") else []
        return f"Not found. Available: {available}"


@tool
def check_health(url: str) -> str:
    """Check if a URL/API endpoint is reachable and healthy.
    Use when asked to verify if a service is running."""
    try:
        r = requests.get(url, timeout=5)
        return json.dumps({
            "url": url, "status": r.status_code,
            "healthy": r.status_code == 200,
            "response_ms": int(r.elapsed.total_seconds() * 1000)
        })
    except Exception as e:
        return json.dumps({"url": url, "healthy": False, "error": str(e)})


# ─── AGENT ───

SYSTEM_PROMPT = """You are an AI support agent for a Kubernetes platform team.
You have access to:
1. A knowledge base of K8s documentation (search_knowledge_base)
2. A database of support tickets and customers (query_database)
3. Troubleshooting runbooks (read_runbook)
4. A service health checker (check_health)

Always use tools to get real data. Never make up information.
When answering from docs, cite the source. When querying the database, show the data."""

llm = ChatOllama(model=CHAT_MODEL, temperature=0)
tools = [search_knowledge_base, query_database, read_runbook, check_health]
llm_with_tools = llm.bind_tools(tools)
tool_map = {t.name: t for t in tools}


def agent_ask(question: str) -> dict:
    messages = [SystemMessage(content=SYSTEM_PROMPT), HumanMessage(content=question)]
    response = llm_with_tools.invoke(messages)

    tools_used = []
    if response.tool_calls:
        messages.append(response)
        for tc in response.tool_calls:
            tools_used.append(tc["name"])
            result = tool_map[tc["name"]].invoke(tc["args"])
            messages.append({
                "role": "tool", "content": str(result), "tool_call_id": tc["id"]
            })
        final = llm_with_tools.invoke(messages)
        return {"answer": final.content, "tools_used": tools_used}
    return {"answer": response.content, "tools_used": []}


# ─── API ───

class AskRequest(BaseModel):
    question: str


@app.get("/health")
def health():
    return {"status": "healthy", "model": CHAT_MODEL, "tools": [t.name for t in tools]}


@app.post("/ask")
def ask(req: AskRequest):
    result = agent_ask(req.question)
    return result
```

&nbsp;

**4 →** Run it

```bash
uvicorn capstone:app --reload --port 8000
```

&nbsp;

**5 →** Test it

```bash
# RAG — searches docs
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "How does Kubernetes scaling work?"}'

# Database — queries tickets
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Show me all open high priority tickets"}'

# Runbook — reads troubleshooting steps
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "A customer has pods stuck in Pending, what should I do?"}'

# API health — checks a live endpoint
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Is the GitHub API healthy?"}'
```

&nbsp;

**6 →** Visit `http://localhost:8000/docs` — interactive API docs.

&nbsp;

---

&nbsp;

## Part 2 — Write the README `25 min`

Create `projects/07-capstone-agent/README.md`:

```markdown
# 🤖 AI Support Agent — Capstone Project

An AI-powered support agent that answers questions using RAG, queries a database,
reads runbooks, and checks service health. Built with Python, LangChain, Ollama,
ChromaDB, and FastAPI.

## Architecture

```
User → FastAPI → LLM Agent → decides which tool:
                                ├── RAG (ChromaDB + docs)
                                ├── Database (SQLite)
                                ├── Runbooks (file system)
                                └── API Health (REST)
```

## What it does

- **RAG search** — answers K8s questions grounded in documentation
- **Database queries** — looks up customer info and support tickets
- **Runbook access** — retrieves step-by-step troubleshooting guides
- **API health checks** — verifies if services are running

The agent decides WHICH tool to use based on your question. No hardcoded routing.

## Tech stack

| Component | Technology |
|-----------|-----------|
| LLM | Ollama (llama3.2) |
| Embeddings | nomic-embed-text |
| Vector DB | ChromaDB |
| Agent framework | LangChain |
| API | FastAPI |
| Database | SQLite |

## How to run

1. Install Ollama and pull models:
   ```bash
   ollama pull llama3.2
   ollama pull nomic-embed-text
   ollama serve
   ```

2. Set up the project:
   ```bash
   python3 -m venv .venv && source .venv/bin/activate
   pip install fastapi uvicorn chromadb requests langchain langchain-ollama langchain-core
   python3 setup_db.py
   ```

3. Run the server:
   ```bash
   uvicorn capstone:app --reload --port 8000
   ```

4. Ask a question:
   ```bash
   curl -X POST http://localhost:8000/ask \
     -H "Content-Type: application/json" \
     -d '{"question": "How many open tickets does Acme Corp have?"}'
   ```

## Built during
AI/MLOps Learning Journey — Sprint 7 (RAG, Agents & Enterprise Connectors)
```

&nbsp;

---

&nbsp;

## Part 3 — Commit & Push `10 min`

```bash
cd ~/projects/ai-mlops-journey
echo -e ".venv/\nsupport.db" > projects/07-capstone-agent/.gitignore
git add projects/07-capstone-agent/ sprint-07-rag-agents/
git commit -m "sprint 7 capstone: AI support agent — RAG + database + runbooks + API health 🚀"
git push
```

&nbsp;

---

&nbsp;

## ✅ Day 5 Checklist

| | Task |
|---|------|
| ☐ | Capstone combines RAG + database + runbooks + health checks |
| ☐ | FastAPI serves the agent with /ask and /health endpoints |
| ☐ | Agent picks the right tool for each question type |
| ☐ | README written with architecture and setup instructions |
| ☐ | Pushed to GitHub 🟩 |

&nbsp;

---

&nbsp;

## 🎉 Sprint 7 Complete — ALL GAPS CLOSED

&nbsp;

### Gap analysis — AFTER

```
┌──────────────────────────────────────────────────────┐
│  REQUIREMENT                        STATUS           │
│                                                      │
│  ✅ Understanding the AI landscape   Sprints 5-6     │
│  ✅ Hands-on with LLMs              Sprints 3, 5-7  │
│  ✅ Vector Databases                 Day 1 — ChromaDB│
│  ✅ RAG                              Day 2 — full    │
│  ✅ Agent builders                   Day 3 — LangChain│
│  ✅ Enterprise connectors            Day 4 — DB, S3, │
│                                      API              │
│  ✅ Capstone project proving it all  Day 5            │
└──────────────────────────────────────────────────────┘
```

&nbsp;

### What you can now say in an interview

```
"I've built RAG pipelines from scratch — document chunking,
 embedding generation with Ollama, semantic search with ChromaDB,
 and LLM-grounded answer generation.

 I've built LLM agents using LangChain with custom tool-calling —
 the agent decides which data source to query based on the question.

 I've connected agents to enterprise data systems including databases,
 file storage, and REST APIs — the same pattern Bedrock Agents uses
 with Lambda action groups.

 All projects are on my GitHub with READMEs and architecture docs."
```

That's not a claim. That's a portfolio. 🔥

&nbsp;

---

&nbsp;

> *You started with nothing installed.*
> *7 sprints later: 2 certifications, 7 projects, hands-on with every AI technology that matters.*
> *Go get that job. 💪*
