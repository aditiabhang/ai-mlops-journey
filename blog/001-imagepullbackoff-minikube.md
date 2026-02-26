# I Broke Kubernetes on Day 2 (and Learned How Banks Deploy Software)

*3 min read · Kubernetes, Podman, Minikube*

---

I'm a Sr Support Engineer learning Kubernetes. Day 2. I typed one command:

```bash
kubectl create deployment my-web --image=nginx --replicas=1
```

Simple, right? Deploy nginx. The "hello world" of Kubernetes.

Then I watched my pod do this:

```
my-web-684f49ddf4-848pv   0/1     ErrImagePull       0     50s
my-web-684f49ddf4-848pv   0/1     ImagePullBackOff   0     46s
```

Cool. Broken already.

---

## What `ImagePullBackOff` Actually Means

Kubernetes runs containers. Containers need images. Images live in registries (like Docker Hub). `ImagePullBackOff` means one thing:

**K8s tried to download the image and failed. Then it gave up and is backing off before trying again.**

It's not your code. It's not your YAML. It's a network problem.

I ran `kubectl describe pod` — the debugging command every K8s engineer lives by — and found this:

```
Failed to pull image "nginx": dial tcp: lookup registry-1.docker.io
on 192.168.64.1:53: i/o timeout
```

The minikube VM couldn't reach Docker Hub. My Mac had internet. Minikube's little Linux VM inside it? Couldn't see the outside world.

---

## The Fix That Taught Me Something Real

My first instinct was to fix minikube's DNS. Restart it. Add flags. The usual.

It didn't work. The VM still couldn't reach Docker Hub.

So I tried something different:

```bash
# Step 1: Pull the image on MY machine (which has internet)
podman pull docker.io/library/nginx:latest

# Step 2: Save it to a file
podman save docker.io/library/nginx:latest -o /tmp/nginx.tar

# Step 3: Load it directly into minikube's VM
minikube image load /tmp/nginx.tar

# Step 4: Tell K8s "don't try to download it, it's already here"
kubectl patch deployment my-web -p \
  '{"spec":{"template":{"spec":{"containers":[{"name":"nginx","imagePullPolicy":"Never"}]}}}}'
```

```
my-web-75c7d7d675-t97vn   1/1     Running   0     20s
```

Running. ✅

---

## Why This Matters Beyond My Laptop

After fixing it, I realized — this isn't a workaround. **This is how production actually works in secure environments.**

Banks, government agencies, healthcare companies — they run "air-gapped" clusters. No internet access. No pulling images from Docker Hub on the fly.

Instead, they:

1. Pull images in a secure environment
2. Scan them for vulnerabilities
3. Push them to a private internal registry
4. Deploy with `imagePullPolicy: Never` or `IfNotPresent`

I accidentally learned a production deployment pattern while debugging a broken "hello world" on my laptop.

---

## The Three Things I'll Remember

**`kubectl describe pod <name>`** — Always your first debugging step. The Events section at the bottom tells you exactly what went wrong.

**`imagePullPolicy`** — Three options: `Always` (download every time), `IfNotPresent` (use local if available), `Never` (don't even try). Default depends on the image tag.

**`minikube image load`** — Sideloads images into minikube when the VM can't reach the internet. Saved my Day 2.

---

## The Takeaway

The best learning happens when things break. I could've followed a tutorial where everything works perfectly and learned nothing about how Kubernetes actually behaves in the real world.

Instead, I spent 20 minutes debugging, and I walked away understanding image pull policies, air-gapped deployments, and `kubectl describe` — things some engineers don't encounter until month 6 on the job.

Break things early. Break things often.

---

*I'm documenting my 12-week journey from Sr Support Engineer to AI/MLOps on [GitHub](https://github.com/aditiabhang/ai-mlops-journey). Day 2 of 60.*
