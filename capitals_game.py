from db import yhteys
import random

def fetch_questions(level, amount):
    sql = f"SELECT question, answer, points FROM capital_game WHERE level = %s ORDER BY RAND() LIMIT %s"
    cursor = yhteys.cursor()
    cursor.execute(sql, (level, amount))
    rows = cursor.fetchall()
    return rows

def fetch_wrong_answers():
    sql = f"SELECT answer FROM capital_game WHERE level != 1 ORDER BY RAND() LIMIT 3"
    cursor = yhteys.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    wrong_answers = [row[0] for row in rows]
    return wrong_answers

def update_score(game_id, user_points):
    sql = "UPDATE games SET score = score + %s WHERE game_id = %s"
    cursor = yhteys.cursor()
    cursor.execute(sql, (user_points, game_id))
    yhteys.commit()
    cursor.close()

def play_level(level, amount):
    questions = fetch_questions(level, amount)
    level_points = 0

    for q in questions:
        if level == 2 or level == 3:
            answers = fetch_wrong_answers()
            answers.append(q[1])
            random.shuffle(answers)
            print(q) #testaamista varten, tulostaa Q&A
            print(answers)
        user_answer = input(q[0] + " ")
        #käyttäjä voi kirjoittaa koko vastauksen (washington dc == Washington, D.C.) tai ### vaihtoehdon numeron
        if ''.join(filter(str.isalpha, user_answer)).casefold() == ''.join(filter(str.isalpha, q[1])).casefold():
            print("Oikein!")
            level_points += q[2]
    return level_points

def capitals_game(game_id):
    user_points = 0
    user_points += play_level(1, 5)
    user_points += play_level(2, 5)
    user_points += play_level(3, 2)
    print(user_points)
    update_score(game_id, user_points)

capitals_game(1)
'''
Helppo: 5 k, 4 p. Vastaukset kirjoitetaan itse.
Normaali: 5 k, 10 p. Pelaaja näkee 4 vastausvaihtoehtoa, mutta syöttää valintansa itse.
Vaikea: 2 kysymystä, 15 p. Pelaaja näkee 4 vastausvaihtoehtoa, mutta syöttää valintansa itse.
'''