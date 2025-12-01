from flask import Flask, jsonify, request, session, render_template
import secrets
import os

from loginfunctions import web_register_user, web_check_user_exists, player_information, random_airports, start_new_game

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)


@app.route("/")
def login():
    return render_template("login.html")

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

        # Send response

        return jsonify({"success": True,
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
                        "random_airports": airports_data})
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

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=3000)