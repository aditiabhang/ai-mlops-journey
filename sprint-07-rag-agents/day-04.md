# Sprint 7 · Day 4

## 🔌 Enterprise Connectors — Wire Your Agent to Real Data

`90 min` · `The "production-ready" day` · `Agent meets database, S3, and APIs`

---

&nbsp;

## Today's Big Picture

> Yesterday your agent used simulated data. Today it talks to real systems.
> A Postgres database. An S3 bucket. A REST API.
> These are "enterprise connectors" — the bridges between AI and real data.

By the end of today, you'll have:

- ✅ Connected an agent tool to a SQLite database (simulating Postgres)
- ✅ Connected a tool to read files from disk (simulating S3)
- ✅ Connected a tool to a live REST API
- ✅ Understand how enterprise connectors work in Bedrock Agents

&nbsp;

---

&nbsp;

## How Enterprise Connectors Work

```
┌──────────────────────────────────────────────────────┐
│  ENTERPRISE AI ARCHITECTURE                         │
│                                                      │
│                    ┌──────────────┐                   │
│                    │   AGENT      │                   │
│                    │   (LLM +    │                   │
│                    │    tools)    │                   │
│                    └──────┬───────┘                   │
│                           │                          │
│           ┌───────────────┼───────────────┐          │
│           │               │               │          │
│           ▼               ▼               ▼          │
│    ┌────────────┐  ┌────────────┐  ┌────────────┐   │
│    │ DATABASE   │  │ FILE       │  │ REST API   │   │
│    │ CONNECTOR  │  │ STORAGE    │  │ CONNECTOR  │   │
│    │            │  │ CONNECTOR  │  │            │   │
│    │ Postgres   │  │ S3 / local │  │ Internal   │   │
│    │ MySQL      │  │ files      │  │ services   │   │
│    │ DynamoDB   │  │            │  │ External   │   │
│    │            │  │            │  │ APIs       │   │
│    └────────────┘  └────────────┘  └────────────┘   │
│                                                      │
│  In AWS:                                             │
│  Bedrock Agents → Action Groups → Lambda → Data     │
└──────────────────────────────────────────────────────┘
```

&nbsp;

---

&nbsp;

## Part 1 — Database Connector (SQLite) `30 min`

&nbsp;

### What you're building

A tool that lets the agent query a real database. We'll use SQLite (built into Python — no install needed) to simulate Postgres. The pattern is identical.

&nbsp;

### Do This

**1 →** Set up the project

```bash
mkdir -p ~/projects/ai-mlops-journey/projects/06-enterprise-agent
cd ~/projects/ai-mlops-journey/projects/06-enterprise-agent
python3 -m venv .venv
source .venv/bin/activate
pip install langchain langchain-ollama langchain-core requests
```

&nbsp;

**2 →** Create `setup_db.py` — build a sample database

```python
import sqlite3

conn = sqlite3.connect("support.db")
cursor = conn.cursor()

# Create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY,
    customer TEXT,
    subject TEXT,
    status TEXT,
    priority TEXT,
    created_at TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY,
    name TEXT,
    plan TEXT,
    pods_limit INTEGER,
    region TEXT
)
""")

# Insert sample data
tickets = [
    (1, "Acme Corp", "Pods stuck in Pending", "open", "high", "2025-02-28"),
    (2, "Acme Corp", "Need to increase pod limit", "open", "medium", "2025-03-01"),
    (3, "Globex Inc", "Deployment failing", "resolved", "high", "2025-02-25"),
    (4, "Initech", "Monitoring not working", "open", "low", "2025-03-01"),
    (5, "Globex Inc", "SSL certificate expiring", "open", "high", "2025-03-02"),
]

customers = [
    (1, "Acme Corp", "enterprise", 100, "us-east-1"),
    (2, "Globex Inc", "pro", 50, "eu-west-1"),
    (3, "Initech", "starter", 10, "us-west-2"),
]

cursor.executemany("INSERT OR REPLACE INTO tickets VALUES (?,?,?,?,?,?)", tickets)
cursor.executemany("INSERT OR REPLACE INTO customers VALUES (?,?,?,?,?)", customers)
conn.commit()
conn.close()

print("✅ Database created: support.db")
```

**3 →** Run it

```bash
python3 setup_db.py
```

&nbsp;

**4 →** Create `enterprise_agent.py`

```python
import sqlite3
import os
import json
import requests
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage


# --- TOOL 1: DATABASE CONNECTOR ---

@tool
def query_database(sql: str) -> str:
    """Execute a read-only SQL query against the support database.
    Available tables:
    - tickets (id, customer, subject, status, priority, created_at)
    - customers (id, name, plan, pods_limit, region)
    Use this to look up customer info, ticket status, or support data.
    Only SELECT queries are allowed."""
    if not sql.strip().upper().startswith("SELECT"):
        return "Error: Only SELECT queries are allowed."
    try:
        conn = sqlite3.connect("support.db")
        cursor = conn.cursor()
        cursor.execute(sql)
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        conn.close()
        results = [dict(zip(columns, row)) for row in rows]
        return json.dumps(results, indent=2)
    except Exception as e:
        return f"SQL Error: {e}"


# --- TOOL 2: FILE STORAGE CONNECTOR ---

@tool
def read_runbook(filename: str) -> str:
    """Read a runbook or documentation file from the runbooks directory.
    Available runbooks: pod-pending.md, deployment-failing.md, monitoring-setup.md
    Use this when you need step-by-step troubleshooting instructions."""
    safe_path = os.path.join("runbooks", os.path.basename(filename))
    try:
        with open(safe_path, "r") as f:
            return f.read()
    except FileNotFoundError:
        available = os.listdir("runbooks") if os.path.exists("runbooks") else []
        return f"File not found. Available runbooks: {available}"


# --- TOOL 3: REST API CONNECTOR ---

@tool
def check_api_health(url: str) -> str:
    """Check if an API endpoint is healthy by making a GET request.
    Use this to verify if a service is running.
    Example: check_api_health('https://api.github.com')"""
    try:
        response = requests.get(url, timeout=5)
        return json.dumps({
            "url": url,
            "status_code": response.status_code,
            "healthy": response.status_code == 200,
            "response_time_ms": int(response.elapsed.total_seconds() * 1000)
        })
    except requests.exceptions.ConnectionError:
        return json.dumps({"url": url, "healthy": False, "error": "Connection refused"})
    except requests.exceptions.Timeout:
        return json.dumps({"url": url, "healthy": False, "error": "Timeout"})


# --- AGENT ---

def run_agent():
    llm = ChatOllama(model="llama3.2", temperature=0)
    tools = [query_database, read_runbook, check_api_health]
    llm_with_tools = llm.bind_tools(tools)
    tool_map = {t.name: t for t in tools}

    system = """You are an enterprise support agent with access to:
1. A database of support tickets and customer information
2. Runbook files with troubleshooting steps
3. An API health checker

When a user asks about a customer or ticket, query the database.
When they need troubleshooting help, read the relevant runbook.
When they want to check if a service is up, use the health checker.
Always provide specific data from your tools — don't make things up."""

    print("🏢 Enterprise Support Agent")
    print("   Connected to: Database · Runbooks · API Health")
    print("   Type 'quit' to exit.\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "quit":
            break
        if not user_input:
            continue

        messages = [SystemMessage(content=system), HumanMessage(content=user_input)]
        response = llm_with_tools.invoke(messages)

        if response.tool_calls:
            messages.append(response)
            for tc in response.tool_calls:
                print(f"   🔧 → {tc['name']}({json.dumps(tc['args'])[:80]})")
                result = tool_map[tc["name"]].invoke(tc["args"])
                messages.append({
                    "role": "tool",
                    "content": str(result),
                    "tool_call_id": tc["id"]
                })
            final = llm_with_tools.invoke(messages)
            print(f"\n🤖: {final.content}\n")
        else:
            print(f"\n🤖: {response.content}\n")


if __name__ == "__main__":
    run_agent()
```

&nbsp;

**5 →** Create sample runbooks

```bash
mkdir -p runbooks
```

Create `runbooks/pod-pending.md`:

```markdown
# Runbook: Pods Stuck in Pending

## Symptoms
- Pod shows status "Pending" for more than 5 minutes
- kubectl describe pod shows "no nodes available"

## Diagnosis Steps
1. Check node resources: `kubectl describe nodes | grep -A5 "Allocated resources"`
2. Check if pod resource requests exceed available capacity
3. Check for taints: `kubectl get nodes -o json | jq '.items[].spec.taints'`

## Resolution
- If resource exhaustion: increase node count or reduce pod resource requests
- If taints blocking: add tolerations to the pod spec
- If PVC pending: check StorageClass and available PVs
```

Create `runbooks/deployment-failing.md`:

```markdown
# Runbook: Deployment Failing

## Symptoms
- Pods in CrashLoopBackOff or ImagePullBackOff
- Deployment rollout stuck

## Diagnosis Steps
1. Check pod events: `kubectl describe pod <name>`
2. Check logs: `kubectl logs <pod> --previous`
3. Check image: verify the image tag exists in the registry

## Resolution
- CrashLoopBackOff: fix the application error (check logs)
- ImagePullBackOff: fix image name/tag or add imagePullSecrets
- Rollout stuck: `kubectl rollout undo deployment/<name>`
```

Create `runbooks/monitoring-setup.md`:

```markdown
# Runbook: Setting Up Monitoring

## Prerequisites
- Kubernetes cluster running
- Helm installed

## Steps
1. Add Prometheus Helm chart: `helm repo add prometheus-community https://prometheus-community.github.io/helm-charts`
2. Install: `helm install prometheus prometheus-community/kube-prometheus-stack`
3. Access Grafana: `kubectl port-forward svc/prometheus-grafana 3000:80`
4. Default login: admin / prom-operator
```

&nbsp;

**6 →** Run the agent

```bash
python3 enterprise_agent.py
```

&nbsp;

**7 →** Try these — watch it pick the right connector

```
You: How many open tickets does Acme Corp have?
You: What plan is Globex Inc on?
You: A customer has pods stuck in Pending. What should I do?
You: Is the GitHub API healthy right now?
You: Show me all high priority open tickets
You: What's the runbook for deployment failures?
```

> The agent queries the DATABASE for ticket/customer questions, reads RUNBOOKS for troubleshooting, and calls the API HEALTH tool for service checks. Three different enterprise data systems, one agent.

&nbsp;

---

&nbsp;

## Part 2 — How This Maps to AWS `10 min`

```
┌──────────────────────────────────────────────────────┐
│  YOUR CODE                PRODUCTION / AWS           │
│                                                      │
│  SQLite + query_database  →  RDS/DynamoDB + Lambda   │
│  runbooks/ + read_runbook →  S3 bucket + Lambda      │
│  requests + health check  →  Lambda calling any API  │
│  LangChain agent          →  Bedrock Agent           │
│  @tool decorator          →  Agent Action Group      │
│  System prompt            →  Agent Instructions      │
│                                                      │
│  BEDROCK AGENTS ARCHITECTURE:                        │
│                                                      │
│  User ──▶ Bedrock Agent ──▶ Action Group ──▶ Lambda  │
│                                               │      │
│                                               ▼      │
│                                          Data System  │
│                                          (RDS, S3,   │
│                                           API, etc.) │
└──────────────────────────────────────────────────────┘
```

&nbsp;

---

&nbsp;

## Part 3 — Commit `5 min`

```bash
cd ~/projects/ai-mlops-journey
echo -e ".venv/\nsupport.db" > projects/06-enterprise-agent/.gitignore
git add projects/06-enterprise-agent/ sprint-07-rag-agents/
git commit -m "sprint 7 day 4: enterprise connectors — database, file storage, REST API 🔌"
git push
```

&nbsp;

---

&nbsp;

## ✅ Day 4 Checklist

| | Task |
|---|------|
| ☐ | Agent queries a real database (SQLite) for customer/ticket data |
| ☐ | Agent reads runbook files from disk (simulating S3) |
| ☐ | Agent checks live API health via REST |
| ☐ | Agent picks the correct connector based on the question |
| ☐ | Understand how this maps to Bedrock Agents + Lambda |
| ☐ | Pushed to GitHub 🟩 |

&nbsp;

---

&nbsp;

## 🧠 Concepts You Now Own

| Concept | One-liner |
|---------|-----------|
| **Enterprise connector** | A bridge between an AI agent and a data system |
| **Database connector** | Tool that translates natural language to SQL queries |
| **File storage connector** | Tool that reads docs from S3 or local filesystem |
| **API connector** | Tool that calls REST endpoints on behalf of the agent |
| **Action Group** | Bedrock Agents term — a collection of tools (Lambda functions) |
| **Read-only safety** | Only allow SELECT queries — agents shouldn't write/delete |
| **Path sanitization** | Prevent agents from reading files outside allowed directories |

&nbsp;

---

&nbsp;

> *Next: Capstone — tie RAG + Agent + Connectors into one portfolio project. 🚀*
