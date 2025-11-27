from flask import Flask, jsonify, request, session, render_template
import secrets
import os


from db import yhteys

def web_check_user_exists(username):

    sql = f"SELECT COUNT(*) FROM players WHERE user_name = %s;"
    kursori = yhteys.cursor()
    kursori.execute(sql, (username,))
    count = kursori.fetchone()[0]
    return count > 0 

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
        return jsonify({"success": True, "message": "Login successful"})
    else:
        return jsonify({"success": False, "message": "User not found"})
    
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    
    if web_register_user(username):     
        session['user_name'] = username  
        return jsonify({"success": True, "message": "Registration successful"})
    else:
        return jsonify({"success": False, "message": "Username already exists"})


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=3000)