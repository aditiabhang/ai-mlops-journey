# Sprint 2 · Day 3

## 🔒 Config & Security — ConfigMaps, Secrets, RBAC

`90 min` · `Needs: minikube` · `The "production readiness" day`

---

&nbsp;

## Today's Big Picture

> Hardcoding passwords in your code? That's how breaches happen.
> Today you learn to do it right — configs outside your code, secrets encrypted, access controlled.

By the end of today, you'll have:

- ✅ Created ConfigMaps to separate config from code
- ✅ Used Secrets to store passwords safely
- ✅ Set resource limits (CPU/memory) on pods
- ✅ Understand RBAC basics (who can do what)
- ✅ Know what Network Policies are (concept level)

&nbsp;

---

&nbsp;

## Part 1 — ConfigMaps `20 min`

&nbsp;

### What are ConfigMaps? (30-second version)

A ConfigMap is a key-value store for non-secret config. Database host, feature flags, log levels — anything that changes between environments but isn't a password.

```
WITHOUT ConfigMaps:              WITH ConfigMaps:

┌──────────────┐                ┌──────────────┐
│  app.py      │                │  app.py      │
│              │                │              │
│  DB_HOST =   │                │  DB_HOST =   │
│  "prod.db"   │ ◀── hardcoded │  os.getenv() │ ◀── reads from env
│              │                │              │
└──────────────┘                └──────────────┘
                                       ▲
                                ┌──────┴───────┐
                                │  ConfigMap   │
                                │  DB_HOST:    │
                                │  "prod.db"   │
                                └──────────────┘
```

> Same code in dev, staging, prod. Only the ConfigMap changes. That's the whole idea.

&nbsp;

### Do This

**1 →** Start minikube

```bash
minikube start
```

&nbsp;

**2 →** Create a ConfigMap

```bash
kubectl create configmap app-config \
  --from-literal=DB_HOST=postgres.default.svc \
  --from-literal=LOG_LEVEL=info \
  --from-literal=APP_ENV=development
```

&nbsp;

**3 →** See it

```bash
kubectl get configmap app-config -o yaml
```

&nbsp;

**4 →** Use it in a Pod — create `sprint-02-kubernetes/pod-with-config.yaml`

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: config-test
spec:
  containers:
  - name: app
    image: busybox
    command: ["sh", "-c", "echo DB=$DB_HOST ENV=$APP_ENV && sleep 3600"]
    envFrom:
    - configMapRef:
        name: app-config
```

&nbsp;

**5 →** Apply and check

```bash
kubectl apply -f sprint-02-kubernetes/pod-with-config.yaml
kubectl logs config-test
```

> You should see `DB=postgres.default.svc ENV=development`. The pod read config from the ConfigMap, not from hardcoded values.

&nbsp;

---

&nbsp;

## Part 2 — Secrets `20 min`

&nbsp;

### What are Secrets? (30-second version)

Same as ConfigMaps, but for sensitive data — passwords, API keys, tokens. K8s base64-encodes them (not true encryption, but keeps them out of plain text).

```
┌──────────────────────────┐
│  Secret: db-credentials  │
│                          │
│  username: YWRtaW4=      │ ◀── base64 encoded "admin"
│  password: cEBzc3cwcmQ=  │ ◀── base64 encoded "p@ssw0rd"
└──────────────────────────┘
```

&nbsp;

### Do This

**1 →** Create a Secret

```bash
kubectl create secret generic db-creds \
  --from-literal=username=admin \
  --from-literal=password=supersecret123
```

&nbsp;

**2 →** See it (notice the values are hidden)

```bash
kubectl get secret db-creds -o yaml
```

> The values are base64 encoded. Not encrypted — anyone with cluster access can decode them. For real security, use something like AWS Secrets Manager or HashiCorp Vault.

&nbsp;

**3 →** Decode a value (for learning — don't do this in prod!)

```bash
echo "c3VwZXJzZWNyZXQxMjM=" | base64 --decode
```

&nbsp;

**4 →** Use it in a Pod — create `sprint-02-kubernetes/pod-with-secret.yaml`

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secret-test
spec:
  containers:
  - name: app
    image: busybox
    command: ["sh", "-c", "echo User=$DB_USER && sleep 3600"]
    env:
    - name: DB_USER
      valueFrom:
        secretKeyRef:
          name: db-creds
          key: username
```

&nbsp;

**5 →** Apply and check

```bash
kubectl apply -f sprint-02-kubernetes/pod-with-secret.yaml
kubectl logs secret-test
```

> You should see `User=admin`. The secret was injected as an environment variable.

&nbsp;

---

&nbsp;

## Part 3 — Resource Limits `15 min`

&nbsp;

### Why limits? (30-second version)

Without limits, one greedy pod can eat all the CPU/memory and starve everything else. Limits are a budget — "you get this much, no more."

```
┌────────────────────────────────────┐
│  Node: 4 CPU, 8Gi memory          │
│                                    │
│  ┌──────┐  ┌──────┐  ┌──────┐    │
│  │ Pod A│  │ Pod B│  │ Pod C│    │
│  │ 1 CPU│  │ 1 CPU│  │ 1 CPU│    │
│  │ 2Gi  │  │ 2Gi  │  │ 2Gi  │    │
│  └──────┘  └──────┘  └──────┘    │
│                                    │
│  Used: 3 CPU, 6Gi | Free: 1 CPU  │
│  Pod D wants 2 CPU? → PENDING ❌  │
└────────────────────────────────────┘
```

&nbsp;

### Quick Reference

| Field | Meaning |
|-------|---------|
| `requests.cpu` | "I need at least this much" (for scheduling) |
| `requests.memory` | "I need at least this much RAM" |
| `limits.cpu` | "Don't let me use more than this" |
| `limits.memory` | "Kill me if I exceed this" (OOMKilled) |

> `100m` CPU = 0.1 CPU core. `256Mi` memory = 256 megabytes.

&nbsp;

---

&nbsp;

## Part 4 — RBAC & Network Policies (Concepts) `15 min`

&nbsp;

### RBAC in 30 seconds

**R**ole-**B**ased **A**ccess **C**ontrol = who can do what.

```
┌─────────────┐     ┌──────────────┐     ┌──────────────┐
│  User/SA    │────▶│  RoleBinding │────▶│  Role        │
│  "alice"    │     │  "alice can  │     │  "can GET    │
│             │     │   use this   │     │   pods in    │
│             │     │   role"      │     │   default ns"│
└─────────────┘     └──────────────┘     └──────────────┘
```

> For the KCNA exam: know that RBAC has Roles, ClusterRoles, RoleBindings, and ClusterRoleBindings. You don't need to create them from scratch — just know what they do.

&nbsp;

### Network Policies in 30 seconds

By default, every pod can talk to every other pod. Network Policies are firewall rules — "only pod A can talk to pod B."

> For the KCNA exam: know they exist and that they require a CNI plugin (like Calico) to enforce.

&nbsp;

---

&nbsp;

## Part 5 — Clean Up & Commit `10 min`

```bash
kubectl delete pod config-test secret-test
kubectl delete configmap app-config
kubectl delete secret db-creds
minikube stop
```

```bash
git add sprint-02-kubernetes/
git commit -m "sprint 2 day 3: configmaps, secrets, RBAC, resource limits"
git push
```

&nbsp;

---

&nbsp;

## ✅ Day 3 Checklist

| | Task |
|---|------|
| ☐ | Created a ConfigMap and used it in a pod |
| ☐ | Created a Secret and injected it as an env var |
| ☐ | Understand requests vs limits for CPU/memory |
| ☐ | Can explain RBAC at a concept level |
| ☐ | Know what Network Policies do |
| ☐ | Pushed to GitHub 🟩 |

&nbsp;

---

&nbsp;

## 🧠 Concepts You Now Own

| Concept | One-liner |
|---------|-----------|
| **ConfigMap** | Key-value config outside your code — changes per environment |
| **Secret** | Like ConfigMap but for passwords — base64 encoded |
| **Resource requests** | "I need at least this much CPU/memory" |
| **Resource limits** | "Don't give me more than this — kill me if I exceed" |
| **RBAC** | Who can do what — Roles + RoleBindings |
| **Network Policy** | Firewall rules between pods |
| **OOMKilled** | Pod exceeded memory limit and got terminated |

&nbsp;

---

&nbsp;

> *Next: The big one — deploy your Flask API on Kubernetes! 🚀*
