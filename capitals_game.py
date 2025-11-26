from db import yhteys
from unidecode import unidecode
import random


def fetch_questions(level, amount):
    sql = "SELECT question, answer, points FROM capital_game WHERE level = %s ORDER BY RAND() LIMIT %s"
    cursor = yhteys.cursor(dictionary=True)
    cursor.execute(sql, (level, amount))
    return cursor.fetchall()


def fetch_wrong_answers(correct_answer):
    sql = "SELECT answer FROM capital_game WHERE answer != %s ORDER BY RAND() LIMIT 3"
    cursor = yhteys.cursor(dictionary=True)
    cursor.execute(sql, (correct_answer,))
    rows = cursor.fetchall()
    return [row['answer'] for row in rows]


def generate_all_questions_for_level(level):
    questions = fetch_questions(level, amount=5 if level < 3 else 2)
    question_list = []

    for q in questions:
        options = []
        if level in (2, 3):
            options = fetch_wrong_answers(q['answer'])
            options.append(q['answer'])
            random.shuffle(options)
        question_list.append({
            "question": q['question'],
            "correct_answer": q['answer'],
            "options": options,
            "points": q['points']
        })
    return question_list
