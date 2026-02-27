# Sprint 4 · Day 4

## 🔨 Weak Area Blitz — Turn Red to Green

`90 min` · `Targeted drilling` · `Only study what you got wrong`

---

&nbsp;

## Today's Big Picture

> Yesterday's mock exam told you exactly where you're weak.
> Today you fix those gaps. Nothing else. Don't re-study what you already know.
> Efficiency > effort.

By the end of today, you'll have:

- ✅ Re-studied every topic you got wrong on Mock #1
- ✅ Created flashcards for tricky terms
- ✅ Tested yourself again on the weak topics
- ✅ Feel ready for Mock Exam #2

&nbsp;

---

&nbsp;

## Part 1 — Open Your Weak Areas List `5 min`

Open `certifications/kcna-notes/weak-areas.md` from Day 2-3.

For each weak topic, follow this process:

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  1. READ     │     │  2. WRITE    │     │  3. QUIZ     │
│              │     │              │     │              │
│  Re-read the │────▶│  Write a     │────▶│  Close notes │
│  sprint day  │     │  1-sentence  │     │  and explain │
│  that covers │     │  flashcard   │     │  it out loud │
│  this topic  │     │  for it      │     │  in your own │
│              │     │              │     │  words       │
└──────────────┘     └──────────────┘     └──────────────┘

Can you explain it? ── Yes → ✅ Move on
                    └── No  → Read again, try a different source
```

&nbsp;

---

&nbsp;

## Part 2 — Common Tricky Topics `40 min`

These are the topics people most often get wrong on the KCNA. If any of these are on your weak list, spend extra time here.

&nbsp;

### 🔴 Most-missed: Service Mesh details

| Question Pattern | Answer |
|-----------------|--------|
| "What does a service mesh provide?" | mTLS, traffic management, observability, access control |
| "How does a sidecar work?" | Proxy container injected alongside your app — intercepts all traffic |
| "Istio vs Linkerd?" | Istio = feature-rich, complex. Linkerd = lightweight, simple. |
| "What is mTLS?" | Mutual TLS — both sides verify identity + encrypt traffic |

&nbsp;

### 🔴 Most-missed: Storage

| Question Pattern | Answer |
|-----------------|--------|
| "PV vs PVC?" | PV = the storage. PVC = the request for storage. Pods use PVCs. |
| "What is a StorageClass?" | Template for dynamic provisioning — defines the type of storage |
| "What is CSI?" | Container Storage Interface — plugin standard. Like CRI but for storage. |

&nbsp;

### 🔴 Most-missed: Deployment Strategies

| Question Pattern | Answer |
|-----------------|--------|
| "What's the default K8s deployment strategy?" | Rolling update |
| "Blue-green vs Canary?" | Blue-green = all-at-once switch. Canary = gradual % rollout. |
| "What does Helm do?" | Package manager for K8s — bundles YAML into reusable charts |
| "Helm vs Kustomize?" | Helm = templating + packaging. Kustomize = patching existing YAML. |

&nbsp;

### 🔴 Most-missed: CNCF & Architecture

| Question Pattern | Answer |
|-----------------|--------|
| "What is a CNCF graduated project?" | Production-ready, battle-tested (K8s, Prometheus, Envoy, Fluentd) |
| "SLI vs SLO vs SLA?" | SLI = metric. SLO = target. SLA = contract with penalties. |
| "What's the difference between HPA and VPA?" | HPA = more pods. VPA = bigger pods. |
| "What does 'scale to zero' mean?" | No traffic → no pods running → saves cost (Knative) |

&nbsp;

---

&nbsp;

## Part 3 — Flashcard Blitz `25 min`

&nbsp;

### Create 20 flashcards

Write them in `certifications/kcna-notes/flashcards.md` or use Anki if you have it.

Format:

```markdown
## KCNA Flashcards

**Q:** What container runtime does K8s use by default?
**A:** containerd

**Q:** What CNCF project handles distributed tracing?
**A:** Jaeger

**Q:** What's the difference between a Role and a ClusterRole?
**A:** Role = scoped to a namespace. ClusterRole = cluster-wide.

(add 17 more from YOUR weak areas)
```

&nbsp;

### Drill them

1. Read the question
2. Say the answer out loud BEFORE looking
3. Check
4. Got it right? → move on. Wrong? → star it and come back.

> Do 3 rounds. By round 3, you should get 18/20+.

&nbsp;

---

&nbsp;

## Part 4 — Commit `5 min`

```bash
git add sprint-04-kcna-exam/ certifications/
git commit -m "sprint 4 day 4: weak area blitz — flashcards, targeted review"
git push
```

&nbsp;

---

&nbsp;

## ✅ Day 4 Checklist

| | Task |
|---|------|
| ☐ | Re-read sprint materials for every weak topic |
| ☐ | Reviewed the common tricky topics above |
| ☐ | Created 20+ flashcards from weak areas |
| ☐ | Drilled flashcards — 3 rounds |
| ☐ | Can explain every weak topic in your own words |
| ☐ | Pushed to GitHub 🟩 |

&nbsp;

---

&nbsp;

## 💡 Exam Day Prep (for tomorrow)

Before you go to bed tonight, handle the logistics:

- [ ] **Book the exam** at [training.linuxfoundation.org](https://training.linuxfoundation.org/certification/kubernetes-cloud-native-associate/) if you haven't
- [ ] **Pick your time slot** — morning brain is usually sharpest
- [ ] **Check your setup** — webcam, mic, government ID, clean desk
- [ ] **Read the [candidate handbook](https://docs.linuxfoundation.org/tc-docs/certification/lf-handbook2)** for exam rules
- [ ] **Close all apps** except the exam browser on exam day

&nbsp;

---

&nbsp;

> *Next: Mock Exam #2 + EXAM DAY. You're ready. 🏆*
