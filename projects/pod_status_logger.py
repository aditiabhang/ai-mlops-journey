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