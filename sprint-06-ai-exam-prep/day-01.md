# Sprint 6 · Day 1

## 🏗️ Domain 3 — Applications of Foundation Models (Part 1)

`90 min` · `AIF-C01 highest-weight domain (28%)` · `The "how to use models" day`

---

&nbsp;

## Today's Big Picture

> Domain 3 is the biggest chunk of the exam. It's not about what models ARE —
> you already know that from Sprint 5. It's about how to USE them.
> RAG, prompt engineering risks, inference parameters, and choosing the right model.

By the end of today, you'll have:

- ✅ Deep understanding of RAG architecture
- ✅ Know how to choose a pre-trained model (selection criteria)
- ✅ Understand inference parameters and their effects
- ✅ Know prompt engineering risks (jailbreaking, poisoning, hijacking)
- ✅ Built a RAG vs Fine-tuning decision tree

&nbsp;

---

&nbsp;

## Part 1 — RAG Deep Dive `25 min`

&nbsp;

### What is RAG? (30-second version)

Retrieval Augmented Generation = look up relevant information FIRST, then ask the model to answer using that information. It grounds the model in YOUR data so it doesn't hallucinate.

```
┌────────────────────────────────────────────────────────────┐
│  RAG ARCHITECTURE                                         │
│                                                           │
│  ┌──────────┐                                             │
│  │ Your     │   1. Chunk documents                        │
│  │ Documents│──────▶ 2. Generate embeddings               │
│  │ (S3)     │            ▼                                │
│  └──────────┘   3. Store in vector DB                     │
│                   ┌─────────────────┐                     │
│                   │  Vector Database│                     │
│                   │  (OpenSearch,   │                     │
│                   │   Aurora, etc.) │                     │
│                   └────────┬────────┘                     │
│                            │                              │
│  User asks ──────────────▶ │ 4. Search for similar        │
│  a question                │    chunks (semantic search)  │
│                            ▼                              │
│                   ┌─────────────────┐                     │
│                   │  Relevant       │                     │
│                   │  chunks found   │                     │
│                   └────────┬────────┘                     │
│                            │                              │
│                            ▼ 5. Send question +           │
│                   ┌─────────────────┐    relevant docs    │
│                   │  Foundation     │    to model          │
│                   │  Model          │                     │
│                   └────────┬────────┘                     │
│                            │                              │
│                            ▼ 6. Model answers using       │
│                   ┌─────────────────┐    YOUR data        │
│                   │  Grounded       │                     │
│                   │  Response ✅    │                     │
│                   └─────────────────┘                     │
└────────────────────────────────────────────────────────────┘
```

&nbsp;

### Why RAG? Why not just fine-tune?

| | RAG | Fine-tuning |
|--|-----|-------------|
| **What it does** | Retrieves external data at query time | Changes model weights with new training data |
| **Data freshness** | Always current — update docs anytime | Frozen at training time |
| **Cost** | Cheaper — no retraining | Expensive — GPU hours for training |
| **Setup time** | Hours | Days to weeks |
| **When to use** | Q&A over docs, support bots, search | Domain-specific language, specialized tasks |
| **Hallucination risk** | Lower — grounded in real docs | Lower for its domain, but still possible |

&nbsp;

### AWS services for RAG

| Component | AWS Service |
|-----------|------------|
| **Document storage** | Amazon S3 |
| **Embedding generation** | Amazon Bedrock (Titan Embeddings) |
| **Vector database** | Amazon OpenSearch, Amazon Aurora, Amazon Neptune, Amazon DocumentDB, Amazon RDS for PostgreSQL |
| **Orchestration** | Bedrock Knowledge Bases (does it all for you) |

> **Exam tip:** If a question says "the company wants to answer questions using their internal documents" — the answer is almost always **RAG with Bedrock Knowledge Bases**.

&nbsp;

---

&nbsp;

## Part 2 — Choosing a Model `15 min`

&nbsp;

### Model selection criteria the exam tests

```
┌──────────────────────────────────────────────────────┐
│  HOW TO CHOOSE A FOUNDATION MODEL                    │
│                                                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐           │
│  │  COST    │  │  LATENCY │  │ ACCURACY │           │
│  │          │  │          │  │          │           │
│  │ Bigger = │  │ Bigger = │  │ Bigger = │           │
│  │ more $$  │  │ slower   │  │ better   │           │
│  └──────────┘  └──────────┘  └──────────┘           │
│                                                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐           │
│  │ MODALITY │  │ LANGUAGE │  │ CONTEXT  │           │
│  │          │  │          │  │ WINDOW   │           │
│  │ Text?    │  │ Multi-   │  │          │           │
│  │ Image?   │  │ lingual? │  │ How much │           │
│  │ Code?    │  │          │  │ can it   │           │
│  │ Multi?   │  │          │  │ "see"?   │           │
│  └──────────┘  └──────────┘  └──────────┘           │
│                                                      │
│  Also consider: compliance, customization needs,     │
│  model complexity, input/output length limits        │
└──────────────────────────────────────────────────────┘
```

&nbsp;

### Quick decision pattern

| Need | Model choice |
|------|-------------|
| Cheapest option | Smaller model (Titan Lite, Llama 8B) |
| Fastest response | Smaller model + provisioned throughput |
| Best quality | Largest available model (Claude, GPT-4) |
| Multi-language | Models with multilingual training |
| Image + text | Multimodal model (Titan, Gemini) |
| Maximum context | Claude (200K), GPT-4 (128K) |
| Open source / on-prem | Llama, Mistral |

&nbsp;

---

&nbsp;

## Part 3 — Inference Parameters `15 min`

&nbsp;

### The parameters and their effects

```
┌──────────────────────────────────────────────────────┐
│  INFERENCE PARAMETERS                                │
│                                                      │
│  Temperature ─────────────────────────────────────   │
│  0.0          0.3          0.7          1.0           │
│  ├────────────┼────────────┼────────────┤            │
│  Deterministic  Focused     Balanced     Creative    │
│  Factual        Best for    General      Wild        │
│  Repetitive     support     purpose      Varied      │
│                                                      │
│  Top-p ──────────────────────────────────────────    │
│  0.1           0.5           0.9           1.0       │
│  ├─────────────┼─────────────┼─────────────┤        │
│  Very narrow    Moderate      Broad         All      │
│  Safe answers   selection     diverse      tokens    │
└──────────────────────────────────────────────────────┘
```

| Parameter | What it controls | Low value | High value |
|-----------|-----------------|-----------|------------|
| **Temperature** | Randomness of output | Consistent, factual | Creative, varied |
| **Top-p** | Token selection pool | Fewer choices, safer | More choices, diverse |
| **Top-k** | Number of tokens to consider | Conservative | Exploratory |
| **Max tokens** | Response length limit | Short answer | Long answer |
| **Stop sequences** | When to stop generating | Cuts off at trigger | — |

&nbsp;

### Exam scenario patterns

| Scenario | Recommended settings |
|----------|---------------------|
| Customer support chatbot | Low temperature (0.1-0.3), moderate max tokens |
| Creative story writing | High temperature (0.7-0.9), high max tokens |
| Code generation | Low temperature (0.1-0.2), precise |
| Data extraction | Temperature 0, deterministic output |
| Summarization | Low temperature (0.2-0.3), controlled length |

&nbsp;

---

&nbsp;

## Part 4 — Prompt Engineering Risks `15 min`

&nbsp;

### The risks the exam tests

```
┌──────────────────────────────────────────────────────┐
│  PROMPT ENGINEERING RISKS                            │
│                                                      │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐     │
│  │ JAILBREAK  │  │ PROMPT     │  │ PROMPT     │     │
│  │            │  │ INJECTION  │  │ LEAKING    │     │
│  │ Trick the  │  │            │  │            │     │
│  │ model into │  │ Hidden     │  │ Model      │     │
│  │ ignoring   │  │ instructions│ │ reveals    │     │
│  │ its rules  │  │ in user    │  │ its system │     │
│  │            │  │ input      │  │ prompt     │     │
│  └────────────┘  └────────────┘  └────────────┘     │
│                                                      │
│  ┌────────────┐  ┌────────────┐                      │
│  │ DATA       │  │ MODEL      │                      │
│  │ POISONING  │  │ HIJACKING  │                      │
│  │            │  │            │                      │
│  │ Bad data   │  │ Redirect   │                      │
│  │ in training│  │ model to   │                      │
│  │ corrupts   │  │ do attacker│                      │
│  │ the model  │  │ 's task    │                      │
│  └────────────┘  └────────────┘                      │
└──────────────────────────────────────────────────────┘
```

| Risk | What it is | Mitigation |
|------|-----------|------------|
| **Jailbreaking** | User tricks model into bypassing safety rules | Guardrails, input filtering |
| **Prompt injection** | Malicious instructions hidden in user input | Input validation, Bedrock Guardrails |
| **Prompt leaking** | Model reveals its system prompt to the user | Don't put secrets in system prompts |
| **Data poisoning** | Training data is corrupted intentionally | Data validation, curation |
| **Model hijacking** | Redirecting model to serve attacker's goals | Access controls, monitoring |

> **Exam tip:** "How to prevent prompt injection?" → **Bedrock Guardrails** + input validation.

&nbsp;

---

&nbsp;

## Part 5 — Build the Decision Tree `15 min`

Create `cheatsheets/rag-vs-finetuning.md`:

```markdown
# RAG vs Fine-tuning vs Prompt Engineering — Decision Tree

## When to use what?

```
Need to answer questions from your docs?
  └─ YES → RAG (Bedrock Knowledge Bases)

Need the model to speak a specialized language?
  └─ YES → Fine-tuning

Need better answers without changing the model?
  └─ YES → Prompt engineering (few-shot, CoT)

Need real-time data access?
  └─ YES → RAG (always up-to-date)

Budget is tight?
  └─ YES → Prompt engineering (free) → RAG (cheap) → Fine-tuning (expensive)
```

## Cost comparison

| Method | Cost | Setup Time | Data Freshness |
|--------|------|------------|---------------|
| Prompt engineering | Free | Minutes | N/A |
| RAG | $ | Hours | Always current |
| Fine-tuning | $$$ | Days | Frozen at training |
| Pre-training | $$$$$ | Weeks | Frozen |
```

&nbsp;

---

&nbsp;

## Part 6 — Commit `5 min`

```bash
git add sprint-06-ai-exam-prep/ cheatsheets/
git commit -m "sprint 6 day 1: domain 3 — RAG, model selection, inference params, prompt risks"
git push
```

&nbsp;

---

&nbsp;

## ✅ Day 1 Checklist

| | Task |
|---|------|
| ☐ | Can draw the RAG architecture from memory |
| ☐ | Know when to use RAG vs fine-tuning vs prompt engineering |
| ☐ | Can name AWS services for each RAG component |
| ☐ | Understand model selection criteria |
| ☐ | Know all inference parameters and their effects |
| ☐ | Can name 5 prompt engineering risks and their mitigations |
| ☐ | Decision tree cheatsheet written and pushed 🟩 |

&nbsp;

---

&nbsp;

## 🧠 Concepts You Now Own

| Concept | One-liner |
|---------|-----------|
| **RAG** | Retrieve docs first, then ask the model — grounded answers |
| **Vector database** | Stores embeddings for semantic search |
| **Bedrock Knowledge Bases** | Managed RAG — upload docs, done |
| **Fine-tuning** | Retrain model weights on your data — expensive, frozen |
| **Temperature** | Randomness dial — low = focused, high = creative |
| **Top-p** | Token selection pool size |
| **Jailbreaking** | Tricking model into ignoring safety rules |
| **Prompt injection** | Hidden malicious instructions in user input |
| **Data poisoning** | Corrupting training data intentionally |
| **Guardrails** | Bedrock feature to filter harmful content |

&nbsp;

---

&nbsp;

> *Next: Fine-tuning process, model evaluation metrics, and a model serving project. 🔬*
