from flask import Flask, jsonify, request, session, render_template

from capitals_game import generate_capitals_questions, update_score
from count_game import generate_math_questions

app = Flask(__name__)
app.secret_key = "your-secret-key"


@app.route("/")
def one():
    return render_template("partonetest.html")

@app.route("/two")
def two():
    return render_template("parttwotest.html")

# Start the first level of capitals_game
@app.route("/part_one/questions", methods=["GET"])
def start_part_one():
    return generate_capitals_questions()


@app.route("/part_two/questions", methods=["GET"])
def start_part_two():
    questions = generate_math_questions()
    return jsonify(questions)

@app.route("/saveResult", methods=["POST"])
def save_level():
    data = request.get_json()
    points = data.get("points")

    # before there is a real session game_id
    session["game_id"] = 57

    is_successful = update_score(points, session["game_id"])

    return jsonify({"success": is_successful})

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=3000)
