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