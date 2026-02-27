# Sprint 1 — Foundations

## 🏗️ Environment + Python + Containers

`4-6 days` · `1.5 hrs/day` · `No prior experience needed`

---

&nbsp;

## What This Sprint Is About

> Before you build a house, you set up the workbench.
> This sprint gets your tools installed, teaches you enough Python to be dangerous,
> and ends with you shipping a real API inside a container.

&nbsp;

### The Flow

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Day 1-2     │     │  Day 3-4     │     │  Day 5       │
│              │     │              │     │              │
│  Setup +     │────▶│  Python      │────▶│  Containers  │
│  Kubernetes  │     │  Essentials  │     │  + Ship It   │
│              │     │              │     │              │
│ • Git/GitHub │     │ • Variables  │     │ • Podman     │
│ • Python env │     │ • Loops/dicts│     │ • Dockerfile │
│ • Podman     │     │ • Functions  │     │ • Flask API  │
│ • kubectl    │     │ • JSON/APIs  │     │ • Port maps  │
│ • minikube   │     │ • try/except │     │ • 🚀 SHIP!  │
└──────────────┘     └──────────────┘     └──────────────┘
```

&nbsp;

---

&nbsp;

## Daily Breakdown

| Day | Focus | You'll Build | Guide |
|-----|-------|-------------|-------|
| 1 | Environment setup — Git, Python, Podman, kubectl, minikube | Dev environment + first commit | [Day 1](../week-01/day-01-mon.md) |
| 2 | Kubernetes deep dive — deploy, scale, self-heal | Nginx on K8s + YAML manifest | [Day 2](../week-01/day-02-tue.md) |
| 3 | Python crash course — variables, loops, functions | Pod health checker script | [Day 3](../week-01/day-03-wed.md) |
| 4 | Python continued — files, JSON, APIs | K8s pod status logger | [Day 4](../week-01/day-04-thu.md) |
| 5 | Podman deep dive + **Sprint 1 Project** | 🚀 Flask API in a container | [Day 5](../week-01/day-05-fri.md) |

&nbsp;

> **Flexible pacing:** Some days you'll fly through in 60 min. Some will take 2 hours.
> That's fine. Move on when you've checked the boxes, not when the calendar says so.

&nbsp;

---

&nbsp;

## ✅ Done When (Exit Criteria)

You're ready for Sprint 2 when ALL of these are true:

| | Criteria |
|---|---------|
| ☐ | Python 3.10+, Podman, kubectl, minikube all installed and working |
| ☐ | Can write a Python script with functions, loops, dicts, and JSON |
| ☐ | Can make an API call with `requests` and parse the response |
| ☐ | Understand what a Pod, Deployment, and Service are in K8s |
| ☐ | Deployed nginx on minikube and watched self-healing |
| ☐ | Built a custom container image with a Containerfile |
| ☐ | **Flask API runs in a container and responds to `curl`** |
| ☐ | Everything pushed to GitHub |

&nbsp;

> 🚦 **All boxes checked?** → Move to [Sprint 2](../sprint-02-kubernetes/sprint-02-overview.md)
>
> **Some boxes unchecked?** → That's fine. Spend one more session on the gaps. No rush.

&nbsp;

---

&nbsp;

## 📊 Sprint Retrospective

*Fill this in when you finish the sprint:*

| | |
|---|---|
| **Days it took:** | |
| **Hardest part:** | |
| **Biggest win:** | |
| **Would I change anything?** | |
| **Energy level (1-5):** | |
| **Confidence level (1-5):** | |

&nbsp;

---

&nbsp;

> *Next: [Sprint 2 — Kubernetes Deep Dive](../sprint-02-kubernetes/sprint-02-overview.md)*
> *You built a Flask API in a container. Now you deploy it on Kubernetes for real. 🔥*
