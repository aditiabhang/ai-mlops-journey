# Day 4 Notes — Python Scripting: Pod Status Logger

---

## What I Did Today

- Built `projects/pod_status_logger.py` — a Python script that simulates a Kubernetes pod monitoring tool
- Used `json` module to write and read pod data to/from a JSON file
- Parsed pod statuses and generated a formatted status report with healthy/unhealthy indicators
- Added an API connectivity check using `requests` library (hit GitHub API)
- Practiced error handling with try/except for network failures
- Ran the script end-to-end, verified JSON output and status report

---

## What the Script Does

Simulates what you'd get from `kubectl get pods -o json`, but in Python:

```
1. Define pod data (4 pods across different namespaces)
2. Write to pod_report.json with timestamp
3. Read it back and print a formatted status report
4. Flag unhealthy pods (anything not "Running")
5. Test API connectivity (prove the script can talk to external endpoints)
```

### Output looks like:

```
✅ Pod data written to pod_report.json

📊 Pod Status Report — 2026-03-02 ...
-------------------------------------------------------
  🟢 nginx-7b8d           default      Running
  🟢 redis-3f2a           cache        Running
  🔴 ml-api-9c1e          inference    CrashLoopBackOff
  🟢 postgres-5d7b        database     Running

⚠️  1 pod(s) need attention

🌐 API check: GitHub API responded with 200
```

---

## Key Python Concepts Used

### JSON Read/Write

```python
# Write
with open("pod_report.json", "w") as f:
    json.dump({"timestamp": str(datetime.now()), "pods": pods}, f, indent=2)

# Read
with open("pod_report.json", "r") as f:
    report = json.load(f)
```

- `json.dump()` → Python dict to JSON file
- `json.load()` → JSON file to Python dict
- `indent=2` → makes the JSON human-readable

### List Comprehension for Filtering

```python
unhealthy = [p for p in report["pods"] if p["status"] != "Running"]
```

One line to filter all pods that aren't healthy. This is the Pythonic way — no for loop, no if/append pattern.

### String Formatting with f-strings

```python
print(f"  {icon} {pod['name']:20s} {pod['namespace']:12s} {pod['status']}")
```

- `:20s` → pad the string to 20 characters (aligns columns in output)
- f-strings are the modern way — cleaner than `.format()` or `%s`

### Try/Except for API Calls

```python
try:
    r = requests.get("https://api.github.com", timeout=5)
    print(f"🌐 API check: GitHub API responded with {r.status_code}")
except requests.exceptions.RequestException:
    print("🌐 API check: Could not reach endpoint")
```

- Always wrap external API calls in try/except — network can fail
- `timeout=5` → don't hang forever if the endpoint is slow
- Catching `RequestException` covers connection errors, timeouts, DNS failures

---

## How This Connects to K8s (Day 2)

| Day 2 (kubectl) | Day 4 (Python) |
|-----------------|----------------|
| `kubectl get pods -o json` | Simulated with a Python list of dicts |
| `kubectl describe pod` → check status | `if pod["status"] != "Running"` |
| Checking pod health manually | Automated with a script |
| One-time check | Could run on a cron/schedule |

> This is the bridge from "I can use kubectl" to "I can build monitoring tools." Day 2 was operating Kubernetes. Day 4 is programming around it.

---

## Why This Matters for MLOps / AI Ops

In production ML pipelines:
- Models run in pods (`ml-api-9c1e` in our data is a realistic example)
- `CrashLoopBackOff` on an inference pod = your ML model is down
- You need automated monitoring, not someone manually running `kubectl get pods`
- This script is the baby version of tools like Prometheus + Grafana alerting

---

## Things I Learned

- **JSON is the universal language between systems.** Kubernetes speaks it, APIs return it, Python reads/writes it natively. If you can handle JSON, you can glue anything together.

- **Error handling isn't optional for real tools.** The try/except on the API call is the difference between a script that crashes at 3am and one that logs "couldn't reach endpoint" and keeps going.

- **f-string formatting with width specifiers** (`:20s`) makes CLI output actually readable. Small detail, big difference.

---

## What I Want to Explore Next

- Hook this up to a real Kubernetes cluster using the `kubernetes` Python client library instead of hardcoded data
- Add Slack/email alerting when unhealthy pods are detected
- Write the report to a file with rotation (keep last 7 days of reports)
- Schedule it with cron or a Kubernetes CronJob
