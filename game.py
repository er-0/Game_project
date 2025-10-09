from functions import intro, part_one, part_two, part_three

game_score = 0
quit_game = False

#intro introduces the game for the player and returns the username, game started/continued and last level reached.
player_id, user_name, game_id, level_reached, kilometers_for_table = intro()

#level is 0 if starting a new game, and 1 or 2 if continuing an old game
while level_reached <= 2 and not quit_game:
    if level_reached == 0:
        #finishing part one returns the score
        score = part_one(user_name, game_id)
        #player has quit the game before finishing this level or something has gone wrong:
        if score is None:
            quit_game = True
    elif level_reached == 1:
        score = part_two(user_name, game_id)
        if score is None:
            quit_game = True
    elif level_reached == 2:
        score = part_three(player_id, user_name, game_id, kilometers_for_table)

    level_reached += 1

