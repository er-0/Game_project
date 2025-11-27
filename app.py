from flask import Flask, jsonify, request, session, render_template

from capitals_game import generate_all_questions

app = Flask(__name__)
app.secret_key = "your-secret-key"


@app.route("/")
def home():
    return render_template("partonetest.html")

# Start the first level of capitals_game
@app.route("/part_one/questions", methods=["GET"])
def start_part_one():
    level = 1
    session["level"] = level
    session["score"] = 0
    session["question_index"] = 0
    session["questions"] = generate_all_questions()

    return session["questions"]

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=3000)
