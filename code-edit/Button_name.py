from reader import Reader
fail = Reader('gamedata/config/control keys.config')

colib_text = fail.read("<colib_text>")
edit_world = fail.read('<edit_world>')
save_button = fail.read('<save_button>')
draw_hud = fail.read('<draw_hud>')

break_key = fail.read('<break_key>')
start_play = fail.read('<start_play>')

P_right = fail.read('<player_right>')
P_left = fail.read('<player_left>')
P_up = fail.read('<player_up>')
P_up_alt = fail.read('<player_up_alt>')
P_down = fail.read('<player_down>')
P_boost = fail.read('<player_boost>')