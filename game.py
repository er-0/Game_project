from db import yhteys

def get_count_game():
    sql = ""
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchall()
    print(result)
    return result





