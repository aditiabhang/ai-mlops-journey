# Sprint 6 · Day 3

## 🔒 Domains 4 & 5 — Responsible AI + Security & Compliance

`90 min` · `28% of exam combined` · `The "do it right" day`

---

&nbsp;

## Today's Big Picture

> Building AI that works is one thing. Building AI that's FAIR, SAFE, and LEGAL
> is another. These two domains are 28% of the exam combined.
> They're also the easiest to score on — the answers are common sense with AWS names attached.

By the end of today, you'll have:

- ✅ Understand responsible AI principles (bias, fairness, transparency)
- ✅ Know AWS tools for detecting and monitoring bias
- ✅ Understand AI security (data privacy, encryption, access control)
- ✅ Know governance frameworks and compliance standards
- ✅ Written a responsible AI cheatsheet

&nbsp;

---

&nbsp;

## Part 1 — Domain 4: Responsible AI (14%) `35 min`

&nbsp;

### The pillars of responsible AI

```
┌──────────────────────────────────────────────────────┐
│  RESPONSIBLE AI PRINCIPLES                           │
│                                                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐           │
│  │ FAIRNESS │  │ TRANS-   │  │ SAFETY   │           │
│  │          │  │ PARENCY  │  │          │           │
│  │ No bias  │  │ Explain  │  │ No harm  │           │
│  │ Inclusive │  │ how it   │  │ Robust   │           │
│  │ Equal    │  │ works    │  │ Tested   │           │
│  └──────────┘  └──────────┘  └──────────┘           │
│                                                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐           │
│  │ VERACITY │  │ PRIVACY  │  │ INCLUS-  │           │
│  │          │  │          │  │ IVITY    │           │
│  │ Truthful │  │ Protect  │  │ Works    │           │
│  │ Accurate │  │ personal │  │ for      │           │
│  │ Grounded │  │ data     │  │ everyone │           │
│  └──────────┘  └──────────┘  └──────────┘           │
└──────────────────────────────────────────────────────┘
```

&nbsp;

### Bias in AI — what the exam tests

```
┌──────────────────────────────────────────────────────┐
│  WHERE BIAS ENTERS THE PIPELINE                      │
│                                                      │
│  Data Collection ──▶ Training ──▶ Output             │
│       ▲                 ▲           ▲                │
│       │                 │           │                │
│  Selection          Algorithmic  Confirmation        │
│  bias               bias         bias                │
│                                                      │
│  "Data doesn't    "Model          "Users only see    │
│   represent        amplifies       results that      │
│   everyone"        existing        confirm their     │
│                    patterns"       beliefs"           │
└──────────────────────────────────────────────────────┘
```

| Bias type | What it means | Example |
|-----------|--------------|---------|
| **Selection bias** | Training data doesn't represent the real population | Hiring model trained only on male resumes |
| **Measurement bias** | Data collection method is flawed | Survey only reaches tech-savvy users |
| **Algorithmic bias** | Model amplifies existing patterns in data | Loan approval model that discriminates |
| **Confirmation bias** | System reinforces existing beliefs | Search results that create echo chambers |

&nbsp;

### AWS tools for responsible AI

| Tool | What it does |
|------|-------------|
| **SageMaker Clarify** | Detect bias in data AND model predictions |
| **SageMaker Model Monitor** | Continuous monitoring for drift and bias in production |
| **SageMaker Model Cards** | Document model details: purpose, training, performance, limitations |
| **Bedrock Guardrails** | Filter harmful content, block PII, enforce topic boundaries |
| **Amazon A2I** | Human-in-the-loop — humans review low-confidence predictions |

&nbsp;

### Transparent vs opaque models

```
┌──────────────────────────────────────────────────────┐
│                                                      │
│  TRANSPARENT / EXPLAINABLE    OPAQUE / BLACK-BOX    │
│                                                      │
│  • Decision trees             • Deep neural networks │
│  • Linear regression          • LLMs                 │
│  • Rule-based systems         • Complex ensembles    │
│                                                      │
│  Easy to explain              Hard to explain        │
│  WHY it decided               but often more         │
│  something                    accurate               │
│                                                      │
│  Trade-off: explainability ◀────────▶ performance    │
└──────────────────────────────────────────────────────┘
```

> **Exam tip:** SageMaker Model Cards help identify which models are explainable. Human-centered design for AI means keeping humans informed and in control.

&nbsp;

### Legal risks of generative AI

| Risk | What it means |
|------|--------------|
| **IP infringement** | Model generates content too similar to copyrighted work |
| **Hallucinations** | Model states false information as fact |
| **Biased outputs** | Model produces discriminatory content |
| **Loss of customer trust** | Users stop trusting the product |
| **Privacy violations** | Model reveals personal information from training data |

&nbsp;

---

&nbsp;

## Part 2 — Domain 5: Security, Compliance & Governance (14%) `35 min`

&nbsp;

### Securing AI systems

```
┌──────────────────────────────────────────────────────┐
│  AI SECURITY LAYERS                                  │
│                                                      │
│  ┌────────────────────────────────────────────────┐  │
│  │  DATA SECURITY                                 │  │
│  │  • Encryption at rest (S3, KMS)                │  │
│  │  • Encryption in transit (TLS/SSL)             │  │
│  │  • Data access control (IAM)                   │  │
│  │  • PII detection (Amazon Macie)                │  │
│  └────────────────────────────────────────────────┘  │
│                                                      │
│  ┌────────────────────────────────────────────────┐  │
│  │  MODEL SECURITY                                │  │
│  │  • Access control to models (IAM roles)        │  │
│  │  • Prompt injection prevention (Guardrails)    │  │
│  │  • Private endpoints (VPC, PrivateLink)        │  │
│  └────────────────────────────────────────────────┘  │
│                                                      │
│  ┌────────────────────────────────────────────────┐  │
│  │  INFRASTRUCTURE SECURITY                       │  │
│  │  • Threat detection (Amazon Inspector)         │  │
│  │  • Activity logging (CloudTrail)               │  │
│  │  • Configuration compliance (AWS Config)       │  │
│  └────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────┘
```

&nbsp;

### AWS security services for AI — the exam cheat table

| Service | What it does | AI context |
|---------|-------------|-----------|
| **IAM** | Access control — who can do what | Control who can invoke models, access data |
| **AWS KMS** | Key management — encryption keys | Encrypt model data and training data |
| **Amazon Macie** | Detect PII in S3 | Find personal data before it enters training |
| **AWS PrivateLink** | Private network connections | Call Bedrock without going through public internet |
| **CloudTrail** | Activity logging | Track who invoked which model, when |
| **AWS Config** | Configuration compliance | Ensure AI resources follow rules |
| **Amazon Inspector** | Vulnerability scanning | Scan containers running models |
| **AWS Artifact** | Compliance reports | Access AWS compliance certifications |
| **AWS Audit Manager** | Audit automation | Generate audit reports for AI systems |
| **Secrets Manager** | Store API keys safely | Store model API keys, database passwords |

&nbsp;

### AWS Shared Responsibility Model for AI

```
┌──────────────────────────────────────────────────────┐
│                                                      │
│  AWS is responsible for:                             │
│  • Physical infrastructure security                  │
│  • Network infrastructure                            │
│  • Bedrock/SageMaker platform security              │
│                                                      │
│  ─────────────────────────────────────────────────   │
│                                                      │
│  YOU are responsible for:                            │
│  • Data security (encryption, access control)        │
│  • Model input/output filtering (Guardrails)        │
│  • Identity management (IAM policies)                │
│  • Compliance with regulations                       │
│  • Responsible AI practices                          │
└──────────────────────────────────────────────────────┘
```

&nbsp;

### Data governance the exam tests

| Concept | What it means |
|---------|--------------|
| **Data lineage** | Tracking where data came from and how it was transformed |
| **Data cataloging** | Organizing and documenting datasets |
| **Data lifecycle** | Collection → storage → use → archival → deletion |
| **Data retention** | How long to keep data and when to delete it |
| **Source citation** | Documenting data origins (SageMaker Model Cards) |

&nbsp;

### Compliance standards

| Standard | What it is |
|----------|-----------|
| **ISO 27001** | Information security management |
| **SOC 1/2/3** | Service organization controls — security audits |
| **GDPR** | EU data protection regulation |
| **HIPAA** | US healthcare data protection |

> **Exam tip:** You don't need to know the details of each standard. Know that AWS Config, AWS Audit Manager, and AWS Artifact help with compliance.

&nbsp;

---

&nbsp;

## Part 3 — Write Your Cheatsheet `15 min`

Create `cheatsheets/responsible-ai-security.md`:

```markdown
# Responsible AI & Security Cheatsheet

## Responsible AI Principles
- (list the 6 pillars in your own words)

## Types of Bias
| Bias | What it means |
|------|-------------|
| (fill in) | |

## AWS Tools for Responsible AI
| Tool | What it does |
|------|-------------|
| SageMaker Clarify | |
| SageMaker Model Monitor | |
| SageMaker Model Cards | |
| Bedrock Guardrails | |
| Amazon A2I | |

## Security Services for AI
| Service | What it does |
|---------|-------------|
| (fill in) | |

## Shared Responsibility
- AWS manages: ...
- You manage: ...
```

&nbsp;

---

&nbsp;

## Part 4 — Commit `5 min`

```bash
git add sprint-06-ai-exam-prep/ cheatsheets/
git commit -m "sprint 6 day 3: responsible AI, bias detection, security, compliance, governance"
git push
```

&nbsp;

---

&nbsp;

## ✅ Day 3 Checklist

| | Task |
|---|------|
| ☐ | Can name the 6 responsible AI principles |
| ☐ | Know 4 types of bias and where they enter the pipeline |
| ☐ | Can name AWS tools for bias detection (Clarify, Model Monitor) |
| ☐ | Understand transparent vs opaque models |
| ☐ | Know 8+ AWS security services and their AI use cases |
| ☐ | Understand the shared responsibility model for AI |
| ☐ | Know data governance concepts (lineage, lifecycle, cataloging) |
| ☐ | Cheatsheet written and pushed 🟩 |

&nbsp;

---

&nbsp;

## 🧠 Concepts You Now Own

| Concept | One-liner |
|---------|-----------|
| **SageMaker Clarify** | Detect bias in data and model predictions |
| **SageMaker Model Monitor** | Watch for drift and bias in production |
| **SageMaker Model Cards** | Document what a model does and how it was trained |
| **Bedrock Guardrails** | Filter harmful content, PII, off-topic responses |
| **Amazon Macie** | Find PII in S3 buckets |
| **Data lineage** | Track where data came from and how it changed |
| **Shared responsibility** | AWS secures infra, YOU secure data and access |
| **Selection bias** | Training data doesn't represent everyone |
| **Explainable AI** | Can you explain WHY the model decided something? |

&nbsp;

---

&nbsp;

> *Next: Mock Exam #1 — all 5 domains, just like the real thing. 💪*
