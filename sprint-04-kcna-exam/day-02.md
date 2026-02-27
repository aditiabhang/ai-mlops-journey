# Sprint 4 · Day 2

## ⚡ Domains 2-4 Speed Review — The Other 56%

`90 min` · `Concept review` · `Cover ground fast, mark what's fuzzy`

---

&nbsp;

## Today's Big Picture

> Domain 1 was deep. Today is wide.
> Three domains, one session. You've already learned all of this in Sprints 2-3.
> This is a speed review — confirm what you know, flag what you don't.

By the end of today, you'll have:

- ✅ Reviewed Container Orchestration concepts (28%)
- ✅ Reviewed Cloud Native App Delivery (16%)
- ✅ Reviewed Cloud Native Architecture (12%)
- ✅ A clear list of weak spots for Day 4 drilling

&nbsp;

---

&nbsp;

## Part 1 — Container Orchestration (28%) `30 min`

&nbsp;

### What this domain covers

```
┌─────────────────────────────────────────────────────┐
│  CONTAINER ORCHESTRATION (28%)                      │
│                                                     │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐       │
│  │ Runtimes  │  │ Networking│  │ Service   │       │
│  │           │  │           │  │ Mesh      │       │
│  │ containerd│  │ ClusterIP │  │ Istio     │       │
│  │ CRI-O    │  │ NodePort  │  │ Linkerd   │       │
│  │ Docker   │  │ LB        │  │ Sidecars  │       │
│  └───────────┘  └───────────┘  └───────────┘       │
│                                                     │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐       │
│  │ Security  │  │ Storage   │  │ Orch.     │       │
│  │           │  │           │  │ Platforms │       │
│  │ 4Cs       │  │ PV / PVC  │  │ K8s       │       │
│  │ RBAC      │  │ StorClass │  │ Nomad     │       │
│  │ PodSec    │  │ CSI       │  │ Swarm     │       │
│  └───────────┘  └───────────┘  └───────────┘       │
└─────────────────────────────────────────────────────┘
```

&nbsp;

### Self-quiz — cover the right column

| Topic | What to know |
|-------|-------------|
| **containerd** | Default K8s runtime — CNCF graduated — runs containers |
| **CRI-O** | Alternative runtime — lightweight, K8s-only |
| **CRI** | Container Runtime Interface — the standard runtimes implement |
| **ClusterIP** | Internal Service — pods talk to pods |
| **NodePort** | Opens port on node — external access |
| **LoadBalancer** | Real external IP — cloud only |
| **CNI** | Container Network Interface — plugins like Calico, Cilium, Flannel |
| **Istio** | Service mesh — feature-rich, sidecar-based |
| **Linkerd** | Service mesh — lightweight, simple |
| **Sidecar** | Helper container alongside your app (proxy for service mesh) |
| **mTLS** | Mutual TLS — encrypted traffic between services (service mesh feature) |
| **PersistentVolume** | Storage resource in the cluster |
| **PersistentVolumeClaim** | Pod's request for storage |
| **StorageClass** | Defines the "type" of storage (SSD, HDD, cloud provider) |
| **CSI** | Container Storage Interface — plugin standard for storage |
| **Docker Swarm** | Docker's orchestrator — simpler than K8s, less features |
| **Nomad** | HashiCorp's orchestrator — not just containers |

&nbsp;

---

&nbsp;

## Part 2 — Cloud Native App Delivery (16%) `20 min`

&nbsp;

### What this domain covers

```
┌─────────────────────────────────────────────────────┐
│  APP DELIVERY (16%)                                 │
│                                                     │
│  Deployment Strategies:                             │
│                                                     │
│  Rolling Update    Blue-Green       Canary          │
│  ┌──────────┐     ┌──────────┐    ┌──────────┐     │
│  │ Replace  │     │ Two envs │    │ Small %  │     │
│  │ pods one │     │ switch   │    │ of users │     │
│  │ by one   │     │ traffic  │    │ get new  │     │
│  │          │     │ at once  │    │ version  │     │
│  │ Default  │     │          │    │          │     │
│  │ in K8s   │     │ Zero     │    │ Gradual  │     │
│  │          │     │ downtime │    │ rollout  │     │
│  └──────────┘     └──────────┘    └──────────┘     │
│                                                     │
│  GitOps + CI/CD:                                    │
│  Argo CD · Flux · Tekton · GitHub Actions · Jenkins │
└─────────────────────────────────────────────────────┘
```

&nbsp;

### Self-quiz

| Topic | What to know |
|-------|-------------|
| **Rolling update** | Default K8s strategy — replace pods gradually |
| **Blue-green** | Two identical environments — switch traffic all at once |
| **Canary** | Send small % of traffic to new version — monitor — expand |
| **A/B testing** | Route by user attributes — for experiments |
| **GitOps** | Git is the source of truth — cluster syncs from Git |
| **Argo CD** | GitOps tool with web UI — CNCF graduated |
| **Flux** | GitOps tool — CLI-focused, lighter — CNCF graduated |
| **CI** | Continuous Integration — build + test automatically on every push |
| **CD** | Continuous Delivery — deploy automatically (or with approval) |
| **Tekton** | Kubernetes-native CI/CD — uses CRDs (Tasks, Pipelines) |
| **Helm** | Package manager for K8s — bundles YAML into reusable charts |
| **Kustomize** | YAML patching tool — built into kubectl |

&nbsp;

---

&nbsp;

## Part 3 — Cloud Native Architecture (12%) `20 min`

&nbsp;

### What this domain covers

```
┌─────────────────────────────────────────────────────┐
│  CLOUD NATIVE ARCHITECTURE (12%)                    │
│                                                     │
│  ┌───────────────┐  ┌───────────────┐               │
│  │ Autoscaling   │  │ Serverless    │               │
│  │               │  │               │               │
│  │ HPA (pods)    │  │ Knative       │               │
│  │ VPA (resources│  │ Scale to zero │               │
│  │ Cluster AS    │  │ Event-driven  │               │
│  └───────────────┘  └───────────────┘               │
│                                                     │
│  ┌───────────────┐  ┌───────────────┐               │
│  │ CNCF & Open   │  │ Roles &       │               │
│  │ Standards     │  │ Concepts      │               │
│  │               │  │               │               │
│  │ OCI           │  │ SRE           │               │
│  │ Sandbox →     │  │ SLI / SLO     │               │
│  │ Incubating → │  │ SLA           │               │
│  │ Graduated     │  │ Microservices │               │
│  └───────────────┘  └───────────────┘               │
└─────────────────────────────────────────────────────┘
```

&nbsp;

### Self-quiz

| Topic | What to know |
|-------|-------------|
| **HPA** | Horizontal Pod Autoscaler — adds/removes pods based on CPU/memory |
| **VPA** | Vertical Pod Autoscaler — adjusts resource requests/limits per pod |
| **Cluster Autoscaler** | Adds/removes nodes when pods can't be scheduled |
| **Knative** | Serverless on K8s — containers that scale to zero |
| **Scale to zero** | No traffic? No pods running. Saves money. |
| **CNCF Sandbox** | Early stage project — still experimental |
| **CNCF Incubating** | Growing — gaining adoption and maturity |
| **CNCF Graduated** | Production-ready — battle-tested (K8s, Prometheus, Envoy) |
| **OCI** | Open Container Initiative — the image/runtime standard |
| **Microservices** | Small, independent services that talk over APIs |
| **Monolith** | One big app — opposite of microservices |
| **SRE** | Site Reliability Engineering — ops with a software mindset |
| **SLI** | Service Level Indicator — the metric you measure (e.g., latency) |
| **SLO** | Service Level Objective — the target (e.g., 99.9% uptime) |
| **SLA** | Service Level Agreement — the contract with consequences |

&nbsp;

### Observability quick check (part of Architecture domain)

| Tool | What it does |
|------|-------------|
| **Prometheus** | Scrapes and stores metrics — CNCF graduated |
| **Grafana** | Dashboards — visualizes Prometheus data |
| **Fluentd** | Log collection and shipping — CNCF graduated |
| **Jaeger** | Distributed tracing — follow a request across services |
| **OpenTelemetry** | One standard for metrics + logs + traces |
| **Kubecost / OpenCost** | K8s cost monitoring and optimization |

&nbsp;

---

&nbsp;

## Part 4 — Gap Tracker `10 min`

Write down everything you were unsure about. Be specific.

Create `certifications/kcna-notes/weak-areas.md`:

```markdown
# KCNA Weak Areas

## Topics I need to review
- (list them here)

## Terms I keep confusing
- (list them here)

## Topics I feel confident about
- (list them here — so you know what NOT to waste time on)
```

&nbsp;

---

&nbsp;

## Part 5 — Commit `5 min`

```bash
git add sprint-04-kcna-exam/ certifications/
git commit -m "sprint 4 day 2: domains 2-4 speed review — orchestration, delivery, architecture"
git push
```

&nbsp;

---

&nbsp;

## ✅ Day 2 Checklist

| | Task |
|---|------|
| ☐ | Reviewed Container Orchestration — runtimes, networking, service mesh, storage |
| ☐ | Reviewed App Delivery — deployment strategies, GitOps, CI/CD |
| ☐ | Reviewed Architecture — autoscaling, serverless, CNCF, observability |
| ☐ | Created weak-areas.md with specific topics to drill |
| ☐ | Pushed to GitHub 🟩 |

&nbsp;

---

&nbsp;

> *Next: Mock Exam #1 — 60 questions, timed, just like the real thing. 💪*
