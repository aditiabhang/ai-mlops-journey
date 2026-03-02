# Sprint 7 · Day 1

## 🧲 Vector Databases — Embeddings, Storage & Semantic Search

`90 min` · `Hands-on from minute one` · `The foundation RAG is built on`

---

&nbsp;

## Today's Big Picture

> In Sprint 5 you learned what embeddings ARE. Today you use them.
> You'll turn text into numbers, store them in a vector database,
> and search by MEANING instead of keywords. This is the backbone of every RAG system.

By the end of today, you'll have:

- ✅ Generated embeddings from text using Ollama
- ✅ Stored embeddings in ChromaDB (a local vector database)
- ✅ Performed semantic search — "find docs similar to my question"
- ✅ Understand why vector search beats keyword search

&nbsp;

---

&nbsp;

## Part 1 — Why Vector Search? `10 min`

&nbsp;

### The problem with keyword search

```
Your docs contain:   "Pods are the smallest deployable units in Kubernetes"

Keyword search for:  "container wrapper"  → ❌ No match (different words)

Vector search for:   "container wrapper"  → ✅ Finds the pod doc!
                     (because "container wrapper" and "smallest deployable unit"
                      MEAN similar things)
```

&nbsp;

### How vector search works

```
┌──────────────────────────────────────────────────────┐
│  VECTOR SEARCH                                       │
│                                                      │
│  Step 1: Convert text to numbers (embeddings)        │
│                                                      │
│  "Kubernetes pod"  → [0.82, 0.15, 0.91, ...]        │
│  "Docker container"→ [0.78, 0.12, 0.88, ...]  ← close!
│  "Sourdough bread" → [0.03, 0.95, 0.11, ...]  ← far!│
│                                                      │
│  Step 2: Store in vector DB                          │
│                                                      │
│  Step 3: When user asks a question:                  │
│    • Convert question to embedding                   │
│    • Find the closest stored embeddings              │
│    • Return those documents                          │
│                                                      │
│  "Closest" = cosine similarity (angle between        │
│   vectors — smaller angle = more similar)            │
└──────────────────────────────────────────────────────┘
```

&nbsp;

---

&nbsp;

## Part 2 — Set Up ChromaDB `10 min`

&nbsp;

### What is ChromaDB? (30-second version)

ChromaDB is an open-source vector database that runs locally. No cloud account, no API keys. Install it with pip, store embeddings, search by similarity. Perfect for learning and prototyping.

```
Vector Database Landscape:

  Local / Free              Cloud / Managed
  ┌──────────────┐         ┌──────────────────┐
  │ ChromaDB     │         │ Pinecone          │
  │ FAISS        │         │ Weaviate Cloud    │
  │ Qdrant       │         │ OpenSearch (AWS)  │
  └──────────────┘         │ Aurora pgvector   │
                           └──────────────────┘
```

&nbsp;

### Do This

**1 →** Create the project and install dependencies

```bash
mkdir -p ~/projects/ai-mlops-journey/projects/03-vector-search
cd ~/projects/ai-mlops-journey/projects/03-vector-search
python3 -m venv .venv
source .venv/bin/activate
pip install chromadb requests
```

&nbsp;

---

&nbsp;

## Part 3 — Generate Embeddings with Ollama `15 min`

&nbsp;

### How Ollama generates embeddings

Ollama has an embeddings endpoint. You send text, it returns a vector (list of numbers).

&nbsp;

### Do This

**1 →** Make sure Ollama is running

```bash
ollama serve
```

&nbsp;

**2 →** Pull an embedding model

```bash
ollama pull nomic-embed-text
```

&nbsp;

**3 →** Create `embeddings_demo.py`

```python
import requests

OLLAMA_URL = "http://localhost:11434/api/embed"

def get_embedding(text):
    """Convert text to a vector using Ollama."""
    response = requests.post(OLLAMA_URL, json={
        "model": "nomic-embed-text",
        "input": text
    })
    return response.json()["embeddings"][0]

# Try it
text = "Kubernetes pods are the smallest deployable units"
embedding = get_embedding(text)

print(f"Text: {text}")
print(f"Embedding length: {len(embedding)}")
print(f"First 5 values: {embedding[:5]}")
```

&nbsp;

**4 →** Run it

```bash
python3 embeddings_demo.py
```

> You should see a vector with 768 numbers. That's your text represented as a point in 768-dimensional space. Texts with similar meanings end up as nearby points.

&nbsp;

---

&nbsp;

## Part 4 — Store & Search with ChromaDB `30 min`

&nbsp;

### Do This

**1 →** Create `vector_search.py`

```python
import chromadb
import requests

OLLAMA_URL = "http://localhost:11434/api/embed"


def get_embedding(text):
    response = requests.post(OLLAMA_URL, json={
        "model": "nomic-embed-text",
        "input": text
    })
    return response.json()["embeddings"][0]


# 1. Create a ChromaDB collection
client = chromadb.Client()
collection = client.create_collection(name="k8s_docs")

# 2. Our "knowledge base" — K8s concepts
docs = [
    "A Pod is the smallest deployable unit in Kubernetes. It wraps one or more containers.",
    "A Deployment manages ReplicaSets and provides declarative updates to Pods.",
    "A Service provides a stable network endpoint for a set of Pods.",
    "ConfigMaps store non-confidential configuration data as key-value pairs.",
    "Secrets store sensitive data like passwords and API keys, base64 encoded.",
    "Namespaces provide isolation between groups of resources in a cluster.",
    "A DaemonSet ensures a copy of a Pod runs on every node in the cluster.",
    "Horizontal Pod Autoscaler automatically scales the number of Pod replicas.",
    "Ingress manages external HTTP access to Services, providing URL routing.",
    "RBAC controls who can access what resources in a Kubernetes cluster.",
]

# 3. Generate embeddings and store them
print("📦 Embedding and storing documents...")
for i, doc in enumerate(docs):
    embedding = get_embedding(doc)
    collection.add(
        ids=[f"doc_{i}"],
        embeddings=[embedding],
        documents=[doc]
    )
print(f"✅ Stored {len(docs)} documents\n")

# 4. Search by meaning
queries = [
    "How do I store passwords safely?",
    "What manages container replicas?",
    "How does traffic reach my application?",
]

for query in queries:
    query_embedding = get_embedding(query)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=2
    )

    print(f"🔍 Query: \"{query}\"")
    for doc, distance in zip(results["documents"][0], results["distances"][0]):
        score = 1 - distance  # convert distance to similarity
        print(f"   → [{score:.2f}] {doc[:80]}...")
    print()
```

&nbsp;

**2 →** Run it

```bash
python3 vector_search.py
```

> 🤯 Look at the results:
> - "How do I store passwords safely?" → finds the **Secrets** doc
> - "What manages container replicas?" → finds the **Deployment** doc
> - "How does traffic reach my application?" → finds the **Service** and **Ingress** docs
>
> NONE of those queries share keywords with the matching docs. That's the power of semantic search.

&nbsp;

**3 →** Try adding your own queries. Try weird phrasings. Watch it find the right doc anyway.

&nbsp;

---

&nbsp;

## Part 5 — Commit `5 min`

```bash
cd ~/projects/ai-mlops-journey
echo ".venv/" > projects/03-vector-search/.gitignore
git add projects/03-vector-search/ sprint-07-rag-agents/
git commit -m "sprint 7 day 1: vector search with ChromaDB — embeddings, storage, semantic search"
git push
```

&nbsp;

---

&nbsp;

## ✅ Day 1 Checklist

| | Task |
|---|------|
| ☐ | Generated embeddings with Ollama (nomic-embed-text) |
| ☐ | Stored embeddings in ChromaDB |
| ☐ | Performed semantic search — queries matched by meaning, not keywords |
| ☐ | Tried at least 3 different queries |
| ☐ | Pushed to GitHub 🟩 |

&nbsp;

---

&nbsp;

## 🧠 Concepts You Now Own

| Concept | One-liner |
|---------|-----------|
| **Embedding** | Text as a list of numbers — similar meanings = nearby vectors |
| **Vector database** | Stores embeddings and finds similar ones fast |
| **ChromaDB** | Open-source local vector DB — pip install and go |
| **Semantic search** | Search by meaning, not keywords |
| **Cosine similarity** | How "close" two vectors are — higher = more similar |
| **Embedding model** | Specialized model that converts text to vectors (nomic-embed-text) |
| **Collection** | ChromaDB's version of a table — holds docs + embeddings |

&nbsp;

---

&nbsp;

> *Next: You add an LLM on top of this search — that's RAG. You're one day away from building it. 🔥*
