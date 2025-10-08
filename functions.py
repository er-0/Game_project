import sys

from db import yhteys
from geopy import distance


# Function to register users ---------------------------------------------------------------------------

def loggin():

    name = input('\nAnna nimi: ')

    sql = f"SELECT COUNT(*) FROM players WHERE user_name = '{name}';"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    count = kursori.fetchone()[0]  

    while count != 0:
         
        print("\nTämä nimi on jo käytössä. ")
        print("\nOle hyvä ja valitse toinen nimi.")

        name = input('\nAnna nimi: ')

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

# This will be the first game function ----------------------------------------------------------------

def first_mini_game():

    score = int(input('Anna ensimmäisen pelin pisteet (0-100): '))

    return score

# -----------------------------------------------------------------------------------------------------

# This will be the second game function ---------------------------------------------------------------

def second_mini_game():

    score = int(input('Anna toisen pelin pisteet (0-100): '))

    return score

# -----------------------------------------------------------------------------------------------------

# This will be the third game function ----------------------------------------------------------------

def third_mini_game():

    score = int(input('Anna kolmannen pelin pisteet (0-100): '))

    return score

# -----------------------------------------------------------------------------------------------------

# Function to update score and level of the player ----------------------------------------------------

def update_user_score(score, game_id):

    sql = f"UPDATE games SET score = score + {score}, level_reached = level_reached + 1 WHERE game_id = {game_id};"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    yhteys.commit()

    tulos = print("Pisteet muutettu.")

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

    tulos = print("Menetit lentolupasi etkä voi lentää.")

    return tulos

# -----------------------------------------------------------------------------------------------------

# This is the begging of the game. We say hello to the player, tell him about the game and ask him if is already regestered

print("Hei ja tervetuloa!\n" \
"Tämä on kevyt lentosimulaatio,\n" \
"jossa pelaat kolmea minipeliä\n" \
"suorittaaksesi onnistuneen lennon.\n" \
"Oletko pelannut aiemmin?\n" \
"1 - Kyllä\n" \
"2 - Ei, olen uusi pelaaja\n")

yes_no = int(input('1 tai 2: '))

# If player is already registered

if yes_no == 1:
    
    user_name = input('Etsitään lentolupasi. Anna lentäjänimesi: ')

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
            print("\nNimeä ei löydy.")
            print("\nYritä uudelleen.")

            user_name = input('\nEtsitään lentolupasi. Anna lentäjänimesi: ')

            sql = f"SELECT COUNT(*) FROM players WHERE user_name = '{user_name}';"
            kursori = yhteys.cursor()
            kursori.execute(sql)
            count = kursori.fetchone()[0]

        # After too many tries we inform the user that he has failed and ask him to create a new account
        
        if tries > 3:
            print("\nOlet yrittänyt liian monta kertaa.")
            print("\nSinulla ei ole lentolupaa.")
            print("\nVoit rekisteröityä lentäjäksi, jos haluat.")
            print("\n1 - Rekisteröidy lentäjäksi" \
            "\n2 - Lopeta peli")

            decision = int(input('\n1 tai 2: '))

            # User creates a new pilot name

            if decision == 1:

                user_name = loggin()
                print("\nNimesi on: " + user_name)

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

    print("\nRekisteröidy lentäjänä.")
    print("\nValitse itsellesi uniikki nimi: ")

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

    print("\nSinun täytyy aloittaa uusi peli.")
    print("\n1 - Aloita uusi peli" \
    "\n2 - Lopeta peli")

    answer = int(input('\n1 tai 2: '))

    if answer == 1:

        # Create new game and get game_id

        game_id = create_game(player_id, airport_country)
        print(game_id)

        games_info = game_information(game_id)

        # Save new game information as global variables

        for game_info in games_info:
            goal_ident, goal_name, goal_latitude_deg, goal_longitude_deg, goal_continent, goal_municipality, goal_country_name, goal_airport, kilometers_traveled, score, level_reached = game_info

        print("\nPelitilasi on seuraava.\n")

        print(game_info)

        new_game = True

    elif answer == 2:

        sys.exit()     

# This path is for when player has an unfinished game

elif last_game != 0:

    print("\nSinulla on keskeneräinen peli. Haluatko aloittaa uuden pelin, jatkaa peliä, vai lopettaa pelin?")
    print("\n1 - Uusi peli" \
    "\n2 - Jatkaa peliä" \
    "\n3 - Lopeta peli")

    answer = int(input("\n1, 2 tai 3: "))

    # Create new game

    if answer == 1:

        game_id = create_game(player_id, airport_country)
        print(game_id)

        games_info = game_information(game_id)

        for game_info in games_info:
            goal_ident, goal_name, goal_latitude_deg, goal_longitude_deg, goal_continent, goal_municipality, goal_country_name, goal_airport, kilometers_traveled, score, level_reached = game_info

        print("\nPelitilasi on seuraava.\n")

        print(game_info)

        new_game = True

    # Load game and get information about the previous game

    elif answer == 2:

        print("\nEdellisen pelin tiedot.\n")

        games_info = game_information(last_game)

        for game_info in games_info:
            goal_ident, goal_name, goal_latitude_deg, goal_longitude_deg, goal_continent, goal_municipality, goal_country_name, goal_airport, kilometers_traveled, score, level_reached = game_info

        print("\nNykyisen pelin tiedot.\n")

        print(game_info)

        new_game = False
    
    elif answer == 3:

        sys.exit()

# First written path for the new game when new_game == True which mmeans that we dont load an old game but start a new game from the beginning

if new_game == True:

    # Reming player where he is traveling and long the flight is

    print("\n Lentokentältä " + airport_name + " lentokentälle " + goal_name + " on: \n")

    kilometers_for_table = distance_in_kilometers(latitude_deg, longitude_deg, goal_latitude_deg, goal_longitude_deg)

    print(kilometers_for_table)
    print(" kilometriä.")

    sql = f"UPDATE games SET  kilometers_traveled = '{kilometers_for_table}' WHERE player_id = '{player_id}';"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    yhteys.commit()

    # Here the first game actually begins

    print("\nOletko valmis aloittamaan?" \
    "\n1 - Kyllä, olen valmis" \
    "\n2 - Ei, haluan poistua pelistä")

    answer = int(input('\n1 tai 2: '))

    if answer == 1:

        # Game play for the first game 

        score = first_mini_game()

        print(score)

        # Try until player either wins the game or desides to quit

        while score < 55:

            print("\nHävisit. Et saanut riittävästi pisteitä.")
            print("\nHaluatko yrittää uudestaan vai lopettaa pelin?" \
            "\n1 - Yritän uudelleen" \
            "\n2 - Lopeta peli")

            answer = int(input('1 tai 2: '))

            if answer == 1:

                score = first_mini_game()
            
            elif answer == 2: 

                sys.exit()
                      
    elif answer == 2:

        sys.exit() 

    print("\n Voitit ensimmäisen pelin!")

    # We finish the first game and now we update user score information in the games table and game information in the players table

    update_user_score(score, game_id)  

    sql = f"UPDATE players SET games_played = games_played + 1, last_game = {game_id} WHERE user_name = '{user_name}';"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    yhteys.commit()  

    # Now we can start with the second mini game

    print("\nOletko valmis aloittamaan toisen pelin?" \
    "\n1 - Kyllä, olen valmis" \
    "\n2 - Lopeta peli")

    answer = int(input('\n1 tai 2: '))

    if answer == 1:

        # Game play for the second game 

        score = second_mini_game()

        print(score)

        # Once again we wait for player to win the game

        while score < 55:

            print("\nEt saanut tarpeeksi pisteitä. Hävisit.")
            print("\nHaluatko yrittää uudestaan vai lopettaa pelin?" \
            "\n1 - Yritän uudeleen" \
            "\n2 - Lopeta peli")

            answer = int(input('\n1 tai 2: '))

            if answer == 1:

                score = second_mini_game()
            
            elif answer == 2: 

                sys.exit()

    elif answer == 2:

        sys.exit() 

    print("\n Voitit toisen pelin!")

    # We again update score and level_reached in the games table
    
    update_user_score(score, game_id)

    print("\nOletko valmis aloittamaan kolmannen pelin??" \
    "\n1 - Kyllä, olen valmis" \
    "\n2 - Lopeta peli")

    answer = int(input('\n1 tai 2: '))

    if answer == 1:

        # Game play for the third game 

        score = third_mini_game()

        print(score)

        if score == 100:

            print("\nVoitit kolmannen ja viimeisen pelin!")

            update_user_score(score, game_id)

            # Set last_game in players back to 0, because we will not load this game

            update_last_game(user_name)

        if score < 100:

            # If player lost in the final game, the information about him is deleted both from games and players tables

            delete_user(player_id, user_name)

    elif answer == 2:

        sys.exit()   


# The second path for loading the game when new_game == False

elif new_game == False:

    print("\nJatketaan vanhasta pelistä.")

    print("\n Lentokentältä " + airport_name + "lentokentälle " + goal_name + "on: \n")

    print(distance_in_kilometers(latitude_deg, longitude_deg, goal_latitude_deg, goal_longitude_deg))
    print("kilometriä.")

    # If level reached is 1, we start player with the second mini game

    if level_reached == 1:

        # Now we can start with the second mini game

        print("\nOletko valmis aloittamaan toisen pelin?" \
        "\n1 - Kyllä, olen valmis" \
        "\n2 - Lopeta peli")

        answer = int(input('\n1 tai 2: '))

        if answer == 1:

            # Game play for the second game 

            score = second_mini_game()

            print(score)

            while score < 55:

                print("\nEt saanut tarpeeksi pisteitä. Hävisit.")
                print("\nHaluatko yrittää uudestaan vai lopettaa pelin?" \
                "\n1 - Yritän uudeleen" \
                "\n2 - Lopeta peli")

                answer = int(input('\n1 tai 2: '))

                if answer == 1:

                    score = second_mini_game()
            
                elif answer == 2: 

                    sys.exit()

        elif answer == 2:

            sys.exit() 

        print("\n Voitit toisen minipelin!")

        # We again update score and level_reached in the games table
    
        update_user_score(score, last_game)

        print("\nOletko valmis aloittamaan toisen pelin?" \
        "\n1 - Kyllä, olen valmis" \
        "\n2 - Lopeta peli")

        answer = int(input('\n1 tai 2: '))

        if answer == 1:

            # Game play for the second game 

            score = third_mini_game()

            print(score)

            if score == 100:

                print("\nVoitit kolmannen ja viimeisen pelin!")

                update_user_score(score, last_game)

                # Set last_game in players back to 0, because we will not load this game

                update_last_game(user_name)

            if score < 100:

                delete_user(player_id, user_name)

        elif answer == 2:

            sys.exit()   
        
    # In case level reached is equal to 2, we start player from the third mini game

    elif level_reached == 2:

        print("\nOletko valmis aloittamaan kolmannen pelin??" \
        "\n1 - Kyllä, olen valmis" \
        "\n2 - Lopeta peli")

        answer = int(input('\n1 tai 2: '))

        if answer == 1:

            # Game play for the second game 

            score = third_mini_game()

            print(score)

            if score == 100:

                print("\noitit kolmannen ja viimeisen pelin!")

                update_user_score(score, last_game)

                # Set last_game in players back to 0, because we will not load this game

                update_last_game(user_name)
            
            if score < 100:

                delete_user(player_id, user_name)

        elif answer == 2:

            sys.exit()    

print("Pelin loppu. Roll the credits....")
print("Kiitos pelaamisesta!")