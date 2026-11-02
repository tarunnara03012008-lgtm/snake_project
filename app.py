
from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

SCORES_FILE = "scores.json"


def load_scores():
    if not os.path.exists(SCORES_FILE):
        return []

    try:
        with open(SCORES_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return []


def save_scores(scores):
    with open(SCORES_FILE, "w", encoding="utf-8") as file:
        json.dump(scores, file, indent=4)


# Frontend page
@app.route("/")
def home():
    return render_template("index.html")


# API 1: Check whether the backend is working
@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "success",
        "message": "Snake Game API is running!"
    })


# API 2: Get saved scores
@app.route("/api/scores", methods=["GET"])
def get_scores():
    scores = load_scores()
    scores.sort(key=lambda item: item["score"], reverse=True)

    return jsonify({
        "status": "success",
        "scores": scores[:10]
    })


# API 3: Save a new game score
@app.route("/api/score", methods=["POST"])
def save_score():
    data = request.get_json(silent=True) or {}
    score = data.get("score")

    if type(score) is not int or score < 0:
        return jsonify({
            "status": "error",
            "message": "Score must be a non-negative integer."
        }), 400

    scores = load_scores()

    scores.append({
        "score": score
    })

    save_scores(scores)

    return jsonify({
        "status": "success",
        "message": "Score saved successfully!",
        "score": score
    }), 201


if __name__ == "__main__":
    app.run(debug=True)
