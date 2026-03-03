# Day 3 — Python Crash Course

## What I did
- Learned variables, types, f-strings
- Lists and dicts — the data structures behind everything
- Loops, conditionals, functions
- Built a pod health checker script

## What I learned
- Python dicts are the building block for JSON/K8s manifests — everything is key-value pairs
- f-strings make log output clean and readable without string concatenation
- List comprehensions are a concise way to filter/transform data (e.g., filtering unhealthy pods)
- Functions keep scripts reusable — wrote `check_pod_health()` and called it on a list of pods

## What confused me
- When to use a list of dicts vs a dict of dicts — both can represent pod data
- Mutable default arguments in functions (e.g., `def f(items=[])`) can cause unexpected behavior

## Code I want to remember
- f-strings: f"Pod {name} is {status}"
- list of dicts: [{"key": "val"}, {"key": "val"}]
- for item in list: / if condition:
- def my_func(arg): return something