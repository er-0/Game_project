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

def play_level(level, amount):
    questions = fetch_questions(level, amount)
    level_points = 0

    for q in questions:
        answers = ""
        if level == 2 or level == 3:
            answers = fetch_wrong_answers()
            answers.append(q[1])
            random.shuffle(answers)
            print(q) #testaamista varten, tulostaa Q&A
            print("\nVaihtoehdot: ", ", ".join(answers))
        user_answer = input(q[0] + " ")
        #käyttäjä voi kirjoittaa koko vastauksen (washington dc == Washington, D.C.)
        if user_answer == "":
            print(f"Oikea vastaus on {q[1]}.")
        elif ''.join(filter(str.isalpha, user_answer)).casefold() == ''.join(filter(str.isalpha, q[1])).casefold():
            print("Oikein!")
            level_points += q[2]
        #käyttäjä voi vastata myös vaihtoehdon numerolla
        elif answers != "" and user_answer.isdigit() and int(user_answer) in range(1,5) and answers[int(
                user_answer)-1] == q[1]:
            print("Oikein!")
            level_points += q[2]
        else:
            print(f"Väärin, oikea vastaus on {q[1]}.")
    return level_points

def capitals_game(game_id):
    user_points = 0
    user_points += play_level(1, 5)
    user_points += play_level(2, 5)
    user_points += play_level(3, 2)
    return user_points

print(capitals_game(1))

'''
Helppo: 5 kysymystä, 4 p. Vastaukset kirjoitetaan itse.
Normaali: 5 kysymystä, 10 p. Pelaaja näkee 4 vastausvaihtoehtoa ja syöttää valintansa itse.
Vaikea: 2 kysymystä, 15 p. Pelaaja näkee 4 vastausvaihtoehtoa ja syöttää valintansa itse.
'''