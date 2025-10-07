from functions import intro, part_one, part_two, part_three

game_score = 0
quit_game = False

user_name, game_id, level_reached = intro()
while level_reached <= 2 and not quit_game:
    if level_reached == 0:
        score = part_one(user_name, game_id)
        if score is None:
            quit_game = True
    elif level_reached == 1:
        score = part_two(user_name, game_id)
        if score is None:
            quit_game = True
    elif level_reached == 2:
        score = part_three(user_name, game_id)

    game_score += score
    level_reached += 1

print(game_score, "total")

