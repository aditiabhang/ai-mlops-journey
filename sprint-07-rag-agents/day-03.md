# Sprint 7 · Day 3

## 🤖🔧 Agents — LLMs That Use Tools

`90 min` · `The "woah" day` · `Your LLM stops just talking and starts DOING`

---

&nbsp;

## Today's Big Picture

> A chatbot answers questions. An AGENT takes actions.
> Need to check a database? The agent writes and runs the query.
> Need to call an API? The agent calls it.
> Today you build an LLM that can use tools — the foundation of every AI agent.

By the end of today, you'll have:

- ✅ Understand what agents are and how they work
- ✅ Know the ReAct pattern (Reason + Act)
- ✅ Built an agent with custom tools using LangChain
- ✅ Watched an LLM decide WHICH tool to use and WHEN

&nbsp;

---

&nbsp;

## Part 1 — What is an Agent? `15 min`

&nbsp;

### Chatbot vs Agent (30-second version)

```
┌──────────────────────────────────────────────────────┐
│                                                      │
│  CHATBOT                       AGENT                 │
│                                                      │
│  User asks ──▶ LLM answers     User asks ──▶ LLM    │
│                                     │        THINKS  │
│  That's it.                         ▼                │
│  Just words.                   "I need to check      │
│                                 the database"        │
│                                     │                │
│                                     ▼                │
│                                CALLS A TOOL          │
│                                (runs SQL query)      │
│                                     │                │
│                                     ▼                │
│                                GETS RESULT           │
│                                     │                │
│                                     ▼                │
│                                "Based on the         │
│                                 data, here's         │
│                                 your answer"         │
└──────────────────────────────────────────────────────┘
```

&nbsp;

### The ReAct Pattern — how agents think

Agents follow a loop: **Re**ason → **Act** → **Observe** → repeat until done.

```
User: "How many pods are running in the cluster?"

Agent thinking:
  THOUGHT: I need to check the cluster status.
  ACTION:  Call the "get_pods" tool
  OBSERVATION: Tool returned: 5 pods running, 1 pending

  THOUGHT: I have the answer now.
  ACTION:  Respond to the user
  ANSWER:  "There are 5 pods running and 1 pending in the cluster."
```

> The LLM decides WHICH tool to call and WHEN. You define the tools. The LLM handles the logic.

&nbsp;

---

&nbsp;

## Part 2 — Set Up LangChain `10 min`

&nbsp;

### What is LangChain? (30-second version)

LangChain is the most popular framework for building LLM applications. It provides pre-built pieces — agents, tools, chains, memory — so you don't build everything from scratch.

```
LangChain pieces you'll use today:

  ┌──────────┐  ┌──────────┐  ┌──────────┐
  │  LLM     │  │  TOOLS   │  │  AGENT   │
  │          │  │          │  │          │
  │  Ollama  │  │  Your    │  │  Connects │
  │  local   │  │  custom  │  │  LLM +    │
  │  model   │  │  Python  │  │  tools    │
  │          │  │  functions│ │  together │
  └──────────┘  └──────────┘  └──────────┘
```

&nbsp;

### Do This

```bash
mkdir -p ~/projects/ai-mlops-journey/projects/05-agent
cd ~/projects/ai-mlops-journey/projects/05-agent
python3 -m venv .venv
source .venv/bin/activate
pip install langchain langchain-ollama langchain-core
```

&nbsp;

---

&nbsp;

## Part 3 — Build Your First Agent `40 min`

&nbsp;

### Do This

**1 →** Create `agent.py`

```python
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage
import json
from datetime import datetime


# --- TOOLS ---
# These are the functions the agent CAN call.
# The docstring tells the LLM what each tool does.

@tool
def get_current_time() -> str:
    """Get the current date and time. Use this when asked about the time or date."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@tool
def get_pod_status() -> str:
    """Get the status of Kubernetes pods in the cluster.
    Use this when asked about pod health, cluster status, or running workloads."""
    # Simulated — in production, this would call the K8s API
    pods = [
        {"name": "nginx-7b8d", "status": "Running", "restarts": 0},
        {"name": "redis-3f2a", "status": "Running", "restarts": 2},
        {"name": "api-9c1e", "status": "CrashLoopBackOff", "restarts": 14},
        {"name": "worker-5d7b", "status": "Running", "restarts": 0},
        {"name": "db-backup-x2", "status": "Completed", "restarts": 0},
    ]
    return json.dumps(pods, indent=2)


@tool
def search_docs(query: str) -> str:
    """Search the knowledge base for information about Kubernetes concepts.
    Use this when asked about K8s concepts, architecture, or best practices."""
    # Simulated — in production, this would be your RAG vector search
    docs = {
        "scaling": "Use HPA for auto-scaling based on CPU/memory. Use kubectl scale for manual scaling.",
        "networking": "Services provide stable endpoints. ClusterIP for internal, NodePort for external.",
        "security": "Use RBAC for access control. Secrets for sensitive data. Network Policies for isolation.",
        "monitoring": "Prometheus for metrics, Grafana for dashboards, Fluentd for logs, Jaeger for traces.",
        "deployment": "Deployments manage ReplicaSets. Support rolling updates and rollbacks.",
    }
    # Simple keyword matching — real version would use vector search
    for key, value in docs.items():
        if key in query.lower():
            return value
    return "No relevant documentation found for that query."


@tool
def calculate(expression: str) -> str:
    """Evaluate a mathematical expression. Use this for any math calculations.
    Example input: '2 + 2' or '100 / 5 * 3'"""
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error: {e}"


# --- AGENT ---

def run_agent():
    # Set up the LLM with tools
    llm = ChatOllama(model="llama3.2", temperature=0)
    tools = [get_current_time, get_pod_status, search_docs, calculate]
    llm_with_tools = llm.bind_tools(tools)

    # Tool lookup map
    tool_map = {t.name: t for t in tools}

    print("🤖 K8s Support Agent")
    print("   I can check pods, search docs, do math, and tell time.")
    print("   Type 'quit' to exit.\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "quit":
            print("👋 Bye!")
            break
        if not user_input:
            continue

        messages = [
            SystemMessage(content=(
                "You are a helpful Kubernetes support agent. "
                "Use the available tools to answer questions accurately. "
                "Always use a tool when one is relevant."
            )),
            HumanMessage(content=user_input)
        ]

        # Ask the LLM — it may request tool calls
        response = llm_with_tools.invoke(messages)

        # Check if the LLM wants to call tools
        if response.tool_calls:
            print(f"   🔧 Agent is using tools...")
            messages.append(response)

            for tc in response.tool_calls:
                tool_name = tc["name"]
                tool_args = tc["args"]
                print(f"   → Calling: {tool_name}({tool_args})")

                # Execute the tool
                tool_result = tool_map[tool_name].invoke(tool_args)
                messages.append({
                    "role": "tool",
                    "content": str(tool_result),
                    "tool_call_id": tc["id"]
                })

            # Get final answer with tool results
            final = llm_with_tools.invoke(messages)
            print(f"\n🤖: {final.content}\n")
        else:
            print(f"\n🤖: {response.content}\n")


if __name__ == "__main__":
    run_agent()
```

&nbsp;

**2 →** Run it

```bash
python3 agent.py
```

&nbsp;

**3 →** Try these — watch which tools the agent picks

```
You: What time is it?
You: Are any pods unhealthy right now?
You: How do I set up monitoring in Kubernetes?
You: If I have 5 pods each using 256Mi memory, what's the total?
You: How many pods are in CrashLoopBackOff and what should I do about it?
```

> 🤯 That last question is the magic moment. The agent:
> 1. Calls `get_pod_status` to check
> 2. Finds the CrashLoopBackOff pod
> 3. Maybe calls `search_docs` for troubleshooting advice
> 4. Gives you a combined answer

It CHOSE which tools to use. You didn't tell it.

&nbsp;

---

&nbsp;

## Part 4 — How This Maps to Production `10 min`

```
┌──────────────────────────────────────────────────────┐
│  YOUR CODE               PRODUCTION EQUIVALENT       │
│                                                      │
│  @tool functions      →  Bedrock Agent action groups │
│  llm.bind_tools()     →  Bedrock Agent configuration│
│  LangChain agent      →  Bedrock Agents / LangGraph │
│  Simulated pod data   →  Real K8s API call           │
│  Keyword doc search   →  RAG vector search           │
│  ChatOllama           →  Bedrock InvokeModel         │
└──────────────────────────────────────────────────────┘
```

&nbsp;

---

&nbsp;

## Part 5 — Commit `5 min`

```bash
cd ~/projects/ai-mlops-journey
echo ".venv/" > projects/05-agent/.gitignore
git add projects/05-agent/ sprint-07-rag-agents/
git commit -m "sprint 7 day 3: LLM agent with tool-calling — pods, docs, math, time 🤖🔧"
git push
```

&nbsp;

---

&nbsp;

## ✅ Day 3 Checklist

| | Task |
|---|------|
| ☐ | Can explain the difference between a chatbot and an agent |
| ☐ | Understand the ReAct pattern (Reason → Act → Observe) |
| ☐ | Built an agent with 4 custom tools |
| ☐ | Watched the LLM decide which tool to call on its own |
| ☐ | Pushed to GitHub 🟩 |

&nbsp;

---

&nbsp;

## 🧠 Concepts You Now Own

| Concept | One-liner |
|---------|-----------|
| **Agent** | An LLM that can take actions, not just generate text |
| **Tool** | A function the agent can call — you define what it does |
| **ReAct** | Reason + Act — the loop agents follow |
| **Tool-calling** | LLM decides which function to invoke based on the question |
| **LangChain** | Framework for building LLM apps — agents, tools, chains |
| **bind_tools()** | Tell the LLM "here are the tools you can use" |
| **Bedrock Agents** | AWS managed agent service — same concept, production-ready |
| **Action group** | Bedrock Agents term for a collection of tools |

&nbsp;

---

&nbsp;

> *Next: Wire your agent to real data — Postgres, S3, REST APIs. Enterprise connectors. 🔌*
