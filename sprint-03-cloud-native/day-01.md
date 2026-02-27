# Sprint 3 · Day 1

## ☁️ The Cloud Native Landscape — What All Those Logos Mean

`90 min` · `No hands-on lab today` · `Concept day — but it's fascinating`

---

&nbsp;

## Today's Big Picture

> Open [landscape.cncf.io](https://landscape.cncf.io) and you'll see 1,000+ logos.
> Terrifying? Yes. But you only need to know ~15 of them for the KCNA exam.
> Today you learn the categories and the big names in each.

By the end of today, you'll have:

- ✅ Understand what CNCF is and why it matters
- ✅ Know the major categories of cloud native tools
- ✅ Can name key projects in each category
- ✅ Understand service mesh and serverless at a concept level
- ✅ Written a CNCF cheatsheet for exam prep

&nbsp;

---

&nbsp;

## Part 1 — What is CNCF? `10 min`

&nbsp;

### 30-second version

The **Cloud Native Computing Foundation** is the organization that manages open-source cloud native projects. They're part of the Linux Foundation. When they "graduate" a project, it means it's battle-tested and production-ready.

```
Project Maturity Levels:

  Sandbox  ──▶  Incubating  ──▶  Graduated
  "new idea"    "growing up"     "production ready"
  
  Examples:                      Examples:
  • OpenKruise                   • Kubernetes
  • Backstage                    • Prometheus
                                 • Envoy
                                 • containerd
```

&nbsp;

---

&nbsp;

## Part 2 — The Landscape Categories `30 min`

&nbsp;

### The categories that matter for KCNA

```
┌─────────────────────────────────────────────────────┐
│              CLOUD NATIVE LANDSCAPE                 │
│                                                     │
│  ┌─────────────┐  ┌─────────────┐  ┌────────────┐  │
│  │ Container   │  │ Orchestration│ │ Service    │  │
│  │ Runtime     │  │ & Scheduling │ │ Mesh       │  │
│  │             │  │              │ │            │  │
│  │ containerd  │  │ Kubernetes   │ │ Istio      │  │
│  │ CRI-O      │  │ Nomad        │ │ Linkerd    │  │
│  └─────────────┘  └─────────────┘  └────────────┘  │
│                                                     │
│  ┌─────────────┐  ┌─────────────┐  ┌────────────┐  │
│  │ Observ-     │  │ CI/CD &     │  │ Networking │  │
│  │ ability     │  │ GitOps      │  │            │  │
│  │             │  │             │  │            │  │
│  │ Prometheus  │  │ Argo CD     │  │ Envoy      │  │
│  │ Grafana     │  │ Flux        │  │ CoreDNS    │  │
│  │ Jaeger      │  │ Tekton      │  │ Cilium     │  │
│  └─────────────┘  └─────────────┘  └────────────┘  │
│                                                     │
│  ┌─────────────┐  ┌─────────────┐  ┌────────────┐  │
│  │ Storage     │  │ Security    │  │ Serverless │  │
│  │             │  │             │  │            │  │
│  │ Rook        │  │ Falco       │  │ Knative    │  │
│  │ Longhorn    │  │ OPA         │  │ OpenFaaS   │  │
│  └─────────────┘  └─────────────┘  └────────────┘  │
└─────────────────────────────────────────────────────┘
```

&nbsp;

### The key projects — what each one does

| Project | Category | One-liner |
|---------|----------|-----------|
| **Kubernetes** | Orchestration | Runs and manages containers at scale |
| **containerd** | Runtime | Actually runs containers (used by K8s) |
| **Prometheus** | Observability | Collects metrics from everything |
| **Grafana** | Observability | Dashboards — makes metrics visual |
| **Jaeger** | Observability | Distributed tracing — follow a request |
| **Fluentd** | Logging | Collects and ships logs |
| **Envoy** | Networking | Smart proxy — used by service meshes |
| **CoreDNS** | Networking | DNS for K8s — how services find each other |
| **Istio** | Service Mesh | Traffic management between services |
| **Linkerd** | Service Mesh | Lightweight service mesh alternative |
| **Argo CD** | GitOps | Deploys apps from Git automatically |
| **Flux** | GitOps | Another GitOps tool — lighter weight |
| **Helm** | Package Mgmt | "apt-get for K8s" — packages YAML into charts |
| **Falco** | Security | Runtime threat detection |
| **OPA** | Security | Policy engine — "is this allowed?" |
| **Knative** | Serverless | Run containers that scale to zero |

&nbsp;

---

&nbsp;

## Part 3 — Service Mesh (Concept) `15 min`

&nbsp;

### What is a Service Mesh? (30-second version)

When you have 50 microservices all talking to each other, things get messy. Who's calling who? What if one service is slow? How do you encrypt traffic between them?

A service mesh adds a tiny proxy (sidecar) next to every pod. The proxy handles traffic routing, encryption, retries, and observability — so your app code doesn't have to.

```
WITHOUT Service Mesh:          WITH Service Mesh:

  App A ──────▶ App B          App A ──▶ Proxy ──▶ Proxy ──▶ App B
  (direct, no visibility)       │         │
                                └── mTLS encryption
                                └── retry logic
                                └── metrics collection
```

> For KCNA: know Istio (feature-rich, complex) vs Linkerd (lightweight, simple). Know that sidecars are the pattern.

&nbsp;

---

&nbsp;

## Part 4 — Serverless (Concept) `10 min`

&nbsp;

### What is Serverless? (30-second version)

"Serverless" doesn't mean no servers. It means you don't manage them. You write a function, upload it, and it runs when triggered. No containers to manage, no scaling to configure.

```
Traditional:     You build image → deploy to K8s → manage scaling
Serverless:      You write function → upload → it runs when needed → scales to zero when idle
```

| Term | Meaning |
|------|---------|
| **Knative** | Serverless on K8s — containers that scale to zero |
| **AWS Lambda** | Serverless functions — no containers at all |
| **Scale to zero** | When nobody's using it, it shuts down (saves money) |

&nbsp;

---

&nbsp;

## Part 5 — OCI Standard `10 min`

&nbsp;

### What is OCI? (30-second version)

**Open Container Initiative** — the standard that says "this is what a container image looks like." It's why Podman, Docker, containerd, and CRI-O can all run the same images. One standard, many tools.

&nbsp;

---

&nbsp;

## Part 6 — Write Your Cheatsheet & Commit `15 min`

Create `cheatsheets/cncf-landscape.md` with everything you learned today. Use the table above as a starting point, add your own notes.

```bash
git add cheatsheets/ sprint-03-cloud-native/
git commit -m "sprint 3 day 1: CNCF landscape, service mesh, serverless concepts"
git push
```

&nbsp;

---

&nbsp;

## ✅ Day 1 Checklist

| | Task |
|---|------|
| ☐ | Can explain what CNCF is and project maturity levels |
| ☐ | Can name 10+ CNCF projects and their categories |
| ☐ | Understand service mesh concept (sidecars, Istio vs Linkerd) |
| ☐ | Understand serverless concept (scale to zero, Knative) |
| ☐ | Know what OCI is |
| ☐ | CNCF cheatsheet written and pushed 🟩 |

&nbsp;

---

&nbsp;

## 🧠 Concepts You Now Own

| Concept | One-liner |
|---------|-----------|
| **CNCF** | Organization that manages cloud native open-source projects |
| **Graduated project** | Battle-tested, production-ready (K8s, Prometheus, Envoy) |
| **Service Mesh** | Proxy sidecars that handle traffic between microservices |
| **Sidecar** | A helper container next to your app container |
| **Serverless** | Write code, don't manage infrastructure, scale to zero |
| **OCI** | The standard that makes all container tools compatible |
| **Helm** | Package manager for K8s — bundles YAML into reusable charts |

&nbsp;

---

&nbsp;

> *Next: Observability + GitOps — the two concepts the KCNA exam loves to test. 📊*
