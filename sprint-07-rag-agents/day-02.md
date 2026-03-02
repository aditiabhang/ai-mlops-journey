# Sprint 7 · Day 2

## 🔗 Build a RAG Pipeline — From Docs to Answers

`90 min` · `The big one` · `You build the thing everyone talks about`

---

&nbsp;

## Today's Big Picture

> Yesterday you built semantic search. Today you add an LLM on top.
> That's RAG — Retrieval Augmented Generation.
> The user asks a question → you find relevant docs → the LLM answers USING those docs.
> No hallucinations. Grounded in YOUR data.

By the end of today, you'll have:

- ✅ Built a document chunking system
- ✅ Created a full RAG pipeline (load → chunk → embed → retrieve → generate)
- ✅ Asked questions and got grounded answers from your own documents
- ✅ Understand every piece of how RAG works — because you built it

&nbsp;

---

&nbsp;

## The Architecture You're Building

```
┌──────────────────────────────────────────────────────────┐
│  YOUR RAG PIPELINE                                       │
│                                                          │
│  ┌────────────┐   ┌────────────┐   ┌────────────────┐   │
│  │ 1. LOAD    │   │ 2. CHUNK   │   │ 3. EMBED       │   │
│  │            │   │            │   │                │   │
│  │ Read your  │──▶│ Split into │──▶│ Convert each   │   │
│  │ documents  │   │ small      │   │ chunk to a     │   │
│  │ (.md files)│   │ pieces     │   │ vector         │   │
│  └────────────┘   └────────────┘   └───────┬────────┘   │
│                                            │             │
│                                            ▼             │
│                                    ┌───────────────┐     │
│                                    │ 4. STORE      │     │
│                                    │               │     │
│                                    │ ChromaDB      │     │
│                                    └───────┬───────┘     │
│                                            │             │
│  User asks: "How do I scale pods?"         │             │
│       │                                    │             │
│       ▼                                    ▼             │
│  ┌────────────┐   ┌────────────┐   ┌───────────────┐    │
│  │ 5. EMBED   │   │ 6. SEARCH  │   │ 7. GENERATE  │    │
│  │ QUERY      │──▶│ Find top 3 │──▶│ Send question│    │
│  │            │   │ relevant   │   │ + docs to LLM│    │
│  │ Convert    │   │ chunks     │   │              │    │
│  │ question   │   │            │   │ LLM answers  │    │
│  │ to vector  │   │            │   │ USING docs   │    │
│  └────────────┘   └────────────┘   └───────────────┘    │
│                                                          │
│  Answer: "You can scale pods using kubectl scale or HPA" │
│  Source: chunk from your HPA doc ✅                      │
└──────────────────────────────────────────────────────────┘
```

&nbsp;

---

&nbsp;

## Part 1 — Create Your Knowledge Base `10 min`

&nbsp;

### Do This

**1 →** Set up the project

```bash
mkdir -p ~/projects/ai-mlops-journey/projects/04-rag-pipeline/docs
cd ~/projects/ai-mlops-journey/projects/04-rag-pipeline
python3 -m venv .venv
source .venv/bin/activate
pip install chromadb requests
```

&nbsp;

**2 →** Create some docs to search over. Create `docs/kubernetes.md`:

```markdown
# Kubernetes Core Concepts

## Pods
A Pod is the smallest deployable unit in Kubernetes. It represents a single instance of a running process. Pods can contain one or more containers that share storage and network. When a pod dies, Kubernetes does not resurrect it — a controller like a Deployment creates a new one.

## Deployments
A Deployment provides declarative updates for Pods and ReplicaSets. You describe a desired state, and the Deployment controller changes the actual state to match. Deployments support rolling updates, rollbacks, and scaling. Use kubectl scale or edit the replicas field in the YAML to scale.

## Services
A Service provides a stable network endpoint for accessing a set of Pods. Pods get random IPs that change on restart — Services solve this with a consistent address. Types include ClusterIP (internal), NodePort (external via port), and LoadBalancer (external via cloud IP).

## Horizontal Pod Autoscaler
The HPA automatically scales the number of pod replicas based on CPU utilization or custom metrics. When load increases, HPA adds more pods. When load decreases, it removes them. This saves cost and handles traffic spikes automatically.

## ConfigMaps and Secrets
ConfigMaps store non-sensitive configuration as key-value pairs. Secrets store sensitive data like passwords and tokens, base64 encoded. Both can be injected into pods as environment variables or mounted as files. This keeps configuration separate from application code.

## RBAC
Role-Based Access Control defines who can do what in a cluster. Roles define permissions within a namespace. ClusterRoles define cluster-wide permissions. RoleBindings and ClusterRoleBindings connect users or service accounts to roles.
```

&nbsp;

**3 →** Create `docs/observability.md`:

```markdown
# Observability in Kubernetes

## Prometheus
Prometheus is a CNCF graduated project for monitoring. It scrapes metrics from application endpoints every 15 seconds and stores them as time-series data. You query metrics using PromQL. Prometheus also supports alerting via Alertmanager.

## Grafana
Grafana provides dashboards and visualization for metrics. It connects to Prometheus as a data source and displays graphs, heatmaps, and alerts. Teams use Grafana to monitor cluster health, application performance, and SLA compliance.

## Logging with Fluentd
Fluentd is a CNCF graduated log collector. It gathers logs from all pods and ships them to a centralized store like Elasticsearch. The EFK stack (Elasticsearch, Fluentd, Kibana) is a common logging solution for Kubernetes.

## Distributed Tracing with Jaeger
Jaeger tracks requests as they flow across microservices. Each request gets a trace ID, and each hop is a span. This helps identify bottlenecks — for example, finding that a database query takes 500ms out of a 600ms total request time.
```

> You can add more docs — your cheatsheets, your sprint notes, anything. More docs = more to search over.

&nbsp;

---

&nbsp;

## Part 2 — Build the RAG Pipeline `45 min`

&nbsp;

### Do This

Create `rag.py`:

```python
import os
import chromadb
import requests

OLLAMA_URL = "http://localhost:11434"
EMBED_MODEL = "nomic-embed-text"
CHAT_MODEL = "llama3.2"


def get_embedding(text):
    """Convert text to a vector."""
    response = requests.post(f"{OLLAMA_URL}/api/embed", json={
        "model": EMBED_MODEL,
        "input": text
    })
    return response.json()["embeddings"][0]


def chat(prompt):
    """Send a prompt to the LLM and get a response."""
    response = requests.post(f"{OLLAMA_URL}/api/chat", json={
        "model": CHAT_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False
    })
    return response.json()["message"]["content"]


def load_and_chunk(docs_dir, chunk_size=500):
    """Load markdown files and split into chunks."""
    chunks = []
    for filename in os.listdir(docs_dir):
        if not filename.endswith(".md"):
            continue
        filepath = os.path.join(docs_dir, filename)
        with open(filepath, "r") as f:
            text = f.read()

        # Split by sections (## headers)
        sections = text.split("\n## ")
        for i, section in enumerate(sections):
            section = section.strip()
            if not section:
                continue
            # Keep a reasonable size
            if len(section) > chunk_size:
                # Split long sections into paragraphs
                paragraphs = section.split("\n\n")
                for p in paragraphs:
                    if p.strip():
                        chunks.append({
                            "text": p.strip(),
                            "source": f"{filename}#section-{i}"
                        })
            else:
                chunks.append({
                    "text": section,
                    "source": f"{filename}#section-{i}"
                })
    return chunks


def build_index(chunks):
    """Embed chunks and store in ChromaDB."""
    client = chromadb.Client()

    # Delete if exists, then create fresh
    try:
        client.delete_collection("knowledge_base")
    except Exception:
        pass
    collection = client.create_collection("knowledge_base")

    print(f"📦 Indexing {len(chunks)} chunks...")
    for i, chunk in enumerate(chunks):
        embedding = get_embedding(chunk["text"])
        collection.add(
            ids=[f"chunk_{i}"],
            embeddings=[embedding],
            documents=[chunk["text"]],
            metadatas=[{"source": chunk["source"]}]
        )
        print(f"   [{i+1}/{len(chunks)}] {chunk['source']}")

    print(f"✅ Indexed {len(chunks)} chunks\n")
    return collection


def ask(question, collection, top_k=3):
    """RAG: retrieve relevant docs, then generate an answer."""
    # 1. Embed the question
    query_embedding = get_embedding(question)

    # 2. Search for relevant chunks
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    # 3. Build context from retrieved chunks
    context_chunks = results["documents"][0]
    sources = [m["source"] for m in results["metadatas"][0]]
    context = "\n\n".join(context_chunks)

    # 4. Build the prompt with context
    prompt = f"""Answer the question based ONLY on the context provided below.
If the context doesn't contain the answer, say "I don't have that information."

Context:
{context}

Question: {question}

Answer:"""

    # 5. Generate answer
    answer = chat(prompt)

    return answer, sources


def main():
    # Load and index documents
    chunks = load_and_chunk("docs")
    collection = build_index(chunks)

    # Interactive Q&A loop
    print("🤖 RAG Q&A System")
    print("   Ask questions about your documents.")
    print("   Type 'quit' to exit.\n")

    while True:
        question = input("You: ").strip()
        if question.lower() == "quit":
            print("👋 Bye!")
            break
        if not question:
            continue

        answer, sources = ask(question, collection)
        print(f"\n🤖: {answer}")
        print(f"📄 Sources: {', '.join(sources)}\n")


if __name__ == "__main__":
    main()
```

&nbsp;

### Run it

```bash
python3 rag.py
```

&nbsp;

### Try these questions

```
You: How do I scale my application in Kubernetes?
You: What happens when a pod crashes?
You: How does monitoring work?
You: What is the difference between ConfigMaps and Secrets?
You: How do I trace a slow API request?
```

> 🎉 Every answer is grounded in YOUR documents. Ask something not in the docs — it should say "I don't have that information." That's RAG working correctly — no hallucinations.

&nbsp;

---

&nbsp;

## Part 3 — Understand What You Built `10 min`

&nbsp;

### Each piece mapped to production equivalents

| Your code | Production equivalent |
|-----------|----------------------|
| `load_and_chunk()` | AWS Glue, LangChain document loaders |
| `get_embedding()` | Bedrock Titan Embeddings, OpenAI Embeddings API |
| ChromaDB | Amazon OpenSearch, Aurora pgvector, Pinecone |
| `ask()` prompt template | Bedrock Knowledge Bases (does this automatically) |
| `chat()` | Bedrock `InvokeModel`, SageMaker endpoint |

> You just built from scratch what Bedrock Knowledge Bases does with a few clicks. But now you understand EVERY piece.

&nbsp;

---

&nbsp;

## Part 4 — Commit `5 min`

```bash
cd ~/projects/ai-mlops-journey
echo ".venv/" > projects/04-rag-pipeline/.gitignore
git add projects/04-rag-pipeline/ sprint-07-rag-agents/
git commit -m "sprint 7 day 2: full RAG pipeline — chunk, embed, retrieve, generate 🔗"
git push
```

&nbsp;

---

&nbsp;

## ✅ Day 2 Checklist

| | Task |
|---|------|
| ☐ | Created a document knowledge base (markdown files) |
| ☐ | Built chunking logic that splits docs by section |
| ☐ | Embedded all chunks and stored in ChromaDB |
| ☐ | RAG pipeline answers questions using retrieved context |
| ☐ | Model refuses to hallucinate when docs don't have the answer |
| ☐ | Pushed to GitHub 🟩 |

&nbsp;

---

&nbsp;

## 🧠 Concepts You Now Own

| Concept | One-liner |
|---------|-----------|
| **Chunking** | Splitting documents into small pieces for embedding |
| **Indexing** | Embedding chunks and storing them in a vector DB |
| **Retrieval** | Finding the most relevant chunks for a user's question |
| **Context injection** | Putting retrieved docs into the LLM prompt |
| **Grounding** | Model answers from YOUR data, not its training data |
| **Source attribution** | Telling the user which document the answer came from |
| **"I don't know"** | Good RAG systems admit when the docs don't have the answer |

&nbsp;

---

&nbsp;

> *Next: Agents — your RAG system learns to use tools, call APIs, and take actions. 🤖🔧*
