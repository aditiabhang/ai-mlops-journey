# Sprint 5 · Day 2

## 🔧 The ML Pipeline + AWS AI Services

`90 min` · `Concept + AWS service mapping` · `AIF-C01 Domain 1 continued`

---

&nbsp;

## Today's Big Picture

> Yesterday you learned WHAT AI is. Today you learn HOW it gets built.
> The ML pipeline is the assembly line — data in, trained model out.
> Then we map it to AWS services so you know which tool to use for what.

By the end of today, you'll have:

- ✅ Understand the full ML pipeline (data → train → evaluate → deploy → monitor)
- ✅ Know key model performance metrics (accuracy, F1, AUC)
- ✅ Understand MLOps basics
- ✅ Can name 10+ AWS AI services and when to use each

&nbsp;

---

&nbsp;

## Part 1 — The ML Pipeline `25 min`

&nbsp;

### The journey of a model — from raw data to production

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  1. DATA │    │  2. DATA │    │ 3. MODEL │    │  4. EVAL │    │ 5. DEPLOY│    │ 6. MONI- │
│  COLLECT │───▶│  PREPARE │───▶│  TRAIN   │───▶│  UATE    │───▶│          │───▶│  TOR     │
│          │    │          │    │          │    │          │    │          │    │          │
│ • Gather │    │ • Clean  │    │ • Pick   │    │ • Test   │    │ • API    │    │ • Drift  │
│   data   │    │ • Label  │    │   algo   │    │ • Metrics│    │ • Serve  │    │ • Retrain│
│ • Store  │    │ • Split  │    │ • Train  │    │ • Tune   │    │ • Scale  │    │ • Alerts │
│          │    │ • Feature│    │ • Iterate│    │          │    │          │    │          │
└──────────┘    └──────────┘    └──────────┘    └──────────┘    └──────────┘    └──────────┘
      │                                                                              │
      └──────────────────────────────── feedback loop ───────────────────────────────┘
```

&nbsp;

### Each stage explained

| Stage | What happens | Key terms |
|-------|-------------|-----------|
| **1. Data Collection** | Gather raw data from databases, APIs, files, sensors | Data sources, data lake |
| **2. Data Preparation** | Clean, label, transform, split into train/test sets | Feature engineering, data wrangling, train/test split |
| **3. Model Training** | Feed data into an algorithm, adjust weights | Epochs, loss function, hyperparameters |
| **4. Evaluation** | Test the model on data it hasn't seen | Accuracy, precision, recall, F1, AUC |
| **5. Deployment** | Make the model available for use | API endpoint, managed service, container |
| **6. Monitoring** | Watch for performance degradation over time | Model drift, data drift, retraining |

&nbsp;

### The train/test split — why it matters

```
Your dataset (1000 emails):

┌────────────────────────────────────────────────────┐
│  Training set (80%)         │  Test set (20%)      │
│  800 emails                 │  200 emails          │
│                             │                      │
│  Model learns from these    │  Model is tested     │
│                             │  on these (never     │
│                             │  seen during         │
│                             │  training)           │
└─────────────────────────────┴──────────────────────┘

Why? If you test on training data, the model just memorizes answers.
That's called OVERFITTING. It looks great in testing, fails in real life.
```

&nbsp;

---

&nbsp;

## Part 2 — Model Metrics `15 min`

&nbsp;

### The metrics the exam tests

```
┌──────────────────────────────────────────────────────┐
│  MODEL PERFORMANCE METRICS                           │
│                                                      │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐     │
│  │  ACCURACY  │  │  PRECISION │  │  RECALL    │     │
│  │            │  │            │  │            │     │
│  │  "How      │  │  "When it  │  │  "Did it   │     │
│  │   often    │  │   says yes │  │   find ALL │     │
│  │   right?"  │  │   is it    │  │   the yes  │     │
│  │            │  │   right?"  │  │   cases?"  │     │
│  └────────────┘  └────────────┘  └────────────┘     │
│                                                      │
│  ┌────────────┐  ┌────────────┐                      │
│  │  F1 SCORE  │  │  AUC       │                      │
│  │            │  │            │                      │
│  │  Balance   │  │  Overall   │                      │
│  │  of prec.  │  │  model     │                      │
│  │  & recall  │  │  quality   │                      │
│  └────────────┘  └────────────┘                      │
└──────────────────────────────────────────────────────┘
```

| Metric | What it measures | When it matters |
|--------|-----------------|-----------------|
| **Accuracy** | % of correct predictions overall | Balanced datasets |
| **Precision** | Of all "yes" predictions, how many were actually yes? | When false positives are costly (spam filter) |
| **Recall** | Of all actual yes cases, how many did we find? | When missing a case is dangerous (cancer detection) |
| **F1 Score** | Harmonic mean of precision and recall | When you need both |
| **AUC** | Area Under the ROC Curve — overall quality | General model comparison |

&nbsp;

### Overfitting vs Underfitting

```
┌──────────────────────────────────────────────────────┐
│                                                      │
│  UNDERFITTING         GOOD FIT         OVERFITTING   │
│                                                      │
│  Too simple           Just right       Too complex   │
│  Misses patterns      Captures signal  Memorizes     │
│  Bad on training      Good on both     noise         │
│  AND test data        datasets         Great on      │
│                                        training,     │
│  "Can't even          "Nailed it"      FAILS on new  │
│   learn the                            data          │
│   basics"                                            │
└──────────────────────────────────────────────────────┘
```

&nbsp;

---

&nbsp;

## Part 3 — MLOps `10 min`

&nbsp;

### What is MLOps? (30-second version)

DevOps for machine learning. Same idea — automate everything, make it repeatable, monitor it in production. The ML pipeline from Part 1 run as an automated, repeatable system.

| MLOps Concept | One-liner |
|--------------|-----------|
| **Experiment tracking** | Log every model training run — parameters, metrics, results |
| **Model registry** | Versioned storage for trained models |
| **Automated pipelines** | Data prep → train → eval → deploy — all automated |
| **Model monitoring** | Watch for drift — retrain when performance drops |
| **Reproducibility** | Same data + same code = same model every time |
| **Feature store** | Central place for reusable data features |
| **Model drift** | Model gets worse over time as real-world data changes |

&nbsp;

---

&nbsp;

## Part 4 — AWS AI/ML Services Map `30 min`

&nbsp;

### The 3 layers of AWS AI

```
┌─────────────────────────────────────────────────────┐
│  LAYER 3: AI SERVICES (no ML knowledge needed)      │
│  Pre-built AI for common tasks                      │
│                                                     │
│  Rekognition · Comprehend · Transcribe · Translate  │
│  Polly · Lex · Textract · Personalize · Kendra      │
│  Fraud Detector                                     │
├─────────────────────────────────────────────────────┤
│  LAYER 2: ML PLATFORMS (some ML knowledge)          │
│  Build, train, deploy custom models                 │
│                                                     │
│  SageMaker · SageMaker JumpStart · Bedrock          │
├─────────────────────────────────────────────────────┤
│  LAYER 1: ML INFRASTRUCTURE (deep ML knowledge)    │
│  Raw compute for training                           │
│                                                     │
│  EC2 (GPU instances) · S3 · EKS                     │
└─────────────────────────────────────────────────────┘
```

> **For the exam:** You'll mostly be asked about Layer 3 (which service for which task) and Layer 2 (SageMaker and Bedrock).

&nbsp;

### AWS AI Services — the cheat table

| Service | What it does | Use case |
|---------|-------------|----------|
| **Amazon Rekognition** | Image and video analysis | Face detection, object labeling, content moderation |
| **Amazon Comprehend** | NLP — text analysis | Sentiment analysis, entity extraction, topic modeling |
| **Amazon Transcribe** | Speech to text | Meeting transcription, call center recordings |
| **Amazon Translate** | Language translation | Translate content to 75+ languages |
| **Amazon Polly** | Text to speech | Voice assistants, audiobook generation |
| **Amazon Lex** | Chatbot builder | Build conversational bots (powers Alexa) |
| **Amazon Textract** | Document data extraction | Pull text/tables from scanned PDFs |
| **Amazon Personalize** | Recommendations | "Customers who bought X also bought Y" |
| **Amazon Kendra** | Intelligent search | Enterprise document search with NLP |
| **Amazon Fraud Detector** | Fraud detection | Online payment fraud, fake account detection |
| **Amazon A2I** | Human review of ML predictions | Human-in-the-loop for low-confidence results |
| **Amazon SageMaker** | Full ML platform | Build, train, deploy custom models |
| **Amazon Bedrock** | Foundation model API | Access Claude, Llama, Titan without managing infra |

&nbsp;

### Quick decision flow for the exam

```
"I need to..."

  Analyze images        → Rekognition
  Understand text       → Comprehend
  Convert speech→text   → Transcribe
  Convert text→speech   → Polly
  Translate languages   → Translate
  Build a chatbot       → Lex
  Extract from docs     → Textract
  Recommend products    → Personalize
  Search documents      → Kendra
  Detect fraud          → Fraud Detector
  Build custom model    → SageMaker
  Use foundation model  → Bedrock
  Need human review     → A2I
```

&nbsp;

---

&nbsp;

## Part 5 — Commit `5 min`

```bash
git add sprint-05-ai-foundations/
git commit -m "sprint 5 day 2: ML pipeline, model metrics, MLOps, AWS AI services map"
git push
```

&nbsp;

---

&nbsp;

## ✅ Day 2 Checklist

| | Task |
|---|------|
| ☐ | Can draw the 6-stage ML pipeline from memory |
| ☐ | Know why train/test split matters (overfitting) |
| ☐ | Understand accuracy, precision, recall, F1, AUC |
| ☐ | Know what MLOps is and why model drift matters |
| ☐ | Can name 10+ AWS AI services and match them to use cases |
| ☐ | Pushed to GitHub 🟩 |

&nbsp;

---

&nbsp;

## 🧠 Concepts You Now Own

| Concept | One-liner |
|---------|-----------|
| **ML Pipeline** | Data → prepare → train → evaluate → deploy → monitor |
| **Feature engineering** | Transforming raw data into useful model inputs |
| **Train/test split** | 80/20 — never test on training data |
| **Overfitting** | Model memorizes training data, fails on new data |
| **Underfitting** | Model too simple, can't learn the pattern |
| **Accuracy** | % of total predictions that are correct |
| **Precision** | Of the "yes" predictions, how many were right? |
| **Recall** | Of the actual "yes" cases, how many did we find? |
| **F1** | Balance of precision and recall |
| **MLOps** | DevOps for ML — automate and monitor the pipeline |
| **Model drift** | Model performance degrades as real data changes |
| **SageMaker** | AWS platform to build, train, deploy ML models |
| **Bedrock** | Access foundation models via API — no infra to manage |

&nbsp;

---

&nbsp;

> *Next: Generative AI — transformers, tokens, and how LLMs actually work under the hood. 🤖*
