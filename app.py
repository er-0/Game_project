from flask import Flask, jsonify, request, session, render_template

from capitals_game import generate_all_questions, update_score

app = Flask(__name__)
app.secret_key = "your-secret-key"


@app.route("/")
def home():
    return render_template("partonetest.html")

# Start the first level of capitals_game
@app.route("/part_one/questions", methods=["GET"])
def start_part_one():
    generate_all_questions()

    return generate_all_questions()

@app.route("/part_one/saveResult", methods=["POST"])
def save_level_one():
    data = request.get_json()
    points = data.get("points")

    # before there is a real session game_id
    session["game_id"] = 70

    is_successful = update_score(points, session["game_id"])

    return jsonify({"success": is_successful})

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=3000)
