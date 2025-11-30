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

# get random 20 airports to start game

def random_airports(country):

    sql = f"SELECT ident, name, latitude_deg, longitude_deg FROM game_airports WHERE country_name != %s ORDER BY RAND() LIMIT 20;"
    kursori = yhteys.cursor()
    kursori.execute(sql, (country,))
    random_airports = kursori.fetchall()

    return random_airports

