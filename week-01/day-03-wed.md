# Week 1 · Day 3 · Wednesday

## 🎯 Python Crash Course — The Essentials

`90 min` · `Needs: Python 3.10+ from Day 1` · `No prior Python needed`

---

&nbsp;

## Today's Big Picture

> Yesterday you deployed containers. Today you learn the language that controls them.
> Every AI model, every ML pipeline, every automation script — it's Python.

By the end of today, you'll have:

- ✅ Variables, data types, and f-strings down cold
- ✅ Lists and dicts — the data structures AI/ML lives on
- ✅ Loops and conditionals working
- ✅ Written your own functions
- ✅ Built a mini pod health checker that ties K8s + Python together

&nbsp;

---

&nbsp;

## Part 1 — Why Python for AI `5 min`

&nbsp;

### Why Python? (30-second version)

Python is the universal language of AI. TensorFlow, PyTorch, LangChain, Hugging Face, Kubernetes client libraries — all Python. It reads like English, it's forgiving, and it has a package for literally everything. You don't need to master it — you need to be dangerous enough to read code and write small scripts.

&nbsp;

### How to run these examples

Every code block below — type it into your terminal like this:

```bash
python3
```

> This opens the Python REPL (interactive mode). Type code line by line. Type `exit()` when done.

Or save code to a `.py` file and run it:

```bash
python3 my_script.py
```

&nbsp;

---

&nbsp;

## Part 2 — Variables & Data Types `15 min`

&nbsp;

### What are variables? (30-second version)

A variable is a label you stick on a piece of data. No need to declare types — Python figures it out. You just write `name = "nginx"` and you're done.

&nbsp;

### Do This

**1 →** Open the Python REPL

```bash
cd ~/projects/ai-mlops-journey
source .venv/bin/activate
python3
```

&nbsp;

**2 →** Try the basic data types

```python
name = "nginx"          # string — text
replicas = 3            # int — whole number
cpu_usage = 72.5        # float — decimal number
is_healthy = True       # boolean — True or False
```

&nbsp;

**3 →** Check types with `type()`

```python
print(type(name))       # <class 'str'>
print(type(replicas))   # <class 'int'>
print(type(cpu_usage))  # <class 'float'>
print(type(is_healthy)) # <class 'bool'>
```

&nbsp;

**4 →** Use f-strings to build readable output

```python
pod_name = "my-web-abc123"
status = "Running"
print(f"Pod {pod_name} is {status}")
```

> f-strings are how you drop variables into text. Put `f` before the quote, then `{variable}` inside. You'll use these constantly.

&nbsp;

**5 →** Quick math

```python
total_pods = 3
healthy = 2
unhealthy = total_pods - healthy
print(f"{unhealthy} pod(s) need attention")
```

&nbsp;

---

&nbsp;

## Part 3 — Lists & Dicts `15 min`

&nbsp;

### What are lists and dicts? (30-second version)

A **list** is an ordered collection — think of it as a column in a spreadsheet. A **dict** (dictionary) is a set of key-value pairs — think of it as a row with labeled columns. In AI/ML, your data is almost always a list of dicts. API responses, training data, pod statuses — all lists of dicts.

&nbsp;

### Do This

**1 →** Create a list

```python
pods = ["nginx-abc", "redis-def", "api-ghi"]
print(pods[0])          # nginx-abc (first item)
print(len(pods))        # 3
```

&nbsp;

**2 →** Add and remove items

```python
pods.append("worker-jkl")   # add to end
print(pods)
pods.remove("redis-def")    # remove by value
print(pods)
```

&nbsp;

**3 →** Create a dict

```python
pod = {
    "name": "nginx-abc",
    "status": "Running",
    "restarts": 0
}
print(pod["name"])      # nginx-abc
print(pod["status"])    # Running
```

&nbsp;

**4 →** A list of dicts — this is the big one

```python
pods = [
    {"name": "nginx-abc", "status": "Running"},
    {"name": "redis-def", "status": "CrashLoopBackOff"},
    {"name": "api-ghi", "status": "Running"},
]
```

> This is what real data looks like. API responses from Kubernetes, JSON from LLMs, training datasets — all structured like this.

&nbsp;

**5 →** Loop through a list of dicts

```python
for pod in pods:
    print(f"{pod['name']} → {pod['status']}")
```

&nbsp;

---

&nbsp;

## Part 4 — Conditionals & Loops `15 min`

&nbsp;

### What are these? (30-second version)

**Conditionals** let your code make decisions — "if this, do that." **Loops** let your code repeat work — "do this for every item in the list." Together they're how you automate anything.

&nbsp;

### Do This

**1 →** if / elif / else

```python
status = "CrashLoopBackOff"

if status == "Running":
    print("✅ Pod is healthy")
elif status == "Pending":
    print("⏳ Pod is starting up")
else:
    print(f"❌ Problem: {status}")
```

> Indentation matters in Python. Use 4 spaces (VS Code does this automatically).

&nbsp;

**2 →** for loop — iterate over a list

```python
services = ["nginx", "redis", "postgres"]
for svc in services:
    print(f"Checking {svc}...")
```

&nbsp;

**3 →** range() — when you need numbers

```python
for i in range(5):
    print(f"Attempt {i + 1}")
```

> `range(5)` gives you 0, 1, 2, 3, 4. Five numbers, starting from zero.

&nbsp;

**4 →** enumerate() — when you need the index AND the item

```python
pods = ["nginx", "redis", "api"]
for i, pod in enumerate(pods):
    print(f"Pod #{i + 1}: {pod}")
```

&nbsp;

**5 →** while loop — repeat until a condition is false

```python
retries = 0
while retries < 3:
    print(f"Retry #{retries + 1}")
    retries += 1
print("Giving up.")
```

> While loops are great for retry logic — "keep trying until it works or you've tried N times."

&nbsp;

---

&nbsp;

## Part 5 — Functions `15 min`

&nbsp;

### What are functions? (30-second version)

A function is a reusable block of code. Instead of copying the same 5 lines everywhere, you wrap them in a function and call it by name. `def` means "I'm defining a function."

&nbsp;

### Do This

**1 →** Write a simple function

```python
def greet(name):
    print(f"Hello, {name}!")

greet("Aditi")
greet("Kubernetes")
```

&nbsp;

**2 →** Return a value

```python
def is_healthy(status):
    return status == "Running"

print(is_healthy("Running"))         # True
print(is_healthy("CrashLoopBackOff")) # False
```

&nbsp;

**3 →** Default parameters

```python
def check_pod(name, status="Unknown"):
    print(f"{name}: {status}")

check_pod("nginx", "Running")   # nginx: Running
check_pod("redis")              # redis: Unknown
```

> Default params are useful when data might be missing — common in API responses.

&nbsp;

**4 →** A function that takes a list

```python
def count_healthy(pods):
    healthy = 0
    for pod in pods:
        if pod["status"] == "Running":
            healthy += 1
    return healthy

pods = [
    {"name": "a", "status": "Running"},
    {"name": "b", "status": "Failed"},
    {"name": "c", "status": "Running"},
]
print(f"Healthy: {count_healthy(pods)}/{len(pods)}")
```

&nbsp;

---

&nbsp;

## Part 6 — Mini-Project: Pod Health Checker `15 min`

&nbsp;

### The Goal

Build a Python script that takes a list of pods (as dicts), checks their status, and prints a health report. This ties your K8s knowledge from yesterday to Python today.

&nbsp;

### Do This

**1 →** Create the file

```bash
mkdir -p projects/pod-checker
touch projects/pod-checker/health_check.py
```

&nbsp;

**2 →** Write this script in `projects/pod-checker/health_check.py`

```python
# Pod Health Checker — ties K8s + Python together

pods = [
    {"name": "nginx-abc12", "status": "Running", "restarts": 0},
    {"name": "redis-def34", "status": "CrashLoopBackOff", "restarts": 5},
    {"name": "api-ghi56", "status": "Running", "restarts": 1},
    {"name": "worker-jkl78", "status": "Pending", "restarts": 0},
    {"name": "db-mno90", "status": "Running", "restarts": 0},
]

def check_pods(pod_list):
    healthy = []
    unhealthy = []

    for pod in pod_list:
        if pod["status"] == "Running":
            healthy.append(pod["name"])
        else:
            unhealthy.append(pod)

    return healthy, unhealthy

def print_report(healthy, unhealthy):
    total = len(healthy) + len(unhealthy)
    print(f"\n🩺 Pod Health Report")
    print(f"{'='*30}")
    print(f"Total pods: {total}")
    print(f"✅ Healthy:  {len(healthy)}")
    print(f"❌ Unhealthy: {len(unhealthy)}")

    if unhealthy:
        print(f"\n⚠️  Pods needing attention:")
        for pod in unhealthy:
            print(f"   → {pod['name']} ({pod['status']}, "
                  f"{pod['restarts']} restarts)")
    else:
        print("\n🎉 All pods healthy!")

# Run it
healthy, unhealthy = check_pods(pods)
print_report(healthy, unhealthy)
```

&nbsp;

**3 →** Run it

```bash
python3 projects/pod-checker/health_check.py
```

> You should see a clean health report showing 3 healthy pods and 2 that need attention. You just wrote a tool that a support engineer would actually use.

&nbsp;

**4 →** Try breaking it — change a pod status to `"ImagePullBackOff"` and re-run. Add a 6th pod. Make it yours.

&nbsp;

---

&nbsp;

## Part 7 — Commit Your Work `10 min`

&nbsp;

### Do This

**1 →** Write your daily log (`daily-logs/week-01/day-03.md`)

```markdown
# Day 3 — Python Crash Course

## What I did
- Learned variables, types, f-strings
- Lists and dicts — the data structures behind everything
- Loops, conditionals, functions
- Built a pod health checker script

## What I learned
- (fill in)

## What confused me
- (fill in)

## Code I want to remember
- f-strings: f"Pod {name} is {status}"
- list of dicts: [{"key": "val"}, {"key": "val"}]
- for item in list: / if condition:
- def my_func(arg): return something
```

&nbsp;

**2 →** Push everything

```bash
git add .
git commit -m "day 3: python essentials — variables, loops, functions, pod health checker"
git push
```

&nbsp;

---

&nbsp;

## ✅ Day 3 Checklist

| | Task |
|---|------|
| ☐ | Can create variables (str, int, float, bool) |
| ☐ | Can use f-strings to format output |
| ☐ | Can create and loop through lists |
| ☐ | Can create dicts and access values by key |
| ☐ | Can write if/elif/else logic |
| ☐ | Can write for loops and while loops |
| ☐ | Can define and call functions with arguments |
| ☐ | Pod health checker script runs and prints a report |
| ☐ | Daily log written and pushed 🟩 |

&nbsp;

---

&nbsp;

## 🧠 Concepts You Now Own

| Concept | One-liner |
|---------|-----------|
| **Variable** | A label stuck on a piece of data |
| **String / Int / Float / Bool** | The four basic data types |
| **f-string** | Drop variables into text: `f"hello {name}"` |
| **List** | Ordered collection — `["a", "b", "c"]` |
| **Dict** | Key-value pairs — `{"name": "nginx"}` |
| **List of dicts** | How real data is structured (APIs, JSON, datasets) |
| **for loop** | "Do this for every item in the list" |
| **while loop** | "Keep doing this until the condition is false" |
| **Function (def)** | Reusable block of code you call by name |
| **return** | How a function sends data back to the caller |

&nbsp;

---

&nbsp;

> *Tomorrow: Python continued — file I/O, JSON, and talking to APIs.*
> *You just learned to think in Python. Tomorrow you teach Python to talk to the outside world. 🌐*
