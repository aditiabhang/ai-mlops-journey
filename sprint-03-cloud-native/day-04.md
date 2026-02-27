# Sprint 3 · Day 4

## 🐍🤖 Sprint Project: Python CLI Chatbot with Ollama

`90 min` · `Needs: Ollama running + Python` · `Your first AI project`

---

&nbsp;

## Today's Big Picture

> Yesterday you chatted with LLMs in the terminal. Cool party trick.
> Today you build a Python app that talks to Ollama's API, has a conversation loop,
> and saves chat history to a file. This is a REAL project for your GitHub portfolio.

By the end of today, you'll have:

- ✅ Called Ollama's REST API from Python
- ✅ Built a conversation loop with memory
- ✅ Saved chat history to JSON
- ✅ Written a README with instructions
- ✅ Sprint 3 project — pushed to GitHub 🎉

&nbsp;

---

&nbsp;

## The Architecture

```
┌─────────────────────────────────────────────┐
│  Your Terminal                              │
│                                             │
│  ┌──────────────────┐    ┌───────────────┐  │
│  │  chatbot.py      │    │  Ollama       │  │
│  │                  │    │  Server       │  │
│  │  You type ────────────▶ POST /api/chat│  │
│  │  a question      │    │               │  │
│  │                  │◀────── response    │  │
│  │  Print answer    │    │               │  │
│  │  Save to JSON    │    │  llama3.2     │  │
│  └──────────────────┘    └───────────────┘  │
│                                             │
│  How it works:                              │
│  1. You type a question                     │
│  2. Python sends ALL past messages + yours  │
│  3. Ollama responds with context            │
│  4. Python saves everything to JSON         │
└─────────────────────────────────────────────┘
```

&nbsp;

---

&nbsp;

## Part 1 — Understand Ollama's API `10 min`

&nbsp;

### The API (30-second version)

Ollama runs a local server on `http://localhost:11434`. You send a POST request with your messages, it sends back the model's response. Same pattern as every AI API in the world — OpenAI, Bedrock, all of them.

```
┌──────────────────────────────────────────────┐
│  Every LLM API works the same way:          │
│                                              │
│  You send:                                   │
│  {                                           │
│    "model": "llama3.2",                      │
│    "messages": [                             │
│      {"role": "user", "content": "Hi!"}      │
│    ]                                         │
│  }                                           │
│                                              │
│  You get back:                               │
│  {                                           │
│    "message": {                              │
│      "role": "assistant",                    │
│      "content": "Hello! How can I help?"     │
│    }                                         │
│  }                                           │
│                                              │
│  That's it. Every. Single. LLM. API.        │
└──────────────────────────────────────────────┘
```

&nbsp;

### Do This — Quick test

**1 →** Make sure Ollama is running (in another terminal tab)

```bash
ollama serve
```

&nbsp;

**2 →** Test the API with curl

```bash
curl http://localhost:11434/api/chat -d '{
  "model": "llama3.2",
  "messages": [{"role": "user", "content": "Say hello in 5 words"}],
  "stream": false
}'
```

> You should get a JSON response with the model's answer. That's the exact API your Python script will call.

&nbsp;

---

&nbsp;

## Part 2 — Build the Chatbot `40 min`

&nbsp;

### How conversation memory works

```
Turn 1:
  You send:    [user: "What is K8s?"]
  Model sees:  1 message → responds

Turn 2:
  You send:    [user: "What is K8s?",
                assistant: "K8s is...",
                user: "How does it scale?"]
  Model sees:  3 messages → responds WITH context

Turn 3:
  You send:    ALL previous messages + new one
  Model sees:  full conversation → responds intelligently
```

> This is why chatbots remember what you said earlier — you're sending the entire history every time.

&nbsp;

### Do This

**1 →** Create the project folder

```bash
mkdir -p ~/projects/ai-mlops-journey/projects/01-ollama-chatbot
cd ~/projects/ai-mlops-journey/projects/01-ollama-chatbot
```

&nbsp;

**2 →** Create `chatbot.py`

```python
import requests
import json
from datetime import datetime

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3.2"


def chat(messages):
    """Send messages to Ollama and get a response."""
    response = requests.post(OLLAMA_URL, json={
        "model": MODEL,
        "messages": messages,
        "stream": False
    })
    return response.json()["message"]["content"]


def save_history(messages):
    """Save the conversation to a JSON file."""
    history = {
        "model": MODEL,
        "saved_at": str(datetime.now()),
        "message_count": len(messages),
        "messages": messages
    }
    with open("chat_history.json", "w") as f:
        json.dump(history, f, indent=2)


def main():
    print(f"\n🤖 Ollama Chatbot")
    print(f"   Model: {MODEL}")
    print(f"   Commands: 'quit' to exit | 'save' to save history")
    print(f"   {'─' * 45}\n")

    messages = []

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() == "quit":
            if messages:
                save_history(messages)
                print("💾 Chat auto-saved.")
            print("👋 Bye!")
            break

        if user_input.lower() == "save":
            save_history(messages)
            print("💾 Saved to chat_history.json\n")
            continue

        if not user_input:
            continue

        messages.append({"role": "user", "content": user_input})

        try:
            reply = chat(messages)
            messages.append({"role": "assistant", "content": reply})
            print(f"\n🤖: {reply}\n")
        except requests.exceptions.ConnectionError:
            print("❌ Can't reach Ollama. Is it running? (ollama serve)")
            messages.pop()
        except Exception as e:
            print(f"❌ Error: {e}")
            messages.pop()


if __name__ == "__main__":
    main()
```

&nbsp;

**3 →** Run it

```bash
cd ~/projects/ai-mlops-journey/projects/01-ollama-chatbot
python3 chatbot.py
```

> Chat with it! Ask follow-up questions — it remembers the conversation.
> Type `save` to save anytime, `quit` to exit (auto-saves).

&nbsp;

**4 →** Check the saved history

```bash
cat chat_history.json
```

> Real conversation data, timestamped, in JSON. This is how production chatbot systems store conversations.

&nbsp;

**5 →** Try breaking it — stop Ollama (`Ctrl+C` in the serve tab) and send a message. Your error handling catches it cleanly.

&nbsp;

---

&nbsp;

## Part 3 — Make It Yours (Pick One) `15 min`

Pick one upgrade to make the chatbot yours. Don't do all of them — just one.

&nbsp;

### Option A — System prompt (give it a personality)

Add this before the `while True` loop:

```python
system_prompt = "You are a Kubernetes expert. Give concise answers with examples."
messages = [{"role": "system", "content": system_prompt}]
```

> Now every response is K8s-flavored. Try asking it non-K8s questions — it'll steer back.

&nbsp;

### Option B — Model picker

Replace the `MODEL` line with:

```python
import sys
MODEL = sys.argv[1] if len(sys.argv) > 1 else "llama3.2"
```

Now you can run:

```bash
python3 chatbot.py mistral
python3 chatbot.py phi3
```

&nbsp;

### Option C — Chat history loader

Add a function to load previous chats:

```python
def load_history():
    try:
        with open("chat_history.json", "r") as f:
            data = json.load(f)
            print(f"📂 Loaded {data['message_count']} messages from last session")
            return data["messages"]
    except FileNotFoundError:
        return []
```

Call it at the start: `messages = load_history()`

&nbsp;

---

&nbsp;

## Part 4 — Write the README `15 min`

Create `projects/01-ollama-chatbot/README.md`:

```markdown
# 🤖 Ollama CLI Chatbot

A Python chatbot that runs LLMs locally using Ollama.
No cloud. No API keys. Fully private.

## What it does

- Chats with a local LLM (llama3.2 by default)
- Remembers conversation context
- Saves chat history to JSON
- Auto-saves on exit

## Setup

1. Install [Ollama](https://ollama.com) and pull a model:

   ```bash
   ollama pull llama3.2
   ollama serve
   ```

2. Run the chatbot:

   ```bash
   python3 chatbot.py
   ```

3. Chat! Type `save` to save history, `quit` to exit.

## Built with

- Python 3.11
- Ollama REST API (`localhost:11434`)
- llama3.2 (Meta)
```

&nbsp;

---

&nbsp;

## Part 5 — Commit & Push `10 min`

```bash
cd ~/projects/ai-mlops-journey
git add projects/01-ollama-chatbot/
git add sprint-03-cloud-native/
git commit -m "sprint 3 project: python CLI chatbot with ollama 🤖"
git push
```

&nbsp;

---

&nbsp;

## ✅ Day 4 Checklist

| | Task |
|---|------|
| ☐ | Tested Ollama API with curl |
| ☐ | Chatbot runs and responds to questions |
| ☐ | Conversation memory works (follow-up questions make sense) |
| ☐ | Chat history saves to JSON |
| ☐ | Added one personal upgrade (Option A, B, or C) |
| ☐ | README written |
| ☐ | Project pushed to GitHub 🟩 |

&nbsp;

---

&nbsp;

## 🧠 Concepts You Now Own

| Concept | One-liner |
|---------|-----------|
| **Ollama API** | POST to `localhost:11434/api/chat` with messages |
| **Messages array** | List of `{role, content}` dicts — how ALL LLM APIs work |
| **Conversation memory** | Send ALL previous messages so the model has context |
| **stream: false** | Get the full response at once (vs word-by-word) |
| **System prompt** | Hidden instruction that shapes the model's personality |
| **roles** | `user` = you, `assistant` = model, `system` = hidden instructions |

&nbsp;

---

&nbsp;

## 🎉 Sprint 3 Complete!

Look at what you built across this sprint:

- Mapped the entire CNCF cloud native ecosystem
- Learned observability and GitOps — the KCNA exam topics
- Ran LLMs on your own laptop
- **Built an AI chatbot from scratch**

That's not "I watched some videos." That's "I built something." Big difference.

&nbsp;

> *Next: [Sprint 4 — KCNA Exam Prep](../sprint-04-kcna-exam/sprint-04-overview.md)*
> *Mock exams, flashcard blitz, and then... you sit the exam. 🏆*
