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

# Read it back
with open("projects/pods.json", "r") as f:
    loaded = json.load(f)

for pod in loaded:
    print(f"{pod['name']:20s} → {pod['status']}")