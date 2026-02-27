# Sprint 2 — Kubernetes Deep Dive

## ☸️ From "I deployed nginx" to "I understand K8s"

`4-6 days` · `1.5 hrs/day` · `Needs: Sprint 1 complete`

---

&nbsp;

## What This Sprint Is About

> You deployed an app on K8s in Sprint 1. Cool.
> But could you explain WHAT happened? Or debug it when it breaks?
> This sprint turns "I followed a tutorial" into "I actually get this."

&nbsp;

### The Flow

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Day 1       │     │  Day 2       │     │  Day 3       │     │  Day 4       │
│              │     │              │     │              │     │              │
│  Core K8s    │────▶│  Networking  │────▶│  Config &    │────▶│  PROJECT:    │
│  Objects     │     │  & Services  │     │  Security    │     │  Flask on    │
│              │     │              │     │              │     │  K8s 🚀      │
│ • Pods deep  │     │ • ClusterIP  │     │ • ConfigMaps │     │              │
│ • ReplicaSet │     │ • NodePort   │     │ • Secrets    │     │ • Deploy     │
│ • Deployment │     │ • LoadBal.   │     │ • RBAC       │     │ • Service    │
│ • Namespaces │     │ • DNS        │     │ • Limits     │     │ • Scale      │
│ • Labels     │     │ • Ingress    │     │ • NetPol     │     │ • Monitor    │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
```

&nbsp;

---

&nbsp;

## Daily Breakdown

| Day | Focus | You'll Build | Guide |
|-----|-------|-------------|-------|
| 1 | Core K8s objects — Pods, ReplicaSets, Deployments, Labels | Multi-label deployment | [Day 1](day-01.md) |
| 2 | Networking — Services, DNS, Ingress concepts | Service exposing your app | [Day 2](day-02.md) |
| 3 | Config & Security — ConfigMaps, Secrets, RBAC, resource limits | Secured app deployment | [Day 3](day-03.md) |
| 4 | **Sprint 2 Project:** Deploy your Flask API on K8s | 🚀 Full K8s deployment | [Day 4](day-04.md) |

&nbsp;

---

&nbsp;

## ✅ Done When (Exit Criteria)

| | Criteria |
|---|---------|
| ☐ | Can explain Pods → ReplicaSets → Deployments relationship |
| ☐ | Understand the 3 Service types and when to use each |
| ☐ | Created ConfigMaps and Secrets, used them in a pod |
| ☐ | Understand RBAC basics and resource limits |
| ☐ | **Flask API from Sprint 1 running on K8s with a Service** |
| ☐ | Everything pushed to GitHub |

&nbsp;

> 🚦 **All boxes checked?** → Move to [Sprint 3](../sprint-03-cloud-native/sprint-03-overview.md)

&nbsp;

---

&nbsp;

## 📊 Sprint Retrospective

| | |
|---|---|
| **Days it took:** | |
| **Hardest part:** | |
| **Biggest win:** | |
| **Confidence level (1-5):** | |

&nbsp;

---

&nbsp;

> *Next: [Sprint 3 — Cloud Native + Your First AI Project](../sprint-03-cloud-native/sprint-03-overview.md)*
