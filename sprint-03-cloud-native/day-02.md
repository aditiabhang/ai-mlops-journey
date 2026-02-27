# Sprint 3 · Day 2

## 📊 Observability + GitOps — See Everything, Deploy from Git

`90 min` · `Concept day with light demos` · `KCNA exam loves this stuff`

---

&nbsp;

## Today's Big Picture

> Something breaks at 3 AM. How do you know? How do you fix it?
> Observability = knowing what's happening. GitOps = deploying safely.
> These are the two topics that show up the most on the KCNA exam after Kubernetes itself.

By the end of today, you'll have:

- ✅ Understand the 3 pillars of observability (metrics, logs, traces)
- ✅ Know what Prometheus, Grafana, Fluentd, and Jaeger do
- ✅ Understand OpenTelemetry (the standard that unifies them)
- ✅ Know what GitOps is and how Argo CD / Flux work
- ✅ Written an observability cheatsheet

&nbsp;

---

&nbsp;

## Part 1 — The 3 Pillars of Observability `20 min`

&nbsp;

### Why observability? (30-second version)

Monitoring tells you "something is broken." Observability tells you "here's WHY it's broken." In a world of microservices, you can't SSH into one server and check logs. You need systems that collect everything automatically.

```
┌───────────────────────────────────────────────┐
│           THE 3 PILLARS                       │
│                                               │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐ │
│  │  METRICS  │  │   LOGS    │  │  TRACES   │ │
│  │           │  │           │  │           │ │
│  │ Numbers   │  │ Text      │  │ Journey   │ │
│  │ over time │  │ events    │  │ of a      │ │
│  │           │  │           │  │ request   │ │
│  │ "CPU is   │  │ "Error:   │  │ "Request  │ │
│  │  at 95%"  │  │  timeout" │  │  hit A→B  │ │
│  │           │  │           │  │  →C→fail" │ │
│  │ Tool:     │  │ Tool:     │  │ Tool:     │ │
│  │ Prometheus│  │ Fluentd   │  │ Jaeger    │ │
│  │ + Grafana │  │ + EFK     │  │ + Zipkin  │ │
│  └───────────┘  └───────────┘  └───────────┘ │
└───────────────────────────────────────────────┘
```

&nbsp;

### Metrics — Prometheus + Grafana

| Tool | What it does |
|------|-------------|
| **Prometheus** | Scrapes metrics from your apps every 15s. Stores them. Alerts you. |
| **Grafana** | Turns those numbers into beautiful dashboards |

```
Your App ──scrape──▶ Prometheus ──query──▶ Grafana Dashboard
  /metrics endpoint    stores data          visualizes it
```

> Your app exposes a `/metrics` endpoint. Prometheus pulls (scrapes) from it. Grafana shows graphs. That's the whole stack.

&nbsp;

### Logs — Fluentd + EFK Stack

| Tool | What it does |
|------|-------------|
| **Fluentd** | Collects logs from all pods and ships them somewhere |
| **Elasticsearch** | Stores and indexes logs (searchable) |
| **Kibana** | UI to search and visualize logs |

> EFK = Elasticsearch + Fluentd + Kibana. Sometimes you see ELK (Logstash instead of Fluentd).

&nbsp;

### Traces — Jaeger

Traces show you the journey of a single request across multiple services.

```
User request → API Gateway (50ms) → Auth Service (20ms) → Database (500ms) ← SLOW!
```

> Without traces, you'd just see "the request took 600ms" with no idea where the time went.

&nbsp;

### OpenTelemetry — The Unifier

OpenTelemetry (OTel) is the standard that lets you collect metrics, logs, AND traces with one library. Instead of using 3 different tools, you instrument your app once with OTel and send data wherever you want.

&nbsp;

---

&nbsp;

## Part 2 — GitOps `25 min`

&nbsp;

### What is GitOps? (30-second version)

Git is the single source of truth. You change a YAML file in Git → the cluster automatically updates to match. No `kubectl apply` by hand. No SSH-ing into servers.

```
Traditional Deployment:
  Developer → build → push image → SSH → kubectl apply → pray 🙏

GitOps Deployment:
  Developer → git push → Argo CD notices → auto-applies to cluster ✅
```

&nbsp;

### The GitOps Principles

1. **Declarative** — everything described in YAML/Git
2. **Versioned** — Git history IS your deployment history
3. **Automated** — changes applied automatically
4. **Self-healing** — drift detected and corrected

&nbsp;

### Argo CD vs Flux

| | Argo CD | Flux |
|--|---------|------|
| **UI** | Beautiful web UI | CLI-focused |
| **Learning curve** | Medium | Easier |
| **CNCF status** | Graduated | Graduated |
| **Best for** | Teams that want a dashboard | Teams that prefer CLI |

```
Git Repo                    Argo CD / Flux              K8s Cluster
┌──────────┐   watches     ┌──────────────┐   applies  ┌──────────┐
│ YAML     │──────────────▶│ Compares Git │──────────▶│ Running  │
│ manifests│               │ vs Cluster   │            │ state    │
└──────────┘               └──────────────┘            └──────────┘
                           "Git says 3 replicas,
                            cluster has 2 → fix it!"
```

&nbsp;

---

&nbsp;

## Part 3 — CI/CD in Cloud Native `15 min`

&nbsp;

### CI vs CD (30-second version)

| | CI | CD |
|--|----|----|
| **Stands for** | Continuous Integration | Continuous Delivery/Deployment |
| **What it does** | Build + test code automatically | Deploy to production automatically |
| **Tools** | GitHub Actions, Jenkins, Tekton | Argo CD, Flux, Spinnaker |

```
Code push → CI (build + test) → CD (deploy) → Production
             GitHub Actions       Argo CD       K8s Cluster
```

&nbsp;

---

&nbsp;

## Part 4 — Write Your Cheatsheet & Commit `15 min`

Create `cheatsheets/observability-gitops.md` with:
- The 3 pillars and which tool handles each
- GitOps principles
- Argo CD vs Flux quick comparison

```bash
git add cheatsheets/ sprint-03-cloud-native/
git commit -m "sprint 3 day 2: observability pillars, GitOps, Argo CD, Flux"
git push
```

&nbsp;

---

&nbsp;

## ✅ Day 2 Checklist

| | Task |
|---|------|
| ☐ | Can name the 3 pillars of observability |
| ☐ | Know what Prometheus, Grafana, Fluentd, Jaeger do |
| ☐ | Understand OpenTelemetry's role |
| ☐ | Can explain GitOps principles |
| ☐ | Know the difference between Argo CD and Flux |
| ☐ | Cheatsheet written and pushed 🟩 |

&nbsp;

---

&nbsp;

## 🧠 Concepts You Now Own

| Concept | One-liner |
|---------|-----------|
| **Metrics** | Numbers over time — CPU, memory, request count |
| **Logs** | Text events — errors, warnings, info messages |
| **Traces** | The journey of one request across services |
| **Prometheus** | Scrapes and stores metrics |
| **Grafana** | Dashboards for metrics |
| **Fluentd** | Collects and ships logs |
| **Jaeger** | Distributed tracing |
| **OpenTelemetry** | One standard for metrics + logs + traces |
| **GitOps** | Git is the source of truth — cluster syncs from Git |
| **Argo CD** | GitOps tool with a web UI |
| **Flux** | GitOps tool, CLI-focused, lightweight |

&nbsp;

---

&nbsp;

> *Next: 🤖 You install Ollama and talk to an LLM on your own laptop. The AI part begins! 🔥*
