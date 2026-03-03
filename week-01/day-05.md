# Day 5 — Podman Deep Dive + Flask API Project

## What I did
- Learned how Containerfiles and image layers work
- Built my first custom container image from scratch
- Learned port mapping (-p) and volumes (-v)
- Built a Flask API with /health and /pods endpoints
- Containerized it and ran it with Podman

## What I learned
- (fill in)

## What confused me
- (fill in)

## Week 1 reflection
- (what was hardest? what clicked? what are you most proud of?)

## Code I want to remember
- Containerfile: FROM → WORKDIR → COPY reqs → RUN pip install → COPY app → CMD
- Build image: podman build -t my-flask-api .
- Run with port map: podman run -p 5000:5000 my-flask-api
- Volume mount: podman run -v /local/path:/container/path my-app
- Flask route: @app.route("/health") def health(): return jsonify({"status": "healthy"})
