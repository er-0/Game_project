from flask import Flask, jsonify, request, session, render_template
import secrets
import os

from db import yhteys

# login
def web_check_user_exists(username):

    sql = f"SELECT COUNT(*) FROM players WHERE user_name = %s;"
    kursori = yhteys.cursor()
    kursori.execute(sql, (username,))
    count = kursori.fetchone()[0]
    return count > 0 

# register new user
def web_register_user(name):
    if web_check_user_exists(name):
        return False
    sql = f"SELECT ident FROM game_airports ORDER BY RAND() LIMIT 1;"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    ident = kursori.fetchone()[0]

    sql = f"SELECT COUNT(*) FROM players WHERE starting_airport = %s;"
    kursori = yhteys.cursor()
    kursori.execute(sql, (ident,))
    count_airport = kursori.fetchone()[0]

    while count_airport != 0:
        sql = f"SELECT ident FROM game_airports ORDER BY RAND() LIMIT 1;"
        kursori = yhteys.cursor()
        kursori.execute(sql)
        ident = kursori.fetchone()[0]

        sql = f"SELECT COUNT(*) FROM players WHERE starting_airport = %s;"
        kursori = yhteys.cursor()
        kursori.execute(sql, (ident,))
        count_airport = kursori.fetchone()[0]

    sql = f"INSERT INTO players (user_name, starting_airport) VALUES (%s, %s);"
    kursori = yhteys.cursor()
    kursori.execute(sql, (name, ident))
    yhteys.commit()

    return True

# get player information
def player_information(name):
    sql = (f"SELECT a.ident, a.name, a.latitude_deg, a.longitude_deg, a.continent, a.municipality, a.country_name, "
           f"p.id, p.games_played, p.last_game FROM game_airports AS a INNER JOIN players AS p ON p.starting_airport "
           f"= a.ident where p.user_name = %s;")
    kursori = yhteys.cursor()
    kursori.execute(sql, (name,))
    users_information = kursori.fetchall()

    return users_information

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)


@app.route("/")
def login():
    return render_template("login.html")

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
                        "last_game": last_game})
    else:
        return jsonify({"success": False, "message": "User not found"})
    
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    
    if web_register_user(username):     
        session['user_name'] = username  

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

        # Get information about the user

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
                        "last_game": last_game})
    else:
        return jsonify({"success": False, "message": "Username already exists"})


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=3000)