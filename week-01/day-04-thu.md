# Week 1 · Day 4 · Thursday

## 🎯 Python Continued — Files, JSON & APIs

`90 min` · `Needs: Python + virtual env from Day 1` · `Yesterday's Python basics`

---

&nbsp;

## Today's Big Picture

> Yesterday you learned to think in Python. Today you learn to talk to the outside world.
> Files, JSON, APIs — this is how every ML pipeline moves data around.

By the end of today, you'll have:

- ✅ Read and written files with Python
- ✅ Parsed and created JSON (the language machines speak)
- ✅ Made a real API call and pulled back live data
- ✅ Wrapped risky code in try/except so your scripts don't crash
- ✅ Built a mini K8s pod status logger that ties it all together

&nbsp;

---

&nbsp;

## Part 1 — Reading & Writing Files `15 min`

&nbsp;

### Why files? (30-second version)

Every ML workflow reads data from somewhere and writes results to somewhere. Config files, training data, model outputs, logs — it's all files. Python makes this dead simple.

&nbsp;

### The `with` statement

You'll see `with open(...)` everywhere. It's a context manager — fancy words for "auto-closes the file for you when you're done." Without it, you'd have to remember to call `.close()` manually. Nobody wants that.

&nbsp;

### Do This

**1 →** Activate your virtual env

```bash
cd ~/projects/ai-mlops-journey
source .venv/bin/activate
```

&nbsp;

**2 →** Create a file called `projects/file_basics.py`

```python
# Writing to a file
with open("projects/output.txt", "w") as f:
    f.write("Pod: nginx-abc123\n")
    f.write("Status: Running\n")
    f.write("Restarts: 0\n")

# Reading it back
with open("projects/output.txt", "r") as f:
    content = f.read()
    print(content)
```

&nbsp;

**3 →** Run it

```bash
python3 projects/file_basics.py
```

> You should see the pod info printed. Check `projects/output.txt` — it's a real file now.

&nbsp;

**4 →** Quick reference

| Mode | What it does |
|------|-------------|
| `"r"` | Read (file must exist) |
| `"w"` | Write (creates or overwrites) |
| `"a"` | Append (adds to the end) |

&nbsp;

---

&nbsp;

## Part 2 — JSON: The Language Machines Speak `20 min`

&nbsp;

### What is JSON? (30-second version)

It's a dict that lives in a file. That's it. When you see `{"name": "nginx", "status": "Running"}` — that's JSON. Every API response, every K8s manifest (internally), every ML config is JSON or YAML. If you know Python dicts, you already know JSON.

&nbsp;

### The 4 functions you need

| Function | What it does |
|----------|-------------|
| `json.loads(string)` | String → Python dict |
| `json.dumps(dict)` | Python dict → string |
| `json.load(file)` | File → Python dict |
| `json.dump(dict, file)` | Python dict → file |

> Memory trick: the `s` stands for **s**tring. With `s` = strings. Without `s` = files.

&nbsp;

### Do This

**1 →** Create `projects/json_basics.py`

```python
import json

# Create some pod data
pods = [
    {"name": "nginx-abc", "status": "Running", "restarts": 0},
    {"name": "redis-xyz", "status": "CrashLoopBackOff", "restarts": 5},
    {"name": "api-def", "status": "Running", "restarts": 1}
]

# Write to a JSON file
with open("projects/pods.json", "w") as f:
    json.dump(pods, f, indent=2)

print("✅ Written to pods.json")
```

&nbsp;

**2 →** Run it and look at the file

```bash
python3 projects/json_basics.py
cat projects/pods.json
```

> Beautiful, structured data. This is exactly what `kubectl get pods -o json` gives you.

&nbsp;

**3 →** Now read it back — add this to the same file

```python
# Read it back
with open("projects/pods.json", "r") as f:
    loaded = json.load(f)

for pod in loaded:
    print(f"{pod['name']:20s} → {pod['status']}")
```

&nbsp;

**4 →** Run it again

```bash
python3 projects/json_basics.py
```

> You just wrote data to JSON and read it back. That's how configs, API responses, and ML metadata all work.

&nbsp;

---

&nbsp;

## Part 3 — Making API Calls with `requests` `20 min`

&nbsp;

### Why APIs? (30-second version)

An API is a URL you can ask for data. Your browser does this every time you load a page. In AI/ML, you'll call APIs constantly — Ollama for local LLMs, AWS Bedrock for cloud models, Kubernetes API for cluster info, monitoring endpoints for metrics. The `requests` library makes it one line of Python.

&nbsp;

### Do This

**1 →** Make sure `requests` is installed (you did this Day 1)

```bash
pip install requests
```

&nbsp;

**2 →** Create `projects/api_basics.py`

```python
import requests

response = requests.get("https://api.github.com/users/aditiabhang")
data = response.json()

print(f"Name:    {data['name']}")
print(f"Bio:     {data['bio']}")
print(f"Repos:   {data['public_repos']}")
print(f"Status:  {response.status_code}")
```

&nbsp;

**3 →** Run it

```bash
python3 projects/api_basics.py
```

> You just talked to GitHub's servers and got live data back — as JSON. Every ML inference endpoint works exactly like this: send a request, get JSON back.

&nbsp;

**4 →** Try another one — a random fact API

```python
import requests

response = requests.get("https://catfact.ninja/fact")
fact = response.json()
print(f"🐱 {fact['fact']}")
```

> Every public API works the same way. `requests.get(url)` → `.json()` → use it.

&nbsp;

---

&nbsp;

## Part 4 — Error Handling: try/except `10 min`

&nbsp;

### Why? (30-second version)

APIs go down. Files go missing. Networks fail. If you don't handle errors, your script crashes and you get a wall of red text. `try/except` says: "try this risky thing, and if it blows up, do this instead." That's it.

&nbsp;

### Do This

**1 →** Create `projects/error_handling.py`

```python
import requests

try:
    response = requests.get("https://api.github.com/users/aditiabhang", timeout=5)
    response.raise_for_status()
    data = response.json()
    print(f"✅ Got data for {data['name']}")
except requests.exceptions.ConnectionError:
    print("❌ Can't reach the server — check your internet")
except requests.exceptions.Timeout:
    print("❌ Request timed out — server too slow")
except requests.exceptions.HTTPError as e:
    print(f"❌ HTTP error: {e}")
```

&nbsp;

**2 →** Run it

```bash
python3 projects/error_handling.py
```

> Works fine. Now try changing the URL to something fake (`https://api.github.com/users/thispersondoesnotexist99999`) and run again. Your script handles it gracefully instead of crashing.

&nbsp;

### The pattern you'll use everywhere

```python
try:
    # risky stuff here
except SomeError:
    # what to do if it fails
```

> Don't overthink it. Wrap risky stuff so your script doesn't crash. That's the whole lesson.

&nbsp;

---

&nbsp;

## Part 5 — Mini-Project: K8s Pod Status Logger `15 min`

&nbsp;

### The Goal

Build a script that ties together everything from today: dicts, JSON, file I/O, API calls, and error handling. It simulates what a real K8s monitoring tool does.

&nbsp;

### Do This

**1 →** Create `projects/pod_status_logger.py`

```python
import json
import requests
from datetime import datetime

# 1. Pod data (like kubectl get pods -o json)
pods = [
    {"name": "nginx-7b8d", "namespace": "default", "status": "Running", "restarts": 0},
    {"name": "redis-3f2a", "namespace": "cache", "status": "Running", "restarts": 2},
    {"name": "ml-api-9c1e", "namespace": "inference", "status": "CrashLoopBackOff", "restarts": 14},
    {"name": "postgres-5d7b", "namespace": "database", "status": "Running", "restarts": 0}
]

# 2. Write pods to JSON file
with open("projects/pod_report.json", "w") as f:
    json.dump({"timestamp": str(datetime.now()), "pods": pods}, f, indent=2)
print("✅ Pod data written to pod_report.json")

# 3. Read it back and print a status report
with open("projects/pod_report.json", "r") as f:
    report = json.load(f)

print(f"\n📊 Pod Status Report — {report['timestamp']}")
print("-" * 55)
for pod in report["pods"]:
    icon = "🟢" if pod["status"] == "Running" else "🔴"
    print(f"  {icon} {pod['name']:20s} {pod['namespace']:12s} {pod['status']}")

unhealthy = [p for p in report["pods"] if p["status"] != "Running"]
print(f"\n⚠️  {len(unhealthy)} pod(s) need attention")

# 4. Simulate an API call (prove you can talk to an endpoint)
try:
    r = requests.get("https://api.github.com", timeout=5)
    print(f"\n🌐 API check: GitHub API responded with {r.status_code}")
except requests.exceptions.RequestException:
    print("\n🌐 API check: Could not reach endpoint")
```

&nbsp;

**2 →** Run it

```bash
python3 projects/pod_status_logger.py
```

> You should see a formatted report, a JSON file on disk, and a live API check. That's a baby version of what Prometheus, Datadog, and every K8s monitoring tool does.

&nbsp;

**3 →** Check the JSON file

```bash
cat projects/pod_report.json
```

> Real, structured data with a timestamp. This is production-style logging.

&nbsp;

---

&nbsp;

## Part 6 — Commit Your Work `10 min`

&nbsp;

### Do This

**1 →** Write your daily log (`daily-logs/week-01/day-04.md`)

```markdown
# Day 4 — Python: Files, JSON & APIs

## What I did
- Read/wrote files with open() and context managers
- Parsed and created JSON with the json module
- Made live API calls with requests
- Built a K8s pod status logger

## What I learned
- (fill in)

## What confused me
- (fill in)
```

&nbsp;

**2 →** Push it

```bash
git add .
git commit -m "day 4: python file I/O, JSON, API calls, pod status logger"
git push
```

&nbsp;

---

&nbsp;

## ✅ Day 4 Checklist

| | Task |
|---|------|
| ☐ | Read and wrote a text file with `open()` |
| ☐ | Used `with` statement (context manager) |
| ☐ | Wrote a Python dict to a JSON file |
| ☐ | Read a JSON file back into Python |
| ☐ | Made a GET request with `requests` |
| ☐ | Parsed JSON from an API response |
| ☐ | Used try/except for error handling |
| ☐ | Built the pod status logger mini-project |
| ☐ | Daily log written and pushed 🟩 |

&nbsp;

---

&nbsp;

## 🧠 Concepts You Now Own

| Concept | One-liner |
|---------|-----------|
| **open()** | Python's way to read/write files |
| **Context manager** | `with` auto-closes the file for you |
| **JSON** | A dict that lives in a file — the universal data format |
| **json.load/dump** | File ↔ Python dict |
| **json.loads/dumps** | String ↔ Python dict |
| **requests.get()** | One-line HTTP call to any API |
| **response.json()** | Parse the API response into a Python dict |
| **try/except** | Wrap risky stuff so your script doesn't crash |
| **status_code** | 200 = good, 404 = not found, 500 = server broke |

&nbsp;

---

&nbsp;

> *Tomorrow: Podman deep dive — you'll build your own container image and ship your Python scripts inside it.*
> *Your code leaves the laptop and enters a container. That's when things get real. 🐳*
