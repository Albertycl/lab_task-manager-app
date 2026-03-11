from flask import Flask, jsonify, request
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# In-memory task store (replace with DB later if needed)
tasks = [
    {"id": 1, "title": "Learn Kubernetes", "done": False},
    {"id": 2, "title": "Deploy with Helm", "done": False},
    {"id": 3, "title": "Set up Argo CD", "done": False},
]
next_id = 4


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "version": os.getenv("APP_VERSION", "v1")})


@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks)


@app.route("/api/tasks", methods=["POST"])
def create_task():
    global next_id
    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "title is required"}), 400
    task = {"id": next_id, "title": data["title"], "done": False}
    next_id += 1
    tasks.append(task)
    return jsonify(task), 201


@app.route("/api/tasks/<int:task_id>", methods=["PATCH"])
def update_task(task_id):
    data = request.get_json()
    for task in tasks:
        if task["id"] == task_id:
            if "title" in data:
                task["title"] = data["title"]
            if "done" in data:
                task["done"] = data["done"]
            return jsonify(task)
    return jsonify({"error": "task not found"}), 404


@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(i)
            return jsonify({"message": "deleted"})
    return jsonify({"error": "task not found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
