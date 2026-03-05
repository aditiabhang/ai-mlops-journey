# Sprint 2 · Day 3 — ConfigMaps, Secrets & a DNS Detour

## What I did
- Created a ConfigMap and injected it into a pod as env vars
- Created a Secret and mounted it the same way
- Learned resource requests vs limits (CPU/memory)
- RBAC and Network Policies at concept level

## 🐛 Bug I hit (twice)

**Error:** `image can't be pulled` on both `config-test` and `secret-test` pods

**What happened:** Both pods use the `busybox` image. Kubernetes tried to pull it from Docker Hub but couldn't — every pull timed out.

**Why it happened:** My Mac's DNS is set to `127.0.0.1` (a local DNS proxy). Minikube runs in a VM, and from inside that VM, `127.0.0.1` points to the VM itself — not my Mac. So DNS lookups for `registry-1.docker.io` went nowhere.

**How we fixed it:**
1. SSH'd into the VM and pointed DNS to Google: `minikube ssh -- "echo nameserver 8.8.8.8 | sudo tee /etc/resolv.conf"`
2. Pre-pulled the image inside the VM: `minikube ssh -- docker pull busybox`
3. Added `imagePullPolicy: Never` to the pod YAML so K8s uses the local cache instead of trying to pull again

**Takeaway:** If minikube can't pull images, check DNS inside the VM first. Your host's DNS config doesn't automatically work inside the VM.

## What I learned
- ConfigMaps = non-secret config outside your code (DB_HOST, LOG_LEVEL)
- Secrets = same idea but for passwords — base64 encoded, not encrypted
- `envFrom` injects all keys from a ConfigMap; `valueFrom.secretKeyRef` injects one key at a time
- `imagePullPolicy: Never` = "trust what's already cached, don't phone home"

## What confused me
- Why Secrets use base64 and not actual encryption — feels like a false sense of security
- `envFrom` vs `env.valueFrom` — two different ways to inject config, not obvious when to pick which
- `requests` vs `limits` — requests are for scheduling, limits are for enforcement, but easy to mix up
