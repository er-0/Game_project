from db import yhteys
import time

print("Olet ilmassa matkalla määränpäähäsi. Hätätilanne! Polttoaine on vähissä! Voit saada lisää polttoainetta ratkaisemalla tämän pelin. Jos epäonnistut, joudut tekemään hätälaskun.")

total_score = 0
level = 2

def get_tasks(cursor, level, limit):
    cursor.execute(
        "SELECT question, answer, points FROM count_game WHERE level=%s ORDER BY RAND() LIMIT %s;",
        (level, limit)
    )
    return cursor.fetchall()

def update_player(cursor, db, player_id, points):
    cursor.execute(
        "UPDATE player SET points = points + %s, level = 2 WHERE id = %s",
        (points, player_id)
    )
    db.commit()

def count_game(player_id=1):
    db = yhteys
    cursor = db.cursor()

    difficulty_levels = [
        (1, 5, 5),  # helppo
        (2, 10, 5),  # normaali
        (3, 15, 2)  # vaikea
    ]


    for level, time_limit, num_q, points in difficulty_levels:
        print(f"\n--- Level: {level.upper()} ---")
        tasks = get_tasks(cursor, level, num_q)

    for question, answer, points in tasks:
        print(f"\nLaske: {question}")
        start_time = time.time()
        player_input = input(f"Sinulla on {time_limit} sekuntia vastata: ")
        elapsed = time.time() - start_time

        if elapsed > time_limit:
            print("⏰ Aika loppui! Et saanut pisteitä tästä laskusta.")
            continue

        try:
            if int(player_input) == int(answer):
                    total_score += points
                    print(f"✅ Oikein! +{points} pistettä.")
            else:
                    print(f"❌ Väärin. Oikea vastaus oli {answer}.")
        except ValueError:
                print("⚠️ Syötä vain numeroita!")

# vähimmäispisteet laskupelistä = 55

score_count_game =


    if points_count_game >=55:
        print(f"Ilmatankkaus onnistui! Voit jatkaa lentoasi. Tämän pelin pistemääräsi on {score_count_game}. Kokonaistuloksesi on "{total_score}")
        update_player(cursor, db, pelaaja_id, total_score)
        choice = input("Haluatko jatkaa pelaamista?(Kyllä/Poistu)")
        if choice == 'Kyllä':
            print("Lento jatkuu!")
        else:
        print(f"Sait {score_count_game} pistettä. Kokonaispisteesi on {total_score}")
        break

    else:
        print("Epäonnistuit ja jouduit tekemään hätälaskun. Sait {pisteet} pistettä.")
        choice = input("Haluatko yrittää uudelleen? (Kyllä/Poistu)")
        if choice == 'Kyllä':
            print("Olet ilmassa matkalla määränpäähäsi. Hätätilanne! Polttoaine on vähissä! Voit saada lisää polttoainetta ratkaisemalla tämän pelin. Jos epäonnistut, joudut tekemään hätälaskun.")
    )   count_game(pelaaja_id)
        else:
            print(f"Sait {score_count_game} pistettä. Kokonaispisteesi on {total_score}")
            break

if __name__ == "__main__":
    count_game()