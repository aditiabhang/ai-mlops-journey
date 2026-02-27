# Sprint 5 · Day 1

## 🧠 ML 101 — What is AI, Really?

`90 min` · `No code today` · `The "aha" day — everything clicks`

---

&nbsp;

## Today's Big Picture

> Everyone talks about AI. Few people can actually explain it.
> After today, you'll be one of the few. No hype, no buzzwords — just what it IS
> and how the pieces connect.

By the end of today, you'll have:

- ✅ Understand the relationship between AI, ML, and Deep Learning
- ✅ Know the 3 types of learning (supervised, unsupervised, reinforcement)
- ✅ Understand neural networks at a concept level
- ✅ Know the difference between training and inference
- ✅ Can name real-world AI use cases and match them to techniques

&nbsp;

---

&nbsp;

## Part 1 — AI vs ML vs Deep Learning `15 min`

&nbsp;

### How they relate (30-second version)

AI is the biggest circle. ML is inside it. Deep Learning is inside ML.

```
┌─────────────────────────────────────────────────┐
│  ARTIFICIAL INTELLIGENCE                        │
│  "Machines that act smart"                      │
│                                                 │
│  ┌───────────────────────────────────────┐      │
│  │  MACHINE LEARNING                     │      │
│  │  "Machines that learn from data"      │      │
│  │                                       │      │
│  │  ┌─────────────────────────────┐      │      │
│  │  │  DEEP LEARNING              │      │      │
│  │  │  "ML with neural networks"  │      │      │
│  │  │                             │      │      │
│  │  │  • Image recognition        │      │      │
│  │  │  • Language models (LLMs)   │      │      │
│  │  │  • Speech-to-text           │      │      │
│  │  └─────────────────────────────┘      │      │
│  │                                       │      │
│  │  • Spam filters                       │      │
│  │  • Recommendation engines             │      │
│  │  • Fraud detection                    │      │
│  └───────────────────────────────────────┘      │
│                                                 │
│  • Rule-based systems                           │
│  • Expert systems                               │
│  • Search algorithms                            │
└─────────────────────────────────────────────────┘
```

&nbsp;

### The key differences

| | AI | ML | Deep Learning |
|--|----|----|---------------|
| **What** | Broad field — machines that seem intelligent | Subset of AI — learns patterns from data | Subset of ML — uses neural networks |
| **How** | Could be rules, logic, or learning | Algorithms trained on data | Many-layered neural networks |
| **Needs data?** | Not always | Yes — lots of it | Yes — even more of it |
| **Example** | Chess engine (rules-based) | Email spam filter | ChatGPT, image recognition |

&nbsp;

---

&nbsp;

## Part 2 — The 3 Types of Learning `20 min`

&nbsp;

### The big picture

```
┌─────────────────────────────────────────────────────────────┐
│                    MACHINE LEARNING                         │
│                                                             │
│  ┌─────────────────┐ ┌─────────────────┐ ┌──────────────┐  │
│  │   SUPERVISED     │ │  UNSUPERVISED    │ │ REINFORCE-   │  │
│  │                  │ │                  │ │ MENT         │  │
│  │  "I'll show you  │ │  "Find patterns  │ │ "Try stuff,  │  │
│  │   the answers    │ │   on your own"   │ │  get rewards │  │
│  │   — now learn"   │ │                  │ │  or punished"│  │
│  │                  │ │                  │ │              │  │
│  │  Data: LABELED   │ │  Data: UNLABELED │ │ Data: NONE   │  │
│  │  (input + answer)│ │  (just input)    │ │ (trial/error)│  │
│  │                  │ │                  │ │              │  │
│  │  • Classification│ │  • Clustering    │ │ • Game AI    │  │
│  │  • Regression    │ │  • Anomaly       │ │ • Robotics   │  │
│  │  • Prediction    │ │    detection     │ │ • Self-driving│  │
│  └─────────────────┘ └─────────────────┘ └──────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

&nbsp;

### Supervised Learning — "Here's the answer key"

You give the model both the question AND the answer. It learns the pattern.

| Technique | What it does | Example |
|-----------|-------------|---------|
| **Classification** | Put things into categories | "Is this email spam or not?" |
| **Regression** | Predict a number | "What will the house price be?" |

```
Training data:
  Email text: "Free money!"     → Label: SPAM
  Email text: "Meeting at 3pm"  → Label: NOT SPAM
  Email text: "You won!!!"     → Label: SPAM

After training:
  New email: "Click for prize"  → Model predicts: SPAM ✅
```

&nbsp;

### Unsupervised Learning — "Figure it out yourself"

No labels. The model finds patterns and groups on its own.

| Technique | What it does | Example |
|-----------|-------------|---------|
| **Clustering** | Group similar items | Customer segmentation |
| **Anomaly detection** | Find the odd one out | Fraud detection |
| **Dimensionality reduction** | Simplify complex data | Data visualization |

&nbsp;

### Reinforcement Learning — "Learn by doing"

The model tries actions, gets rewards or penalties, and learns what works.

```
Agent (the AI) → takes Action → Environment gives Reward/Penalty
                                  ↓
                    Agent adjusts behavior for next time
```

> Think of it like training a dog. Good behavior → treat. Bad behavior → no treat. Eventually the dog learns.

&nbsp;

---

&nbsp;

## Part 3 — Neural Networks `20 min`

&nbsp;

### What is a neural network? (30-second version)

A neural network is layers of math that transform input into output. Each layer learns a slightly more complex pattern. Simple layers near the input, abstract layers near the output.

```
┌─────────────────────────────────────────────────┐
│  NEURAL NETWORK                                 │
│                                                 │
│  Input        Hidden Layers        Output       │
│  Layer        (the learning)       Layer        │
│                                                 │
│  ○───┐    ┌───○───┐    ┌───○───┐    ┌───○      │
│      ├────┤       ├────┤       ├────┤           │
│  ○───┤    ├───○───┤    ├───○───┤    ├───○      │
│      ├────┤       ├────┤       ├────┤           │
│  ○───┤    ├───○───┤    ├───○───┤    └───○      │
│      └────┘       └────┘       └────┘           │
│                                                 │
│  "Is this     "I see       "I see        "It's  │
│   a cat?"      edges"       shapes"       a cat"│
└─────────────────────────────────────────────────┘
```

&nbsp;

### Key terms

| Term | One-liner |
|------|-----------|
| **Neuron / Node** | One unit that takes input, does math, passes output |
| **Weight** | How important each input is — adjusted during training |
| **Bias** | An offset that helps the model fit the data better |
| **Activation function** | Decides if a neuron "fires" — adds non-linearity |
| **Layer** | A row of neurons — input, hidden, or output |
| **Deep learning** | "Deep" = many hidden layers (that's literally all it means) |
| **Epoch** | One complete pass through the entire training dataset |
| **Loss function** | Measures how wrong the model is — training minimizes this |

&nbsp;

---

&nbsp;

## Part 4 — Training vs Inference `10 min`

&nbsp;

### The two phases of any ML model

```
┌───────────────────────────────┐     ┌──────────────────────────────┐
│  TRAINING                     │     │  INFERENCE                   │
│                               │     │                              │
│  "Teaching the model"         │     │  "Using the model"           │
│                               │     │                              │
│  • Needs LOTS of data         │     │  • Needs one input at a time │
│  • Takes hours/days/weeks     │     │  • Takes milliseconds        │
│  • Expensive (GPUs)           │     │  • Cheaper                   │
│  • Done once (or periodically)│     │  • Done constantly           │
│  • Output: a trained model    │     │  • Output: a prediction      │
│                               │     │                              │
│  Example:                     │     │  Example:                    │
│  Feed 1M emails → model       │     │  New email arrives → model   │
│  learns spam patterns          │     │  says "spam" or "not spam"   │
└───────────────────────────────┘     └──────────────────────────────┘
```

&nbsp;

### Inference types the exam tests

| Type | How it works | Example |
|------|-------------|---------|
| **Real-time** | Instant response — request → answer | Chatbot, fraud check |
| **Batch** | Process many items at once — scheduled | Nightly report, data scoring |

&nbsp;

---

&nbsp;

## Part 5 — Data Types in AI `10 min`

&nbsp;

### What the exam expects

| Data Type | What it means | Example |
|-----------|--------------|---------|
| **Labeled** | Data WITH the answer attached | Email + "spam/not spam" tag |
| **Unlabeled** | Data WITHOUT answers | 1M emails, no tags |
| **Structured** | Organized in rows/columns | Spreadsheet, database table |
| **Unstructured** | No fixed format | Images, audio, free text |
| **Tabular** | Rows and columns — classic data | CSV, SQL table |
| **Time-series** | Data ordered by time | Stock prices, server metrics |
| **Text** | Natural language | Emails, reviews, chat logs |
| **Image** | Visual data | Photos, X-rays, satellite images |

&nbsp;

---

&nbsp;

## Part 6 — Real-World AI Use Cases `5 min`

&nbsp;

### Match the technique to the use case

| Use Case | AI Technique |
|----------|-------------|
| Spam detection | Supervised — classification |
| House price prediction | Supervised — regression |
| Customer segmentation | Unsupervised — clustering |
| Fraud detection | Unsupervised — anomaly detection |
| Game-playing AI | Reinforcement learning |
| Image recognition | Deep learning — CNN |
| Language translation | Deep learning — transformer |
| Speech-to-text | Deep learning — NLP |
| Product recommendations | Collaborative filtering (ML) |
| Forecasting sales | Supervised — regression + time-series |

&nbsp;

---

&nbsp;

## Part 7 — Commit `5 min`

```bash
git add sprint-05-ai-foundations/
git commit -m "sprint 5 day 1: ML 101 — AI vs ML vs DL, learning types, neural nets"
git push
```

&nbsp;

---

&nbsp;

## ✅ Day 1 Checklist

| | Task |
|---|------|
| ☐ | Can explain AI vs ML vs Deep Learning |
| ☐ | Know supervised, unsupervised, reinforcement learning + examples |
| ☐ | Understand classification vs regression |
| ☐ | Can describe a neural network at a concept level |
| ☐ | Know the difference between training and inference |
| ☐ | Know labeled vs unlabeled, structured vs unstructured data |
| ☐ | Pushed to GitHub 🟩 |

&nbsp;

---

&nbsp;

## 🧠 Concepts You Now Own

| Concept | One-liner |
|---------|-----------|
| **AI** | Machines that act smart — broad field |
| **ML** | Machines that learn patterns from data |
| **Deep Learning** | ML with many-layered neural networks |
| **Supervised** | Learn from labeled data (answer key provided) |
| **Unsupervised** | Find patterns in unlabeled data |
| **Reinforcement** | Learn by trial and error — rewards/penalties |
| **Classification** | "Which category?" — spam or not spam |
| **Regression** | "What number?" — predict house price |
| **Clustering** | "What groups exist?" — customer segments |
| **Neural network** | Layers of math that learn patterns |
| **Training** | Teaching the model — expensive, slow, done once |
| **Inference** | Using the model — cheap, fast, done constantly |
| **Labeled data** | Input + correct answer attached |

&nbsp;

---

&nbsp;

> *Next: The ML pipeline — how models go from idea to production, plus AWS AI services. 🔧*
