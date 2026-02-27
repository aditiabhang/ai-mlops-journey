# Sprint 4 · Day 1

## ☸️ Domain 1 Review — Kubernetes Fundamentals (44%)

`90 min` · `No new concepts` · `This is a memory refresh, not a lesson`

---

&nbsp;

## Today's Big Picture

> Domain 1 is 44% of the exam. That's ~26 questions out of 60.
> If you ace this domain alone, you only need 19 more correct answers to pass.
> Today you review everything K8s and quiz yourself until it's automatic.

By the end of today, you'll have:

- ✅ Reviewed every K8s object you've learned
- ✅ Quizzed yourself on architecture components
- ✅ Reviewed scheduling, containers, and the K8s API
- ✅ Identified any gaps to drill later

&nbsp;

---

&nbsp;

## Part 1 — K8s Architecture Review `15 min`

&nbsp;

### Can you fill in these boxes from memory?

Try it FIRST, then check below.

```
┌─────────────────────────────────────────┐
│              CONTROL PLANE              │
│                                         │
│  ┌──────────┐  ┌────────────────────┐   │
│  │ ???????? │  │ ??????????         │   │
│  │ (front   │  │ "which node has    │   │
│  │  door)   │  │  room?"            │   │
│  └──────────┘  └────────────────────┘   │
│  ┌──────────┐  ┌────────────────────┐   │
│  │ ???????? │  │ ??????????         │   │
│  │ (database│  │ "are we running    │   │
│  │  of      │  │  what we should?"  │   │
│  │  truth)  │  │                    │   │
│  └──────────┘  └────────────────────┘   │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│              WORKER NODE                │
│                                         │
│  ┌──────────┐  ┌────────────────────┐   │
│  │ ???????? │  │ ??????????         │   │
│  │ (node    │  │ (runs containers)  │   │
│  │  agent)  │  │                    │   │
│  └──────────┘  └────────────────────┘   │
└─────────────────────────────────────────┘
```

&nbsp;

### Answers

| Component | Role |
|-----------|------|
| **kube-apiserver** | Front door — all communication goes through it |
| **kube-scheduler** | Decides which node a pod runs on |
| **etcd** | Key-value store — the database of truth for all cluster state |
| **kube-controller-manager** | Runs control loops — ensures desired state matches actual state |
| **kubelet** | Agent on each node — talks to API server, manages pods |
| **Container runtime** | Actually runs containers (containerd, CRI-O) |

> If you got 5/6 right → you're solid. 4 or fewer → re-read Sprint 1 Day 2 and Sprint 2 Day 1.

&nbsp;

---

&nbsp;

## Part 2 — K8s Resources Self-Quiz `20 min`

&nbsp;

### Flash quiz — cover the right column and test yourself

| Term | Definition |
|------|-----------|
| **Pod** | Smallest deployable unit — wraps one or more containers |
| **ReplicaSet** | Ensures a specified number of pod replicas are running |
| **Deployment** | Manages ReplicaSets — handles rolling updates and rollbacks |
| **Service** | Stable network endpoint for a set of pods |
| **ConfigMap** | Key-value config data — injected into pods as env vars or files |
| **Secret** | Like ConfigMap but for sensitive data — base64 encoded |
| **Namespace** | Virtual cluster — isolates resources within a cluster |
| **DaemonSet** | Runs one pod on EVERY node (monitoring agents, log collectors) |
| **StatefulSet** | Like Deployment but for stateful apps — stable names and storage |
| **Job** | Runs a pod to completion — then stops (batch processing) |
| **CronJob** | A Job on a schedule — "run this every hour" |
| **PersistentVolume (PV)** | A piece of storage provisioned in the cluster |
| **PersistentVolumeClaim (PVC)** | A request for storage — pods use PVCs, not PVs directly |
| **Ingress** | Routes external HTTP traffic to Services — "pretty URLs" |
| **NetworkPolicy** | Firewall rules between pods |
| **HPA** | Horizontal Pod Autoscaler — scales replicas based on metrics |

&nbsp;

### Score yourself

- 14-16 correct → 🟢 You're exam-ready for this section
- 10-13 correct → 🟡 Review the ones you missed
- Below 10 → 🔴 Re-read Sprint 2 day files before moving on

&nbsp;

---

&nbsp;

## Part 3 — Containers & Scheduling `15 min`

&nbsp;

### Container concepts the exam tests

| Concept | What to know |
|---------|-------------|
| **Container image** | Immutable blueprint — built from a Dockerfile/Containerfile |
| **Container** | Running instance of an image |
| **Layers** | Each Dockerfile instruction = a cached layer |
| **Registry** | Where images are stored (Docker Hub, ECR, GHCR) |
| **OCI** | Open Container Initiative — the standard all runtimes follow |
| **containerd** | The default container runtime in most K8s clusters |
| **CRI-O** | Alternative runtime — lighter, K8s-focused |

&nbsp;

### Scheduling concepts the exam tests

```
Pod needs to be scheduled:

  ┌────────────────────────────────────────┐
  │  kube-scheduler checks:               │
  │                                        │
  │  1. Resource requests — does any node  │
  │     have enough CPU/memory?            │
  │                                        │
  │  2. Node selectors — does the pod      │
  │     require a specific node label?     │
  │                                        │
  │  3. Taints & tolerations — is the      │
  │     node tainted? Does the pod         │
  │     tolerate it?                       │
  │                                        │
  │  4. Affinity rules — does the pod      │
  │     prefer or require certain nodes?   │
  └────────────────────────────────────────┘
```

| Concept | One-liner |
|---------|-----------|
| **Resource requests** | "I need at least this much" — used for scheduling decisions |
| **Resource limits** | "Don't let me use more than this" — enforced at runtime |
| **Node selector** | Simple: "only schedule me on nodes with label X" |
| **Taint** | A mark on a node: "don't schedule here unless you tolerate me" |
| **Toleration** | A pod's permission to run on a tainted node |
| **Affinity** | Advanced rules: "prefer nodes with label X" or "require it" |

&nbsp;

---

&nbsp;

## Part 4 — K8s API & kubectl `10 min`

&nbsp;

### What the exam expects you to know

| Concept | What to know |
|---------|-------------|
| **API Server** | All cluster communication goes through it — REST API |
| **kubectl** | CLI that talks to the API server |
| **YAML manifests** | Declarative — "make reality match this file" |
| **`kubectl apply`** | Create or update resources from YAML |
| **`kubectl get`** | List resources |
| **`kubectl describe`** | Detailed info + events |
| **`kubectl logs`** | Container output |
| **`kubectl delete`** | Remove resources |
| **Custom Resource Definitions (CRDs)** | Extend K8s with your own resource types |

> **CRDs** are a common exam question. Know that they let you add custom objects to K8s — operators use them heavily. Example: a `Database` CRD that automatically provisions a Postgres instance.

&nbsp;

---

&nbsp;

## Part 5 — Security Basics `10 min`

&nbsp;

### The 4Cs of Cloud Native Security

```
┌──────────────────────────────────────┐
│  Cloud                               │
│  ┌──────────────────────────────┐    │
│  │  Cluster                     │    │
│  │  ┌──────────────────────┐    │    │
│  │  │  Container            │    │    │
│  │  │  ┌──────────────┐    │    │    │
│  │  │  │  Code         │    │    │    │
│  │  │  └──────────────┘    │    │    │
│  │  └──────────────────────┘    │    │
│  └──────────────────────────────┘    │
└──────────────────────────────────────┘
```

| Layer | Examples |
|-------|---------|
| **Cloud** | IAM, network security, encryption |
| **Cluster** | RBAC, Network Policies, Pod Security |
| **Container** | Minimal base images, no root, scan for vulnerabilities |
| **Code** | Input validation, dependency scanning, secrets management |

&nbsp;

### RBAC quick review

| Object | What it does |
|--------|-------------|
| **Role** | Permissions within a namespace ("can GET pods in default") |
| **ClusterRole** | Permissions cluster-wide |
| **RoleBinding** | Connects a user/SA to a Role |
| **ClusterRoleBinding** | Connects a user/SA to a ClusterRole |

&nbsp;

---

&nbsp;

## Part 6 — Commit `5 min`

Write down which sections you felt shaky on. You'll drill those on Day 4.

```bash
git add sprint-04-kcna-exam/
git commit -m "sprint 4 day 1: k8s fundamentals review — architecture, resources, scheduling"
git push
```

&nbsp;

---

&nbsp;

## ✅ Day 1 Checklist

| | Task |
|---|------|
| ☐ | Can draw the K8s architecture from memory |
| ☐ | Scored 14+ on the resources self-quiz |
| ☐ | Know container runtimes (containerd, CRI-O) and OCI |
| ☐ | Understand scheduling: requests, limits, taints, affinity |
| ☐ | Know the 4Cs of security and RBAC objects |
| ☐ | Wrote down weak areas for Day 4 drilling |
| ☐ | Pushed to GitHub 🟩 |

&nbsp;

---

&nbsp;

> *Next: Domains 2-4 speed review — Orchestration, App Delivery, Architecture. 🚀*
