# Sprint 3 · Day 3

## 🤖 Ollama — Run an LLM on Your Laptop

`90 min` · `Needs: 8GB+ RAM, ~5GB disk` · `The moment AI becomes real`

---

&nbsp;

## Today's Big Picture

> Forget ChatGPT. Forget API keys. Forget the cloud.
> Today you download a large language model and run it on YOUR machine.
> No internet needed. No data sent anywhere. Just you and a neural network.

By the end of today, you'll have:

- ✅ Ollama installed and running
- ✅ Chatted with at least 2 different models
- ✅ Compared model sizes, speeds, and quality
- ✅ Understand what's actually happening when you "chat with AI"
- ✅ Tried basic prompt engineering techniques

&nbsp;

---

&nbsp;

## Part 1 — Install Ollama `10 min`

&nbsp;

### What is Ollama? (30-second version)

Ollama makes it dead simple to run LLMs locally. One command to download a model, one command to chat with it. No Python setup, no GPU drivers, no config files.

```
What Ollama does for you:

  ┌──────────────────────────────────────┐
  │  Without Ollama:                     │
  │  • Download model weights (4GB+)     │
  │  • Install PyTorch                   │
  │  • Configure CUDA/Metal              │
  │  • Write inference code              │
  │  • Handle tokenization               │
  │  • 2 hours of setup                  │
  └──────────────────────────────────────┘
                    vs
  ┌──────────────────────────────────────┐
  │  With Ollama:                        │
  │  • brew install ollama               │
  │  • ollama run llama3.2               │
  │  • Done. You're chatting.            │
  └──────────────────────────────────────┘
```

&nbsp;

### Do This

**1 →** Install Ollama

```bash
# Mac
brew install ollama
```

> Or download from [ollama.com](https://ollama.com)

&nbsp;

**2 →** Start the Ollama server

```bash
ollama serve
```

> Leave this running in a terminal tab. Open a new tab for the next steps.

&nbsp;

**3 →** Pull and run your first model

```bash
ollama run llama3.2
```

> This downloads ~2GB and starts a chat. Type anything. You're talking to an LLM on your own machine. 🤯

&nbsp;

**4 →** Try asking it something

```
>>> Explain Kubernetes pods to a 5-year-old
>>> Write a Python function that checks if a number is prime
>>> What's the difference between Docker and Podman?
```

> Type `/bye` to exit the chat.

&nbsp;

---

&nbsp;

## Part 2 — What's Actually Happening? `10 min`

&nbsp;

### Under the hood (30-second version)

When you type a question, the model isn't "thinking." It's predicting the next word, one at a time, based on patterns it learned from billions of text examples.

```
You type:  "What is a pod in"

Model sees: ["What", "is", "a", "pod", "in"]

Model predicts next word probabilities:
  "Kubernetes"  → 82%
  "Docker"      → 8%
  "biology"     → 5%
  "cooking"     → 2%
  ...

Picks "Kubernetes" → then predicts the NEXT word → repeats until done
```

&nbsp;

### Key terms you just learned by doing

| Term | What it means |
|------|--------------|
| **Model** | The brain — a file full of learned patterns (weights) |
| **Parameters** | The numbers inside the model — more = smarter but slower |
| **Inference** | Running a model to get an answer (not training it) |
| **Token** | A piece of a word — "Kubernetes" = ~3 tokens |
| **Context window** | How much text the model can "remember" in one conversation |

&nbsp;

---

&nbsp;

## Part 3 — Compare Models `25 min`

&nbsp;

### Why different models?

Models come in different sizes. Bigger = smarter but slower. Smaller = faster but less capable. Picking the right model for the job is a real-world skill.

```
┌──────────────────────────────────────────────────┐
│  Model Size Spectrum                             │
│                                                  │
│  Small              Medium             Large     │
│  ┌──────┐          ┌──────┐          ┌──────┐   │
│  │ 1-3B │          │ 7-8B │          │ 70B+ │   │
│  │      │          │      │          │      │   │
│  │ Fast │          │ Good │          │ Best │   │
│  │ OK   │          │balance│         │ Slow │   │
│  │quality│         │      │          │ Needs│   │
│  │      │          │      │          │ GPU  │   │
│  └──────┘          └──────┘          └──────┘   │
│  phi3              llama3.2          llama3.1   │
│  gemma:2b          mistral           (skip)     │
└──────────────────────────────────────────────────┘
```

&nbsp;

### Do This — Try 3 models

**1 →** You already have llama3.2. Now try Mistral:

```bash
ollama run mistral
```

Ask it the same questions you asked llama3.2. Notice the difference in style and quality.

&nbsp;

**2 →** Try a small, fast model:

```bash
ollama run phi3
```

> Phi3 is Microsoft's small model — fast but less capable. Great for quick tasks.

&nbsp;

**3 →** Compare them — fill this in as you test

| | llama3.2 | mistral | phi3 |
|--|----------|---------|------|
| **Size on disk** | ~2GB | ~4GB | ~2GB |
| **Speed** | (your notes) | (your notes) | (your notes) |
| **Answer quality** | (your notes) | (your notes) | (your notes) |
| **Best for** | (your notes) | (your notes) | (your notes) |

> This comparison skill matters for the AWS AI Practitioner exam — you'll be asked when to choose different model sizes.

&nbsp;

---

&nbsp;

## Part 4 — Prompt Engineering Basics `20 min`

&nbsp;

### What is prompt engineering? (30-second version)

The same model gives wildly different answers depending on HOW you ask. Prompt engineering is the art of asking better questions.

```
┌──────────────────────────────────────────────────┐
│  Same model, different prompts:                  │
│                                                  │
│  Bad prompt:                                     │
│  "Tell me about Python"                          │
│   → Generic 500-word essay 😴                    │
│                                                  │
│  Good prompt:                                    │
│  "Explain Python virtual environments in         │
│   3 bullet points. Audience: someone who         │
│   knows JavaScript but not Python."              │
│   → Focused, useful answer 🎯                    │
└──────────────────────────────────────────────────┘
```

&nbsp;

### Techniques to try

Pick any model and try each of these in the chat:

&nbsp;

**1 →** Zero-shot (just ask directly — no examples)

```
>>> What is a Kubernetes ConfigMap?
```

&nbsp;

**2 →** Few-shot (give examples first, then ask)

```
>>> I'll give you K8s terms and you explain them in one sentence:
>>> Pod: The smallest deployable unit in Kubernetes
>>> Service: A stable network address for a set of pods
>>> Now explain: ReplicaSet
```

&nbsp;

**3 →** Chain-of-thought (ask it to think step by step)

```
>>> A pod is in CrashLoopBackOff status. Walk me through the debugging steps
>>> one by one, explaining why each step matters.
```

&nbsp;

**4 →** Role-based (give it a persona)

```
>>> You are a senior Kubernetes administrator. A junior engineer asks you
>>> why their deployment isn't scaling. What questions do you ask them?
```

&nbsp;

### The pattern

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Zero-shot  │     │  Few-shot   │     │  Chain-of-   │
│             │     │             │     │  thought     │
│  Just ask   │     │  Give       │     │  "Think      │
│             │────▶│  examples   │────▶│  step by     │
│  Simplest   │     │  first      │     │  step"       │
│  approach   │     │             │     │              │
│             │     │  Better     │     │  Best for    │
│             │     │  accuracy   │     │  reasoning   │
└─────────────┘     └─────────────┘     └─────────────┘
```

&nbsp;

---

&nbsp;

## Part 5 — Commit `10 min`

Write notes on which model you liked best and what prompt techniques worked.

```bash
git add sprint-03-cloud-native/
git commit -m "sprint 3 day 3: ollama installed, compared 3 LLMs, prompt engineering"
git push
```

&nbsp;

---

&nbsp;

## ✅ Day 3 Checklist

| | Task |
|---|------|
| ☐ | Ollama installed and running |
| ☐ | Chatted with llama3.2 |
| ☐ | Tried at least 2 other models (mistral, phi3) |
| ☐ | Filled in the model comparison table |
| ☐ | Tried zero-shot, few-shot, and chain-of-thought prompting |
| ☐ | Pushed notes to GitHub 🟩 |

&nbsp;

---

&nbsp;

## 🧠 Concepts You Now Own

| Concept | One-liner |
|---------|-----------|
| **LLM** | Large Language Model — predicts the next word, really well |
| **Ollama** | Tool that runs LLMs locally with one command |
| **Parameters (B)** | Billions of numbers inside the model — bigger = smarter but slower |
| **Inference** | Running a model to get answers (vs training it) |
| **Token** | A piece of a word — how models read text |
| **Context window** | How much text the model can "see" at once |
| **Prompt engineering** | The art of asking better questions to get better answers |
| **Zero-shot** | Just ask — no examples given |
| **Few-shot** | Give examples first, then ask |
| **Chain-of-thought** | "Think step by step" — improves reasoning |

&nbsp;

---

&nbsp;

> *Next: You turn this into a Python project — a CLI chatbot that saves conversations. 🐍🤖*
