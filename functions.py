import sys

from db import yhteys
from geopy import distance

from capitals_game import capitals_game
from count_game import count_game
from word_game import word_game


# Function to register users ---------------------------------------------------------------------------

def login():
    name = input('\nAnna nimesi: ')

    sql = f"SELECT COUNT(*) FROM players WHERE user_name = %s;"
    kursori = yhteys.cursor()
    kursori.execute(sql, (name,))
    count = kursori.fetchone()[0]

    while count != 0:
        print("\nTämä nimi on jo käytössä.")
        print("\nOle hyvä ja valitse toinen nimi.")

        name = input('\nAnna nimi: ')

        sql = f"SELECT COUNT(*) FROM players WHERE user_name = %s;"
        kursori = yhteys.cursor()
        kursori.execute(sql, (name,))
        count = kursori.fetchone()[0]

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

    return name


# -------------------------------------------------------------------------------------------------------

# Function to fetch all information from the database on the user ----------------------------------------

def player_information(name):
    sql = (f"SELECT a.ident, a.name, a.latitude_deg, a.longitude_deg, a.continent, a.municipality, a.country_name, "
           f"p.id, p.games_played, p.last_game FROM game_airports AS a INNER JOIN players AS p ON p.starting_airport "
           f"= a.ident where p.user_name = %s;")
    kursori = yhteys.cursor()
    kursori.execute(sql, (name,))
    users_information = kursori.fetchall()

    return users_information


# -----------------------------------------------------------------------------------------------------

# Function to create a new game ------------------------------------------------------------------------

def create_game(player_id, airport_country):
    sql = f"SELECT ident FROM game_airports WHERE country_name != %s ORDER BY RAND() LIMIT 1;"
    kursori = yhteys.cursor()
    kursori.execute(sql, (airport_country,))
    goal_ident = kursori.fetchone()[0]

    sql = f"INSERT INTO games (player_id, goal_airport) VALUES (%s, %s) RETURNING game_id;"
    kursori = yhteys.cursor()
    kursori.execute(sql, (player_id, goal_ident))
    game_id = kursori.fetchone()[0]
    yhteys.commit()

    return game_id


# -----------------------------------------------------------------------------------------------------

# Function to fetch all information about player games ------------------------------------------------

def game_information(id):
    sql = (f"SELECT a.ident, a.name, a.latitude_deg, a.longitude_deg, a.continent, a.municipality, a.country_name, "
           f"g.goal_airport, g.kilometers_traveled, g.score, g.level_reached from games as g LEFT JOIN game_airports "
           f"AS a ON g.goal_airport = a.ident WHERE g.game_id = %s;")
    kursori = yhteys.cursor()
    kursori.execute(sql, (id,))
    information = kursori.fetchall()

    return information


# -----------------------------------------------------------------------------------------------------

# Function to calculate the distance between airports -------------------------------------------------

def distance_in_kilometers(first_lat, first_long, second_lat, second_long):
    start_coordinates = (first_lat, first_long)
    finish_coordinates = (second_lat, second_long)

    kilometers = int(distance.distance(start_coordinates, finish_coordinates).km)

    return kilometers


# -----------------------------------------------------------------------------------------------------

# Function to update score and level of the player ----------------------------------------------------

def update_user_score(score, game_id):
    sql = f"UPDATE games SET score = score + %s, level_reached = level_reached + 1 WHERE game_id = %s;"
    kursori = yhteys.cursor()
    kursori.execute(sql, (score, game_id))
    yhteys.commit()

    return


# -----------------------------------------------------------------------------------------------------

# Function to return last game to 0 after level 3 -----------------------------------------------------

def update_last_game(name):
    sql = f"UPDATE players SET last_game = 0 WHERE user_name = %s;"
    kursori = yhteys.cursor()
    kursori.execute(sql, (name,))
    yhteys.commit()

    return


# -----------------------------------------------------------------------------------------------------

# Function to check final score -----------------------------------------------------------------------

def check_score(game_id):
    sql = f"SELECT score FROM games WHERE game_id = %s;"
    kursori = yhteys.cursor()
    kursori.execute(sql, (game_id,))
    score = kursori.fetchone()[0]

    return score


# -----------------------------------------------------------------------------------------------------

# Function to delete player from the database ---------------------------------------------------------

def delete_user(id, name):
    sql = f"DELETE FROM games WHERE player_id = %s;"
    kursori = yhteys.cursor()
    kursori.execute(sql, (id,))
    yhteys.commit()

    sql = f"DELETE FROM players WHERE user_name = %s;"
    kursori = yhteys.cursor()
    kursori.execute(sql, (name,))
    yhteys.commit()

    return


# -----------------------------------------------------------------------------------------------------

# Function to update kilometers_traveled in the games -------------------------------------------------

def update_kilometers(kilometers_for_table, player_id):
    sql = f"UPDATE games SET kilometers_traveled = %s WHERE player_id = %s;"
    kursori = yhteys.cursor()
    kursori.execute(sql, (kilometers_for_table, player_id))
    yhteys.commit()

    return


# -----------------------------------------------------------------------------------------------------

# This is the begging of the game. We say hello to the player, tell him about the game and ask him if is already
# registered
def intro():
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

        sql = f"SELECT COUNT(*) FROM players WHERE user_name = %s;"
        kursori = yhteys.cursor()
        kursori.execute(sql, (user_name,))
        count = kursori.fetchone()[0]

        tries = 0

        # If there is no such name count will be equal to 0, if there is such a name, count will be 1.
        # We want count to be 1.

        while count == 0:

            tries = tries + 1

            # Player will have limited tries to enter the name

            if tries < 3:
                print("\nNimeä ei löydy.")
                print("\nYritä uudelleen.")

                user_name = input('\nEtsitään lentolupasi. Anna lentäjänimesi: ')

                sql = f"SELECT COUNT(*) FROM players WHERE user_name = %s;"
                kursori = yhteys.cursor()
                kursori.execute(sql, (user_name,))
                count = kursori.fetchone()[0]

            # After too many tries we inform the user that he has failed and ask him to create a new account

            if tries > 3:
                print("\nOlet yrittänyt liian monta kertaa." \
                      "\nSinulla ei ole lentolupaa." \
                      "\nVoit rekisteröityä lentäjäksi, jos haluat." \
                      "\n1 - Rekisteröidy lentäjäksi" \
                      "\n2 - Lopeta peli")

                decision = int(input('\n1 tai 2: '))

                # User creates a new pilot name

                if decision == 1:

                    user_name = login()
                    print("\nNimesi on: " + user_name)

                    count = 1

                    break

                elif decision == 2:

                    sys.exit()

        # Get all information about the user and save as global variables

        users_information = player_information(user_name)

        for user_information in users_information:
            (airport_ident, airport_name, latitude_deg, longitude_deg, airport_continent, airport_municipality,
             airport_country, player_id, games_played, last_game) = user_information

        # Variables for user information

        print(f"\nOlet lentäjä, jonka kotikenttä on {airport_name} ({airport_ident})."
              f"\nLentokenttä sijaitsee maassa {airport_country}, kunnassa {airport_municipality}."
              f"\nPelaamiesi pelien määrä on: {games_played}")

    # This answer means that the user is a new player and we ask him to register

    elif yes_no == 2:

        print("\nRekisteröidy lentäjänä.")
        print("\nValitse itsellesi uniikki nimi: ")

        # Player creates a new pilot id

        user_name = login()

        # Get information about the user

        users_information = player_information(user_name)

        for user_information in users_information:
            (airport_ident, airport_name, latitude_deg, longitude_deg, airport_continent, airport_municipality,
             airport_country, player_id, games_played, last_game) = user_information

        print(f"\nOlet lentäjä, jonka kotikenttä on {airport_name} ({airport_ident})."
              f"\nLentokenttä sijaitsee maassa {airport_country}, kunnassa {airport_municipality}."
              f"\nPelaamiesi pelien määrä on: {games_played}")

        # Check for an existence of the last game. If user has a lat game not equal to 0 we can load an old game
    # information or create new game, if last game is 0, we create new game

    # This is the path for no previous game

    if last_game == 0:

        print("\nSinun täytyy aloittaa uusi peli.")
        print("\n1 - Aloita uusi peli" \
              "\n2 - Lopeta peli")

        answer = int(input('\n1 tai 2: '))

        if answer == 1:

            # Create new game and get game_id

            game_id = create_game(player_id, airport_country)

            games_info = game_information(game_id)

            # Save new game information as global variables

            for game_info in games_info:
                (goal_ident, goal_name, goal_latitude_deg, goal_longitude_deg, goal_continent, goal_municipality,
                 goal_country_name, goal_airport, kilometers_traveled, score, level_reached) = game_info

            print(f"Kohdemaaksesi on määrätty {goal_name} ({goal_ident}). \nLentokenttä sijaitsee maassa"
                  f" {goal_country_name}, kunnassa {goal_municipality}.")


        elif answer == 2:

            sys.exit()

    # This path is for when player has an unfinished game

    elif last_game != 0:

        print("\nSinulla on keskeneräinen peli. Haluatko aloittaa uuden pelin, jatkaa peliä, vai lopettaa pelin?")
        print("\n1 - Uusi peli" \
              "\n2 - Jatka peliä" \
              "\n3 - Lopeta peli")

        answer = int(input("\n1, 2 tai 3: "))

        # Create new game

        if answer == 1:

            game_id = create_game(player_id, airport_country)
            print(game_id)

            games_info = game_information(game_id)

            for game_info in games_info:
                (goal_ident, goal_name, goal_latitude_deg, goal_longitude_deg, goal_continent, goal_municipality,
                 goal_country_name, goal_airport, kilometers_traveled, score, level_reached) = game_info

            print(f"Kohdemaaksesi on määrätty {goal_name} ({goal_ident}). \nLentokenttä sijaitsee maassa"
                  f" {goal_country_name}, kunnassa {goal_municipality}.")


        # Load game and get information about the previous game

        elif answer == 2:

            games_info = game_information(last_game)

            for game_info in games_info:
                (goal_ident, goal_name, goal_latitude_deg, goal_longitude_deg, goal_continent, goal_municipality,
                 goal_country_name, goal_airport, kilometers_traveled, score, level_reached) = game_info

            print(f"Kohdemaaksesi on määrätty {goal_name} ({goal_ident}). \nLentokenttä sijaitsee maassa"
                  f" {goal_country_name}, kunnassa {goal_municipality}.")
            print(f"Olet saavuttanut tason {level_reached}  ja pisteesi ovat {score}")

            game_id = last_game

        elif answer == 3:

            sys.exit()

    kilometers_for_table = distance_in_kilometers(latitude_deg, longitude_deg, goal_latitude_deg, goal_longitude_deg)

    if level_reached == 0:
        # Reming player where he is traveling and long the flight is

        print("\nEtäisyys kenttien " + airport_name + " ja " + goal_name + " välillä on: \n")

        print(distance_in_kilometers(latitude_deg, longitude_deg, goal_latitude_deg, goal_longitude_deg))

    return player_id, user_name, game_id, level_reached, kilometers_for_table

    # Here the first game actually begins


def part_one(user_name, game_id, answer=None):
    if answer is None:
        return {
            "message": "Oletko valmis aloittamaan?",
            "options": ["1 - Kyllä", "2 - Ei"]
        }

    # If answer is 1, calculate score
    if answer == 1:
        score = capitals_game(game_id)
        update_user_score(score, game_id)
        return {
            "message": "Peli suoritettu",
            "score": score
        }

    elif answer == 2:
        return {"message": "Peli keskeytetty"}


def part_two(user_name, game_id):
    print("\nOletko valmis aloittamaan toisen pelin?" \
          "\n1 - Kyllä, olen valmis" \
          "\n2 - Lopeta peli")

    answer = int(input('\n1 tai 2: '))

    if answer == 1:

        # Game play for the second game

        print(
            "Olet ilmassa matkalla määränpäähäsi. Hätätilanne! Polttoaine on vähissä! \nVoit saada lisää "
            "polttoainetta ratkaisemalla tämän laskupelin. Jos epäonnistut, joudut tekemään hätälaskun.")

        score = count_game()

        # Once again we wait for player to win the game

        while score < 55:

            print(f"\nEpäonnistuit ja jouduit tekemään hätälaskun. Sait {score} pistettä.")
            choice = input("Haluatko yrittää uudelleen? \n1 - Kyllä \n2 - Poistu\n1 tai 2: ")

            if choice == '1':
                score = count_game()

            elif choice == '2':
                print(f"Sait {score} pistettä.")
                sys.exit()

    elif answer == 2:
        sys.exit()

    print(f"Ilmatankkaus onnistui! Voit jatkaa lentoasi. Tämän pelin pistemääräsi on {score}.")
    update_user_score(score, game_id)

    choice = input("Haluatko jatkaa pelaamista?\n1 - Kyllä\n2 - Poistu\n1 tai 2: ")
    if choice == '1':
        print("Lento jatkuu!")
    else:
        sys.exit()

    # We finish the second game and update user score information in the games table

    return score


def part_three(player_id, user_name, game_id, kilometers_for_table):
    # Now we can start with the third mini game
    print("\nOletko valmis aloittamaan kolmannen pelin??" \
          "\n1 - Kyllä, olen valmis" \
          "\n2 - Lopeta peli")

    answer = int(input('\n1 tai 2: '))

    if answer == 1:

        # Game play for the third game

        score = word_game()

        if score >= 100:
            print("\nVoitit kolmannen ja viimeisen pelin!")

            update_kilometers(kilometers_for_table, player_id)

            update_user_score(score, game_id)

            # Set last_game in players back to 0, because we will not load this game

            update_last_game(user_name)

            final_score = check_score(game_id)

            print("Olet mahtava lentäjä! Kiitos pelaamisesta!")
            print(f"Pistemääräsi on {final_score}")

        if score < 100:
            # If player lost in the final game, the information about him is deleted both from games and players tables

            delete_user(player_id, user_name)

    elif answer == 2:
        sys.exit()

    yhteys.close()

    return score
