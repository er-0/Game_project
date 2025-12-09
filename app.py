from flask import Flask, jsonify, request, session, render_template
import secrets
import os

from loginfunctions import web_register_user, web_check_user_exists, player_information, random_airports, \
    start_new_game, last_game_information, update_last_game, get_highscorers
from capitals_game import generate_capitals_questions, update_score
from count_game import generate_math_questions

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)


# HTML pages
@app.route("/")
def home():
    return render_template("home.html")


# Login form actions

@app.route("/login", methods=["POST"])
def login_page():
    data = request.get_json()
    username = data.get("username")

    if web_check_user_exists(username):
        session['user_name'] = username

        # Get information about the user
        users_information = player_information(username)

        for user_information in users_information:
            (airport_ident, airport_name, latitude_deg, longitude_deg, airport_continent,
             airport_municipality, airport_country, player_id, games_played, last_game, lifetime_score) = (
                user_information)

        session['airport_ident'] = airport_ident
        session['airport_name'] = airport_name
        session['latitude_deg'] = latitude_deg
        session['longitude_deg'] = longitude_deg
        session['airport_continent'] = airport_continent
        session['airport_municipality'] = airport_municipality
        session['airport_country'] = airport_country
        session['player_id'] = player_id
        session['games_played'] = games_played
        session['last_game'] = last_game
        session['lifetime_score'] = lifetime_score

        # Get 20 random airports
        random_airports_list = random_airports(airport_country)

        airports_data = []
        for airport in random_airports_list:
            ident, name, lat, lon = airport
            airports_data.append({
                'ident': ident,
                'name': name,
                'latitude_deg': lat,
                'longitude_deg': lon
            })

        # Base response dictionary
        response_data = {
            "success": True,
            "message": "Login successful",
            "username": username,
            "airport_ident": airport_ident,
            "airport_name": airport_name,
            "latitude_deg": latitude_deg,
            "longitude_deg": longitude_deg,
            "airport_continent": airport_continent,
            "airport_municipality": airport_municipality,
            "airport_country": airport_country,
            "player_id": player_id,
            "games_played": games_played,
            "last_game": last_game,
            "random_airports": airports_data
        }

        # Add last game info if available
        if session['last_game'] != 0:
            last_game_info = last_game_information(session['last_game'])

            if last_game_info:
                for last_game_data in last_game_info:
                    (last_ident, last_name, last_latitude_deg, last_longitude_deg,
                     last_continent, last_municipality, last_country, last_goal_airport,
                     last_kilometers_traveled, last_score, last_level_reached) = last_game_data

                    response_data.update({
                        "last_ident": last_ident,
                        "last_name": last_name,
                        "last_latitude_deg": last_latitude_deg,
                        "last_longitude_deg": last_longitude_deg,
                        "last_continent": last_continent,
                        "last_municipality": last_municipality,
                        "last_country": last_country,
                        "last_goal_airport": last_goal_airport,
                        "last_kilometers_traveled": last_kilometers_traveled,
                        "last_score": last_score,
                        "last_level_reached": last_level_reached
                    })
                    break

        return jsonify(response_data)

    else:
        return jsonify({"success": False, "message": "User not found"})


# Registration form actions

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")

    if web_register_user(username):
        session['user_name'] = username

        # Get information about the user

        users_information = player_information(username)

        for user_information in users_information:
            (airport_ident, airport_name, latitude_deg, longitude_deg, airport_continent, airport_municipality,
             airport_country, player_id, games_played, last_game) = user_information

        session['airport_ident'] = airport_ident
        session['airport_name'] = airport_name
        session['latitude_deg'] = latitude_deg
        session['longitude_deg'] = longitude_deg
        session['airport_continent'] = airport_continent
        session['airport_municipality'] = airport_municipality
        session['airport_country'] = airport_country
        session['player_id'] = player_id
        session['games_played'] = games_played
        session['last_game'] = last_game

        # Get 20 random airports

        random_airports_list = random_airports(airport_country)

        airports_data = []
        for airport in random_airports_list:
            ident, name, lat, lon = airport
            airports_data.append({
                'ident': ident,
                'name': name,
                'latitude_deg': lat,
                'longitude_deg': lon
            })

        return jsonify({"success": True,
                        "message": "Registration successful",
                        "username": username,
                        "airport_ident": airport_ident,
                        "airport_name": airport_name,
                        "latitude_deg": latitude_deg,
                        "longitude_deg": longitude_deg,
                        "airport_continent": airport_continent,
                        "airport_municipality": airport_municipality,
                        "airport_country": airport_country,
                        "player_id": player_id,
                        "games_played": games_played,
                        "last_game": last_game,
                        "random_airports": airports_data})
    else:
        return jsonify({"success": False, "message": "Username already exists"})


@app.route("/newgame", methods=["POST"])
def newgame():
    data = request.get_json()
    airport = data.get("airport")

    game_id = start_new_game(session['player_id'], airport)

    if game_id:

        session['game_id'] = game_id

        return jsonify({"success": True,
                        "game_id": game_id})
    else:
        return jsonify({"success": False, "message": "Failed to create new game"})

@app.route("/firstgame_finished")
def first_game_finished():
    if session['games_played'] > 0:
        return {"first_game": False}


# Start the first minigame: CAPITALS
@app.route("/part_one/questions", methods=["GET"])
def start_part_one():
    if "game_id" not in session:
        session["game_id"] = "69"
    print(session["game_id"])
    return generate_capitals_questions()


# Start the second minigame: MATH
@app.route("/part_two/questions", methods=["GET"])
def start_part_two():
    questions = generate_math_questions()
    return jsonify(questions)


# Check player submitted words against the finnish-words.txt file
@app.route("/part_three/check_word", methods=["POST"])
def check_word():
    data = request.get_json()
    user_word = data.get("word", "").strip().lower()

    with open("static/finnish-words.txt", "r", encoding="utf-8") as f:
        words = {w.strip().lower() for w in f.readlines()}

    return jsonify({"valid": user_word in words})


# Save the result of the -------------------------------------------FIRST AND SECOND minigame
@app.route("/saveResult", methods=["POST"])
def save_level():
    data = request.get_json()
    points = data.get("points")
    if "player_id" not in session:
        session["player_id"] = "41"

    print(points, session["game_id"], "from approute")
    is_successful = update_score(points, session["game_id"])

    #update_last_game(session["game_id"], session["player_id"])

    return jsonify({"success": is_successful})

@app.route("/scoreboard", methods=["GET"])
def get_scoreboard():
    scoreboard = get_highscorers()
    return jsonify(scoreboard)


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=3000)
