from db import yhteys
import time
import random


def get_tasks(level, limit):
    db = yhteys
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "SELECT question, answer, points FROM count_game WHERE level=%s ORDER BY RAND() LIMIT %s;",
        (level, limit)
    )
    return cursor.fetchall()

def generate_math_questions():
    questions = get_tasks(1, 5)
    questions.extend(get_tasks(2, 5))
    questions.extend(get_tasks(3, 2))
    return questions

if __name__ == "__main__":
    count_game()