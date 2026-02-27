# Week 1 · Day 1 · Monday

## 🎯 Environment Setup + GitHub Repo

`90 min` · `No prior knowledge needed` · `All free tools`

---

&nbsp;

## Today's Big Picture

> You're building a workbench before you build anything.
> Every carpenter sets up their tools first — today you're that carpenter.

By the end of today, you'll have:

- ✅ A GitHub repo that tracks your entire 12-week journey
- ✅ Python running on your machine
- ✅ Docker installed and verified
- ✅ kubectl + minikube ready for Kubernetes
- ✅ VS Code with the right extensions
- ✅ Your first commit pushed 🟩

&nbsp;

---

&nbsp;

## Part 1 — Git + GitHub Repo `15 min`

&nbsp;

### What is Git? (30-second version)

Git is a time machine for your code. Every time you "commit," you're saving a snapshot. You can always go back. GitHub is where those snapshots live online so the world (and recruiters) can see them.

&nbsp;

### Do This

**1 →** Check if Git is installed

```bash
git --version
```

> If you see a version number, you're good. If not → [install Git](https://git-scm.com/downloads)

&nbsp;

**2 →** Create your journey repo on GitHub

- Go to [github.com/new](https://github.com/new)
- Repo name: `ai-mlops-journey`
- Set to **Public**
- Check ✅ "Add a README file"
- Click **Create repository**

&nbsp;

**3 →** Clone it to your machine

```bash
cd ~/projects    # or wherever you keep code
git clone https://github.com/YOUR-USERNAME/ai-mlops-journey.git
cd ai-mlops-journey
```

&nbsp;

**4 →** Create the folder structure

```bash
mkdir -p daily-logs/week-01
mkdir -p projects
mkdir -p cheatsheets
mkdir -p certifications/kcna-notes
mkdir -p certifications/aws-ai-notes
```

&nbsp;

**5 →** Make your first daily log

Create a file `daily-logs/week-01/day-01.md` and write:

```markdown
# Day 1 — Setup Day

## What I did
- Set up dev environment
- Created this repo

## What I learned
- (fill in at end of session)

## What confused me
- (fill in at end of session)
```

&nbsp;

**6 →** Push it

```bash
git add .
git commit -m "day 1: initial repo setup"
git push
```

> 🟩 That's your first green square. One down, 59 to go.

&nbsp;

---

&nbsp;

## Part 2 — Python `15 min`

&nbsp;

### What is Python? (30-second version)

Python is the language AI speaks. Almost every ML tool, every LLM library, every data pipeline is written in Python. You don't need to be an expert — you need to be comfortable enough to read it and write small scripts.

&nbsp;

### Do This

**1 →** Check if Python is installed

```bash
python3 --version
```

> Need 3.10 or higher. If not installed → [python.org/downloads](https://www.python.org/downloads/)

&nbsp;

**2 →** Set up a virtual environment

A virtual environment is a sandbox. It keeps your project's packages separate from everything else on your machine. Think of it as a clean room for each project.

```bash
cd ~/projects/ai-mlops-journey
python3 -m venv .venv
source .venv/bin/activate    # on Mac/Linux
```

> You should see `(.venv)` in your terminal prompt now. That means you're inside the sandbox.

&nbsp;

**3 →** Install your first package

```bash
pip install requests
```

&nbsp;

**4 →** Quick sanity check — run this in your terminal

```bash
python3 -c "import requests; print('✅ Python is working!')"
```

> If you see `✅ Python is working!` — you're golden.

&nbsp;

**5 →** Add `.venv/` to `.gitignore` so you don't push it

```bash
echo ".venv/" >> .gitignore
```

&nbsp;

---

&nbsp;

## Part 3 — Podman `20 min`

&nbsp;

### What is Podman? (30-second version)

Imagine you built an app on your laptop and it works perfectly. You send it to a friend and it breaks. Different OS, different versions, missing libraries. Containers fix this. They package your app + everything it needs into a tiny, portable box that runs the same everywhere.

Podman does the same thing as Docker — but it's open source, daemonless (no background process hogging memory), and rootless by default (more secure). Every `docker` command you see online? Just swap in `podman`. They're interchangeable.

In the AI world, containers are how models get shipped to production. Every ML pipeline, every inference server, every Kubernetes deployment starts with a container image.

&nbsp;

### Do This

> Assuming you already have **Podman Machine** app installed on your Mac.

&nbsp;

**1 →** Open Podman Machine app and start the machine

- Open **Podman Machine** from your Applications
- Click **Start** (it boots a lightweight Linux VM under the hood)
- Wait until the status shows **Running** ✅

&nbsp;

**2 →** Verify it works in your terminal

```bash
podman --version
podman machine info
```

> You should see the version + machine status. The "machine" is a tiny Linux VM that Podman uses to run containers on macOS.

&nbsp;

**3 →** Run your first container

```bash
podman run hello-world
```

> You should see "Hello from Docker!" (yes, it says Docker — it's the same image from the same registry, Podman just runs it without Docker's daemon).

&nbsp;

**4 →** Understand what just happened

```
You typed:        podman run hello-world
Podman did:       1. Checked if "hello-world" image exists locally → nope
                  2. Asked which registry (pick docker.io)
                  3. Downloaded it from Docker Hub
                  4. Created a container from that image
                  5. Ran it → printed the message
                  6. Container stopped (it's done)
```

&nbsp;

**5 →** Try one more — run a real OS in a container

```bash
podman run -it ubuntu bash
```

> You're now inside an Ubuntu Linux container. Type `ls` to look around. Type `exit` to leave. You just ran a whole Linux OS inside a box on your machine. 🤯

&nbsp;

**6 →** (Optional) Set up the Docker alias so any tutorial works

```bash
echo 'alias docker=podman' >> ~/.zshrc
source ~/.zshrc
```

> Now `docker run`, `docker build`, etc. all just work — they silently call Podman instead.

&nbsp;

---

&nbsp;

## Part 4 — kubectl + minikube `20 min`

&nbsp;

### What is Kubernetes? (30-second version)

Docker runs one container. Kubernetes runs thousands of them, keeps them alive, scales them up when traffic spikes, and restarts them when they crash. It's the operating system for containers. When companies say "we run AI in production," they usually mean "we run AI on Kubernetes."

**kubectl** = the remote control for Kubernetes
**minikube** = a mini Kubernetes cluster that runs on your laptop (for practice)

&nbsp;

### Do This

**1 →** Install kubectl

```bash
# Mac (with Homebrew)
brew install kubectl

# Verify
kubectl version --client
```

> [Other OS instructions](https://kubernetes.io/docs/tasks/tools/)

&nbsp;

**2 →** Install minikube

```bash
# Mac (with Homebrew)
brew install minikube

# Verify
minikube version
```

> [Other OS instructions](https://minikube.sigs.k8s.io/docs/start/)

&nbsp;

**3 →** Start your first cluster

```bash
minikube start
```

> This takes 2-3 minutes the first time. It's downloading a VM and setting up a single-node Kubernetes cluster on your machine.

&nbsp;

**4 →** Talk to your cluster

```bash
kubectl get nodes
```

> You should see one node with status `Ready`. You now have Kubernetes running locally. That's the same technology running Netflix, Spotify, and OpenAI's infrastructure.

&nbsp;

**5 →** Stop it (save battery for now)

```bash
minikube stop
```

&nbsp;

---

&nbsp;

## Part 5 — VS Code Extensions `10 min`

&nbsp;

### Do This

Open VS Code, go to Extensions (`Cmd+Shift+X`), and install:

| Extension | Why |
|-----------|-----|
| **Python** (Microsoft) | Syntax, linting, debugging |
| **Podman** (Podman Desktop extension) | Manage containers visually |
| **Kubernetes** (Microsoft) | See cluster resources in sidebar |
| **YAML** (Red Hat) | K8s manifests are YAML — this validates them |
| **Markdown All in One** | Makes your daily logs look nice |

&nbsp;

---

&nbsp;

## Part 6 — Final Commit `10 min`

&nbsp;

### Do This

**1 →** Go back to your daily log and fill it in

```bash
code daily-logs/week-01/day-01.md
```

Fill in what you learned and what confused you. Be honest — future you will thank present you.

&nbsp;

**2 →** Push everything

```bash
git add .
git commit -m "day 1: dev environment complete — python, podman, kubectl, minikube"
git push
```

&nbsp;

---

&nbsp;

## ✅ Day 1 Checklist

| | Task |
|---|------|
| ☐ | GitHub repo `ai-mlops-journey` created and cloned |
| ☐ | Folder structure created |
| ☐ | Python 3.10+ installed, virtual env working |
| ☐ | Podman running, `hello-world` container ran |
| ☐ | kubectl + minikube installed, cluster started |
| ☐ | VS Code extensions installed |
| ☐ | Daily log filled in and pushed |
| ☐ | **2 commits pushed** 🟩🟩 |

&nbsp;

---

&nbsp;

## 🧠 Concepts You Now Own

| Concept | One-liner |
|---------|-----------|
| **Git** | Time machine for code |
| **Virtual env** | Sandbox so packages don't fight each other |
| **Container image** | A recipe — the blueprint |
| **Container** | A running instance of that recipe |
| **Podman** | Docker alternative — daemonless, rootless, same commands |
| **Kubernetes** | The manager that runs thousands of containers |
| **kubectl** | Your remote control for K8s |
| **minikube** | A tiny K8s cluster on your laptop |

&nbsp;

---

&nbsp;

> *Tomorrow: Python crash course — variables, loops, functions, lists, dicts.*
> *You'll write actual code. Today was the hard part. 💪*
