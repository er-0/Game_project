import sys

from db import yhteys


# Function to register users ---------------------------------------------------------------------------

def loggin():

    name = input('\nGive me your name: ')

    sql = f"SELECT COUNT(*) FROM players WHERE user_name = '{name}';"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    count = kursori.fetchone()[0]  

    while count != 0:
         
        print("\nThis name already exists in the darabase")
        print("\nTry amother name")

        name = input('\nGive me your name: ')

        sql = f"SELECT COUNT(*) FROM players WHERE user_name = '{name}';"
        kursori = yhteys.cursor()
        kursori.execute(sql)
        count = kursori.fetchone()[0]

    sql = f"SELECT ident FROM game_airports ORDER BY RAND() LIMIT 1;"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    ident = kursori.fetchone()[0]  

    sql = f"SELECT COUNT(*) FROM players WHERE starting_airport = '{ident}';"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    count_airport = kursori.fetchone()[0] 

    while count_airport != 0:

        sql = f"SELECT ident FROM game_airports ORDER BY RAND() LIMIT 1;"
        kursori = yhteys.cursor()
        kursori.execute(sql)
        ident = kursori.fetchone()[0]  

        sql = f"SELECT COUNT(*) FROM players WHERE starting_airport = '{ident}';"
        kursori = yhteys.cursor()
        kursori.execute(sql)
        count_airport = kursori.fetchone()[0]

    sql = f"INSERT INTO players (user_name, starting_airport) VALUES ('{name}','{ident}');"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    yhteys.commit()

    return name

# -------------------------------------------------------------------------------------------------------

# Function to fetch all information from the databse on the user ----------------------------------------

def player_information(name):

    sql = f"SELECT a.ident, a.name, a.latitude_deg, a.longitude_deg, a.continent, a.municipality, a.country_name, p.id, p.games_played, p.last_game FROM game_airports AS a INNER JOIN players AS p ON p.starting_airport = a.ident where p.user_name = '{name}';"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    users_information = kursori.fetchall()
    
    return users_information

# -----------------------------------------------------------------------------------------------------

# Fuction to create a new game ------------------------------------------------------------------------

def create_game(player_id, airport_country):

    sql = f"SELECT ident FROM game_airports WHERE country_name != '{airport_country}' ORDER BY RAND() LIMIT 1;"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    goal_ident = kursori.fetchone()[0]

    sql = f"INSERT INTO games (player_id, goal_airport) VALUES ('{player_id}','{goal_ident}') RETURNING game_id;"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    game_id = kursori.fetchone()[0]
    yhteys.commit()

    return game_id

# -----------------------------------------------------------------------------------------------------

# Function to fetch all information about player games ------------------------------------------------

def game_information(id):

    sql = f"SELECT a.ident, a.name, a.latitude_deg, a.longitude_deg, a.continent, a.municipality, a.country_name, g.goal_airport, g.kilometers_traveled, g.score, g.level_reached from games as g LEFT JOIN game_airports AS a ON g.goal_airport = a.ident WHERE g.game_id = '{id}';"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    information = kursori.fetchall()

    return information


# -----------------------------------------------------------------------------------------------------

print("Hello player!\n" \
"This is our pilot simulator game\n" \
"Have you played before:\n" \
"1 - Yes, I have played before\n" \
"2 - No, I am a new player\n")

yes_no = int(input('Give your answer: '))

if yes_no == 1:
    
    user_name = input('Lets find your pilot liscence. Give us you pilot name: ')

    sql = f"SELECT COUNT(*) FROM players WHERE user_name = '{user_name}';"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    count = kursori.fetchone()[0]

    tries = 0

    while count == 0:

        tries = tries + 1

        if tries <= 3:
            print("\nThere is no such name in the table")
            print("\nMaybe you got it wrong. Try again")

            user_name = input('\nLets find your pilot liscence. Give us you pilot name: ')

            sql = f"SELECT COUNT(*) FROM players WHERE user_name = '{user_name}';"
            kursori = yhteys.cursor()
            kursori.execute(sql)
            count = kursori.fetchone()[0]
        
        if tries > 3:
            print("\nYou have axceeded the amount of tries")
            print("\nYou are not registered as a pilot in our database")
            print("\nDo you want to register as a new pilot? or exit game.")
            print("\n1 - register as a new pilot" \
            "\n2 - exit game")

            decision = int(input('\nGive me your coice: '))

            if decision == 1:
                user_name = loggin()
                print("\nGlobal user name is " + user_name)

                count = 1

                break

            elif decision == 2:
                sys.exit()

    users_information = player_information(user_name)

    for user_information in users_information:
        airport_ident, airport_name, latitude_deg, longitude_deg, airport_continent, airport_municipality, airport_country, player_id, games_played, last_game = user_information

    print(airport_name)
    print(airport_continent)
    print(airport_municipality)
    print(airport_country)
    print(games_played)

    print(user_information)
                   
elif yes_no == 2:
    print("\nYou need to register as a new pilot")
    print("\nSelect a unique name for yourself")

    user_name = loggin()

    users_information = player_information(user_name)

    for user_information in users_information:
        airport_ident, airport_name, latitude_deg, longitude_deg, airport_continent, airport_municipality, airport_country, player_id, games_played, last_game = user_information

    print(airport_name)
    print(airport_continent)
    print(airport_municipality)
    print(airport_country)

if last_game == 0:

    print("\nNever played")
    game_id = create_game(player_id, airport_country)
    print(game_id)

    games_info = game_information(game_id)

    for game_info in games_info:
        goal_ident, goal_name, goal_latitude_deg, goal_longitude_deg, goal_continent, goal_municipality, goal_country_name, goal_airport, kilometers_traveled, score, level_reached = game_info

    print("\nCurrent game info\n")

    print(game_info) 

elif last_game != 0:

    print("Played before")
    print(last_game)


