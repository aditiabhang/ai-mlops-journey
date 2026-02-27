# Sprint 5 · Day 3

## 🤖 Generative AI — How LLMs Actually Work

`90 min` · `AIF-C01 Domain 2 starts here` · `The "how does ChatGPT work?" day`

---

&nbsp;

## Today's Big Picture

> You've used Ollama. You've chatted with LLMs. But how do they work?
> Today you learn transformers, tokens, embeddings, and context windows —
> the building blocks of every AI product in 2025.

By the end of today, you'll have:

- ✅ Understand what a foundation model is
- ✅ Know how transformers and attention work (concept level)
- ✅ Understand tokenization and context windows
- ✅ Know what embeddings are and why they matter
- ✅ Understand the foundation model lifecycle (pre-train → fine-tune → deploy)

&nbsp;

---

&nbsp;

## Part 1 — Foundation Models `15 min`

&nbsp;

### What is a foundation model? (30-second version)

A foundation model is a massive model trained on a huge amount of general data. You don't build it from scratch — you take it and adapt it for your task. Think of it as a college graduate: broadly educated, needs job-specific training.

```
┌─────────────────────────────────────────────────────┐
│  FOUNDATION MODEL LIFECYCLE                         │
│                                                     │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐      │
│  │ PRE-     │    │ FINE-    │    │ DEPLOY   │      │
│  │ TRAIN    │───▶│ TUNE     │───▶│          │      │
│  │          │    │          │    │          │      │
│  │ Train on │    │ Adapt to │    │ Serve    │      │
│  │ billions │    │ YOUR     │    │ via API  │      │
│  │ of text  │    │ specific │    │          │      │
│  │ pages    │    │ task     │    │          │      │
│  │          │    │          │    │          │      │
│  │ Cost:$$$ │    │ Cost: $  │    │ Cost: $  │      │
│  │ Time:wks │    │ Time:hrs │    │ Time:ms  │      │
│  └──────────┘    └──────────┘    └──────────┘      │
│                                                     │
│  Done by:        Done by:        Done by:           │
│  OpenAI, Meta,   YOU (or your    YOU                │
│  Amazon, Google  team)                              │
└─────────────────────────────────────────────────────┘
```

&nbsp;

### Key foundation models you should know

| Model | Creator | Known for |
|-------|---------|-----------|
| **GPT-4** | OpenAI | ChatGPT — general purpose |
| **Claude** | Anthropic | Safety-focused, long context |
| **Llama** | Meta | Open-source, runs locally |
| **Titan** | Amazon | Built for Bedrock |
| **Gemini** | Google | Multimodal (text + images) |
| **Mistral** | Mistral AI | Open-source, efficient |
| **Stable Diffusion** | Stability AI | Image generation |

&nbsp;

---

&nbsp;

## Part 2 — Transformers & Attention `20 min`

&nbsp;

### What is a transformer? (30-second version)

The transformer is the architecture behind every modern LLM. Before transformers, AI processed text word-by-word (slow). Transformers process ALL words at once and figure out which words matter most to each other. That "figuring out" is called **attention**.

```
Old approach (RNN):                 Transformer:
Process one word at a time          Process ALL words at once

"The" → "cat" → "sat" → "on"       "The cat sat on the mat"
  ↓       ↓       ↓       ↓              ↓
Slow. Forgets early words.          Fast. Sees everything at once.
```

&nbsp;

### Attention — the key insight

When the model reads "The cat sat on the mat," it needs to know that "sat" is connected to "cat" (who sat?) and "mat" (sat where?). Attention scores tell the model which words to focus on.

```
Input: "The bank was on the river bank"

  "bank" (first) → attention looks at "river" → aha, it's a RIVER bank
  "bank" (second) → attention looks at context → same meaning confirmed

Without attention, the model can't tell the two "bank"s apart.
```

&nbsp;

### The transformer architecture (simplified)

```
┌─────────────────────────────────────┐
│  INPUT: "What is Kubernetes?"       │
│                                     │
│  ┌─────────────────────────────┐    │
│  │  1. TOKENIZE                │    │
│  │  Split into tokens          │    │
│  │  ["What", "is", "Kub",     │    │
│  │   "ern", "etes", "?"]      │    │
│  └──────────────┬──────────────┘    │
│                 ▼                   │
│  ┌─────────────────────────────┐    │
│  │  2. EMBED                   │    │
│  │  Convert tokens to numbers  │    │
│  │  (vectors in high-dim space)│    │
│  └──────────────┬──────────────┘    │
│                 ▼                   │
│  ┌─────────────────────────────┐    │
│  │  3. ATTENTION LAYERS        │    │
│  │  "Which tokens relate to    │    │
│  │   which?" (many layers)     │    │
│  └──────────────┬──────────────┘    │
│                 ▼                   │
│  ┌─────────────────────────────┐    │
│  │  4. PREDICT NEXT TOKEN      │    │
│  │  "Kubernetes" → "is" → "an" │    │
│  │  → "open" → "source" → ... │    │
│  └─────────────────────────────┘    │
│                                     │
│  OUTPUT: "Kubernetes is an open     │
│  source container orchestration..." │
└─────────────────────────────────────┘
```

> You don't need to know the math. Know the FLOW: tokenize → embed → attention → predict.

&nbsp;

---

&nbsp;

## Part 3 — Tokens, Context Windows, Embeddings `20 min`

&nbsp;

### Tokens

Tokens are how models read text. A token is NOT a word — it's a piece of a word. Common words = 1 token. Long/rare words = multiple tokens.

```
"Hello"           → 1 token
"Kubernetes"      → 3 tokens ("Kub", "ern", "etes")
"I love Python"   → 3 tokens
"CrashLoopBackOff" → 5 tokens

Rule of thumb: 1 token ≈ 4 characters ≈ 0.75 words
```

> **Why tokens matter for the exam:** Pricing is per token. Context windows are measured in tokens. A model with a 128K context window can "see" ~96,000 words at once.

&nbsp;

### Context Window

The maximum number of tokens a model can process in one conversation. Everything — your question, the model's previous answers, system prompts — all counts toward the limit.

| Model | Context Window |
|-------|---------------|
| GPT-4 | 128K tokens |
| Claude 3 | 200K tokens |
| Llama 3.2 | 128K tokens |
| Titan | 8K-32K tokens |

```
Context window is like the model's short-term memory:

  ┌──────────────────────────────────────┐
  │  System prompt: 200 tokens           │
  │  Your message 1: 100 tokens          │
  │  Model response 1: 300 tokens        │
  │  Your message 2: 50 tokens           │
  │  Model response 2: ???               │
  │  ─────────────────────────           │
  │  Total so far: 650 tokens            │
  │  Remaining: 127,350 tokens           │
  └──────────────────────────────────────┘
```

&nbsp;

### Embeddings

An embedding is a way to represent text as numbers (a vector). Similar meanings end up close together in this number space.

```
"king"  → [0.9, 0.2, 0.8, ...]
"queen" → [0.9, 0.2, 0.7, ...]  ← very close to "king"!
"cat"   → [0.1, 0.7, 0.3, ...]  ← far away from "king"
```

> **Why embeddings matter:** They power search, recommendations, and RAG (Retrieval Augmented Generation). You convert your documents into embeddings, store them in a vector database, and search by meaning instead of keywords.

&nbsp;

---

&nbsp;

## Part 4 — Prompt Engineering Deep Dive `15 min`

&nbsp;

### You already know the basics from Sprint 3. Here's the exam-level detail:

```
┌──────────────────────────────────────────────────────┐
│  PROMPT ENGINEERING TECHNIQUES                       │
│                                                      │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐     │
│  │ ZERO-SHOT  │  │ FEW-SHOT   │  │ CHAIN-OF-  │     │
│  │            │  │            │  │ THOUGHT    │     │
│  │ Just ask.  │  │ Give 2-3   │  │ "Think     │     │
│  │ No examples│  │ examples   │  │  step by   │     │
│  │            │  │ first.     │  │  step"     │     │
│  └────────────┘  └────────────┘  └────────────┘     │
│                                                      │
│  ┌────────────┐  ┌────────────┐                      │
│  │ SYSTEM     │  │ RAG        │                      │
│  │ PROMPT     │  │            │                      │
│  │            │  │ Retrieve   │                      │
│  │ Hidden     │  │ relevant   │                      │
│  │ persona /  │  │ docs THEN  │                      │
│  │ rules      │  │ ask model  │                      │
│  └────────────┘  └────────────┘                      │
└──────────────────────────────────────────────────────┘
```

&nbsp;

### New for the exam: inference parameters

| Parameter | What it does | Low value | High value |
|-----------|-------------|-----------|------------|
| **Temperature** | Controls randomness | More focused, deterministic | More creative, varied |
| **Top-p** | Limits token selection pool | Fewer options, safer | More options, diverse |
| **Max tokens** | Output length limit | Short response | Long response |
| **Stop sequences** | When to stop generating | — | — |

> **Exam tip:** Temperature is the most tested parameter. Low temp (0.1) = factual, consistent. High temp (0.9) = creative, varied. For customer support = low. For creative writing = high.

&nbsp;

---

&nbsp;

## Part 5 — GenAI Use Cases `5 min`

&nbsp;

### What generative AI can do (exam loves these)

| Use Case | Example |
|----------|---------|
| **Text generation** | Write emails, articles, code |
| **Summarization** | Condense long documents |
| **Translation** | Convert between languages |
| **Code generation** | Write Python, SQL, YAML |
| **Chatbots** | Customer service, support |
| **Image generation** | Create visuals from text prompts |
| **Search** | Semantic search — find by meaning, not keywords |
| **Data extraction** | Pull structured data from unstructured text |

&nbsp;

### What it CAN'T do well (exam tests these too)

| Limitation | What it means |
|-----------|--------------|
| **Hallucinations** | Makes up facts that sound convincing |
| **No real-time data** | Only knows what it was trained on |
| **Bias** | Reflects biases in training data |
| **Not deterministic** | Same prompt can give different answers |
| **Context limits** | Forgets beyond the context window |

&nbsp;

---

&nbsp;

## Part 6 — Commit `5 min`

```bash
git add sprint-05-ai-foundations/
git commit -m "sprint 5 day 3: generative AI — transformers, tokens, embeddings, prompt eng"
git push
```

&nbsp;

---

&nbsp;

## ✅ Day 3 Checklist

| | Task |
|---|------|
| ☐ | Know what a foundation model is and name 5+ |
| ☐ | Can explain transformers and attention at a concept level |
| ☐ | Understand tokens, context windows, and embeddings |
| ☐ | Know all prompt engineering techniques for the exam |
| ☐ | Understand temperature and inference parameters |
| ☐ | Can name GenAI use cases AND limitations |
| ☐ | Pushed to GitHub 🟩 |

&nbsp;

---

&nbsp;

## 🧠 Concepts You Now Own

| Concept | One-liner |
|---------|-----------|
| **Foundation model** | Massive model pre-trained on general data — you adapt it |
| **Transformer** | Architecture that processes all words at once using attention |
| **Attention** | "Which words matter most to each other?" |
| **Token** | A piece of a word — how models read text (~4 chars) |
| **Context window** | Max tokens a model can see in one conversation |
| **Embedding** | Text as numbers — similar meanings = similar numbers |
| **Vector database** | Stores embeddings for similarity search |
| **Temperature** | Controls randomness: low = focused, high = creative |
| **Hallucination** | Model confidently makes up wrong information |
| **RAG** | Retrieve documents first, then ask the model |

&nbsp;

---

&nbsp;

> *Next: AWS GenAI services — Bedrock, SageMaker JumpStart, Amazon Q, and how they all fit together. ☁️*
