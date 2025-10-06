import sys

from db import yhteys
from geopy import distance


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

# Function to calculate the destance between airports -------------------------------------------------

def distance_in_kilometers(first_lat, first_long, second_lat, second_long):

    start_coordinates = (first_lat, first_long)
    finish_coordinates = (second_lat, second_long)

    kilometers = distance.distance(start_coordinates, finish_coordinates).km

    return kilometers

# -----------------------------------------------------------------------------------------------------

# Get user name or create a new one

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

# Check for an existance of the last game and get information either on new or last game

if last_game == 0:

    print("\nYou need to start a new game")
    print("\n1 - Create a new game" \
    "\n2 - Exit game")

    answer = int(input('\nGive me your answer: '))

    if answer == 1:

        game_id = create_game(player_id, airport_country)
        print(game_id)

        games_info = game_information(game_id)

        for game_info in games_info:
            goal_ident, goal_name, goal_latitude_deg, goal_longitude_deg, goal_continent, goal_municipality, goal_country_name, goal_airport, kilometers_traveled, score, level_reached = game_info

        print("\nCurrent game info\n")

        print(game_info)

        new_game = True

    elif answer == 2:

        sys.exit()     

elif last_game != 0:

    print("\nYou have an unfinished game. Do you want to load game ar start a new game?")
    print("\n1 - New game" \
    "\n2 - Old" \
    "\n3 - Exit")

    answer = int(input("\nGive me your answer: "))

    if answer == 1:

        game_id = create_game(player_id, airport_country)
        print(game_id)

        games_info = game_information(game_id)

        for game_info in games_info:
            goal_ident, goal_name, goal_latitude_deg, goal_longitude_deg, goal_continent, goal_municipality, goal_country_name, goal_airport, kilometers_traveled, score, level_reached = game_info

        print("\nCurrent game info\n")

        print(game_info)

        new_game = True

    elif answer == 2:

        print("\nLast game information\n")

        games_info = game_information(last_game)

        for game_info in games_info:
            goal_ident, goal_name, goal_latitude_deg, goal_longitude_deg, goal_continent, goal_municipality, goal_country_name, goal_airport, kilometers_traveled, score, level_reached = game_info

        print("\nCurrent game info\n")

        print(game_info)

        new_game = False
    
    elif answer == 3:

        sys.exit()

# Start new game or continue old game

if new_game == True:

    print("\nWe start a new game\n")

    print("\n The distance between " + airport_name + " and airport " + goal_name + " is: \n")

    print(distance_in_kilometers(latitude_deg, longitude_deg, goal_latitude_deg, goal_longitude_deg))

    # Here goes function for game 1


elif new_game == False:

    print("\nWe continue with the old game")

    print("\n The distance between " + airport_name + " and airport " + goal_name + " is: \n")

    print(distance_in_kilometers(latitude_deg, longitude_deg, goal_latitude_deg, goal_longitude_deg))
    