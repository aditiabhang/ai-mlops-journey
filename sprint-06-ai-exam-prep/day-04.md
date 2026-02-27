# Sprint 6 · Day 4

## 📝 Mock Exam #1 + Weak Area Drilling

`90 min` · `All 5 domains` · `Find your gaps, fill them`

---

&nbsp;

## Today's Big Picture

> You've covered all 5 domains. Time to test yourself.
> Mock exam, score it, drill the weak spots.
> Same process that worked for KCNA works here.

By the end of today, you'll have:

- ✅ Taken a full AIF-C01 mock exam
- ✅ Scored yourself by domain
- ✅ Drilled weak areas with targeted review
- ✅ Created flashcards for tricky topics

&nbsp;

---

&nbsp;

## Part 1 — Take the Mock Exam `50 min`

&nbsp;

### Where to take it

| Resource | Notes |
|----------|-------|
| **[AWS Skill Builder — Official Practice Questions](https://explore.skillbuilder.aws/learn/course/external/view/elearning/19790/exam-prep-official-practice-question-set-aws-certified-ai-practitioner-aif-c01-english)** | Free — official AWS questions ✅ |
| **[AWS Skill Builder — Official Practice Exam](https://explore.skillbuilder.aws/learn/public/learning_plan/view/2193/standard-exam-prep-plan-aws-certified-ai-practitioner-aif-c01)** | Free learning plan with practice exam |
| **Udemy AIF-C01 Practice Tests** | Paid but thorough |

&nbsp;

### Rules

```
┌──────────────────────────────────────────┐
│  MOCK EXAM RULES                         │
│                                          │
│  ✅ 65 questions                         │
│  ✅ 90 minute timer                      │
│  ✅ No notes or Google                   │
│  ✅ Mark unsure questions, move on       │
│  ✅ Answer EVERY question (no penalty)   │
│  ❌ Don't check answers during the exam  │
└──────────────────────────────────────────┘
```

Go take the exam now. Come back when you're done.

&nbsp;

---

&nbsp;

## Part 2 — Score & Analyze `15 min`

&nbsp;

### Record your score

```
My score: ______ / 65  =  ______%

Passing score: ~70% (700/1000)
```

&nbsp;

### Score by domain

| Domain | Weight | My Score | Status |
|--------|--------|----------|--------|
| Fundamentals of AI/ML | 20% | ___% | 🟢 🟡 🔴 |
| Fundamentals of GenAI | 24% | ___% | 🟢 🟡 🔴 |
| Applications of Foundation Models | 28% | ___% | 🟢 🟡 🔴 |
| Responsible AI | 14% | ___% | 🟢 🟡 🔴 |
| Security & Compliance | 14% | ___% | 🟢 🟡 🔴 |

&nbsp;

### What to do with your score

```
┌─────────────────────────────────────────────┐
│                                             │
│  75%+ → 🟢 Strong. Light review tomorrow,  │
│           then sit the exam.                │
│                                             │
│  65-74% → 🟡 Close. Drill weak domains     │
│            below, then Mock #2 tomorrow.    │
│                                             │
│  Below 65% → 🔴 Needs work. Spend today    │
│               AND an extra day drilling.    │
│               Re-read the sprint days for   │
│               your weakest domains.         │
│                                             │
└─────────────────────────────────────────────┘
```

&nbsp;

---

&nbsp;

## Part 3 — Drill Weak Areas `20 min`

&nbsp;

### Most-missed topics on the AIF-C01

Review any of these you got wrong:

&nbsp;

**🔴 Domain 1 — Common traps**

| Question pattern | Key answer |
|-----------------|-----------|
| "Supervised vs unsupervised?" | Supervised = labeled data. Unsupervised = unlabeled. |
| "Which AWS service for [NLP task]?" | Comprehend = text analysis. Lex = chatbot. Transcribe = speech-to-text. |
| "What is feature engineering?" | Transforming raw data into useful model inputs |
| "Overfitting vs underfitting?" | Overfit = memorizes data. Underfit = too simple to learn. |

&nbsp;

**🔴 Domain 2 — Common traps**

| Question pattern | Key answer |
|-----------------|-----------|
| "What does temperature control?" | Randomness. Low = focused. High = creative. |
| "Bedrock vs SageMaker?" | Bedrock = use existing models. SageMaker = build custom. |
| "What is a token?" | Piece of a word (~4 chars). Pricing is per token. |
| "PartyRock vs Bedrock?" | PartyRock = no-code playground. Bedrock = production API. |

&nbsp;

**🔴 Domain 3 — Common traps (highest weight!)**

| Question pattern | Key answer |
|-----------------|-----------|
| "RAG vs fine-tuning?" | RAG = current data, cheaper. Fine-tuning = specialized language, expensive. |
| "Best for Q&A over internal docs?" | RAG with Bedrock Knowledge Bases |
| "ROUGE vs BLEU?" | ROUGE = summarization. BLEU = translation. |
| "How to prevent prompt injection?" | Bedrock Guardrails + input validation |
| "Inference parameter for factual responses?" | Low temperature (0.1-0.3) |

&nbsp;

**🔴 Domains 4 & 5 — Common traps**

| Question pattern | Key answer |
|-----------------|-----------|
| "Detect bias in a model?" | SageMaker Clarify |
| "Monitor model in production?" | SageMaker Model Monitor |
| "Filter harmful AI output?" | Bedrock Guardrails |
| "Find PII in S3?" | Amazon Macie |
| "Track who invoked a model?" | CloudTrail |
| "Document a model's purpose?" | SageMaker Model Cards |

&nbsp;

---

&nbsp;

## Part 4 — Flashcards `10 min`

Create `certifications/aws-ai-notes/flashcards.md`:

Write 20 flashcards from YOUR wrong answers. Format:

```markdown
# AIF-C01 Flashcards

**Q:** What's the difference between RAG and fine-tuning?
**A:** RAG retrieves docs at query time (always current, cheaper).
Fine-tuning retrains weights (specialized language, expensive, frozen).

**Q:** Which metric measures summarization quality?
**A:** ROUGE

(add 18 more from your weak areas)
```

&nbsp;

---

&nbsp;

## Part 5 — Commit `5 min`

```bash
git add sprint-06-ai-exam-prep/ certifications/
git commit -m "sprint 6 day 4: mock exam 1 — score ___%, weak area drilling"
git push
```

&nbsp;

---

&nbsp;

## ✅ Day 4 Checklist

| | Task |
|---|------|
| ☐ | Took full 65-question mock exam |
| ☐ | Scored and recorded results by domain |
| ☐ | Reviewed every wrong answer |
| ☐ | Drilled common trap questions above |
| ☐ | Created 20 flashcards from weak areas |
| ☐ | Pushed to GitHub 🟩 |

&nbsp;

---

&nbsp;

## 💡 Exam Day Prep (for tomorrow)

- [ ] **Book the exam** at [aws.training](https://www.aws.training/certification?p=cert&c=ai&z=1) if you haven't
- [ ] **Pick your time slot** — morning brain is usually sharpest
- [ ] **Check your setup** — webcam, mic, government ID, clean desk
- [ ] **Review the [exam guide](https://d1.awsstatic.com/training-and-certification/docs-ai-practitioner/AWS-Certified-AI-Practitioner_Exam-Guide.pdf)** one more time

&nbsp;

---

&nbsp;

> *Next: Mock Exam #2 + EXAM DAY. Two certs in your pocket by tomorrow. 🏆🏆*
