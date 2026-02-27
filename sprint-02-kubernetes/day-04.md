# Sprint 2 · Day 4

## 🚀 Sprint Project: Flask API on Kubernetes

`90 min` · `Needs: Sprint 1 Flask API + minikube` · `This is the payoff`

---

&nbsp;

## Today's Big Picture

> In Sprint 1, you built a Flask API and ran it in a container.
> Today that container runs on Kubernetes — with scaling, self-healing, and a Service.
> This is what "deploying to production" actually looks like.

By the end of today, you'll have:

- ✅ Pushed your Flask image to minikube's local registry
- ✅ Written a full K8s Deployment YAML with resource limits
- ✅ Created a Service to expose the API
- ✅ Scaled it up and watched K8s distribute traffic
- ✅ Your Sprint 2 project — live on Kubernetes 🎉

&nbsp;

---

&nbsp;

## The Architecture

```
┌──────────────────────────────────────────────┐
│  minikube cluster                            │
│                                              │
│  ┌── Deployment: flask-api (replicas: 3) ──┐│
│  │                                          ││
│  │  ┌──────┐  ┌──────┐  ┌──────┐          ││
│  │  │ Pod 1│  │ Pod 2│  │ Pod 3│          ││
│  │  │:5000 │  │:5000 │  │:5000 │          ││
│  │  └──┬───┘  └──┬───┘  └──┬───┘          ││
│  └─────┼─────────┼─────────┼────────────────┘│
│        └─────────┼─────────┘                 │
│             ┌────▼────┐                      │
│             │ Service │                      │
│             │ NodePort│                      │
│             │ :80     │                      │
│             └────┬────┘                      │
└──────────────────┼───────────────────────────┘
                   │
            Your browser
            localhost:????
```

&nbsp;

---

&nbsp;

## Part 1 — Load Your Image Into Minikube `10 min`

&nbsp;

### Why this step?

Minikube runs its own Docker/Podman inside a VM. It can't see images on your machine. You need to either push to a registry or use minikube's built-in image loading.

&nbsp;

### Do This

**1 →** Build the image inside minikube's environment

```bash
minikube start
eval $(minikube docker-env)
```

> This makes your terminal's `docker`/`podman` commands target minikube's container runtime instead of your local one.

&nbsp;

**2 →** Build your Flask image (same Containerfile from Sprint 1)

```bash
cd ~/projects/ai-mlops-journey/projects/01-flask-api
docker build -t my-flask-api:v1 .
```

> Now the image exists inside minikube. K8s can use it.

&nbsp;

---

&nbsp;

## Part 2 — Write the Deployment YAML `20 min`

&nbsp;

### Do This

Create `sprint-02-kubernetes/flask-k8s.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flask-api
  labels:
    app: flask-api
spec:
  replicas: 2
  selector:
    matchLabels:
      app: flask-api
  template:
    metadata:
      labels:
        app: flask-api
    spec:
      containers:
      - name: flask-api
        image: my-flask-api:v1
        imagePullPolicy: Never
        ports:
        - containerPort: 5000
        resources:
          requests:
            memory: "64Mi"
            cpu: "100m"
          limits:
            memory: "128Mi"
            cpu: "250m"
---
apiVersion: v1
kind: Service
metadata:
  name: flask-api-svc
spec:
  type: NodePort
  selector:
    app: flask-api
  ports:
  - port: 80
    targetPort: 5000
```

> `imagePullPolicy: Never` tells K8s "don't try to pull this from Docker Hub — it's already here locally."

&nbsp;

---

&nbsp;

## Part 3 — Deploy & Test `20 min`

&nbsp;

**1 →** Apply it

```bash
cd ~/projects/ai-mlops-journey
kubectl apply -f sprint-02-kubernetes/flask-k8s.yaml
```

&nbsp;

**2 →** Watch pods come up

```bash
kubectl get pods -w
```

> Wait for both pods to show `Running`. Press `Ctrl+C`.

&nbsp;

**3 →** Open it in the browser

```bash
minikube service flask-api-svc
```

> Add `/health` or `/pods` to the URL. Your Flask API is running on Kubernetes! 🎉

&nbsp;

**4 →** Scale it

```bash
kubectl scale deployment flask-api --replicas=4
kubectl get pods
```

&nbsp;

**5 →** Test self-healing

```bash
kubectl delete pod <any-flask-pod-name>
kubectl get pods
```

> Still 4 pods. K8s replaced the dead one instantly.

&nbsp;

**6 →** Check the Service routing

```bash
kubectl describe svc flask-api-svc
```

> Look at `Endpoints` — all 4 pod IPs are listed. Traffic is load-balanced across them.

&nbsp;

---

&nbsp;

## Part 4 — Clean Up & Commit `10 min`

```bash
kubectl delete -f sprint-02-kubernetes/flask-k8s.yaml
eval $(minikube docker-env -u)
minikube stop
```

```bash
git add sprint-02-kubernetes/
git commit -m "sprint 2 day 4: flask API deployed on kubernetes 🚀"
git push
```

&nbsp;

---

&nbsp;

## ✅ Day 4 Checklist

| | Task |
|---|------|
| ☐ | Built Flask image inside minikube |
| ☐ | Wrote a Deployment YAML with resource limits |
| ☐ | Created a NodePort Service |
| ☐ | Flask API accessible in browser via K8s |
| ☐ | Scaled to 4 replicas and tested self-healing |
| ☐ | Pushed to GitHub 🟩 |

&nbsp;

---

&nbsp;

## 🧠 Concepts You Now Own

| Concept | One-liner |
|---------|-----------|
| **imagePullPolicy: Never** | Use local images — don't pull from a registry |
| **targetPort vs port** | Service listens on `port`, forwards to pod's `targetPort` |
| **eval $(minikube docker-env)** | Point your terminal at minikube's container runtime |
| **Multi-resource YAML** | Use `---` to separate multiple K8s objects in one file |

&nbsp;

---

&nbsp;

## 🎉 Sprint 2 Complete!

You went from "I can run nginx" to:

- Understanding every K8s building block
- Networking, DNS, and how traffic flows
- Config management and security basics
- **Deploying YOUR OWN app on Kubernetes**

That's not tutorial following. That's engineering.

&nbsp;

> *Next: [Sprint 3 — Cloud Native + Your First AI Project](../sprint-03-cloud-native/sprint-03-overview.md)*
> *KCNA prep begins + you talk to an LLM for the first time. 🤖*
