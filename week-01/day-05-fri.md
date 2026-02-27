# Week 1 · Day 5 · Friday

## 🎯 Podman Deep Dive + Week 1 Project

`90 min` · `Needs: Podman, Python, Flask` · `This is the big one — you ship today 🚀`

---

&nbsp;

## Today's Big Picture

> On Day 1 you ran `hello-world` in a container. Cool party trick.
> Today you build your own container from scratch and ship a real API.
> This is what MLOps engineers do every single day.

By the end of today, you'll have:

- ✅ Understand how container images are built (layers, caching)
- ✅ Written your own Containerfile from scratch
- ✅ Built and run a custom image with Podman
- ✅ Understand port mapping and volumes
- ✅ Built a Flask API and containerized it
- ✅ Your Week 1 project — live, tested, and pushed 🎉

&nbsp;

---

&nbsp;

## Part 1 — How Container Images Work `15 min`

&nbsp;

### What is a Containerfile? (30-second version)

A Containerfile is a recipe. Each line is a step. The result is an image. You run the image to get a container.

> Containerfile = Dockerfile. Same syntax, same everything. Podman just prefers the name "Containerfile." If you see `Dockerfile` in a tutorial, it works with Podman too — no changes needed.

&nbsp;

### Layers — Why Rebuilds Are Fast

Every instruction in your Containerfile creates a **layer**. Layers are cached. If nothing changed in a layer, Podman skips it on rebuild.

```
FROM python:3.11-slim       ← Layer 1: base image (cached after first pull)
WORKDIR /app                ← Layer 2: set working dir (instant)
COPY requirements.txt .     ← Layer 3: copy requirements file
RUN pip install -r req...   ← Layer 4: install packages (cached if req.txt unchanged)
COPY . .                    ← Layer 5: copy your code (only this rebuilds when you edit code)
CMD ["python", "app.py"]    ← Layer 6: what to run when container starts
```

> This is why you copy `requirements.txt` before copying your code. If your code changes but your dependencies don't, Podman reuses the cached pip install layer. Builds go from minutes to seconds.

&nbsp;

### Key Containerfile Instructions

| Instruction | What it does |
|-------------|-------------|
| `FROM` | Starting image — your foundation |
| `WORKDIR` | Set the working directory inside the container |
| `COPY` | Copy files from your machine into the container |
| `RUN` | Run a command during build (install packages, etc.) |
| `EXPOSE` | Document which port the app uses (doesn't actually open it) |
| `CMD` | The default command when the container starts |

&nbsp;

---

&nbsp;

## Part 2 — Build Your First Image `15 min`

&nbsp;

### Do This

**1 →** Create a project folder

```bash
mkdir -p ~/projects/ai-mlops-journey/projects/hello-container
cd ~/projects/ai-mlops-journey/projects/hello-container
```

&nbsp;

**2 →** Create a simple Python script

Create a file called `hello.py`:

```python
print("🐳 Hello from inside a container!")
print("This image was built with Podman.")
print("I wrote the Containerfile myself. No hand-holding.")
```

&nbsp;

**3 →** Create the Containerfile

Create a file called `Containerfile` (no extension):

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY hello.py .
CMD ["python", "hello.py"]
```

> That's it. Four lines. Base image → set directory → copy code → run it.

&nbsp;

**4 →** Build it

```bash
podman build -t hello-container .
```

> `-t hello-container` gives your image a name (a "tag"). The `.` means "use the Containerfile in this directory."

&nbsp;

**5 →** Run it

```bash
podman run hello-container
```

> You should see your three print statements. You just ran your own code inside a container you built yourself. 🎉

&nbsp;

**6 →** See your images and containers

```bash
podman images
podman ps -a
```

> `podman images` shows all images on your machine. `podman ps -a` shows all containers (including stopped ones).

&nbsp;

---

&nbsp;

## Part 3 — Port Mapping & Volumes `10 min`

&nbsp;

### Port Mapping (30-second version)

Containers are isolated. Your app inside runs on port 5000, but your laptop can't see it. `-p` creates a tunnel.

```
podman run -p 8080:5000 my-app
              │     │
              │     └── port inside the container
              └──────── port on YOUR machine
```

> So `localhost:8080` on your machine → hits port `5000` inside the container. You'll use this for the Flask project in 5 minutes.

&nbsp;

### Volumes (30-second version)

A volume is a shared folder between your machine and the container. Changes on either side show up on the other.

```bash
podman run -v /my/local/folder:/app/data my-app
```

> Everything in `/my/local/folder` on your machine appears at `/app/data` inside the container. Great for:
> - Sharing datasets with ML containers
> - Persisting database files
> - Live-reloading code during development

&nbsp;

### When to Use Each

| Situation | Use |
|-----------|-----|
| "I need to access my app from a browser" | Port mapping (`-p`) |
| "I need my container to read/write files on my machine" | Volume (`-v`) |
| "I'm developing and want live code changes" | Volume (`-v`) |
| "I'm shipping to production" | Neither — everything is baked into the image |

&nbsp;

---

&nbsp;

## Part 4 — 🎉 Week 1 Project: Flask API in a Container `35 min`

&nbsp;

> This is it. Everything from this week comes together.
> You're building a real API, containerizing it, and shipping it.

&nbsp;

### Step 1 → Set up the project

```bash
mkdir -p ~/projects/ai-mlops-journey/projects/01-flask-api
cd ~/projects/ai-mlops-journey/projects/01-flask-api
```

&nbsp;

### Step 2 → Create a virtual environment and install Flask

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install flask
```

&nbsp;

### Step 3 → Create the Flask app

Create a file called `app.py`:

```python
from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/health")
def health():
    return jsonify({"status": "healthy"})


@app.route("/pods")
def pods():
    pod_statuses = [
        {"name": "nginx-7b8d6c5d9-abc12", "status": "Running", "restarts": 0},
        {"name": "nginx-7b8d6c5d9-def34", "status": "Running", "restarts": 1},
        {"name": "nginx-7b8d6c5d9-ghi56", "status": "CrashLoopBackOff", "restarts": 5},
    ]
    return jsonify({"pods": pod_statuses})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

> Two endpoints. `/health` returns a status check (every production API has one). `/pods` returns fake Kubernetes pod statuses — tying back to what you learned on Day 2.

&nbsp;

### Step 4 → Create requirements.txt

```bash
pip freeze > requirements.txt
```

> Or just create a `requirements.txt` file with one line:

```
flask
```

> Either works. The minimal version is cleaner.

&nbsp;

### Step 5 → Test it locally first

```bash
python3 app.py
```

Open another terminal:

```bash
curl http://localhost:5000/health
curl http://localhost:5000/pods
```

> You should see JSON responses. Kill the server with `Ctrl+C` once you've confirmed it works.

&nbsp;

### Step 6 → Write the Containerfile

Create a file called `Containerfile` in the `01-flask-api/` folder:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]
```

> Line by line:
> 1. Start from a slim Python image
> 2. Set `/app` as the working directory
> 3. Copy requirements first (for layer caching)
> 4. Install dependencies
> 5. Copy your app code
> 6. Document that port 5000 is used
> 7. Run the app when the container starts

&nbsp;

### Step 7 → Build the image

```bash
podman build -t my-flask-api .
```

> Watch the layers build. First time takes a minute (downloading the base image). Rebuilds will be fast thanks to caching.

&nbsp;

### Step 8 → Run it in a container

```bash
podman run -p 5000:5000 my-flask-api
```

> Your Flask app is now running inside a container. Port 5000 on your machine tunnels to port 5000 in the container.

&nbsp;

### Step 9 → Test it

Open another terminal:

```bash
curl http://localhost:5000/health
```

```json
{"status": "healthy"}
```

```bash
curl http://localhost:5000/pods
```

```json
{"pods": [{"name": "nginx-7b8d6c5d9-abc12", "restarts": 0, "status": "Running"}, ...]}
```

> 🎉 **You just containerized and shipped a Flask API.** Open `http://localhost:5000/health` in your browser to see it there too.

&nbsp;

### Step 10 → Stop the container

Press `Ctrl+C` in the terminal running the container. Or:

```bash
podman ps
podman stop <container-id>
```

&nbsp;

---

&nbsp;

## Part 5 — Commit & Push Week 1 Project `10 min`

&nbsp;

### Do This

**1 →** Deactivate the virtual environment

```bash
deactivate
```

&nbsp;

**2 →** Make sure `.venv/` is in `.gitignore`

```bash
cd ~/projects/ai-mlops-journey
echo ".venv/" >> projects/01-flask-api/.gitignore
```

&nbsp;

**3 →** Write your daily log (`daily-logs/week-01/day-05.md`)

```markdown
# Day 5 — Podman Deep Dive + Flask API Project

## What I did
- Learned how Containerfiles and image layers work
- Built my first custom container image
- Learned port mapping and volumes
- Built a Flask API with /health and /pods endpoints
- Containerized it and ran it with Podman

## What I learned
- (fill in)

## What confused me
- (fill in)

## Week 1 reflection
- (what was hardest? what clicked? what are you most proud of?)
```

&nbsp;

**4 →** Push it all

```bash
git add projects/01-flask-api/
git add projects/hello-container/
git add daily-logs/week-01/day-05.md
git commit -m "day 5: week 1 project — flask api containerized with podman 🚀"
git push
```

> 🟩 That green square means something today. You shipped a real project.

&nbsp;

---

&nbsp;

## ✅ Week 1 Checklist (Full Week Review)

| | Task |
|---|------|
| ☐ | Dev environment set up (Python, Podman, kubectl, minikube) |
| ☐ | GitHub repo created with folder structure |
| ☐ | Deployed nginx on Kubernetes, scaled it, watched self-healing |
| ☐ | Python fundamentals — variables, loops, functions, dicts |
| ☐ | Read the Kubernetes API with Python |
| ☐ | Understand Containerfile instructions and layers |
| ☐ | Built a custom container image with Podman |
| ☐ | Understand port mapping (`-p`) and volumes (`-v`) |
| ☐ | **Week 1 Project: Flask API containerized and running** 🎉 |
| ☐ | All daily logs written and pushed |
| ☐ | **5 days of commits pushed** 🟩🟩🟩🟩🟩 |

&nbsp;

---

&nbsp;

## 🧠 Concepts You Now Own

| Concept | One-liner |
|---------|-----------|
| **Containerfile** | A recipe — line-by-line instructions to build an image |
| **Image** | The blueprint — built from a Containerfile |
| **Container** | A running instance of an image |
| **Layer** | Each Containerfile instruction = a cached layer |
| **Layer caching** | Unchanged layers are skipped on rebuild (fast!) |
| **`podman build`** | Build an image from a Containerfile |
| **`podman run`** | Create and start a container from an image |
| **Port mapping (`-p`)** | Tunnel: your machine's port → container's port |
| **Volume (`-v`)** | Shared folder between your machine and the container |
| **Flask** | Lightweight Python web framework — perfect for APIs |
| **`/health` endpoint** | Every production API has one — "am I alive?" |

&nbsp;

---

&nbsp;

## 🎉 Week 1 Wrap-Up

You started Monday with nothing installed.

Five days later, you can:

- Spin up a Kubernetes cluster and deploy apps on it
- Write Python scripts that do useful things
- Build container images from scratch
- Ship a Flask API inside a container

That's not "learning." That's **building.** You have a GitHub repo with green squares and a real project to prove it.

Most people are still watching YouTube tutorials. You're shipping.

&nbsp;

---

&nbsp;

> *Next week: **Week 2 — Kubernetes Fundamentals.** You'll deploy THIS Flask API on Kubernetes.*
> *The container you built today? It's about to run on a real cluster. See you Monday. 🔥*
