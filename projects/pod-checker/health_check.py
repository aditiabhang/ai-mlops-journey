# Pod Health Checker — ties K8s + Python together

pods = [
    {"name": "nginx-abc12", "status": "Running", "restarts": 0},
    {"name": "redis-def34", "status": "CrashLoopBackOff", "restarts": 5},
    {"name": "api-ghi56", "status": "ImagePullBackOff", "restarts": 1},
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