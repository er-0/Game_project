from db import yhteys
import time
import random


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
    score = 0

    score += play_level(1, 5, time_limit=5)
    score += play_level(2, 5, time_limit=10)
    score += play_level(3, 2, time_limit=15)
    return score

if __name__ == "__main__":
    count_game()