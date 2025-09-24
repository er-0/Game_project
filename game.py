from db import yhteys  # import the connection from db.py

def lentoasema():
    sql = "SELECT count(*) FROM game_airports"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchall()
    return tulos

print(lentoasema())