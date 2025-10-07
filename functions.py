import sys

from db import yhteys
from geopy import distance

from capitals_game import capitals_game
from count_game import count_game


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

# Function to update score and level of the player ----------------------------------------------------

def update_user_score(score, game_id):

    sql = f"UPDATE games SET score = score + {score}, level_reached = level_reached + 1 WHERE game_id = {game_id};"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    yhteys.commit()

    tulos = print("Score has been changed")

    return tulos

# -----------------------------------------------------------------------------------------------------

# Function to return last game to 0 after level 3 -----------------------------------------------------

def update_last_game(name):

    sql = f"UPDATE players SET last_game = 0 WHERE user_name = '{name}';"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    yhteys.commit()

    return

# -----------------------------------------------------------------------------------------------------

# Function to delete player from the database ---------------------------------------------------------

def delete_user(id, name):

    sql = f"DELETE FROM games WHERE player_id = '{id}';"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    yhteys.commit()

    sql = f"DELETE FROM players WHERE user_name = '{name}';"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    yhteys.commit()

    tulos = print("You lost youe liscence")

    return tulos

# -----------------------------------------------------------------------------------------------------

# This is the begging of the game. We say hello to the player, tell him about the game and ask him if is already regestered
def intro():
    print("Hello player!\n" \
          "This is our pilot simulator game\n" \
          "Have you played before:\n" \
          "1 - Yes, I have played before\n" \
          "2 - No, I am a new player\n")

    yes_no = int(input('Give your answer: '))

    # If player is already registered

    if yes_no == 1:

        user_name = input('Lets find your pilot liscence. Give us you pilot name: ')

        # Check if the name in the database

        sql = f"SELECT COUNT(*) FROM players WHERE user_name = '{user_name}';"
        kursori = yhteys.cursor()
        kursori.execute(sql)
        count = kursori.fetchone()[0]

        tries = 0

        # If there is no such name count will be equal to 0, if there is such a name, count will be 1. We want count to be 1

        while count == 0:

            tries = tries + 1

            # Player will have limited tries to enter the name

            if tries <= 3:
                print("\nThere is no such name in the table")
                print("\nMaybe you got it wrong. Try again")

                user_name = input('\nLets find your pilot liscence. Give us you pilot name: ')

                sql = f"SELECT COUNT(*) FROM players WHERE user_name = '{user_name}';"
                kursori = yhteys.cursor()
                kursori.execute(sql)
                count = kursori.fetchone()[0]

            # After too many tries we inform the user that he has failed and ask him to create a new account

            if tries > 3:
                print("\nYou have axceeded the amount of tries")
                print("\nYou are not registered as a pilot in our database")
                print("\nDo you want to register as a new pilot? or exit game.")
                print("\n1 - register as a new pilot" \
                      "\n2 - exit game")

                decision = int(input('\nGive me your coice: '))

                # User creates a new pilot name

                if decision == 1:

                    user_name = loggin()
                    print("\nGlobal user name is " + user_name)

                    count = 1

                    break

                elif decision == 2:

                    sys.exit()

        # Get all information about the user and save as global variables

        users_information = player_information(user_name)

        for user_information in users_information:
            airport_ident, airport_name, latitude_deg, longitude_deg, airport_continent, airport_municipality, airport_country, player_id, games_played, last_game = user_information

        print(airport_name)
        print(airport_continent)
        print(airport_municipality)
        print(airport_country)
        print(games_played)

        print(user_information)

    # This answer means that the user is a new player and we ask him to register

    elif yes_no == 2:

        print("\nYou need to register as a new pilot")
        print("\nSelect a unique name for yourself")

        # Player creates a new pilot id

        user_name = loggin()

        # Get information about the user

        users_information = player_information(user_name)

        for user_information in users_information:
            airport_ident, airport_name, latitude_deg, longitude_deg, airport_continent, airport_municipality, airport_country, player_id, games_played, last_game = user_information

        print(airport_name)
        print(airport_continent)
        print(airport_municipality)
        print(airport_country)

    # Check for an existance of the last game. If user has a lat game not equal to 0 we can load an old game information or crate new game, if last game is 0, we create new game

    # This is the path for no previos game

    if last_game == 0:

        print("\nYou need to start a new game")
        print("\n1 - Create a new game" \
              "\n2 - Exit game")

        answer = int(input('\nGive me your answer: '))

        if answer == 1:

            # Create new game and get game_id

            game_id = create_game(player_id, airport_country)
            print(game_id)

            games_info = game_information(game_id)

            # Save new game information as global variables

            for game_info in games_info:
                goal_ident, goal_name, goal_latitude_deg, goal_longitude_deg, goal_continent, goal_municipality, goal_country_name, goal_airport, kilometers_traveled, score, level_reached = game_info

            print("\nCurrent game info\n")

            print(game_info)

            new_game = True

        elif answer == 2:

            sys.exit()

    # This path is for when player has an unfinished game

    elif last_game != 0:

        print("\nYou have an unfinished game. Do you want to load game ar start a new game?")
        print("\n1 - New game" \
              "\n2 - Old" \
              "\n3 - Exit")

        answer = int(input("\nGive me your answer: "))

        # Create new game

        if answer == 1:

            game_id = create_game(player_id, airport_country)
            print(game_id)

            games_info = game_information(game_id)

            for game_info in games_info:
                goal_ident, goal_name, goal_latitude_deg, goal_longitude_deg, goal_continent, goal_municipality, goal_country_name, goal_airport, kilometers_traveled, score, level_reached = game_info

            print("\nCurrent game info\n")

            print(game_info)

            new_game = True

        # Load game and get information about the previous game

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

    # First written path for the new game when new_game == True which mmeans that we dont load an old game but start a new game from the beginning

    if new_game == True:

        # Reming player where he is traveling and long the flight is

        print("\n The distance between " + airport_name + " and airport " + goal_name + " is: \n")

        print(distance_in_kilometers(latitude_deg, longitude_deg, goal_latitude_deg, goal_longitude_deg))

    return user_name, game_id

        # Here the first game actually begins

def part_one(user_name, game_id):

        print("\nAre you ready to start the game?" \
              "\n1 - Yes, I am ready!" \
              "\n2 - No, I want to exit game!")

        answer = int(input('Give me your answer: '))

        if answer == 1:

            # Game play for the first game

            score = capitals_game(game_id)

            print(score)

            # Try until player either wins the game or desides to quit

            while score < 55:

                print("\nYou lost. Not enough points")
                print("\nDo you eant to try again or finish game?" \
                      "\n1 - Try again" \
                      "\n2 - Finish game")

                answer = int(input('Give me your answer: '))

                if answer == 1:

                    score = capitals_game(game_id)

                elif answer == 2:

                    sys.exit()

        elif answer == 2:

            sys.exit()

        print("\n You won the first mini game!")

        # We finish the first game and now we update user score information in the games table and game information in the players table

        update_user_score(score, game_id)

        sql = f"UPDATE players SET games_played = games_played + 1, last_game = {game_id} WHERE user_name = '{user_name}';"
        kursori = yhteys.cursor()
        kursori.execute(sql)
        yhteys.commit()
        print("ok!")
        return score



def part_two(game_id):
    print("\nAre you ready to start the second game?" \
    "\n1 - Yes, I am ready!" \
    "\n2 - No, I want to exit game!")

    answer = int(input('\nGive me your answer: '))

    if answer == 1:

        # Game play for the second game

        score = count_game()

        print(score)

        # Once again we wait for player to win the game
        if score >= 55:
            print(
                f"Ilmatankkaus onnistui! Voit jatkaa lentoasi. Tämän pelin pistemääräsi on {score}.")
            # update_player(cursor, db, pelaaja_id, total_score)
            choice = input("Haluatko jatkaa pelaamista?(Kyllä/Poistu)")
            if choice == 'Kyllä':
                print("Lento jatkuu!")
            else:
                print(f"Sait {score} pistettä.")


        else:
            print(f"Epäonnistuit ja jouduit tekemään hätälaskun. Sait {score} pistettä.")
            choice = input("Haluatko yrittää uudelleen? (Kyllä/Poistu)")
            if choice == 'Kyllä':
                print(
                    "Olet ilmassa matkalla määränpäähäsi. Hätätilanne! Polttoaine on vähissä! Voit saada lisää polttoainetta ratkaisemalla tämän pelin. Jos epäonnistut, joudut tekemään hätälaskun.")
                count_game(pelaaja_id)
            else:
                print(f"Sait {score_count_game} pistettä.")
        while score < 55:

            print("\nEpäonnistuit ja jouduit tekemään hätälaskun. Sait {score} pistettä.")
            choice = input("Haluatko yrittää uudelleen? (Kyllä/Poistu)")

            answer = int(input('\nGive me your answer: '))

            if answer == 1:

                score = count_game()

            elif answer == 2:

                sys.exit()

    elif answer == 2:

        sys.exit()

    print("\n You won the second mini game!")

    # We again update score and level_reached in the games table

    update_user_score(score, game_id)
    return score

def part_three(game_id):
    # Now we can start with the third mini game
    print("\nAre you ready to start the third game?" \
          "\n1 - Yes, I am ready!" \
    "\n2 - No, I want to exit game!")

    answer = int(input('\nGive me your answer: '))

    if answer == 1:

        # Game play for the third game

        score = count_game()

        print(score)

        if score == 100:

            print("\nYou won third and final game!")

            update_user_score(score, game_id)

            # Set last_game in players back to 0, because we will not load this game

            update_last_game(user_name)

        #if score < 100:

            # If player lost in the final game, the information about him is deleted both from games and players tables

            #delete_user(player_id, user_name)

    elif answer == 2:

        sys.exit()

    return score

if __name__ == "__main__":
    # The second path for loading the game when new_game == False

    '''elif new_game == False:

        print("\nWe continue with the old game")

        print("\n The distance between " + airport_name + " and airport " + goal_name + " is: \n")

        print(distance_in_kilometers(latitude_deg, longitude_deg, goal_latitude_deg, goal_longitude_deg))

        # If level reached is 1, we start player with the second mini game

        if level_reached == 1:

            # Now we can start with the second mini game

            print("\nAre you ready to start the second game?" \
            "\n1 - Yes, I am ready!" \
            "\n2 - No, I want to exit game!")

            answer = int(input('\nGive me your answer: '))

            if answer == 1:

                # Game play for the second game

                score = second_mini_game()

                print(score)

                while score < 55:

                    print("\nYou lost. Not enough points")
                    print("\nDo you eant to try again or finish game?" \
                    "\n1 - Try again" \
                    "\n2 - Finish game")

                    answer = int(input('\nGive me your answer: '))

                    if answer == 1:

                        score = word_game()

                    elif answer == 2:

                        sys.exit()

            elif answer == 2:

                sys.exit()

            print("\n You won the second mini game!")

            # We again update score and level_reached in the games table

            update_user_score(score, last_game)

            print("\nAre you ready to start the third game?" \
            "\n1 - Yes, I am ready!" \
            "\n2 - No, I want to exit game!")

            answer = int(input('\nGive me your answer: '))

            if answer == 1:

                # Game play for the second game

                score = third_mini_game()

                print(score)

                if score == 100:

                    print("\nYou won third and final game!")

                    update_user_score(score, last_game)

                    # Set last_game in players back to 0, because we will not load this game

                    update_last_game(user_name)

                if score < 100:

                    delete_user(player_id, user_name)

            elif answer == 2:

                sys.exit()

        # In case level reached is equal to 2, we start player from the third mini game

        elif level_reached == 2:

            print("\nAre you ready to start the third game?" \
            "\n1 - Yes, I am ready!" \
            "\n2 - No, I want to exit game!")

            answer = int(input('\nGive me your answer: '))

            if answer == 1:

                # Game play for the second game

                score = third_mini_game()

                print(score)

                if score == 100:

                    print("\nYou won third and final game!")

                    update_user_score(score, last_game)

                    # Set last_game in players back to 0, because we will not load this game

                    update_last_game(user_name)

                if score < 100:

                    delete_user(player_id, user_name)

            elif answer == 2:

                sys.exit()
    '''