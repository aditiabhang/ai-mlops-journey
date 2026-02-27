# Sprint 5 · Day 4

## ☁️ AWS GenAI Services — Bedrock, SageMaker, Amazon Q

`90 min` · `AIF-C01 Domain 2 continued` · `The "which AWS service?" day`

---

&nbsp;

## Today's Big Picture

> The exam LOVES asking "which AWS service should you use for X?"
> Today you learn the GenAI services deeply — especially Bedrock,
> which is the star of the AIF-C01 exam.

By the end of today, you'll have:

- ✅ Deep understanding of Amazon Bedrock and what it offers
- ✅ Know SageMaker vs Bedrock — when to use each
- ✅ Understand SageMaker JumpStart, PartyRock, and Amazon Q
- ✅ Know GenAI pricing models (token-based, provisioned throughput)

&nbsp;

---

&nbsp;

## Part 1 — Amazon Bedrock `30 min`

&nbsp;

### What is Bedrock? (30-second version)

Bedrock is a fully managed service that gives you API access to foundation models from multiple providers. You don't manage any infrastructure. Just pick a model, send a prompt, get a response.

```
┌──────────────────────────────────────────────────────┐
│  AMAZON BEDROCK                                      │
│                                                      │
│  "Foundation Models as a Service"                    │
│                                                      │
│  ┌──────────────────────────────────────────────┐    │
│  │  Available Models:                            │    │
│  │                                               │    │
│  │  Amazon Titan    │  Text, embeddings, image   │    │
│  │  Anthropic Claude│  Text, long context, safe  │    │
│  │  Meta Llama      │  Text, open-source         │    │
│  │  Mistral         │  Text, efficient           │    │
│  │  Stability AI    │  Image generation          │    │
│  │  Cohere          │  Text, embeddings          │    │
│  └──────────────────────────────────────────────┘    │
│                                                      │
│  Features:                                           │
│  • No infrastructure to manage                       │
│  • Pay per token (input + output)                    │
│  • Fine-tune models on your data                     │
│  • Knowledge bases (RAG built-in)                    │
│  • Guardrails (content filtering)                    │
│  • Agents (multi-step task automation)               │
│  • Model evaluation tools                            │
└──────────────────────────────────────────────────────┘
```

&nbsp;

### Bedrock features the exam tests heavily

| Feature | What it does |
|---------|-------------|
| **Model access** | API to multiple foundation models — pick the best one for your task |
| **Knowledge Bases** | Upload your docs → Bedrock does RAG for you automatically |
| **Agents** | Multi-step tasks — model can call APIs, query databases, take actions |
| **Guardrails** | Filter harmful content, PII, off-topic responses |
| **Fine-tuning** | Adapt a model to your domain with your data |
| **Model evaluation** | Compare models on your specific use case |
| **Provisioned throughput** | Reserved capacity for consistent performance |

&nbsp;

### Bedrock Knowledge Bases — RAG made easy

```
┌──────────────────────────────────────────────┐
│  How Bedrock Knowledge Bases work (RAG):     │
│                                              │
│  1. Upload your docs (S3)                    │
│     ↓                                        │
│  2. Bedrock converts them to embeddings      │
│     ↓                                        │
│  3. Stores in a vector database              │
│     (OpenSearch, Aurora, etc.)               │
│     ↓                                        │
│  4. User asks a question                     │
│     ↓                                        │
│  5. Bedrock searches your docs for           │
│     relevant chunks                          │
│     ↓                                        │
│  6. Sends question + relevant docs           │
│     to the foundation model                  │
│     ↓                                        │
│  7. Model answers using YOUR data            │
│     (not hallucinating — grounded!)          │
└──────────────────────────────────────────────┘
```

&nbsp;

---

&nbsp;

## Part 2 — SageMaker vs Bedrock `15 min`

&nbsp;

### When to use which?

```
┌──────────────────────────────────────────────────────┐
│                                                      │
│  "I want to USE a model"        → BEDROCK            │
│  "I want to BUILD a model"      → SAGEMAKER          │
│                                                      │
│  ┌───────────────────────┐  ┌─────────────────────┐  │
│  │  BEDROCK              │  │  SAGEMAKER           │  │
│  │                       │  │                      │  │
│  │  • API access to      │  │  • Build custom      │  │
│  │    existing models    │  │    models from       │  │
│  │  • No infra needed    │  │    scratch           │  │
│  │  • Pay per token      │  │  • Full control      │  │
│  │  • Fast to start      │  │  • Training +        │  │
│  │  • RAG built-in       │  │    deployment        │  │
│  │  • Content guardrails │  │  • Managed notebooks │  │
│  │                       │  │  • MLOps pipelines   │  │
│  │  "I need a chatbot    │  │                      │  │
│  │   with my docs"       │  │  "I need a custom    │  │
│  │                       │  │   fraud model on     │  │
│  │                       │  │   my data"           │  │
│  └───────────────────────┘  └─────────────────────┘  │
└──────────────────────────────────────────────────────┘
```

&nbsp;

### SageMaker features the exam tests

| Feature | What it does |
|---------|-------------|
| **SageMaker Studio** | IDE for ML — notebooks, experiments, deployment |
| **SageMaker JumpStart** | Pre-trained models you can deploy with one click |
| **SageMaker Pipelines** | Automated ML workflows (data prep → train → deploy) |
| **SageMaker Data Wrangler** | Visual data preparation — no code |
| **SageMaker Feature Store** | Central storage for ML features |
| **SageMaker Model Monitor** | Detect model drift in production |
| **SageMaker Clarify** | Detect bias in data and models |
| **SageMaker Model Cards** | Document what a model does, how it was trained |

&nbsp;

---

&nbsp;

## Part 3 — Other AWS GenAI Services `15 min`

&nbsp;

### PartyRock

An Amazon Bedrock Playground — build GenAI apps without code. Great for prototyping. Free to try.

```
PartyRock = "No-code Bedrock"
  • Build an app in minutes
  • Share it with a link
  • No AWS account needed to try
  • Good for demos and experiments
```

&nbsp;

### Amazon Q

AWS's AI assistant — like ChatGPT but for AWS and your business.

| Variant | What it does |
|---------|-------------|
| **Amazon Q Business** | AI assistant over your company's data (docs, wikis, email) |
| **Amazon Q Developer** | AI coding assistant — code suggestions, debugging, transformation |
| **Amazon Q in AWS Console** | Ask questions about AWS services right in the console |

&nbsp;

### Quick reference for the exam

| "I need to..." | Use this |
|----------------|----------|
| Access foundation models via API | **Bedrock** |
| Build a custom ML model from scratch | **SageMaker** |
| Deploy a pre-trained model quickly | **SageMaker JumpStart** |
| Build a GenAI app without code | **PartyRock** |
| AI assistant for my company docs | **Amazon Q Business** |
| AI coding help | **Amazon Q Developer** |
| Detect bias in my model | **SageMaker Clarify** |
| Monitor model in production | **SageMaker Model Monitor** |
| Document my model | **SageMaker Model Cards** |

&nbsp;

---

&nbsp;

## Part 4 — GenAI Pricing & Cost `10 min`

&nbsp;

### How Bedrock pricing works

```
┌──────────────────────────────────────────────────────┐
│  BEDROCK PRICING MODELS                              │
│                                                      │
│  ┌────────────────────┐  ┌────────────────────────┐  │
│  │  ON-DEMAND         │  │  PROVISIONED           │  │
│  │                    │  │  THROUGHPUT             │  │
│  │  Pay per token     │  │                        │  │
│  │  (input + output)  │  │  Reserved capacity     │  │
│  │                    │  │  Fixed hourly rate      │  │
│  │  Best for:         │  │                        │  │
│  │  Variable traffic  │  │  Best for:             │  │
│  │  Experimentation   │  │  Consistent traffic    │  │
│  │  Low/moderate use  │  │  Low latency needed    │  │
│  └────────────────────┘  └────────────────────────┘  │
│                                                      │
│  Custom models: extra cost for fine-tuning           │
│  + storage of custom model weights                   │
└──────────────────────────────────────────────────────┘
```

&nbsp;

### Cost considerations for the exam

| Factor | Impact on cost |
|--------|---------------|
| **Model size** | Larger models cost more per token |
| **Input tokens** | You pay for the prompt too, not just the answer |
| **Output tokens** | Usually more expensive than input tokens |
| **Fine-tuning** | Training hours + model storage |
| **RAG** | Additional cost for vector DB + embedding generation |
| **Provisioned throughput** | Higher upfront, lower per-request for high volume |

&nbsp;

---

&nbsp;

## Part 5 — Commit `5 min`

```bash
git add sprint-05-ai-foundations/
git commit -m "sprint 5 day 4: AWS GenAI services — Bedrock, SageMaker, Q, pricing"
git push
```

&nbsp;

---

&nbsp;

## ✅ Day 4 Checklist

| | Task |
|---|------|
| ☐ | Can explain what Bedrock does and name 5+ features |
| ☐ | Know when to use Bedrock vs SageMaker |
| ☐ | Understand Bedrock Knowledge Bases (managed RAG) |
| ☐ | Can explain SageMaker JumpStart, Clarify, Model Monitor |
| ☐ | Know what PartyRock and Amazon Q do |
| ☐ | Understand token-based pricing vs provisioned throughput |
| ☐ | Pushed to GitHub 🟩 |

&nbsp;

---

&nbsp;

## 🧠 Concepts You Now Own

| Concept | One-liner |
|---------|-----------|
| **Bedrock** | API access to foundation models — no infra to manage |
| **Bedrock Knowledge Bases** | Managed RAG — upload docs, ask questions |
| **Bedrock Guardrails** | Content filters — block harmful or off-topic output |
| **Bedrock Agents** | Multi-step task automation — model calls APIs |
| **SageMaker** | Full ML platform — build, train, deploy custom models |
| **SageMaker JumpStart** | One-click deploy of pre-trained models |
| **SageMaker Clarify** | Bias and explainability detection |
| **SageMaker Model Monitor** | Detect model drift in production |
| **PartyRock** | No-code Bedrock playground |
| **Amazon Q** | AWS AI assistant — business, developer, console |
| **Token pricing** | Pay per input + output token — larger models cost more |

&nbsp;

---

&nbsp;

> *Next: Hands-on Bedrock + your "Foundation Models Explained" cheatsheet. Time to touch real AWS AI. ☁️🤖*
