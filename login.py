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


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=3000)