# Sprint 5 · Day 5

## 🚀 Sprint Project: Hands-on Bedrock + Foundation Models Cheatsheet

`90 min` · `Hands-on AWS + writing` · `Your AI portfolio piece`

---

&nbsp;

## Today's Big Picture

> Four days of concepts. Today you TOUCH it.
> You'll invoke a foundation model on Bedrock (or explore PartyRock if no AWS account),
> then write a cheatsheet that proves you understand it all.

By the end of today, you'll have:

- ✅ Called a foundation model via AWS Bedrock (or built a PartyRock app)
- ✅ Compared models on the same prompt
- ✅ Written a "Foundation Models Explained" cheatsheet
- ✅ Sprint 5 project — pushed to GitHub 🎉

&nbsp;

---

&nbsp;

## Part 1 — Pick Your Path `5 min`

```
┌──────────────────────────────────────────────────────┐
│  Do you have an AWS account with free tier?          │
│                                                      │
│  YES → Path A: Bedrock Console + API                 │
│  NO  → Path B: PartyRock (free, no account needed)   │
│                                                      │
│  Both paths give you hands-on experience.            │
│  Both are valid for learning and the exam.            │
└──────────────────────────────────────────────────────┘
```

&nbsp;

---

&nbsp;

## Path A — Bedrock Console (AWS account) `40 min`

&nbsp;

### Step 1 → Enable model access

1. Go to [Amazon Bedrock console](https://console.aws.amazon.com/bedrock)
2. Click **Model access** in the left sidebar
3. Request access to these models:
   - Amazon Titan Text Express
   - Anthropic Claude (if available)
   - Meta Llama (if available)
4. Wait for approval (usually instant for Titan)

&nbsp;

### Step 2 → Try the Bedrock playground

1. Click **Chat** in the left sidebar
2. Select **Amazon Titan Text Express**
3. Try these prompts:

```
Prompt 1: "Explain Kubernetes pods in 3 sentences."

Prompt 2: "You are a senior AWS architect. A customer asks:
'Should I use Bedrock or SageMaker for a chatbot over our internal docs?'
Explain your recommendation."

Prompt 3: "Summarize the benefits of RAG in 5 bullet points."
```

&nbsp;

### Step 3 → Experiment with parameters

Try the same prompt with different settings:

| Setting | First try | Second try |
|---------|-----------|------------|
| **Temperature** | 0.1 | 0.9 |
| **Max tokens** | 100 | 500 |

> Notice how temperature 0.1 gives focused, consistent answers.
> Temperature 0.9 gives more varied, creative (sometimes wild) answers.

&nbsp;

### Step 4 → Compare models

Try the SAME prompt on 2 different models. Note differences in:
- Response quality
- Response length
- Speed
- Style

&nbsp;

### Step 5 → (Optional) Try the API with Python

```python
import boto3
import json

client = boto3.client("bedrock-runtime", region_name="us-east-1")

body = json.dumps({
    "inputText": "What is a Kubernetes pod?",
    "textGenerationConfig": {
        "maxTokenCount": 200,
        "temperature": 0.3
    }
})

response = client.invoke_model(
    modelId="amazon.titan-text-express-v1",
    body=body,
    contentType="application/json",
    accept="application/json"
)

result = json.loads(response["body"].read())
print(result["results"][0]["outputText"])
```

> Save this as `projects/bedrock-test/invoke_model.py` if you run it.

&nbsp;

---

&nbsp;

## Path B — PartyRock (no AWS account needed) `40 min`

&nbsp;

### Step 1 → Go to PartyRock

1. Visit [partyrock.aws](https://partyrock.aws)
2. Sign in with a social account (Google, Apple, etc.)
3. No AWS account needed. Completely free.

&nbsp;

### Step 2 → Build a simple app

1. Click **Build your own app**
2. Describe it: *"A tool that takes a Kubernetes error message and explains what it means, what caused it, and how to fix it."*
3. PartyRock auto-generates an app with input/output widgets
4. Test it with real K8s errors:

```
Error: CrashLoopBackOff
Error: ImagePullBackOff
Error: OOMKilled
Error: pod has unbound immediate PersistentVolumeClaims
```

&nbsp;

### Step 3 → Try different prompts

Build a second app:
*"A study helper that quizzes me on AWS AI Practitioner exam topics. It asks one question, I answer, and it tells me if I'm right with an explanation."*

&nbsp;

### Step 4 → Share it

Click **Share** and copy the link. Add it to your project README.

&nbsp;

---

&nbsp;

## Part 2 — Write Your Cheatsheet `30 min`

&nbsp;

### Do This

Create `cheatsheets/foundation-models-explained.md`:

```markdown
# Foundation Models Explained

## What is a foundation model?
(your explanation — 2-3 sentences)

## Key models

| Model | Creator | Type | Known for |
|-------|---------|------|-----------|
| GPT-4 | OpenAI | Text | (your notes) |
| Claude | Anthropic | Text | (your notes) |
| Llama | Meta | Text | (your notes) |
| Titan | Amazon | Text + Embeddings | (your notes) |
| Stable Diffusion | Stability AI | Image | (your notes) |

## How transformers work
(your explanation — the flow: tokenize → embed → attention → predict)

## Key terms

| Term | My explanation |
|------|---------------|
| Token | |
| Context window | |
| Embedding | |
| Temperature | |
| RAG | |
| Fine-tuning | |
| Hallucination | |

## AWS services for GenAI

| Service | When to use it |
|---------|---------------|
| Bedrock | |
| SageMaker | |
| SageMaker JumpStart | |
| PartyRock | |
| Amazon Q | |

## Prompt engineering techniques

| Technique | When to use it |
|-----------|---------------|
| Zero-shot | |
| Few-shot | |
| Chain-of-thought | |
| System prompt | |
| RAG | |
```

> Fill in EVERY cell in your own words. If you can't explain it, go back to the day that covered it. This cheatsheet IS your exam study guide for Domains 1-2.

&nbsp;

---

&nbsp;

## Part 3 — Commit & Push `10 min`

```bash
cd ~/projects/ai-mlops-journey
git add cheatsheets/foundation-models-explained.md
git add sprint-05-ai-foundations/
# If you did Path A:
git add projects/bedrock-test/ 2>/dev/null
git commit -m "sprint 5 project: bedrock hands-on + foundation models cheatsheet 🤖"
git push
```

&nbsp;

---

&nbsp;

## ✅ Day 5 Checklist

| | Task |
|---|------|
| ☐ | Invoked a foundation model (Bedrock or PartyRock) |
| ☐ | Tested different temperature settings |
| ☐ | Compared at least 2 models on the same prompt |
| ☐ | "Foundation Models Explained" cheatsheet written — all cells filled |
| ☐ | Pushed to GitHub 🟩 |

&nbsp;

---

&nbsp;

## 🎉 Sprint 5 Complete!

Look at what you know now:

- How AI, ML, and deep learning relate to each other
- The full ML pipeline from data to production
- How transformers, tokens, and embeddings power every LLM
- Every AWS AI service and when to use it
- Prompt engineering techniques that actually work
- **Hands-on experience with a real foundation model**

Domains 1 and 2 of the AIF-C01? You own them. That's 44% of the exam locked in.

&nbsp;

> *Next: [Sprint 6 — AIF-C01 Domains 3-5 + Exam Prep](../sprint-06-ai-exam-prep/sprint-06-overview.md)*
> *RAG deep dive, responsible AI, security, mock exams, and then... your second cert. 🏆*
