from db import yhteys
import time
import random


print("Olet ilmassa matkalla määränpäähäsi. Hätätilanne! Polttoaine on vähissä! Voit saada lisää polttoainetta ratkaisemalla tämän laskupelin. Jos epäonnistut, joudut tekemään hätälaskun.")

player_id = 2

def get_tasks(level, limit):
    db = yhteys
    cursor = db.cursor()
    cursor.execute(
        "SELECT question, answer, points FROM count_game WHERE level=%s ORDER BY RAND() LIMIT %s;",
        (level, limit)
    )
    return cursor.fetchall()

def play_level(level, limit, time_limit):
    level_score = 0
    tasks = get_tasks(level, limit)
    random.shuffle(tasks)
    for question, answer, points in tasks:
        print(f"\nLaske: {question}")
        start_time = time.time()
        player_input = input(f"Sinulla on {time_limit} sekuntia vastata: ")
        elapsed = time.time() - start_time

        if elapsed > time_limit:
            print(f"Aika loppui! Et saanut pisteitä tästä laskusta. Oikea vastaus oli {answer}.")
            continue

        try:
            if int(player_input) == int(answer):
                level_score += points
                print(f"Oikein! {points} pistettä.")
            else:
                print(f"Väärin. Oikea vastaus oli {answer}.")
        except ValueError:
                print("Syötä vain numeroita!")
    return level_score

def count_game():
    score_count_game = 0

    score_count_game += play_level(1, 5, time_limit=5)
    score_count_game += play_level(2, 5, time_limit=10)
    score_count_game += play_level(3, 2, time_limit=15)
    print(score_count_game)

# vähimmäispisteet laskupelistä = 55


    if score_count_game >=55:
        print(f"Ilmatankkaus onnistui! Voit jatkaa lentoasi. Tämän pelin pistemääräsi on {score_count_game}.")
        choice = input("Haluatko jatkaa pelaamista?(Kyllä/Poistu)")
        if choice == 'Kyllä':
            print("Lento jatkuu!")
        else:
            print(f"Sait {score_count_game} pistettä.")


    else:
        print(f"Epäonnistuit ja jouduit tekemään hätälaskun. Sait {score_count_game} pistettä.")
        choice = input("Haluatko yrittää uudelleen? (Kyllä/Poistu)")
        if choice == 'Kyllä':
            print("Olet ilmassa matkalla määränpäähäsi. Hätätilanne! Polttoaine on vähissä! Voit saada lisää polttoainetta ratkaisemalla tämän laskupelin. Jos epäonnistut, joudut tekemään hätälaskun.")
            count_game()
        else:
            print("Peli sulkeutuu")


if __name__ == "__main__":
    count_game()