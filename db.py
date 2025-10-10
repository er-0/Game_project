# db.py
import mysql.connector

# Create a connection object
yhteys = mysql.connector.connect(
    host='127.0.0.1',
    port=3306,
    database='flight_game',
    user='user',
    password='password',
    autocommit=True
)
