# Sprint 6 · Day 2

## 🔬 Domain 3 Continued — Fine-tuning, Evaluation & Model Serving

`90 min` · `AIF-C01 Domain 3 Part 2` · `The "how models get better" day`

---

&nbsp;

## Today's Big Picture

> Yesterday was about USING models. Today is about IMPROVING and EVALUATING them.
> How do you make a model better at your specific task? How do you measure if it's working?
> And how do you serve it in production?

By the end of today, you'll have:

- ✅ Understand the fine-tuning process and methods
- ✅ Know how to prepare data for fine-tuning
- ✅ Understand foundation model evaluation metrics (ROUGE, BLEU, BERTScore)
- ✅ Know how to serve a model in production
- ✅ Built a simple model serving API (FastAPI)

&nbsp;

---

&nbsp;

## Part 1 — Fine-tuning Foundation Models `25 min`

&nbsp;

### What is fine-tuning? (30-second version)

Pre-training teaches a model everything. Fine-tuning teaches it YOUR thing. It's the difference between a college graduate (general knowledge) and an employee after onboarding (knows your company's way of doing things).

```
┌──────────────────────────────────────────────────────┐
│  CUSTOMIZATION SPECTRUM                              │
│                                                      │
│  No change                                 Full      │
│  ◀──────────────────────────────────────▶  rebuild   │
│                                                      │
│  Prompt         In-context    Fine-        Contin-   │
│  Engineering    Learning      tuning       uous      │
│                                            Pre-      │
│  "Ask better"   "Give         "Retrain     training  │
│                  examples      some                   │
│  Cost: Free     in prompt"    weights"    "Train     │
│  Time: Instant                             from      │
│                 Cost: $       Cost: $$     more data" │
│                 Time: Instant Time: Hours             │
│                                           Cost: $$$$ │
│                                           Time: Days │
└──────────────────────────────────────────────────────┘
```

&nbsp;

### Fine-tuning methods the exam tests

| Method | What it does | When to use |
|--------|-------------|-------------|
| **Instruction tuning** | Train the model to follow specific instructions | Customer service bots, task-specific assistants |
| **Domain adaptation** | Train on domain-specific data (medical, legal) | When the model doesn't know your industry's language |
| **Transfer learning** | Take knowledge from one task, apply to another | Limited data for your specific task |
| **Continuous pre-training** | Keep training the base model on new data | Model needs updated knowledge |
| **RLHF** | Reinforcement Learning from Human Feedback — humans rate outputs | Making responses more helpful and safe |

&nbsp;

### Preparing data for fine-tuning

```
┌──────────────────────────────────────────────────────┐
│  DATA PREPARATION CHECKLIST                          │
│                                                      │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐     │
│  │ CURATE     │  │ QUALITY    │  │ FORMAT     │     │
│  │            │  │            │  │            │     │
│  │ • Relevant │  │ • Clean    │  │ • Prompt + │     │
│  │ • Diverse  │  │ • Accurate │  │   completion│    │
│  │ • Represen-│  │ • No PII   │  │   pairs     │    │
│  │   tative   │  │ • No bias  │  │ • JSONL    │     │
│  │ • Enough   │  │ • Labeled  │  │ • Consistent│    │
│  │   volume   │  │            │  │            │     │
│  └────────────┘  └────────────┘  └────────────┘     │
└──────────────────────────────────────────────────────┘
```

| Consideration | What to know |
|--------------|-------------|
| **Data curation** | Select relevant, high-quality examples |
| **Data governance** | Ensure compliance, track data lineage |
| **Size** | More data = better fine-tuning (typically 100s-1000s of examples) |
| **Labeling** | Human-reviewed labels for quality |
| **Representativeness** | Data should reflect real-world distribution |
| **RLHF** | Human raters score model outputs to improve alignment |

&nbsp;

---

&nbsp;

## Part 2 — Model Evaluation `20 min`

&nbsp;

### How do you know if a model is good?

Two approaches: automated metrics and human evaluation.

```
┌──────────────────────────────────────────────────────┐
│  MODEL EVALUATION                                    │
│                                                      │
│  ┌──────────────────────┐  ┌──────────────────────┐  │
│  │  AUTOMATED METRICS   │  │  HUMAN EVALUATION    │  │
│  │                      │  │                      │  │
│  │  Fast, cheap,        │  │  Slow, expensive,    │  │
│  │  consistent          │  │  but captures nuance │  │
│  │                      │  │                      │  │
│  │  • ROUGE             │  │  • Relevance rating  │  │
│  │  • BLEU              │  │  • Helpfulness score │  │
│  │  • BERTScore         │  │  • Safety review     │  │
│  │  • Perplexity        │  │  • A/B testing       │  │
│  └──────────────────────┘  └──────────────────────┘  │
└──────────────────────────────────────────────────────┘
```

&nbsp;

### Automated metrics — the ones the exam tests

| Metric | Stands for | Measures | Best for |
|--------|-----------|----------|----------|
| **ROUGE** | Recall-Oriented Understudy for Gisting Evaluation | Overlap between model output and reference text | **Summarization** |
| **BLEU** | Bilingual Evaluation Understudy | Precision of generated text vs reference | **Translation** |
| **BERTScore** | BERT-based similarity | Semantic similarity using embeddings | **General text quality** |
| **Perplexity** | — | How surprised the model is by text (lower = better) | **Language modeling** |

> **Memory trick:**
> - **ROUGE** = **R**ecall → **S**ummarization (both start with S... close enough)
> - **BLEU** = **B**ilingual → **T**ranslation
> - **BERTScore** = **B**EST for general comparison

&nbsp;

### Business metrics (also tested)

| Metric | What it measures |
|--------|-----------------|
| **Cost per user** | How much each AI interaction costs |
| **Development costs** | Total cost to build and deploy |
| **Customer feedback** | User satisfaction scores |
| **ROI** | Return on investment — value vs cost |
| **User engagement** | How much users interact with the AI |
| **Task completion rate** | % of tasks the AI successfully handles |

&nbsp;

---

&nbsp;

## Part 3 — Model Serving `15 min`

&nbsp;

### How models get to production

```
┌──────────────────────────────────────────────────────┐
│  MODEL SERVING OPTIONS                               │
│                                                      │
│  ┌────────────────────┐  ┌────────────────────────┐  │
│  │  MANAGED API       │  │  SELF-HOSTED           │  │
│  │                    │  │                        │  │
│  │  • Bedrock         │  │  • FastAPI + Docker    │  │
│  │  • SageMaker       │  │  • On EC2 or EKS       │  │
│  │    endpoint        │  │  • Full control        │  │
│  │  • No infra mgmt   │  │  • You manage scaling  │  │
│  │  • Pay per use     │  │  • Pay for compute     │  │
│  │                    │  │                        │  │
│  │  Best for:         │  │  Best for:             │  │
│  │  Most use cases    │  │  Custom models,        │  │
│  │                    │  │  strict requirements   │  │
│  └────────────────────┘  └────────────────────────┘  │
└──────────────────────────────────────────────────────┘
```

&nbsp;

---

&nbsp;

## Part 4 — Mini-Project: Model Serving API `20 min`

&nbsp;

### Build a simple model serving API with FastAPI

This demonstrates the concept of serving a model via REST API — the same pattern Bedrock and SageMaker use, just simpler.

**1 →** Create the project

```bash
mkdir -p ~/projects/ai-mlops-journey/projects/02-model-serving
cd ~/projects/ai-mlops-journey/projects/02-model-serving
python3 -m venv .venv
source .venv/bin/activate
pip install fastapi uvicorn requests
```

&nbsp;

**2 →** Create `app.py`

```python
from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI(title="Model Serving API")


class PromptRequest(BaseModel):
    prompt: str
    model: str = "llama3.2"


class PromptResponse(BaseModel):
    model: str
    prompt: str
    response: str


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/generate", response_model=PromptResponse)
def generate(req: PromptRequest):
    result = requests.post("http://localhost:11434/api/chat", json={
        "model": req.model,
        "messages": [{"role": "user", "content": req.prompt}],
        "stream": False
    })
    answer = result.json()["message"]["content"]
    return PromptResponse(model=req.model, prompt=req.prompt, response=answer)
```

&nbsp;

**3 →** Run it (make sure `ollama serve` is running in another tab)

```bash
uvicorn app:app --reload --port 8000
```

&nbsp;

**4 →** Test it

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is RAG in 2 sentences?"}'
```

> You just built a model serving API. This is exactly what happens behind Bedrock and SageMaker — a REST API that wraps a model.

&nbsp;

**5 →** Visit `http://localhost:8000/docs` — FastAPI auto-generates interactive API docs. Click "Try it out" to test from your browser.

&nbsp;

---

&nbsp;

## Part 5 — Commit `5 min`

```bash
cd ~/projects/ai-mlops-journey
echo ".venv/" > projects/02-model-serving/.gitignore
git add projects/02-model-serving/ sprint-06-ai-exam-prep/
git commit -m "sprint 6 day 2: fine-tuning, eval metrics, model serving API"
git push
```

&nbsp;

---

&nbsp;

## ✅ Day 2 Checklist

| | Task |
|---|------|
| ☐ | Can explain fine-tuning methods (instruction tuning, RLHF, domain adaptation) |
| ☐ | Know how to prepare data for fine-tuning |
| ☐ | Can name ROUGE, BLEU, BERTScore and what each measures |
| ☐ | Understand managed API vs self-hosted model serving |
| ☐ | Built a FastAPI model serving API |
| ☐ | Pushed to GitHub 🟩 |

&nbsp;

---

&nbsp;

## 🧠 Concepts You Now Own

| Concept | One-liner |
|---------|-----------|
| **Fine-tuning** | Retrain some model weights on your specific data |
| **Instruction tuning** | Teach model to follow instructions better |
| **RLHF** | Humans rate outputs to improve alignment |
| **Transfer learning** | Apply knowledge from one task to another |
| **ROUGE** | Summarization metric — recall-based overlap |
| **BLEU** | Translation metric — precision-based overlap |
| **BERTScore** | Semantic similarity using embeddings |
| **Perplexity** | How "surprised" the model is — lower is better |
| **Model serving** | Making a model available via API for predictions |
| **FastAPI** | Python framework for building REST APIs — fast and modern |

&nbsp;

---

&nbsp;

> *Next: Responsible AI + Security & Compliance — the "don't be evil" domains. 🔒*
