# Week 1 · Day 2 · Tuesday

## 🎯 Kubernetes Deep Dive + Hands-On Project

`90 min` · `Needs: minikube, kubectl from Day 1` · `You will deploy a real app today`

---

&nbsp;

## Today's Big Picture

> Yesterday you installed the tools. Today you use them.
> By the end of this session, you'll have a web app running on Kubernetes
> that you can scale up and down like Netflix does.

By the end of today, you'll have:

- ✅ Understand how K8s actually works (not just buzzwords)
- ✅ Deployed a real web server on your local cluster
- ✅ Scaled it from 1 → 3 replicas and watched K8s manage it
- ✅ Exposed it so you can see it in your browser
- ✅ Broken things on purpose and watched K8s self-heal

&nbsp;

---

&nbsp;

## Part 1 — How Kubernetes Actually Works `20 min`

&nbsp;

### The Restaurant Analogy 🍕

Think of Kubernetes as a restaurant:

| K8s Concept | Restaurant Equivalent |
|-------------|----------------------|
| **Cluster** | The entire restaurant |
| **Node** | A kitchen (you can have multiple kitchens) |
| **Pod** | One chef working on one dish |
| **Deployment** | The head chef's instructions: "I need 3 pizzas at all times" |
| **Service** | The front counter where customers pick up food |
| **kubectl** | You — the restaurant owner giving orders |

&nbsp;

### The Architecture (what's actually running)

```
┌─────────────────────────────────────────┐
│              CONTROL PLANE              │
│  (the brain — makes all the decisions)  │
│                                         │
│  ┌──────────┐  ┌────────────────────┐   │
│  │ API      │  │ Scheduler          │   │
│  │ Server   │  │ "which node has    │   │
│  │ (front   │  │  room for this     │   │
│  │  door)   │  │  pod?"             │   │
│  └──────────┘  └────────────────────┘   │
│  ┌──────────┐  ┌────────────────────┐   │
│  │ etcd     │  │ Controller Manager │   │
│  │ (the     │  │ "are we running    │   │
│  │  database│  │  what we should    │   │
│  │  of      │  │  be running?"      │   │
│  │  truth)  │  │                    │   │
│  └──────────┘  └────────────────────┘   │
└─────────────────────────────────────────┘
                    │
          kubectl talks to API Server
                    │
┌─────────────────────────────────────────┐
│              WORKER NODE                │
│  (the kitchen — where work happens)     │
│                                         │
│  ┌──────────┐  ┌────────────────────┐   │
│  │ kubelet  │  │ Container Runtime  │   │
│  │ (node    │  │ (Podman/containerd │   │
│  │  agent)  │  │  — runs the       │   │
│  │          │  │  actual containers)│   │
│  └──────────┘  └────────────────────┘   │
│                                         │
│  ┌─────┐  ┌─────┐  ┌─────┐            │
│  │ Pod │  │ Pod │  │ Pod │            │
│  │ 🍕  │  │ 🍕  │  │ 🍕  │            │
│  └─────┘  └─────┘  └─────┘            │
└─────────────────────────────────────────┘
```

&nbsp;

### The Flow (what happens when you deploy something)

```
You run:  kubectl apply -f my-app.yaml

1. kubectl sends the YAML to the API Server
2. API Server saves it in etcd ("someone wants 3 pods")
3. Controller Manager notices: "we have 0 pods but need 3"
4. Scheduler picks which node(s) to put them on
5. kubelet on that node creates the containers
6. Pods are running ✅
7. If a pod dies → Controller Manager notices → creates a new one
```

> That last step is the magic. **K8s is self-healing.** You tell it what you want, and it makes it happen — forever.

&nbsp;

---

&nbsp;

## Part 2 — Key Concepts in Plain English `10 min`

&nbsp;

### Pod

The smallest thing K8s runs. It's a wrapper around one (or more) containers. Think of it as a single worker doing a single job.

```
Pod = Container + networking + storage config
```

> You almost never create a Pod directly. You create a Deployment, and it creates Pods for you.

&nbsp;

### Deployment

Your instructions to K8s: "I want 3 copies of this app running at all times." If one crashes, K8s replaces it. If you want 5 instead, K8s adds 2 more.

&nbsp;

### Service

Pods get random IP addresses that change every time they restart. A Service gives them a stable address — like a phone number that never changes, even if the person holding the phone swaps out.

| Service Type | What it does |
|-------------|--------------|
| **ClusterIP** | Only reachable inside the cluster (default) |
| **NodePort** | Opens a port on the node so you can access it from outside |
| **LoadBalancer** | Gets a real external IP (cloud only, or minikube tunnel) |

&nbsp;

### Namespace

A folder for your K8s stuff. Keeps things organized. `default` is where your stuff goes unless you say otherwise.

&nbsp;

---

&nbsp;

## Part 3 — Hands-On: Deploy, Scale & Break Things 🔨 `45 min`

&nbsp;

### Step 1 → Start your cluster

```bash
minikube start
```

> Wait for "Done! kubectl is now configured to use minikube cluster"

&nbsp;

### Step 2 → Check what's running

```bash
kubectl get nodes
kubectl get pods --all-namespaces
```

> You'll see system pods (coredns, etcd, etc.) — that's K8s itself running. Your node should say `Ready`.

&nbsp;

### Step 3 → Deploy nginx (a real web server)

```bash
kubectl create deployment my-web --image=nginx --replicas=1
```

> That one command told K8s: "Run 1 copy of nginx and keep it alive."

&nbsp;

**Watch it come to life:**

```bash
kubectl get pods -w
```

> You'll see the status go from `ContainerCreating` → `Running`. Press `Ctrl+C` to stop watching.

&nbsp;

### Step 4 → Look at what you created

```bash
kubectl get deployments
kubectl get pods
kubectl describe pod <paste-pod-name-here>
```

> `describe` is your best friend for debugging. It shows events, status, IP, node, everything.

&nbsp;

### Step 5 → Expose it so you can see it in a browser

```bash
kubectl expose deployment my-web --type=NodePort --port=80
```

```bash
minikube service my-web
```

> 🎉 **Your browser should open with the nginx welcome page.** You just served a website from Kubernetes on your laptop.

&nbsp;

### Step 6 → Scale it up

```bash
kubectl scale deployment my-web --replicas=3
```

```bash
kubectl get pods
```

> You should see 3 pods now. K8s created 2 more in seconds. This is how Netflix handles traffic spikes — just more replicas.

&nbsp;

### Step 7 → Watch K8s self-heal 🪄

Delete a pod on purpose:

```bash
kubectl get pods
kubectl delete pod <paste-any-pod-name-here>
```

Now immediately check:

```bash
kubectl get pods
```

> 🤯 **There are still 3 pods.** K8s noticed one died and instantly created a replacement. You told it "I want 3" and it will fight to keep 3 running. That's self-healing.

&nbsp;

### Step 8 → Scale it down

```bash
kubectl scale deployment my-web --replicas=1
```

```bash
kubectl get pods
```

> K8s gracefully terminated 2 pods. Back to 1.

&nbsp;

### Step 9 → Try it with YAML (the real way)

All those `kubectl create` commands? In production, nobody types those. Everything is a YAML file checked into Git. Let's try it.

Create a file called `nginx-deployment.yaml` in your `projects/` folder:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-web-yaml
spec:
  replicas: 2
  selector:
    matchLabels:
      app: my-web-yaml
  template:
    metadata:
      labels:
        app: my-web-yaml
    spec:
      containers:
      - name: nginx
        image: nginx:latest
        ports:
        - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: my-web-yaml-svc
spec:
  type: NodePort
  selector:
    app: my-web-yaml
  ports:
  - port: 80
    targetPort: 80
```

&nbsp;

**Apply it:**

```bash
kubectl apply -f projects/nginx-deployment.yaml
```

```bash
kubectl get pods
kubectl get svc
minikube service my-web-yaml-svc
```

> Same result, but now it's in a file you can commit to Git. That's **GitOps** — infrastructure as code.

&nbsp;

### Step 10 → Clean up

```bash
kubectl delete deployment my-web
kubectl delete svc my-web
kubectl delete -f projects/nginx-deployment.yaml
minikube stop
```

&nbsp;

---

&nbsp;

## Part 4 — Commit Your Work `10 min`

&nbsp;

### Do This

**1 →** Save the YAML file you created

```bash
git add projects/nginx-deployment.yaml
```

&nbsp;

**2 →** Write your daily log (`daily-logs/week-01/day-02.md`)

```markdown
# Day 2 — Kubernetes Hands-On

## What I did
- Learned K8s architecture (control plane, worker nodes, pods)
- Deployed nginx, scaled to 3 replicas, watched self-healing
- Created my first YAML manifest

## What I learned
- (fill in)

## What confused me
- (fill in)

## Commands I want to remember
- kubectl get pods
- kubectl describe pod <name>
- kubectl scale deployment <name> --replicas=N
- kubectl apply -f <file>.yaml
```

&nbsp;

**3 →** Push it

```bash
git add .
git commit -m "day 2: first k8s deployment — nginx, scaling, self-healing"
git push
```

&nbsp;

---

&nbsp;

## ✅ Day 2 Checklist

| | Task |
|---|------|
| ☐ | Can explain what a Pod, Deployment, and Service are |
| ☐ | Deployed nginx on minikube |
| ☐ | Scaled to 3 replicas and saw all 3 pods |
| ☐ | Deleted a pod and watched K8s self-heal |
| ☐ | Created a YAML manifest and applied it |
| ☐ | Saw nginx in the browser via `minikube service` |
| ☐ | Daily log written and pushed 🟩 |

&nbsp;

---

&nbsp;

## 🧠 Concepts You Now Own

| Concept | One-liner |
|---------|-----------|
| **Pod** | Smallest unit in K8s — wraps a container |
| **Deployment** | "Keep N copies of this app running, always" |
| **Service** | Stable address for your pods (they get random IPs) |
| **Replica** | A copy of your pod — more replicas = more capacity |
| **Self-healing** | K8s replaces dead pods automatically |
| **YAML manifest** | A file that describes what you want K8s to run |
| **kubectl apply** | "Make reality match this YAML file" |
| **Namespace** | A folder to organize your K8s resources |

&nbsp;

---

&nbsp;

## 💡 Cheat Sheet — Commands You'll Use Forever

```bash
kubectl get pods                    # list all pods
kubectl get deployments             # list all deployments
kubectl get svc                     # list all services
kubectl get all                     # list everything
kubectl describe pod <name>         # deep info about a pod
kubectl logs <pod-name>             # see container logs
kubectl scale deployment <n> --replicas=X
kubectl apply -f <file>.yaml        # create/update from YAML
kubectl delete -f <file>.yaml       # delete what the YAML created
```

&nbsp;

---

&nbsp;

> *Tomorrow: Python crash course — you'll write the code that talks to these K8s pods.*
> *Today you proved you can run infrastructure. Tomorrow you write the software that runs on it. 🔥*
