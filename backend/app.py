# backend/app.py
import os
import sys
from flask import Flask, render_template, request, jsonify


# --- Ensure backend modules are importable ---
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.ai_engine import get_article_from_wikipedia, generate_facts
from backend.game_logic import parse_facts, shuffle_facts, get_correct_index

# --- Define project directories ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

# --- Create Flask app ---
app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)


@app.route("/")
def index():
    """Render the main HTML page."""
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    """Generate AI facts for a given topic and difficulty level."""
    data = request.get_json()
    topic = data.get("topic")
    level = data.get("level", "easy")

    if not topic:
        return jsonify({"error": "Topic is required"}), 400

    # 1. Get Wikipedia content
    article = get_article_from_wikipedia(topic)
    if not article:
        return jsonify({"error": f"No Wikipedia article found for '{topic}'"}), 404

    # 2. Generate AI facts
    try:
        raw = generate_facts(article, level)
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500

    facts = parse_facts(raw)
    facts = shuffle_facts(facts)

    # 3. Return JSON response to frontend
    return jsonify({
        "facts": [{"text": f, "is_true": t} for f, t in facts],
        "fake_index": get_correct_index(facts),
        "topic": topic,
        "level": level
    })


if __name__ == "__main__":
    app.run(debug=True)
