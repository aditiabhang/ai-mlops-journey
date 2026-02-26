# Day 2 Notes — K8s Hands-On Learnings

---

## What I Did Today

- Started minikube cluster
- Ran `kubectl get pods --all-namespaces` → saw all 7 system pods
- Deployed nginx with `kubectl create deployment` → hit ImagePullBackOff
- Debugged it: minikube VM couldn't reach Docker Hub (DNS timeout)
- Fixed it: pulled image via Podman, sideloaded into minikube, set `imagePullPolicy: Never`
- Scaled deployment to 3 replicas, deleted a pod, watched K8s self-heal
- Created first YAML manifest (nginx-deployment.yaml) with Deployment + Service
- Applied it, saw 2 pods running, opened nginx in browser via `minikube service`
- Cleaned up everything: deleted deployments, services, stopped minikube

---

## Reading `kubectl describe pod`

When something breaks, run: `kubectl describe pod <pod-name>`

It dumps a wall of text. Here's what to actually look at, in priority order:

### 🔴 #1 — Events (always scroll to the bottom first)

The timeline of what happened. Scheduling, image pulls, crashes, restarts. Your error messages live here. This is where we spotted ImagePullBackOff. **80% of debugging starts and ends here.**

```
Events:
  Type     Reason      Age   From              Message
  Normal   Scheduled   26m   default-scheduler Successfully assigned...
  Warning  Failed      26m   kubelet           Failed to pull image "nginx"
  Normal   Started     26m   kubelet           Container started
```

### 🟠 #2 — Status + State + Restart Count

```
Status:         Running       ← good. "Pending" or "CrashLoopBackOff" = problem
State:          Running       ← the container itself
Restart Count:  0             ← high number = your app keeps crashing and restarting
```

### 🟡 #3 — Conditions

Five quick green/red lights:

| Condition | Meaning |
|-----------|---------|
| `PodScheduled: True` | Was it assigned to a node? |
| `Initialized: True` | Did init containers finish? |
| `ContainersReady: True` | Are all containers healthy? |
| `Ready: True` | Can it receive traffic? |
| `PodReadyToStartContainers: True` | Is the sandbox ready? |

> If any say `False`, that's your clue.

### 🔵 #4 — Node + IP

```
Node:   minikube/192.168.64.2    ← which machine it's running on
IP:     10.244.0.8               ← its internal address in the cluster
```

Useful when debugging networking or "why is this pod on this node?"

### ⚪ #5 — Image + Container ID

```
Image:    docker.io/library/nginx:latest
Image ID: docker://sha256:0000f06a...
```

Confirms the exact image. Catches "I deployed the wrong version" mistakes.

> **Rule:** scroll to the bottom first. Events tell you 80% of the story.

---

## Troubleshooting: ImagePullBackOff

**What it means:**
K8s tried to download the container image from a registry and failed. It backed off and will retry with increasing delays.

**Root cause (our case):**
Minikube's VM couldn't reach Docker Hub. DNS timeout. My Mac had internet, but minikube's Linux VM inside it didn't.

**How we found it:**
`kubectl describe pod <name>` → Events section showed:

```
"dial tcp: lookup registry-1.docker.io ... i/o timeout"
```

**The fix:**
Pulled the image on the host machine and sideloaded it into minikube.

```bash
podman pull docker.io/library/nginx:latest
podman save docker.io/library/nginx:latest -o /tmp/nginx.tar
minikube image load /tmp/nginx.tar
```

Then told K8s not to try pulling from the internet:

```bash
kubectl patch deployment my-web -p '{"spec":{"template":{"spec":{"containers":[{"name":"nginx","imagePullPolicy":"Never"}]}}}}'
```

> **Why this matters:** This is exactly how air-gapped environments work (banks, government, healthcare). They never pull from public registries in production. Images are pre-loaded into private registries after being scanned for vulnerabilities.

---

## `imagePullPolicy` — Three Options

| Policy | What it does |
|--------|-------------|
| `Always` | Download the image every time, even if it's already local |
| `IfNotPresent` | Use local copy if it exists, pull only if missing |
| `Never` | Don't pull at all, fail if the image isn't already on the node |

**Default behavior:**
- Tag is `latest` → defaults to `Always`
- Tag is specific (e.g. `nginx:1.25`) → defaults to `IfNotPresent`

---

## System Pods — What's Running in `kube-system`

| Pod | What it does |
|-----|-------------|
| `coredns` | Cluster DNS — translates service names to IPs |
| `etcd` | Database that stores all cluster state |
| `kube-apiserver` | Front door — everything talks to this |
| `kube-controller-manager` | Self-healing engine — "are we running what we should?" |
| `kube-proxy` | Routes network traffic to the right pods |
| `kube-scheduler` | Decides which node gets each new pod |
| `storage-provisioner` | Minikube-specific — handles local storage volumes |

> You never touch these. They're the engine under the hood. Your apps go in the `default` namespace.

---

## YAML Manifest Lesson

One YAML file can define multiple resources separated by `---`

Our `nginx-deployment.yaml` had:
1. A **Deployment** (2 replicas of nginx)
2. A **Service** (NodePort to expose it)

**Key Deployment fields:**

| Field | What it does |
|-------|-------------|
| `replicas` | How many pods to run |
| `selector` | How the deployment finds its pods (matchLabels) |
| `template` | The pod blueprint (what containers to run) |
| `imagePullPolicy` | `Always`, `IfNotPresent`, or `Never` |

**Key Service fields:**

| Field | What it does |
|-------|-------------|
| `type` | `ClusterIP` (internal), `NodePort` (external port), `LoadBalancer` |
| `selector` | Which pods to route traffic to (must match pod labels) |
| `port` | The service port |
| `targetPort` | The container port |

```bash
kubectl apply -f <file>.yaml    # create or update
kubectl delete -f <file>.yaml   # remove everything in the file
```

> This is **GitOps** — infrastructure defined in files, checked into Git.

---

## Self-Healing Demo

```bash
# Told K8s: I want 3 replicas
kubectl scale deployment my-web --replicas=3

# Killed one
kubectl delete pod <pod-name>

# Immediately checked
kubectl get pods    # → still 3 pods!
```

> K8s noticed one died and instantly replaced it. It will always fight to match the desired state you declared.

---

## Commands to Remember

| Command | What it does |
|---------|-------------|
| `kubectl get pods` | List all pods |
| `kubectl get pods -w` | Watch pods in real time (Ctrl+C to stop) |
| `kubectl get pods --all-namespaces` | See system pods too |
| `kubectl get deployments` | List deployments |
| `kubectl get svc` | List services |
| `kubectl get all` | List everything |
| `kubectl describe pod <name>` | Deep info (Events at the bottom!) |
| `kubectl logs <pod-name>` | See container stdout/stderr |
| `kubectl scale deployment <n> --replicas=X` | Scale up or down |
| `kubectl apply -f <file>.yaml` | Create/update from YAML |
| `kubectl delete -f <file>.yaml` | Delete what the YAML created |
| `kubectl delete pod <name>` | Kill a pod (K8s will recreate it) |
| `minikube image load <file>.tar` | Sideload an image into minikube |
| `minikube service <svc-name>` | Open a service in browser |

---

## Things That Surprised Me

- **K8s self-heals.** Delete a pod, it comes right back. It fights to maintain the desired state you declared.

- **YAML manifests are the "real" way.** Nobody types `kubectl create` in production. Everything is a file, checked into Git. That's GitOps.

- **Minikube runs a full Linux VM.** That VM has its own network, its own DNS, its own container runtime. That's why it couldn't reach Docker Hub even though my Mac could.

- **The `describe` command is the most important tool in the toolbox.** Not `get`. Not `logs`. `Describe`.

---

## What Confused Me

- Basic things, like what happens under the hood when we get the `ImagePullBackOff` error.
- What concerning factors to look for with the `kubectl describe pod` command.

## What I Want to Explore Next

- How K8s can get complicated as I dig deeper and learn more about it.
