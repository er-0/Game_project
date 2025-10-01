from db import yhteys

def get_count_game():
    sql = "SELECT * FROM game_airports"
    cursor = yhteys.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchall()
    print(result)
    return result

get_count_game()
