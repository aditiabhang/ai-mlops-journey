# Day 5 Notes — Podman Deep Dive + Flask API Project

---

## What I Did Today

- Learned how Containerfiles work — instructions, layers, and caching
- Built my first custom container image (`hello-container`) with Podman
- Learned port mapping (`-p`) and volumes (`-v`)
- Built a Flask API with `/health` and `/pods` endpoints
- Wrote a Containerfile for the Flask app — proper layer ordering for cache efficiency
- Built and ran the containerized Flask API with `podman build` and `podman run`
- Tested both endpoints with `curl` from another terminal
- Pushed the full Week 1 project to GitHub

---

## How Container Images Work

### Containerfile = A Recipe

Each line is a step. Each step creates a **layer**. Layers are cached — unchanged layers get skipped on rebuild.

```dockerfile
FROM python:3.11-slim       ← Layer 1: base image (cached after first pull)
WORKDIR /app                ← Layer 2: set working dir
COPY requirements.txt .     ← Layer 3: copy deps file
RUN pip install -r req...   ← Layer 4: install packages (cached if deps unchanged)
COPY . .                    ← Layer 5: copy code (only this rebuilds when code changes)
CMD ["python", "app.py"]    ← Layer 6: run command
```

**The trick:** Copy `requirements.txt` BEFORE copying your code. If your code changes but dependencies don't, Podman reuses the cached pip install layer. Builds go from minutes to seconds.

### Key Instructions

| Instruction | What it does |
|-------------|-------------|
| `FROM` | Base image — your starting point |
| `WORKDIR` | Set working directory inside container |
| `COPY` | Copy files from host into container |
| `RUN` | Execute a command during build (install packages) |
| `EXPOSE` | Document which port the app uses (doesn't actually open it) |
| `CMD` | Default command when container starts |

> `Containerfile` = `Dockerfile`. Same syntax. Podman prefers the name Containerfile, but both work.

---

## Port Mapping & Volumes

### Port Mapping (`-p`)

Containers are isolated. Your app runs on port 5000 inside, but your laptop can't see it. `-p` creates a tunnel:

```
podman run -p 8080:5000 my-app
              │     │
              │     └── port INSIDE the container
              └──────── port on YOUR machine
```

### Volumes (`-v`)

Shared folder between host and container. Changes on either side show up on the other:

```bash
podman run -v /my/local/folder:/app/data my-app
```

| Use case | Use |
|----------|-----|
| Access app from browser | Port mapping (`-p`) |
| Container reads/writes host files | Volume (`-v`) |
| Live code reloading during dev | Volume (`-v`) |
| Production deployment | Neither — everything baked into image |

---

## Week 1 Project: Flask API in a Container

### What I Built

A Flask API with two endpoints, containerized with Podman:

- `GET /health` → returns `{"status": "healthy"}` — every production API needs this
- `GET /pods` → returns simulated Kubernetes pod statuses as JSON

### The Flask App (`app.py`)

```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/health")
def health():
    return jsonify({"status": "healthy"})

@app.route("/pods")
def pods():
    pod_statuses = [
        {"name": "nginx-7b8d", "status": "Running", "restarts": 0},
        {"name": "redis-3f2a", "status": "CrashLoopBackOff", "restarts": 5},
        ...
    ]
    return jsonify({"pods": pod_statuses})
```

- `@app.route("/health")` → decorator that maps a URL path to a function
- `jsonify()` → converts a Python dict to a proper JSON HTTP response
- Flask runs a dev server on port 5000 by default

### The Containerfile

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
EXPOSE 5000
CMD ["python", "app.py"]
```

### Build & Run Commands

```bash
podman build -t my-flask-api .        # build the image
podman run -p 5000:5000 my-flask-api  # run it with port mapping

# Test from another terminal:
curl http://localhost:5000/health      # {"status": "healthy"}
curl http://localhost:5000/pods        # {"pods": [...]}
```

### Useful Podman Commands

| Command | What it does |
|---------|-------------|
| `podman build -t name .` | Build image from Containerfile in current dir |
| `podman run -p 5000:5000 name` | Run container with port mapping |
| `podman images` | List all images on your machine |
| `podman ps` | List running containers |
| `podman ps -a` | List ALL containers (including stopped) |
| `podman stop <id>` | Stop a running container |
| `podman rm <id>` | Remove a stopped container |
| `podman rmi <image>` | Remove an image |

---

## How This Week Connects

| Day | What I learned | How it builds |
|-----|---------------|---------------|
| Day 1 | Dev environment, ran first container | Foundation |
| Day 2 | K8s hands-on — deployed nginx, debugged ImagePullBackOff | Operating clusters |
| Day 3 | Python fundamentals — variables, loops, functions, dicts | The language |
| Day 4 | File I/O, JSON, APIs, error handling, pod status logger | Python talks to the outside world |
| Day 5 | Containerfile, Podman build, Flask API containerized | **Shipped a real project** |

> Day 1: "What is a container?" → Day 5: "I built and shipped one."

---

## Things I Learned

- **Layer ordering matters.** Copy dependencies before code. It's a small detail that makes a huge difference in build times. This is the kind of thing that separates "I followed a tutorial" from "I understand how it works."

- **`/health` endpoints are non-negotiable.** Every production service needs one. Kubernetes uses them (liveness/readiness probes), load balancers use them, monitoring uses them. It's the first endpoint you write.

- **Containers are just processes with walls.** They feel magical until you realize it's just: take a Linux process, give it its own filesystem (the image), its own network (port mapping), and isolate it. That's it.

- **Flask is dead simple for APIs.** Three lines to get a JSON endpoint running. It's why it's the go-to for ML model serving — wrap your model in a Flask app, containerize it, deploy.

---

## What Confused Me

- The difference between `EXPOSE` and `-p`. `EXPOSE` is just documentation in the Containerfile — it doesn't actually open the port. You still need `-p` at runtime to create the actual tunnel.
- Why `--no-cache-dir` in `pip install`? Keeps the image smaller — pip won't store downloaded package files inside the container.

---

## Week 1 Reflection

- **Hardest part:** Day 2 — debugging the ImagePullBackOff error. Minikube's VM couldn't reach Docker Hub, and figuring out it was a DNS issue inside the VM took a while. But that's the exact kind of debugging I'll do in production.

- **What clicked:** The connection between everything. Python reads JSON, APIs return JSON, Kubernetes speaks JSON, containers run Python. It's all the same data flowing through different tools.

- **Most proud of:** The Flask API project. Five days ago I had nothing installed. Now I have a containerized API running with endpoints I wrote, an image I built, and it's all pushed to GitHub.

---

## What I Want to Explore Next

- Deploy this Flask API on Kubernetes (that's Week 2!)
- Add a `/predict` endpoint that serves a simple ML model
- Learn Kubernetes Services and Ingress to expose it externally
- Try multi-stage builds to make the container image even smaller
