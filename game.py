from capitals_game import capitals_game
from count_game import count_game
from word_game import word_game
from functions import intro, part_one, part_two, part_three

game_score = 0

user_name, game_id = intro()
print(game_id, "game_id")
print(user_name, "username")
#score = part_one(user_name, game_id)
score = 100
game_score += score
print(score, "score1")
print(game_score, "gamescore")
#score = part_two(game_id)
score = 100
print(score, "score2")
game_score += score
print(game_score, "gamescore")
#score = part_three(game_id)
score = 80
print(score, "score3")
game_score += score
print(game_score, "total")

