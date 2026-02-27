# Sprint 2 · Day 2

## 🌐 K8s Networking — How Traffic Finds Your Pods

`90 min` · `Needs: minikube running` · `The "aha!" moment for Services`

---

&nbsp;

## Today's Big Picture

> Your pod has an IP address. Cool. It changes every time the pod restarts. Not cool.
> Today you learn how K8s solves this with Services — stable addresses that never change.

By the end of today, you'll have:

- ✅ Understand why Pods need Services
- ✅ Created ClusterIP, NodePort, and LoadBalancer Services
- ✅ Understand K8s DNS ("my-svc.my-namespace.svc.cluster.local")
- ✅ Know what Ingress does (concept level)

&nbsp;

---

&nbsp;

## Part 1 — Why Services Exist `10 min`

&nbsp;

### The Problem

```
                   Pod dies → new Pod → NEW IP 😱
                   
  App A ──────▶  Pod B (10.0.0.5)
  
  Pod B crashes, K8s creates replacement:
  
  App A ──────▶  ??? (10.0.0.5 is gone!)
                  Pod B-v2 (10.0.0.9) ← nobody knows this address
```

### The Fix: Services

```
  App A ──────▶  Service (stable address) ──────▶  Pod B (whatever IP)
                 "my-web-svc"                      Pod B dies? 
                 never changes                     Service finds the new one
```

> A Service is a phone number that never changes, even when the person holding the phone swaps out.

&nbsp;

---

&nbsp;

## Part 2 — The 3 Service Types `20 min`

&nbsp;

### Quick Reference

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│  ClusterIP          NodePort          LoadBalancer   │
│  ┌─────────┐       ┌─────────┐       ┌─────────┐   │
│  │ Internal │       │ + Opens │       │ + Gets  │   │
│  │ only     │       │ a port  │       │ a real  │   │
│  │          │       │ on the  │       │ external│   │
│  │ Pod ↔ Pod│       │ node    │       │ IP      │   │
│  │ comms    │       │         │       │         │   │
│  └─────────┘       └─────────┘       └─────────┘   │
│                                                     │
│  Default            Dev/testing        Production   │
│  Free               Free               Cloud only  │
└─────────────────────────────────────────────────────┘
```

&nbsp;

### Do This

**1 →** Start minikube and deploy an app

```bash
minikube start
kubectl create deployment web --image=nginx --replicas=2
```

&nbsp;

**2 →** Create a ClusterIP Service (default)

```bash
kubectl expose deployment web --port=80 --name=web-internal
kubectl get svc web-internal
```

> This Service is only reachable from inside the cluster. Other pods can reach it, but you can't from your browser.

&nbsp;

**3 →** Create a NodePort Service

```bash
kubectl expose deployment web --type=NodePort --port=80 --name=web-external
kubectl get svc web-external
minikube service web-external
```

> 🎉 Browser opens! NodePort opened a hole in the node so you can reach in from outside.

&nbsp;

**4 →** See how Services find Pods

```bash
kubectl describe svc web-external
```

> Look at `Endpoints` — those are the Pod IPs. The Service discovered them automatically using label selectors.

&nbsp;

---

&nbsp;

## Part 3 — K8s DNS `15 min`

&nbsp;

### How pods find each other (30-second version)

Every Service gets a DNS name automatically. Instead of remembering IP addresses, pods just use the name.

```
Format:   <service-name>.<namespace>.svc.cluster.local
Example:  web-internal.default.svc.cluster.local
Shortcut: web-internal   (works within the same namespace)
```

&nbsp;

### Do This — Prove DNS works

**1 →** Launch a test pod

```bash
kubectl run dns-test --image=busybox --restart=Never -- sleep 3600
```

&nbsp;

**2 →** Query DNS from inside the cluster

```bash
kubectl exec dns-test -- nslookup web-internal
```

> You'll see the ClusterIP address resolved from the name. That's K8s DNS doing its thing. In real apps, your code just calls `http://web-internal` and it works.

&nbsp;

**3 →** Clean up the test pod

```bash
kubectl delete pod dns-test
```

&nbsp;

---

&nbsp;

## Part 4 — Ingress (Concept Only) `10 min`

&nbsp;

### What is Ingress? (30-second version)

NodePort gives you `http://node-ip:30000`. Ugly. Ingress gives you `https://myapp.com/api`. Pretty.

```
Internet ──▶ Ingress Controller ──▶ Service ──▶ Pods
              (nginx/traefik)
              
Rules:
  myapp.com/api    → api-service
  myapp.com/web    → web-service
  myapp.com/admin  → admin-service
```

> You won't set up Ingress today — it needs extra setup on minikube. But the KCNA exam will ask about it. Know that it's the "pretty URL router" for K8s.

&nbsp;

---

&nbsp;

## Part 5 — Clean Up & Commit `10 min`

```bash
kubectl delete deployment web
kubectl delete svc web-internal web-external
minikube stop
```

```bash
git add sprint-02-kubernetes/
git commit -m "sprint 2 day 2: k8s networking — services, DNS, ingress concepts"
git push
```

&nbsp;

---

&nbsp;

## ✅ Day 2 Checklist

| | Task |
|---|------|
| ☐ | Can explain why Services exist (stable address for changing Pods) |
| ☐ | Created ClusterIP and NodePort Services |
| ☐ | Saw a Service's Endpoints (auto-discovered Pod IPs) |
| ☐ | Proved DNS works from inside a pod |
| ☐ | Can explain what Ingress does at a concept level |
| ☐ | Pushed to GitHub 🟩 |

&nbsp;

---

&nbsp;

## 🧠 Concepts You Now Own

| Concept | One-liner |
|---------|-----------|
| **Service** | Stable address for a set of Pods — never changes |
| **ClusterIP** | Internal only — pods talk to pods |
| **NodePort** | Opens a port on the node — accessible from outside |
| **LoadBalancer** | Gets a real external IP — cloud/production use |
| **Endpoints** | The actual Pod IPs behind a Service |
| **K8s DNS** | Every Service gets a name: `svc-name.namespace.svc.cluster.local` |
| **Ingress** | Pretty URL router — `myapp.com/api` instead of `:30000` |

&nbsp;

---

&nbsp;

> *Next: Config & Security — ConfigMaps, Secrets, and keeping your cluster safe. 🔒*
