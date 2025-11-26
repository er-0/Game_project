from flask import Flask, jsonify, request, session, render_template

from capitals_game import generate_all_questions_for_level

app = Flask(__name__)
app.secret_key = "your-secret-key"


@app.route("/")
def home():
    return render_template("partonetest.html")

# Start the first level of capitals_game
@app.route("/part_one/start", methods=["POST"])
def start_part_one():
    level = 1
    session["level"] = level
    session["score"] = 0
    session["question_index"] = 0
    session["questions"] = generate_all_questions_for_level(level)
    return jsonify({"message": "Part One started", "level": level})


# Get the next question
@app.route("/part_one/question", methods=["GET"])
def next_question():
    q_index = session.get("question_index", 0)
    questions = session.get("questions", [])

    if q_index >= len(questions):
        return jsonify({"finished": True, "score": session.get("score", 0)})

    q = questions[q_index]
    return jsonify({
        "question": q["question"],
        "options": q["options"],
        "level": session["level"],
        "question_index": q_index
    })


# Submit an answer
@app.route("/part_one/answer", methods=["POST"])
def answer_question():
    data = request.get_json()
    selected = data.get("answer")
    q_index = session.get("question_index", 0)
    questions = session.get("questions", [])

    if q_index >= len(questions):
        return jsonify({"finished": True, "score": session.get("score", 0)})

    q = questions[q_index]
    correct = (selected == q["correct_answer"])
    if correct:
        session["score"] += q["points"]

    session["question_index"] += 1
    finished = session["question_index"] >= len(questions)

    return jsonify({
        "correct": correct,
        "correct_answer": q["correct_answer"],
        "score": session["score"],
        "finished": finished
    })


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=3000)
