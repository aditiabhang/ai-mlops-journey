# Sprint 2 · Day 1

## ☸️ Core K8s Objects — The Building Blocks

`90 min` · `Needs: minikube, kubectl` · `You'll actually understand K8s after this`

---

&nbsp;

## Today's Big Picture

> In Sprint 1 you ran `kubectl create deployment` and magic happened.
> Today you open the hood and see every piece that makes it work.

By the end of today, you'll have:

- ✅ Understand how Pods, ReplicaSets, and Deployments connect
- ✅ Used Labels and Selectors to organize resources
- ✅ Created Namespaces to separate environments
- ✅ Debugged a broken deployment using `describe` and `logs`

&nbsp;

---

&nbsp;

## Part 1 — The K8s Object Hierarchy `15 min`

&nbsp;

### How the pieces fit together

```
You create this:
┌─────────────────────────────────────┐
│           DEPLOYMENT                │
│  "I want 3 copies of my app"       │
│                                     │
│  ┌─────────────────────────────┐   │
│  │       REPLICASET            │   │
│  │  "I'll make sure there      │   │
│  │   are exactly 3 pods"       │   │
│  │                             │   │
│  │  ┌─────┐ ┌─────┐ ┌─────┐  │   │
│  │  │ POD │ │ POD │ │ POD │  │   │
│  │  │  🍕 │ │  🍕 │ │  🍕 │  │   │
│  │  └─────┘ └─────┘ └─────┘  │   │
│  └─────────────────────────────┘   │
└─────────────────────────────────────┘
```

- **You** talk to the **Deployment**
- The Deployment creates a **ReplicaSet**
- The ReplicaSet creates the **Pods**
- You almost never touch ReplicaSets or Pods directly

> Think of it like a restaurant chain: You (CEO) tell the regional manager (Deployment) "I want 3 stores." The manager hires a supervisor (ReplicaSet) who opens 3 stores (Pods).

&nbsp;

---

&nbsp;

## Part 2 — Labels & Selectors `15 min`

&nbsp;

### What are Labels? (30-second version)

Labels are sticky notes you put on K8s objects. They don't do anything by themselves — but everything else uses them to find things. Services find Pods by label. ReplicaSets track Pods by label. Without labels, K8s is blind.

```
┌─────────────────────────────┐
│  Pod: nginx-abc123          │
│                             │
│  Labels:                    │
│    app: my-web       ◀──── Service uses this to route traffic
│    env: production   ◀──── You use this to filter
│    tier: frontend    ◀──── You use this to organize
└─────────────────────────────┘
```

&nbsp;

### Do This

**1 →** Start minikube

```bash
minikube start
```

&nbsp;

**2 →** Create a deployment with labels

```bash
kubectl create deployment labeled-app --image=nginx
kubectl label deployment labeled-app env=dev tier=frontend
```

&nbsp;

**3 →** Find things by label

```bash
kubectl get pods --show-labels
kubectl get pods -l app=labeled-app
kubectl get all -l env=dev
```

> Labels are how K8s connects the dots. Service → finds Pods with matching labels. Deployment → manages Pods with matching labels. Everything talks through labels.

&nbsp;

---

&nbsp;

## Part 3 — Namespaces `15 min`

&nbsp;

### What are Namespaces? (30-second version)

Folders for your K8s stuff. Want to keep dev separate from prod? Different namespace. Want each team to have their own space? Different namespace.

```
┌── Cluster ──────────────────────────────┐
│                                         │
│  ┌─ default ──────┐  ┌─ production ──┐  │
│  │ my test pods   │  │ real apps     │  │
│  │ experiments    │  │ databases     │  │
│  └────────────────┘  └───────────────┘  │
│                                         │
│  ┌─ kube-system ──┐  ┌─ monitoring ──┐  │
│  │ K8s itself     │  │ prometheus    │  │
│  │ DNS, etc.      │  │ grafana       │  │
│  └────────────────┘  └───────────────┘  │
└─────────────────────────────────────────┘
```

&nbsp;

### Do This

**1 →** See existing namespaces

```bash
kubectl get namespaces
```

&nbsp;

**2 →** Create your own

```bash
kubectl create namespace dev
kubectl create namespace staging
```

&nbsp;

**3 →** Deploy something in a specific namespace

```bash
kubectl create deployment ns-test --image=nginx -n dev
kubectl get pods -n dev
kubectl get pods -n staging
```

> Pods in `dev` and `staging` can't see each other by default. Isolation for free.

&nbsp;

**4 →** Clean up

```bash
kubectl delete namespace dev staging
```

&nbsp;

---

&nbsp;

## Part 4 — Debugging Like a Pro `20 min`

&nbsp;

### The 3 commands that solve 90% of K8s problems

```
┌──────────────────────┐
│  Something broken?   │
└──────────┬───────────┘
           │
     ┌─────▼─────┐     "What's running?"
     │ kubectl    │
     │ get pods   │
     └─────┬─────┘
           │
     ┌─────▼──────────┐  "What happened to it?"
     │ kubectl         │
     │ describe pod X  │
     └─────┬──────────┘
           │
     ┌─────▼──────────┐  "What did it say?"
     │ kubectl         │
     │ logs X          │
     └────────────────┘
```

&nbsp;

### Do This — Break something on purpose

**1 →** Deploy a broken image

```bash
kubectl create deployment broken --image=nginx:doesnotexist
```

&nbsp;

**2 →** Watch it fail

```bash
kubectl get pods
```

> You'll see `ErrImagePull` or `ImagePullBackOff`. That's K8s saying "I can't find that image."

&nbsp;

**3 →** Debug it

```bash
kubectl describe pod <paste-broken-pod-name>
```

> Scroll to the **Events** section at the bottom. It tells you exactly what went wrong.

&nbsp;

**4 →** Check logs (for pods that started but crashed)

```bash
kubectl logs <pod-name>
```

&nbsp;

**5 →** Fix and clean up

```bash
kubectl delete deployment broken
```

&nbsp;

---

&nbsp;

## Part 5 — YAML Deep Dive `15 min`

&nbsp;

### Do This

**1 →** Create `sprint-02-kubernetes/multi-app.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-frontend
  labels:
    app: web
    tier: frontend
spec:
  replicas: 2
  selector:
    matchLabels:
      app: web
      tier: frontend
  template:
    metadata:
      labels:
        app: web
        tier: frontend
    spec:
      containers:
      - name: nginx
        image: nginx:latest
        ports:
        - containerPort: 80
        resources:
          requests:
            memory: "64Mi"
            cpu: "100m"
          limits:
            memory: "128Mi"
            cpu: "200m"
```

&nbsp;

**2 →** Apply and verify

```bash
kubectl apply -f sprint-02-kubernetes/multi-app.yaml
kubectl get pods --show-labels
kubectl get pods -l tier=frontend
```

&nbsp;

**3 →** Clean up

```bash
kubectl delete -f sprint-02-kubernetes/multi-app.yaml
minikube stop
```

&nbsp;

---

&nbsp;

## Part 6 — Commit `5 min`

```bash
git add sprint-02-kubernetes/
git commit -m "sprint 2 day 1: k8s objects — pods, replicasets, labels, namespaces"
git push
```

&nbsp;

---

&nbsp;

## ✅ Day 1 Checklist

| | Task |
|---|------|
| ☐ | Can explain Pod → ReplicaSet → Deployment hierarchy |
| ☐ | Added labels to a deployment and filtered by them |
| ☐ | Created and used namespaces |
| ☐ | Debugged a broken pod with `describe` and `logs` |
| ☐ | Created a YAML with resource limits |
| ☐ | Pushed to GitHub 🟩 |

&nbsp;

---

&nbsp;

## 🧠 Concepts You Now Own

| Concept | One-liner |
|---------|-----------|
| **Pod** | Smallest deployable unit — wraps one or more containers |
| **ReplicaSet** | The babysitter — keeps the right number of pods running |
| **Deployment** | Your instruction to K8s — manages ReplicaSets for you |
| **Label** | A sticky note on a resource — how K8s connects things |
| **Selector** | "Find me all pods with label X" |
| **Namespace** | A folder — keeps resources separated |
| **Resource limits** | "This pod gets max 128Mi RAM and 200m CPU" |

&nbsp;

---

&nbsp;

> *Next: Networking — Services, DNS, and how traffic finds your pods. 🌐*
