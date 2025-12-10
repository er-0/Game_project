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
           f"p.id, p.games_played, p.last_game, p.lifetime_score FROM game_airports AS a INNER JOIN players AS p ON "
           f"p.starting_airport "
           f"= a.ident where p.user_name = %s;")
    kursori = yhteys.cursor()
    kursori.execute(sql, (name,))
    users_information = kursori.fetchall()

    return users_information

# get random 20 airports to start game

def random_airports(country):

    sql = f"SELECT ident, name, latitude_deg, longitude_deg, iso_country, municipality, country_name FROM game_airports WHERE country_name != %s ORDER BY RAND() LIMIT 20;"
    kursori = yhteys.cursor()
    kursori.execute(sql, (country,))
    random_airports = kursori.fetchall()

    return random_airports

# start new game
def start_new_game(player_id, goal_ident):
    kursori = yhteys.cursor()
    sql = " INSERT INTO games (player_id, goal_airport, start_time) VALUES (%s, %s, CURTIME())"
    kursori.execute(sql, (player_id, goal_ident))
    yhteys.commit()

    game_id = kursori.lastrowid

    kursori.execute("SELECT start_time FROM games WHERE game_id = %s", (game_id,))
    start_time = kursori.fetchone()[0]

    return game_id, start_time 

# get information about the old game
def last_game_information(id):
    sql = (f"SELECT a.ident, a.name, a.latitude_deg, a.longitude_deg, a.continent, a.municipality, a.country_name, "
           f"g.goal_airport, g.kilometers_traveled, g.score, g.level_reached from games as g LEFT JOIN game_airports "
           f"AS a ON g.goal_airport = a.ident WHERE g.game_id = %s;")
    kursori = yhteys.cursor()
    kursori.execute(sql, (id,))
    information = kursori.fetchall()

    return information

def update_last_game(game_id, player_id):

    sql = f"UPDATE players SET last_game = %s WHERE id = %s;"
    kursori = yhteys.cursor()
    kursori.execute(sql, (game_id, player_id))
    yhteys.commit()

    return True

def get_highscorers():
    sql = (f"SELECT user_name, lifetime_score from players ORDER BY lifetime_score DESC LIMIT 5")
    kursori = yhteys.cursor()
    kursori.execute(sql, )
    highscorers = kursori.fetchall()

    return highscorers

def delete_last_game(id):
    sql = "UPDATE players SET last_game = 0 WHERE id = %s;"
    kursori = yhteys.cursor()
    kursori.execute(sql, (id,))
    yhteys.commit()
    
    return True

def add_game_score_to_lifetime(player_id, game_id):
    sql = (f"SELECT score FROM games WHERE game_id = %s;")
    cursor = yhteys.cursor()
    cursor.execute(sql, (game_id,))
    row = cursor.fetchone()
    if not row:
        print(f"Game {game_id} not found.")
        return False

    score = row[0]

    # Update player's lifetime_score and games_played
    sql = "UPDATE players SET lifetime_score = lifetime_score + %s, games_played = games_played + 1 WHERE id = %s"
    cursor.execute(sql, (score, player_id))
    yhteys.commit()
    print(f"Added {score} points to player {player_id}'s lifetime_score.")
    return True

# To get information about the destination airport

# def game_information(id):
#     sql = (f"SELECT a.ident, a.municipality, a.country_name, g.goal_airport from games as g LEFT JOIN game_airports AS a ON g.goal_airport = a.ident WHERE g.game_id = %s;")
#     kursori = yhteys.cursor()
#     kursori.execute(sql, (id,))
#     information = kursori.fetchall()

#     return information