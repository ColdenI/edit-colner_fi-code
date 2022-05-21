import pygame, keyboard, colors, random, time, Button_name as butN

import os
import PlayerClass
from reader import Reader
from PlayerClass import Player
from BlockClass import Block

pygame.mixer.pre_init(44100, -16, 3, 512)
pygame.init()

config_start = Reader("gamedata/config/start_config.config")
config_player = Reader("gamedata/config/config player.config")
config_sound = Reader("gamedata/music/sound config.config")
config_setings = Reader('gamedata/config/setings.config')
config_start_le = Reader('gamedata/config/start_level.config')


#-----------------------
VERSION = "V-1.05"
is_Window_open = True
is_draw_colin_text = False
sleep_time_pres_button = config_start.read_float("<sleep_time_button>")
FPS = config_start.read_int("<fps>")
screen_resolution = (int(config_start.read("<screen_resolution>").split("x")[0]), int(config_start.read("<screen_resolution>").split("x")[1]))
screen_name = 'Colner FI'
screen_icon = 'gamedata/texture/icon.bmp'
ground = screen_resolution[1]
is_sky = False
is_edit_world = False
sky_cloud_max_Y = screen_resolution[1] // 6
is_world = [0,""]
koll_worlds_ = [1, ""]
old_mouse_pos = pygame.mouse.get_pos()
screen_I = 0
indi_te = ["Colner FI",0]
is_draw_HUD = True
volume = config_setings.read_int('<volume>') / 100
is_down = False
level_name = ["",0]
file_for_save = ['','']
#-----------------------


sc = pygame.display.set_mode(screen_resolution)
pygame.display.set_icon(pygame.image.load(screen_icon))
pygame.display.set_caption(screen_name)
clock = pygame.time.Clock()
player = Player(screen_resolution[0]//2, screen_resolution[1]//2, PlayerClass.ANIMA_PLAYER['F'], config_player.read_int('<player_speed>'), config_player.read_int('<player_speed_max>'))
player.GND = ground
player.screen_res = screen_resolution
player.max_jamp = config_player.read_int('<player_max_jamp>')
font_1 = pygame.font.SysFont('arial', 22)
font_2 = pygame.font.Font(config_start.read('<my_font-1>'), 40)
font_2_ = pygame.font.Font(config_start.read('<my_font-1>'), 30)
font_2__ = pygame.font.Font(config_start.read('<my_font-1>'), 25)

#--------indi_panel----------
indi_panel_ = Block(0, 0, "gamedata/texture/indi/indi_panel1_.png")
indi_panel = Block(0, 0, "gamedata/texture/indi/indi_panel1.png")
indi_li = Block(1372, 38, "gamedata/texture/indi/li_100.png")
indi_st = Block(1372, 98, "gamedata/texture/indi/st_100.png")

#---------SOUNDS--------
pygame.mixer.music.set_volume(volume)
event_sound = pygame.mixer.Sound(config_sound.read('<s_event>'))
event_sound.set_volume(volume)
event_2_sound = pygame.mixer.Sound(config_sound.read('<s_event-2>'))
event_2_sound.set_volume(volume)
jamp_sound = pygame.mixer.Sound(config_sound.read('<s_jamp>'))
jamp_sound.set_volume(volume)
uron_sound = pygame.mixer.Sound(config_sound.read('<s_uron>'))
uron_sound.set_volume(volume)
uron_2_sound = pygame.mixer.Sound(config_sound.read('<s_uron-1>'))
uron_2_sound.set_volume(volume)
live_max_sound = pygame.mixer.Sound(config_sound.read('<s_live_max>'))
live_max_sound.set_volume(volume)
walk_sound = pygame.mixer.Sound(config_sound.read('<s_walk>'))
walk_sound.set_volume(volume)
game_over_sound = pygame.mixer.Sound(config_sound.read('<s_game_over>'))
game_over_sound.set_volume(volume)
game_close_sound = pygame.mixer.Sound(config_sound.read('<s_game_close>'))
game_close_sound.set_volume(volume)
repl_sound = pygame.mixer.Sound(config_sound.read('<s_repl>'))
repl_sound.set_volume(volume)

#------------TIMERS------------
anim_timer = pygame.USEREVENT + 1
anim_timer_max = pygame.USEREVENT + 2
stamina_timer = pygame.USEREVENT + 3
cloud_update_timer = pygame.USEREVENT + 4
gener_item_timer = pygame.USEREVENT + 5
player_sound_timer = pygame.USEREVENT + 6
player_sound_timer_boost = pygame.USEREVENT + 7
pygame.time.set_timer(anim_timer, config_player.read_int('<player_anim_speed>'))
pygame.time.set_timer(anim_timer_max, config_player.read_int('<player_anim_speed_max>'))
pygame.time.set_timer(stamina_timer, config_player.read_int('<player_stamina_timer>'))
pygame.time.set_timer(player_sound_timer, config_player.read_int('<player_sound_timer>'))
pygame.time.set_timer(player_sound_timer_boost, config_player.read_int('<player_sound_timer_boost>'))


#----------OBJECT CREATE BLOCK-----------
player_ = (player, "")

block_all = []
block_fizik = []
block_cloud = []
block_fon = []
block_uron = []
block_item = []
block_item_G = None

level_worlds = []

obst_group = pygame.sprite.Group()
obst_no_coliz_group = pygame.sprite.Group()
obst_uron_group = pygame.sprite.Group()
obst_fizik_group = pygame.sprite.Group()
obst_item_group = pygame.sprite.Group()
obst_item_G_group = pygame.sprite.Group()


def save(file_name):
    save_file = Reader(file_name)
    save_file.write(('<world>', '<live>', '<stamina>', '<money>'), (is_world[0] + 1, player.live, player.stamina, player.money), start_text = "Colner Fi  Colden I GAME - save - Colden I GAME  Colner Fi")
    indi_te[0] = "Игра успшно сохранена."

def cloud_uplate():
    for cloud in block_cloud:
        cloud.cloud_update(screen_resolution[0])


def create_obj_list(load_world):
    file = Reader(load_world)
    obst_group.empty()
    obst_no_coliz_group.empty()
    obst_uron_group.empty()
    obst_item_group.empty()
    obst_item_G_group.empty()


    block_item.clear()
    block_fizik.clear()
    obst_fizik_group.empty()
    block_item_G = None
    block_cloud.clear()
    block_uron.clear()
    block_fon.clear()

    player.rect.x = int(file.read('<start_pos>').split('x')[0])
    player.rect.y = int(file.read('<start_pos>').split('x')[1])

    if file.read('<background_music>') != 'none':
        pygame.mixer.music.load(file.read('<background_music>'))
        pygame.mixer.music.play(-1)

    koll_fizik = file.read_int('<fizik>')

    if koll_fizik >= 1: fizik_01 = Block(int(file.read('<fi_01-ko>').split('x')[0]), int(file.read('<fi_01-ko>').split('x')[1]), file.read('<fi_01-pa>'), gnd = file.read_int('<fi_01-gnd>')); obst_fizik_group.add(fizik_01)
    if koll_fizik >= 2: fizik_02 = Block(int(file.read('<fi_02-ko>').split('x')[0]), int(file.read('<fi_02-ko>').split('x')[1]), file.read('<fi_02-pa>'), gnd = file.read_int('<fi_02-gnd>')); obst_fizik_group.add(fizik_02)
    if koll_fizik >= 3: fizik_03 = Block(int(file.read('<fi_03-ko>').split('x')[0]), int(file.read('<fi_03-ko>').split('x')[1]), file.read('<fi_03-pa>'), gnd = file.read_int('<fi_03-gnd>')); obst_fizik_group.add(fizik_03)
    if koll_fizik >= 4: fizik_04 = Block(int(file.read('<fi_04-ko>').split('x')[0]), int(file.read('<fi_04-ko>').split('x')[1]), file.read('<fi_04-pa>'), gnd = file.read_int('<fi_04-gnd>')); obst_fizik_group.add(fizik_04)
    if koll_fizik >= 5: fizik_05 = Block(int(file.read('<fi_05-ko>').split('x')[0]), int(file.read('<fi_05-ko>').split('x')[1]), file.read('<fi_05-pa>'), gnd = file.read_int('<fi_05-gnd>')); obst_fizik_group.add(fizik_05)
    if koll_fizik >= 6: fizik_06 = Block(int(file.read('<fi_06-ko>').split('x')[0]), int(file.read('<fi_06-ko>').split('x')[1]), file.read('<fi_06-pa>'), gnd = file.read_int('<fi_06-gnd>')); obst_fizik_group.add(fizik_06)
    if koll_fizik >= 7: fizik_07 = Block(int(file.read('<fi_07-ko>').split('x')[0]), int(file.read('<fi_07-ko>').split('x')[1]), file.read('<fi_07-pa>'), gnd = file.read_int('<fi_07-gnd>')); obst_fizik_group.add(fizik_07)
    if koll_fizik >= 8: fizik_08 = Block(int(file.read('<fi_08-ko>').split('x')[0]), int(file.read('<fi_08-ko>').split('x')[1]), file.read('<fi_08-pa>'), gnd = file.read_int('<fi_08-gnd>')); obst_fizik_group.add(fizik_08)
    if koll_fizik >= 9: fizik_09 = Block(int(file.read('<fi_09-ko>').split('x')[0]), int(file.read('<fi_09-ko>').split('x')[1]), file.read('<fi_09-pa>'), gnd = file.read_int('<fi_09-gnd>')); obst_fizik_group.add(fizik_09)
    if koll_fizik >= 10: fizik_10 = Block(int(file.read('<fi_10-ko>').split('x')[0]), int(file.read('<fi_10-ko>').split('x')[1]), file.read('<fi_10-pa>'), gnd = file.read_int('<fi_10-gnd>')); obst_fizik_group.add(fizik_10)
    if koll_fizik >= 11: fizik_11 = Block(int(file.read('<fi_11-ko>').split('x')[0]), int(file.read('<fi_11-ko>').split('x')[1]), file.read('<fi_11-pa>'), gnd = file.read_int('<fi_11-gnd>')); obst_fizik_group.add(fizik_11)
    if koll_fizik >= 12: fizik_12 = Block(int(file.read('<fi_12-ko>').split('x')[0]), int(file.read('<fi_12-ko>').split('x')[1]), file.read('<fi_12-pa>'), gnd = file.read_int('<fi_12-gnd>')); obst_fizik_group.add(fizik_12)
    if koll_fizik >= 13: fizik_13 = Block(int(file.read('<fi_13-ko>').split('x')[0]), int(file.read('<fi_13-ko>').split('x')[1]), file.read('<fi_13-pa>'), gnd = file.read_int('<fi_13-gnd>')); obst_fizik_group.add(fizik_13)
    if koll_fizik >= 14: fizik_14 = Block(int(file.read('<fi_14-ko>').split('x')[0]), int(file.read('<fi_14-ko>').split('x')[1]), file.read('<fi_14-pa>'), gnd = file.read_int('<fi_14-gnd>')); obst_fizik_group.add(fizik_14)
    if koll_fizik >= 15: fizik_15 = Block(int(file.read('<fi_15-ko>').split('x')[0]), int(file.read('<fi_15-ko>').split('x')[1]), file.read('<fi_15-pa>'), gnd = file.read_int('<fi_15-gnd>')); obst_fizik_group.add(fizik_15)
    if koll_fizik >= 16: fizik_16 = Block(int(file.read('<fi_16-ko>').split('x')[0]), int(file.read('<fi_16-ko>').split('x')[1]), file.read('<fi_16-pa>'), gnd = file.read_int('<fi_16-gnd>')); obst_fizik_group.add(fizik_16)
    if koll_fizik >= 17: fizik_17 = Block(int(file.read('<fi_17-ko>').split('x')[0]), int(file.read('<fi_17-ko>').split('x')[1]), file.read('<fi_17-pa>'), gnd = file.read_int('<fi_17-gnd>')); obst_fizik_group.add(fizik_17)
    if koll_fizik >= 18: fizik_18 = Block(int(file.read('<fi_18-ko>').split('x')[0]), int(file.read('<fi_18-ko>').split('x')[1]), file.read('<fi_18-pa>'), gnd = file.read_int('<fi_18-gnd>')); obst_fizik_group.add(fizik_18)
    if koll_fizik >= 19: fizik_19 = Block(int(file.read('<fi_19-ko>').split('x')[0]), int(file.read('<fi_19-ko>').split('x')[1]), file.read('<fi_19-pa>'), gnd = file.read_int('<fi_19-gnd>')); obst_fizik_group.add(fizik_19)
    if koll_fizik >= 20: fizik_20 = Block(int(file.read('<fi_20-ko>').split('x')[0]), int(file.read('<fi_20-ko>').split('x')[1]), file.read('<fi_20-pa>'), gnd = file.read_int('<fi_20-gnd>')); obst_fizik_group.add(fizik_20)
    if koll_fizik >= 21: fizik_21 = Block(int(file.read('<fi_21-ko>').split('x')[0]), int(file.read('<fi_21-ko>').split('x')[1]), file.read('<fi_21-pa>'), gnd = file.read_int('<fi_21-gnd>')); obst_fizik_group.add(fizik_21)
    if koll_fizik >= 22: fizik_22 = Block(int(file.read('<fi_22-ko>').split('x')[0]), int(file.read('<fi_22-ko>').split('x')[1]), file.read('<fi_22-pa>'), gnd = file.read_int('<fi_22-gnd>')); obst_fizik_group.add(fizik_22)
    if koll_fizik >= 23: fizik_23 = Block(int(file.read('<fi_23-ko>').split('x')[0]), int(file.read('<fi_23-ko>').split('x')[1]), file.read('<fi_23-pa>'), gnd = file.read_int('<fi_23-gnd>')); obst_fizik_group.add(fizik_23)
    if koll_fizik >= 24: fizik_24 = Block(int(file.read('<fi_24-ko>').split('x')[0]), int(file.read('<fi_24-ko>').split('x')[1]), file.read('<fi_24-pa>'), gnd = file.read_int('<fi_24-gnd>')); obst_fizik_group.add(fizik_24)
    if koll_fizik >= 25: fizik_25 = Block(int(file.read('<fi_25-ko>').split('x')[0]), int(file.read('<fi_25-ko>').split('x')[1]), file.read('<fi_25-pa>'), gnd = file.read_int('<fi_25-gnd>')); obst_fizik_group.add(fizik_25)
    if koll_fizik >= 26: fizik_26 = Block(int(file.read('<fi_26-ko>').split('x')[0]), int(file.read('<fi_12-ko>').split('x')[1]), file.read('<fi_26-pa>'), gnd = file.read_int('<fi_26-gnd>')); obst_fizik_group.add(fizik_26)
    if koll_fizik >= 27: fizik_27 = Block(int(file.read('<fi_27-ko>').split('x')[0]), int(file.read('<fi_27-ko>').split('x')[1]), file.read('<fi_27-pa>'), gnd = file.read_int('<fi_27-gnd>')); obst_fizik_group.add(fizik_27)
    if koll_fizik >= 28: fizik_28 = Block(int(file.read('<fi_28-ko>').split('x')[0]), int(file.read('<fi_28-ko>').split('x')[1]), file.read('<fi_28-pa>'), gnd = file.read_int('<fi_28-gnd>')); obst_fizik_group.add(fizik_28)
    if koll_fizik >= 29: fizik_29 = Block(int(file.read('<fi_29-ko>').split('x')[0]), int(file.read('<fi_29-ko>').split('x')[1]), file.read('<fi_29-pa>'), gnd = file.read_int('<fi_29-gnd>')); obst_fizik_group.add(fizik_29)
    if koll_fizik >= 30: fizik_30 = Block(int(file.read('<fi_30-ko>').split('x')[0]), int(file.read('<fi_30-ko>').split('x')[1]), file.read('<fi_30-pa>'), gnd = file.read_int('<fi_30-gnd>')); obst_fizik_group.add(fizik_30)




    koll_fon = file.read_int('<fons>')

    if koll_fon >= 1: fon_01 = Block(int(file.read('<f_01-ko>').split('x')[0]), int(file.read('<f_01-ko>').split('x')[1]), file.read('<f_01-pa>')); obst_no_coliz_group.add(fon_01)
    if koll_fon >= 2: fon_02 = Block(int(file.read('<f_02-ko>').split('x')[0]), int(file.read('<f_02-ko>').split('x')[1]), file.read('<f_02-pa>')); obst_no_coliz_group.add(fon_02)
    if koll_fon >= 3: fon_03 = Block(int(file.read('<f_03-ko>').split('x')[0]), int(file.read('<f_03-ko>').split('x')[1]), file.read('<f_03-pa>')); obst_no_coliz_group.add(fon_03)
    if koll_fon >= 4: fon_04 = Block(int(file.read('<f_04-ko>').split('x')[0]), int(file.read('<f_04-ko>').split('x')[1]), file.read('<f_04-pa>')); obst_no_coliz_group.add(fon_04)
    if koll_fon >= 5: fon_05 = Block(int(file.read('<f_05-ko>').split('x')[0]), int(file.read('<f_05-ko>').split('x')[1]), file.read('<f_05-pa>')); obst_no_coliz_group.add(fon_05)
    if koll_fon >= 6: fon_06 = Block(int(file.read('<f_06-ko>').split('x')[0]), int(file.read('<f_06-ko>').split('x')[1]), file.read('<f_06-pa>')); obst_no_coliz_group.add(fon_06)
    if koll_fon >= 7: fon_07 = Block(int(file.read('<f_07-ko>').split('x')[0]), int(file.read('<f_07-ko>').split('x')[1]), file.read('<f_07-pa>')); obst_no_coliz_group.add(fon_07)
    if koll_fon >= 8: fon_08 = Block(int(file.read('<f_08-ko>').split('x')[0]), int(file.read('<f_08-ko>').split('x')[1]), file.read('<f_08-pa>')); obst_no_coliz_group.add(fon_08)
    if koll_fon >= 9: fon_09 = Block(int(file.read('<f_09-ko>').split('x')[0]), int(file.read('<f_09-ko>').split('x')[1]), file.read('<f_09-pa>')); obst_no_coliz_group.add(fon_09)
    if koll_fon >= 10: fon_10 = Block(int(file.read('<f_10-ko>').split('x')[0]), int(file.read('<f_10-ko>').split('x')[1]), file.read('<f_10-pa>')); obst_no_coliz_group.add(fon_10)
    if koll_fon >= 11: fon_11 = Block(int(file.read('<f_11-ko>').split('x')[0]), int(file.read('<f_11-ko>').split('x')[1]), file.read('<f_11-pa>')); obst_no_coliz_group.add(fon_11)
    if koll_fon >= 12: fon_12 = Block(int(file.read('<f_12-ko>').split('x')[0]), int(file.read('<f_12-ko>').split('x')[1]), file.read('<f_12-pa>')); obst_no_coliz_group.add(fon_12)
    if koll_fon >= 13: fon_13 = Block(int(file.read('<f_13-ko>').split('x')[0]), int(file.read('<f_13-ko>').split('x')[1]), file.read('<f_13-pa>')); obst_no_coliz_group.add(fon_13)
    if koll_fon >= 14: fon_14 = Block(int(file.read('<f_14-ko>').split('x')[0]), int(file.read('<f_14-ko>').split('x')[1]), file.read('<f_14-pa>')); obst_no_coliz_group.add(fon_14)
    if koll_fon >= 15: fon_15 = Block(int(file.read('<f_15-ko>').split('x')[0]), int(file.read('<f_15-ko>').split('x')[1]), file.read('<f_15-pa>')); obst_no_coliz_group.add(fon_15)
    if koll_fon >= 16: fon_16 = Block(int(file.read('<f_16-ko>').split('x')[0]), int(file.read('<f_16-ko>').split('x')[1]), file.read('<f_16-pa>')); obst_no_coliz_group.add(fon_16)
    if koll_fon >= 17: fon_17 = Block(int(file.read('<f_17-ko>').split('x')[0]), int(file.read('<f_17-ko>').split('x')[1]), file.read('<f_17-pa>')); obst_no_coliz_group.add(fon_17)
    if koll_fon >= 18: fon_18 = Block(int(file.read('<f_18-ko>').split('x')[0]), int(file.read('<f_18-ko>').split('x')[1]), file.read('<f_18-pa>')); obst_no_coliz_group.add(fon_18)
    if koll_fon >= 19: fon_19 = Block(int(file.read('<f_19-ko>').split('x')[0]), int(file.read('<f_19-ko>').split('x')[1]), file.read('<f_19-pa>')); obst_no_coliz_group.add(fon_19)
    if koll_fon >= 20: fon_20 = Block(int(file.read('<f_20-ko>').split('x')[0]), int(file.read('<f_20-ko>').split('x')[1]), file.read('<f_20-pa>')); obst_no_coliz_group.add(fon_20)
    if koll_fon >= 21: fon_21 = Block(int(file.read('<f_21-ko>').split('x')[0]), int(file.read('<f_21-ko>').split('x')[1]), file.read('<f_21-pa>')); obst_no_coliz_group.add(fon_21)
    if koll_fon >= 22: fon_22 = Block(int(file.read('<f_22-ko>').split('x')[0]), int(file.read('<f_22-ko>').split('x')[1]), file.read('<f_22-pa>')); obst_no_coliz_group.add(fon_22)
    if koll_fon >= 23: fon_23 = Block(int(file.read('<f_23-ko>').split('x')[0]), int(file.read('<f_23-ko>').split('x')[1]), file.read('<f_23-pa>')); obst_no_coliz_group.add(fon_23)
    if koll_fon >= 24: fon_24 = Block(int(file.read('<f_24-ko>').split('x')[0]), int(file.read('<f_24-ko>').split('x')[1]), file.read('<f_24-pa>')); obst_no_coliz_group.add(fon_24)
    if koll_fon >= 25: fon_25 = Block(int(file.read('<f_25-ko>').split('x')[0]), int(file.read('<f_25-ko>').split('x')[1]), file.read('<f_25-pa>')); obst_no_coliz_group.add(fon_25)
    if koll_fon >= 26: fon_26 = Block(int(file.read('<f_26-ko>').split('x')[0]), int(file.read('<f_26-ko>').split('x')[1]), file.read('<f_26-pa>')); obst_no_coliz_group.add(fon_26)
    if koll_fon >= 27: fon_27 = Block(int(file.read('<f_27-ko>').split('x')[0]), int(file.read('<f_27-ko>').split('x')[1]), file.read('<f_27-pa>')); obst_no_coliz_group.add(fon_27)
    if koll_fon >= 28: fon_28 = Block(int(file.read('<f_28-ko>').split('x')[0]), int(file.read('<f_28-ko>').split('x')[1]), file.read('<f_28-pa>')); obst_no_coliz_group.add(fon_28)
    if koll_fon >= 29: fon_29 = Block(int(file.read('<f_29-ko>').split('x')[0]), int(file.read('<f_29-ko>').split('x')[1]), file.read('<f_29-pa>')); obst_no_coliz_group.add(fon_29)
    if koll_fon >= 30: fon_30 = Block(int(file.read('<f_30-ko>').split('x')[0]), int(file.read('<f_30-ko>').split('x')[1]), file.read('<f_30-pa>')); obst_no_coliz_group.add(fon_30)



    if file.read('<sky>') == "True":
        is_sky = True
        sky_cloud_max_Y = file.read_int('<sky_cloud_y>')
        koll_cloud = file.read_int('<cloud>')
        cloud_pa = (file.read('<sky_cloud_pa_1>'), file.read('<sky_cloud_pa_2>'), file.read('<sky_cloud_pa_3>'), file.read('<sky_cloud_pa_4>'), file.read('<sky_cloud_pa_5>'), file.read('<sky_cloud_pa_6>'))
        cloud_speed_max = file.read_int('<sky_cloud_speed_max>')
        pygame.time.set_timer(cloud_update_timer, file.read_int('<sky_cloud_timer_update>'))

        if koll_cloud >= 1: cloud_01 = Block(random.randint(0, screen_resolution[0]), random.randint(-50, sky_cloud_max_Y), cloud_pa[random.randint(0, len(cloud_pa) - 1)], cloud_speep_ = random.randint(1, cloud_speed_max)); obst_no_coliz_group.add(cloud_01); block_cloud.append(cloud_01)
        if koll_cloud >= 2: cloud_02 = Block(random.randint(0, screen_resolution[0]), random.randint(-50, sky_cloud_max_Y), cloud_pa[random.randint(0, len(cloud_pa) - 1)], cloud_speep_ = random.randint(1, cloud_speed_max)); obst_no_coliz_group.add(cloud_02); block_cloud.append(cloud_02)
        if koll_cloud >= 3: cloud_03 = Block(random.randint(0, screen_resolution[0]), random.randint(-50, sky_cloud_max_Y), cloud_pa[random.randint(0, len(cloud_pa) - 1)], cloud_speep_ = random.randint(1, cloud_speed_max)); obst_no_coliz_group.add(cloud_03); block_cloud.append(cloud_03)
        if koll_cloud >= 4: cloud_04 = Block(random.randint(0, screen_resolution[0]), random.randint(-50, sky_cloud_max_Y), cloud_pa[random.randint(0, len(cloud_pa) - 1)], cloud_speep_ = random.randint(1, cloud_speed_max)); obst_no_coliz_group.add(cloud_04); block_cloud.append(cloud_04)
        if koll_cloud >= 5: cloud_05 = Block(random.randint(0, screen_resolution[0]), random.randint(-50, sky_cloud_max_Y), cloud_pa[random.randint(0, len(cloud_pa) - 1)], cloud_speep_ = random.randint(1, cloud_speed_max)); obst_no_coliz_group.add(cloud_05); block_cloud.append(cloud_05)
        if koll_cloud >= 6: cloud_06 = Block(random.randint(0, screen_resolution[0]), random.randint(-50, sky_cloud_max_Y), cloud_pa[random.randint(0, len(cloud_pa) - 1)], cloud_speep_ = random.randint(1, cloud_speed_max)); obst_no_coliz_group.add(cloud_06); block_cloud.append(cloud_06)
        if koll_cloud >= 7: cloud_07 = Block(random.randint(0, screen_resolution[0]), random.randint(-50, sky_cloud_max_Y), cloud_pa[random.randint(0, len(cloud_pa) - 1)], cloud_speep_ = random.randint(1, cloud_speed_max)); obst_no_coliz_group.add(cloud_07); block_cloud.append(cloud_07)
        if koll_cloud >= 8: cloud_08 = Block(random.randint(0, screen_resolution[0]), random.randint(-50, sky_cloud_max_Y), cloud_pa[random.randint(0, len(cloud_pa) - 1)], cloud_speep_ = random.randint(1, cloud_speed_max)); obst_no_coliz_group.add(cloud_08); block_cloud.append(cloud_08)
        if koll_cloud >= 9: cloud_09 = Block(random.randint(0, screen_resolution[0]), random.randint(-50, sky_cloud_max_Y), cloud_pa[random.randint(0, len(cloud_pa) - 1)], cloud_speep_ = random.randint(1, cloud_speed_max)); obst_no_coliz_group.add(cloud_09); block_cloud.append(cloud_09)
        if koll_cloud >= 10: cloud_10 = Block(random.randint(0, screen_resolution[0]), random.randint(-50, sky_cloud_max_Y), cloud_pa[random.randint(0, len(cloud_pa) - 1)], cloud_speep_ = random.randint(1, cloud_speed_max)); obst_no_coliz_group.add(cloud_10); block_cloud.append(cloud_10)
        if koll_cloud >= 11: cloud_11 = Block(random.randint(0, screen_resolution[0]), random.randint(-50, sky_cloud_max_Y), cloud_pa[random.randint(0, len(cloud_pa) - 1)], cloud_speep_ = random.randint(1, cloud_speed_max)); obst_no_coliz_group.add(cloud_11); block_cloud.append(cloud_11)
        if koll_cloud >= 12: cloud_12 = Block(random.randint(0, screen_resolution[0]), random.randint(-50, sky_cloud_max_Y), cloud_pa[random.randint(0, len(cloud_pa) - 1)], cloud_speep_ = random.randint(1, cloud_speed_max)); obst_no_coliz_group.add(cloud_12); block_cloud.append(cloud_12)
        if koll_cloud >= 13: cloud_13 = Block(random.randint(0, screen_resolution[0]), random.randint(-50, sky_cloud_max_Y), cloud_pa[random.randint(0, len(cloud_pa) - 1)], cloud_speep_ = random.randint(1, cloud_speed_max)); obst_no_coliz_group.add(cloud_13); block_cloud.append(cloud_13)
        if koll_cloud >= 14: cloud_14 = Block(random.randint(0, screen_resolution[0]), random.randint(-50, sky_cloud_max_Y), cloud_pa[random.randint(0, len(cloud_pa) - 1)], cloud_speep_ = random.randint(1, cloud_speed_max)); obst_no_coliz_group.add(cloud_14); block_cloud.append(cloud_14)
        if koll_cloud >= 15: cloud_15 = Block(random.randint(0, screen_resolution[0]), random.randint(-50, sky_cloud_max_Y), cloud_pa[random.randint(0, len(cloud_pa) - 1)], cloud_speep_ = random.randint(1, cloud_speed_max)); obst_no_coliz_group.add(cloud_15); block_cloud.append(cloud_15)


    koll_obj = file.read_int('<obj>')

    if koll_obj >= 1: block_01 = Block(int(file.read('<01-ko>').split('x')[0]), int(file.read('<01-ko>').split('x')[1]), file.read('<01-pa>')); obst_group.add(block_01)
    if koll_obj >= 2:        block_02 =  Block(int(file.read('<02-ko>').split('x')[0]), int(file.read('<02-ko>').split('x')[1]), file.read('<02-pa>'));        obst_group.add(block_02)
    if koll_obj >= 3:        block_03 = Block(int(file.read('<03-ko>').split('x')[0]), int(file.read('<03-ko>').split('x')[1]), file.read('<03-pa>'));        obst_group.add(block_03)
    if koll_obj >= 4:        block_04 = Block(int(file.read('<04-ko>').split('x')[0]), int(file.read('<04-ko>').split('x')[1]), file.read('<04-pa>'));        obst_group.add(block_04)
    if koll_obj >= 5:        block_05 = Block(int(file.read('<05-ko>').split('x')[0]), int(file.read('<05-ko>').split('x')[1]), file.read('<05-pa>'));        obst_group.add(block_05)
    if koll_obj >= 6:        block_06 = Block(int(file.read('<06-ko>').split('x')[0]), int(file.read('<06-ko>').split('x')[1]), file.read('<06-pa>'));        obst_group.add(block_06)
    if koll_obj >= 7:        block_07 = Block(int(file.read('<07-ko>').split('x')[0]), int(file.read('<07-ko>').split('x')[1]), file.read('<07-pa>'));        obst_group.add(block_07)
    if koll_obj >= 8:        block_08 = Block(int(file.read('<08-ko>').split('x')[0]), int(file.read('<08-ko>').split('x')[1]), file.read('<08-pa>'));        obst_group.add(block_08)
    if koll_obj >= 9:        block_09 = Block(int(file.read('<09-ko>').split('x')[0]), int(file.read('<09-ko>').split('x')[1]), file.read('<09-pa>'));        obst_group.add(block_09)
    if koll_obj >= 10:        block_10 = Block(int(file.read('<10-ko>').split('x')[0]), int(file.read('<10-ko>').split('x')[1]), file.read('<10-pa>'));        obst_group.add(block_10)
    if koll_obj >= 11:        block_11 = Block(int(file.read('<11-ko>').split('x')[0]), int(file.read('<11-ko>').split('x')[1]), file.read('<11-pa>'));        obst_group.add(block_11)
    if koll_obj >= 12:        block_12 = Block(int(file.read('<12-ko>').split('x')[0]), int(file.read('<12-ko>').split('x')[1]), file.read('<12-pa>'));        obst_group.add(block_12)
    if koll_obj >= 13:        block_13 = Block(int(file.read('<13-ko>').split('x')[0]), int(file.read('<13-ko>').split('x')[1]), file.read('<13-pa>'));        obst_group.add(block_13)
    if koll_obj >= 14:        block_14 = Block(int(file.read('<14-ko>').split('x')[0]), int(file.read('<14-ko>').split('x')[1]), file.read('<14-pa>'));        obst_group.add(block_14)
    if koll_obj >= 15:        block_15 = Block(int(file.read('<15-ko>').split('x')[0]), int(file.read('<15-ko>').split('x')[1]), file.read('<15-pa>'));        obst_group.add(block_15)
    if koll_obj >= 16:        block_16 = Block(int(file.read('<16-ko>').split('x')[0]), int(file.read('<16-ko>').split('x')[1]), file.read('<16-pa>'));        obst_group.add(block_16)
    if koll_obj >= 17:        block_17 = Block(int(file.read('<17-ko>').split('x')[0]), int(file.read('<17-ko>').split('x')[1]), file.read('<17-pa>'));        obst_group.add(block_17)
    if koll_obj >= 18:        block_18 = Block(int(file.read('<18-ko>').split('x')[0]), int(file.read('<18-ko>').split('x')[1]), file.read('<18-pa>'));        obst_group.add(block_18)
    if koll_obj >= 19:        block_19 = Block(int(file.read('<19-ko>').split('x')[0]), int(file.read('<19-ko>').split('x')[1]), file.read('<19-pa>'));        obst_group.add(block_19)
    if koll_obj >= 20:        block_20 = Block(int(file.read('<20-ko>').split('x')[0]), int(file.read('<20-ko>').split('x')[1]), file.read('<20-pa>'));        obst_group.add(block_20)
    if koll_obj >= 21:        block_21 = Block(int(file.read('<21-ko>').split('x')[0]), int(file.read('<21-ko>').split('x')[1]), file.read('<21-pa>'));        obst_group.add(block_21)
    if koll_obj >= 22:        block_22 = Block(int(file.read('<22-ko>').split('x')[0]), int(file.read('<22-ko>').split('x')[1]), file.read('<22-pa>'));        obst_group.add(block_22)
    if koll_obj >= 23:        block_23 = Block(int(file.read('<23-ko>').split('x')[0]), int(file.read('<23-ko>').split('x')[1]), file.read('<23-pa>'));        obst_group.add(block_23)
    if koll_obj >= 24:        block_24 = Block(int(file.read('<24-ko>').split('x')[0]), int(file.read('<24-ko>').split('x')[1]), file.read('<24-pa>'));        obst_group.add(block_24)
    if koll_obj >= 25:        block_25 = Block(int(file.read('<25-ko>').split('x')[0]), int(file.read('<25-ko>').split('x')[1]), file.read('<25-pa>'));        obst_group.add(block_25)
    if koll_obj >= 26:        block_26 = Block(int(file.read('<26-ko>').split('x')[0]), int(file.read('<26-ko>').split('x')[1]), file.read('<26-pa>'));        obst_group.add(block_26)
    if koll_obj >= 27:        block_27 = Block(int(file.read('<27-ko>').split('x')[0]), int(file.read('<27-ko>').split('x')[1]), file.read('<27-pa>'));        obst_group.add(block_27)
    if koll_obj >= 28:        block_28 = Block(int(file.read('<28-ko>').split('x')[0]), int(file.read('<28-ko>').split('x')[1]), file.read('<28-pa>'));        obst_group.add(block_28)
    if koll_obj >= 29:        block_29 = Block(int(file.read('<29-ko>').split('x')[0]), int(file.read('<29-ko>').split('x')[1]), file.read('<29-pa>'));        obst_group.add(block_29)
    if koll_obj >= 30:        block_30 = Block(int(file.read('<30-ko>').split('x')[0]), int(file.read('<30-ko>').split('x')[1]), file.read('<30-pa>'));        obst_group.add(block_30)
    if koll_obj >= 31:        block_31 = Block(int(file.read('<31-ko>').split('x')[0]), int(file.read('<31-ko>').split('x')[1]), file.read('<31-pa>'));        obst_group.add(block_31)
    if koll_obj >= 32:        block_32 = Block(int(file.read('<32-ko>').split('x')[0]), int(file.read('<32-ko>').split('x')[1]), file.read('<32-pa>'));        obst_group.add(block_32)
    if koll_obj >= 33:        block_33 = Block(int(file.read('<33-ko>').split('x')[0]), int(file.read('<33-ko>').split('x')[1]), file.read('<33-pa>'));        obst_group.add(block_33)
    if koll_obj >= 34:        block_34 = Block(int(file.read('<34-ko>').split('x')[0]), int(file.read('<34-ko>').split('x')[1]), file.read('<34-pa>'));        obst_group.add(block_34)
    if koll_obj >= 35:        block_35 = Block(int(file.read('<35-ko>').split('x')[0]), int(file.read('<35-ko>').split('x')[1]), file.read('<35-pa>'));        obst_group.add(block_35)
    if koll_obj >= 36:        block_36 = Block(int(file.read('<36-ko>').split('x')[0]), int(file.read('<36-ko>').split('x')[1]), file.read('<36-pa>'));        obst_group.add(block_36)
    if koll_obj >= 37:        block_37 = Block(int(file.read('<37-ko>').split('x')[0]), int(file.read('<37-ko>').split('x')[1]), file.read('<37-pa>'));        obst_group.add(block_37)
    if koll_obj >= 38:        block_38 = Block(int(file.read('<38-ko>').split('x')[0]), int(file.read('<38-ko>').split('x')[1]), file.read('<38-pa>'));        obst_group.add(block_38)
    if koll_obj >= 39:        block_39 = Block(int(file.read('<39-ko>').split('x')[0]), int(file.read('<39-ko>').split('x')[1]), file.read('<39-pa>'));        obst_group.add(block_39)
    if koll_obj >= 40:        block_40 = Block(int(file.read('<40-ko>').split('x')[0]), int(file.read('<40-ko>').split('x')[1]), file.read('<40-pa>'));        obst_group.add(block_40)
    if koll_obj >= 41:        block_41 = Block(int(file.read('<41-ko>').split('x')[0]), int(file.read('<41-ko>').split('x')[1]), file.read('<41-pa>'));        obst_group.add(block_41)
    if koll_obj >= 42:        block_42 = Block(int(file.read('<42-ko>').split('x')[0]), int(file.read('<42-ko>').split('x')[1]), file.read('<42-pa>'));        obst_group.add(block_42)
    if koll_obj >= 43:        block_43 = Block(int(file.read('<43-ko>').split('x')[0]), int(file.read('<43-ko>').split('x')[1]), file.read('<43-pa>'));        obst_group.add(block_43)
    if koll_obj >= 44:        block_44 = Block(int(file.read('<44-ko>').split('x')[0]), int(file.read('<44-ko>').split('x')[1]), file.read('<44-pa>'));        obst_group.add(block_44)
    if koll_obj >= 45:        block_45 = Block(int(file.read('<45-ko>').split('x')[0]), int(file.read('<45-ko>').split('x')[1]), file.read('<45-pa>'));        obst_group.add(block_45)
    if koll_obj >= 46:        block_46 = Block(int(file.read('<46-ko>').split('x')[0]), int(file.read('<46-ko>').split('x')[1]), file.read('<46-pa>'));        obst_group.add(block_46)
    if koll_obj >= 47:        block_47 = Block(int(file.read('<27-ko>').split('x')[0]), int(file.read('<47-ko>').split('x')[1]), file.read('<47-pa>'));        obst_group.add(block_47)
    if koll_obj >= 48:        block_48 = Block(int(file.read('<48-ko>').split('x')[0]), int(file.read('<48-ko>').split('x')[1]), file.read('<48-pa>'));        obst_group.add(block_48)
    if koll_obj >= 49:        block_49 = Block(int(file.read('<49-ko>').split('x')[0]), int(file.read('<49-ko>').split('x')[1]), file.read('<49-pa>'));        obst_group.add(block_49)
    if koll_obj >= 50:        block_50 = Block(int(file.read('<50-ko>').split('x')[0]), int(file.read('<50-ko>').split('x')[1]), file.read('<50-pa>'));        obst_group.add(block_50)

    koll_uron = file.read_int('<uron>')

    if koll_uron >= 1: uron_01 = Block(int(file.read('<u_01-ko>').split('x')[0]), int(file.read('<u_01-ko>').split('x')[1]), file.read('<u_01-pa>'), uron = file.read_int('<u_01-ur>')); obst_uron_group.add(uron_01)
    if koll_uron >= 2: uron_02 = Block(int(file.read('<u_02-ko>').split('x')[0]), int(file.read('<u_02-ko>').split('x')[1]), file.read('<u_02-pa>'), uron = file.read_int('<u_02-ur>')); obst_uron_group.add(uron_02)
    if koll_uron >= 3: uron_03 = Block(int(file.read('<u_03-ko>').split('x')[0]), int(file.read('<u_03-ko>').split('x')[1]), file.read('<u_03-pa>'), uron = file.read_int('<u_03-ur>')); obst_uron_group.add(uron_03)
    if koll_uron >= 4: uron_04 = Block(int(file.read('<u_04-ko>').split('x')[0]), int(file.read('<u_04-ko>').split('x')[1]), file.read('<u_04-pa>'), uron = file.read_int('<u_04-ur>')); obst_uron_group.add(uron_04)
    if koll_uron >= 5: uron_05 = Block(int(file.read('<u_05-ko>').split('x')[0]), int(file.read('<u_05-ko>').split('x')[1]), file.read('<u_05-pa>'), uron = file.read_int('<u_05-ur>')); obst_uron_group.add(uron_05)
    if koll_uron >= 6: uron_06 = Block(int(file.read('<u_06-ko>').split('x')[0]), int(file.read('<u_06-ko>').split('x')[1]), file.read('<u_06-pa>'), uron = file.read_int('<u_06-ur>')); obst_uron_group.add(uron_06)
    if koll_uron >= 7: uron_07 = Block(int(file.read('<u_07-ko>').split('x')[0]), int(file.read('<u_07-ko>').split('x')[1]), file.read('<u_07-pa>'), uron = file.read_int('<u_07-ur>')); obst_uron_group.add(uron_07)
    if koll_uron >= 8: uron_08 = Block(int(file.read('<u_08-ko>').split('x')[0]), int(file.read('<u_08-ko>').split('x')[1]), file.read('<u_08-pa>'), uron = file.read_int('<u_08-ur>')); obst_uron_group.add(uron_08)
    if koll_uron >= 9: uron_09 = Block(int(file.read('<u_09-ko>').split('x')[0]), int(file.read('<u_09-ko>').split('x')[1]), file.read('<u_09-pa>'), uron = file.read_int('<u_09-ur>')); obst_uron_group.add(uron_09)
    if koll_uron >= 10: uron_10 = Block(int(file.read('<u_10-ko>').split('x')[0]), int(file.read('<u_10-ko>').split('x')[1]), file.read('<u_10-pa>'), uron = file.read_int('<u_10-ur>')); obst_uron_group.add(uron_10)
    if koll_uron >= 11: uron_11 = Block(int(file.read('<u_11-ko>').split('x')[0]), int(file.read('<u_11-ko>').split('x')[1]), file.read('<u_11-pa>'), uron = file.read_int('<u_11-ur>')); obst_uron_group.add(uron_11)
    if koll_uron >= 12: uron_12 = Block(int(file.read('<u_12-ko>').split('x')[0]), int(file.read('<u_12-ko>').split('x')[1]), file.read('<u_12-pa>'), uron = file.read_int('<u_12-ur>')); obst_uron_group.add(uron_12)
    if koll_uron >= 12: uron_13 = Block(int(file.read('<u_13-ko>').split('x')[0]), int(file.read('<u_13-ko>').split('x')[1]), file.read('<u_13-pa>'), uron = file.read_int('<u_13-ur>')); obst_uron_group.add(uron_13)
    if koll_uron >= 13: uron_14 = Block(int(file.read('<u_14-ko>').split('x')[0]), int(file.read('<u_14-ko>').split('x')[1]), file.read('<u_14-pa>'), uron = file.read_int('<u_14-ur>')); obst_uron_group.add(uron_14)
    if koll_uron >= 14: uron_15 = Block(int(file.read('<u_15-ko>').split('x')[0]), int(file.read('<u_15-ko>').split('x')[1]), file.read('<u_15-pa>'), uron = file.read_int('<u_15-ur>')); obst_uron_group.add(uron_15)
    if koll_uron >= 15: uron_16 = Block(int(file.read('<u_16-ko>').split('x')[0]), int(file.read('<u_16-ko>').split('x')[1]), file.read('<u_16-pa>'), uron = file.read_int('<u_16-ur>')); obst_uron_group.add(uron_16)
    if koll_uron >= 16: uron_17 = Block(int(file.read('<u_17-ko>').split('x')[0]), int(file.read('<u_17-ko>').split('x')[1]), file.read('<u_17-pa>'), uron = file.read_int('<u_17-ur>')); obst_uron_group.add(uron_17)
    if koll_uron >= 17: uron_18 = Block(int(file.read('<u_18-ko>').split('x')[0]), int(file.read('<u_18-ko>').split('x')[1]), file.read('<u_18-pa>'), uron = file.read_int('<u_18-ur>')); obst_uron_group.add(uron_18)
    if koll_uron >= 18: uron_19 = Block(int(file.read('<u_19-ko>').split('x')[0]), int(file.read('<u_19-ko>').split('x')[1]), file.read('<u_19-pa>'), uron = file.read_int('<u_19-ur>')); obst_uron_group.add(uron_19)
    if koll_uron >= 20: uron_20 = Block(int(file.read('<u_20-ko>').split('x')[0]), int(file.read('<u_20-ko>').split('x')[1]), file.read('<u_20-pa>'), uron = file.read_int('<u_20-ur>')); obst_uron_group.add(uron_20)
    if koll_uron >= 21: uron_21 = Block(int(file.read('<u_21-ko>').split('x')[0]), int(file.read('<u_21-ko>').split('x')[1]), file.read('<u_21-pa>'), uron = file.read_int('<u_21-ur>')); obst_uron_group.add(uron_21)
    if koll_uron >= 22: uron_22 = Block(int(file.read('<u_22-ko>').split('x')[0]), int(file.read('<u_22-ko>').split('x')[1]), file.read('<u_22-pa>'), uron = file.read_int('<u_22-ur>')); obst_uron_group.add(uron_22)
    if koll_uron >= 22: uron_23 = Block(int(file.read('<u_23-ko>').split('x')[0]), int(file.read('<u_23-ko>').split('x')[1]), file.read('<u_23-pa>'), uron = file.read_int('<u_23-ur>')); obst_uron_group.add(uron_23)
    if koll_uron >= 23: uron_24 = Block(int(file.read('<u_24-ko>').split('x')[0]), int(file.read('<u_24-ko>').split('x')[1]), file.read('<u_24-pa>'), uron = file.read_int('<u_24-ur>')); obst_uron_group.add(uron_24)
    if koll_uron >= 24: uron_25 = Block(int(file.read('<u_25-ko>').split('x')[0]), int(file.read('<u_25-ko>').split('x')[1]), file.read('<u_25-pa>'), uron = file.read_int('<u_25-ur>')); obst_uron_group.add(uron_25)
    if koll_uron >= 25: uron_26 = Block(int(file.read('<u_26-ko>').split('x')[0]), int(file.read('<u_26-ko>').split('x')[1]), file.read('<u_26-pa>'), uron = file.read_int('<u_26-ur>')); obst_uron_group.add(uron_26)
    if koll_uron >= 26: uron_27 = Block(int(file.read('<u_27-ko>').split('x')[0]), int(file.read('<u_27-ko>').split('x')[1]), file.read('<u_27-pa>'), uron = file.read_int('<u_27-ur>')); obst_uron_group.add(uron_27)
    if koll_uron >= 27: uron_28 = Block(int(file.read('<u_28-ko>').split('x')[0]), int(file.read('<u_28-ko>').split('x')[1]), file.read('<u_28-pa>'), uron = file.read_int('<u_28-ur>')); obst_uron_group.add(uron_28)
    if koll_uron >= 28: uron_29 = Block(int(file.read('<u_29-ko>').split('x')[0]), int(file.read('<u_29-ko>').split('x')[1]), file.read('<u_29-pa>'), uron = file.read_int('<u_29-ur>')); obst_uron_group.add(uron_29)
    if koll_uron >= 30: uron_30 = Block(int(file.read('<u_30-ko>').split('x')[0]), int(file.read('<u_30-ko>').split('x')[1]), file.read('<u_30-pa>'), uron = file.read_int('<u_30-ur>')); obst_uron_group.add(uron_30)


    koll_item = file.read_int('<item>')

    if koll_item >= 1: item_01 = Block(int(file.read('<i_01-ko>').split('x')[0]), int(file.read('<i_01-ko>').split('x')[1]), file.read('<i_01-pa>'), item_type= file.read('<i_01-ty>'), pow= file.read_int('<i_01-po>')); obst_item_group.add(item_01)
    if koll_item >= 2: item_02 = Block(int(file.read('<i_02-ko>').split('x')[0]), int(file.read('<i_02-ko>').split('x')[1]), file.read('<i_02-pa>'), item_type= file.read('<i_02-ty>'), pow= file.read_int('<i_02-po>')); obst_item_group.add(item_02)
    if koll_item >= 3: item_03 = Block(int(file.read('<i_03-ko>').split('x')[0]), int(file.read('<i_03-ko>').split('x')[1]), file.read('<i_03-pa>'), item_type= file.read('<i_03-ty>'), pow= file.read_int('<i_03-po>')); obst_item_group.add(item_03)
    if koll_item >= 4: item_04 = Block(int(file.read('<i_04-ko>').split('x')[0]), int(file.read('<i_04-ko>').split('x')[1]), file.read('<i_04-pa>'), item_type= file.read('<i_04-ty>'), pow= file.read_int('<i_04-po>')); obst_item_group.add(item_04)
    if koll_item >= 5: item_05 = Block(int(file.read('<i_05-ko>').split('x')[0]), int(file.read('<i_05-ko>').split('x')[1]), file.read('<i_05-pa>'), item_type= file.read('<i_05-ty>'), pow= file.read_int('<i_05-po>')); obst_item_group.add(item_05)
    if koll_item >= 6: item_06 = Block(int(file.read('<i_06-ko>').split('x')[0]), int(file.read('<i_06-ko>').split('x')[1]), file.read('<i_06-pa>'), item_type= file.read('<i_06-ty>'), pow= file.read_int('<i_06-po>')); obst_item_group.add(item_06)
    if koll_item >= 7: item_07 = Block(int(file.read('<i_07-ko>').split('x')[0]), int(file.read('<i_07-ko>').split('x')[1]), file.read('<i_07-pa>'), item_type= file.read('<i_07-ty>'), pow= file.read_int('<i_07-po>')); obst_item_group.add(item_07)
    if koll_item >= 8: item_08 = Block(int(file.read('<i_08-ko>').split('x')[0]), int(file.read('<i_08-ko>').split('x')[1]), file.read('<i_08-pa>'), item_type= file.read('<i_08-ty>'), pow= file.read_int('<i_08-po>')); obst_item_group.add(item_08)
    if koll_item >= 9: item_09 = Block(int(file.read('<i_09-ko>').split('x')[0]), int(file.read('<i_09-ko>').split('x')[1]), file.read('<i_09-pa>'), item_type= file.read('<i_09-ty>'), pow= file.read_int('<i_09-po>')); obst_item_group.add(item_09)
    if koll_item >= 10: item_10 = Block(int(file.read('<i_10-ko>').split('x')[0]), int(file.read('<i_10-ko>').split('x')[1]), file.read('<i_10-pa>'), item_type= file.read('<i_10-ty>'), pow= file.read_int('<i_10-po>')); obst_item_group.add(item_10)
    if koll_item >= 11: item_11 = Block(int(file.read('<i_11-ko>').split('x')[0]), int(file.read('<i_11-ko>').split('x')[1]), file.read('<i_11-pa>'), item_type= file.read('<i_11-ty>'), pow= file.read_int('<i_11-po>')); obst_item_group.add(item_11)
    if koll_item >= 12: item_12 = Block(int(file.read('<i_12-ko>').split('x')[0]), int(file.read('<i_12-ko>').split('x')[1]), file.read('<i_12-pa>'), item_type= file.read('<i_12-ty>'), pow= file.read_int('<i_12-po>')); obst_item_group.add(item_12)
    if koll_item >= 13: item_13 = Block(int(file.read('<i_13-ko>').split('x')[0]), int(file.read('<i_13-ko>').split('x')[1]), file.read('<i_13-pa>'), item_type= file.read('<i_13-ty>'), pow= file.read_int('<i_13-po>')); obst_item_group.add(item_13)
    if koll_item >= 14: item_14 = Block(int(file.read('<i_14-ko>').split('x')[0]), int(file.read('<i_14-ko>').split('x')[1]), file.read('<i_14-pa>'), item_type= file.read('<i_14-ty>'), pow= file.read_int('<i_14-po>')); obst_item_group.add(item_14)
    if koll_item >= 15: item_15 = Block(int(file.read('<i_15-ko>').split('x')[0]), int(file.read('<i_15-ko>').split('x')[1]), file.read('<i_15-pa>'), item_type= file.read('<i_15-ty>'), pow= file.read_int('<i_15-po>')); obst_item_group.add(item_15)
    if koll_item >= 16: item_16 = Block(int(file.read('<i_16-ko>').split('x')[0]), int(file.read('<i_16-ko>').split('x')[1]), file.read('<i_16-pa>'), item_type= file.read('<i_16-ty>'), pow= file.read_int('<i_16-po>')); obst_item_group.add(item_16)
    if koll_item >= 17: item_17 = Block(int(file.read('<i_17-ko>').split('x')[0]), int(file.read('<i_17-ko>').split('x')[1]), file.read('<i_17-pa>'), item_type= file.read('<i_17-ty>'), pow= file.read_int('<i_17-po>')); obst_item_group.add(item_17)
    if koll_item >= 18: item_18 = Block(int(file.read('<i_18-ko>').split('x')[0]), int(file.read('<i_18-ko>').split('x')[1]), file.read('<i_18-pa>'), item_type= file.read('<i_18-ty>'), pow= file.read_int('<i_18-po>')); obst_item_group.add(item_18)
    if koll_item >= 19: item_19 = Block(int(file.read('<i_19-ko>').split('x')[0]), int(file.read('<i_19-ko>').split('x')[1]), file.read('<i_19-pa>'), item_type= file.read('<i_19-ty>'), pow= file.read_int('<i_19-po>')); obst_item_group.add(item_19)
    if koll_item >= 20: item_20 = Block(int(file.read('<i_20-ko>').split('x')[0]), int(file.read('<i_20-ko>').split('x')[1]), file.read('<i_20-pa>'), item_type= file.read('<i_20-ty>'), pow= file.read_int('<i_20-po>')); obst_item_group.add(item_20)


def load_level(load_level):
    Level = Reader(load_level)



    if Level.read('<versi>') != VERSION:
        print("Версия игры и версия уровня НЕСОВПАДАЮТ!!! возможны ошибки и баги!")
    koll_worlds_[0] = Level.read_int('<worlds>')
    level_name[0] = Level.read('<level_name>')

    if koll_worlds_[0] >= 1: level_worlds.append(Level.read('<01-world>'))
    if koll_worlds_[0] >= 2: level_worlds.append(Level.read('<02-world>'))
    if koll_worlds_[0] >= 3: level_worlds.append(Level.read('<03-world>'))
    if koll_worlds_[0] >= 4: level_worlds.append(Level.read('<04-world>'))
    if koll_worlds_[0] >= 5: level_worlds.append(Level.read('<05-world>'))
    if koll_worlds_[0] >= 6: level_worlds.append(Level.read('<06-world>'))
    if koll_worlds_[0] >= 7: level_worlds.append(Level.read('<07-world>'))
    if koll_worlds_[0] >= 8: level_worlds.append(Level.read('<08-world>'))
    if koll_worlds_[0] >= 9: level_worlds.append(Level.read('<09-world>'))
    if koll_worlds_[0] >= 10: level_worlds.append(Level.read('<10-world>'))
    if koll_worlds_[0] >= 11: level_worlds.append(Level.read('<11-world>'))
    if koll_worlds_[0] >= 12: level_worlds.append(Level.read('<12-world>'))
    if koll_worlds_[0] >= 13: level_worlds.append(Level.read('<13-world>'))
    if koll_worlds_[0] >= 14: level_worlds.append(Level.read('<14-world>'))
    if koll_worlds_[0] >= 15: level_worlds.append(Level.read('<15-world>'))
    if koll_worlds_[0] >= 16: level_worlds.append(Level.read('<16-world>'))
    if koll_worlds_[0] >= 17: level_worlds.append(Level.read('<17-world>'))
    if koll_worlds_[0] >= 18: level_worlds.append(Level.read('<18-world>'))
    if koll_worlds_[0] >= 19: level_worlds.append(Level.read('<19-world>'))
    if koll_worlds_[0] >= 20: level_worlds.append(Level.read('<20-world>'))
    if koll_worlds_[0] >= 21: level_worlds.append(Level.read('<21-world>'))
    if koll_worlds_[0] >= 22: level_worlds.append(Level.read('<22-world>'))
    if koll_worlds_[0] >= 23: level_worlds.append(Level.read('<23-world>'))
    if koll_worlds_[0] >= 24: level_worlds.append(Level.read('<24-world>'))
    if koll_worlds_[0] >= 25: level_worlds.append(Level.read('<25-world>'))
    if koll_worlds_[0] >= 26: level_worlds.append(Level.read('<26-world>'))
    if koll_worlds_[0] >= 27: level_worlds.append(Level.read('<27-world>'))
    if koll_worlds_[0] >= 28: level_worlds.append(Level.read('<28-world>'))
    if koll_worlds_[0] >= 29: level_worlds.append(Level.read('<29-world>'))
    if koll_worlds_[0] >= 30: level_worlds.append(Level.read('<30-world>'))
    if koll_worlds_[0] >= 31: level_worlds.append(Level.read('<31-world>'))
    if koll_worlds_[0] >= 32: level_worlds.append(Level.read('<32-world>'))
    if koll_worlds_[0] >= 33: level_worlds.append(Level.read('<33-world>'))
    if koll_worlds_[0] >= 34: level_worlds.append(Level.read('<34-world>'))
    if koll_worlds_[0] >= 35: level_worlds.append(Level.read('<35-world>'))
    if koll_worlds_[0] >= 36: level_worlds.append(Level.read('<36-world>'))
    if koll_worlds_[0] >= 37: level_worlds.append(Level.read('<37-world>'))
    if koll_worlds_[0] >= 38: level_worlds.append(Level.read('<38-world>'))
    if koll_worlds_[0] >= 39: level_worlds.append(Level.read('<39-world>'))
    if koll_worlds_[0] >= 40: level_worlds.append(Level.read('<40-world>'))
    if koll_worlds_[0] >= 41: level_worlds.append(Level.read('<41-world>'))
    if koll_worlds_[0] >= 42: level_worlds.append(Level.read('<42-world>'))
    if koll_worlds_[0] >= 43: level_worlds.append(Level.read('<43-world>'))
    if koll_worlds_[0] >= 44: level_worlds.append(Level.read('<44-world>'))
    if koll_worlds_[0] >= 45: level_worlds.append(Level.read('<45-world>'))
    if koll_worlds_[0] >= 46: level_worlds.append(Level.read('<46-world>'))
    if koll_worlds_[0] >= 47: level_worlds.append(Level.read('<47-world>'))
    if koll_worlds_[0] >= 48: level_worlds.append(Level.read('<48-world>'))
    if koll_worlds_[0] >= 49: level_worlds.append(Level.read('<49-world>'))

    Save = Reader(Level.read('<load_save>'))
    is_world[0] = Save.read_int('<world>') - 1
    player.live = Save.read_int('<live>')
    player.stamina = Save.read_int('<stamina>')
    player.money = Save.read_int('<money>')

    file_for_save[0] = Level.read('<load_save>')

###########-MAIN-###########
load_level(config_start_le.read('<load_level>'))
create_obj_list(level_worlds[is_world[0]])


#main play loop


while is_Window_open:
    sc.fill(colors.BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            _is_close_this_window_for_this_play = True
            game_close_sound.play()
            pygame.mixer.music.pause()
            while _is_close_this_window_for_this_play:
                sc.fill(colors.LIGHT_BLUE)
                text = "Вы действительно хотите покинуть игру?"
                close_pr_text = font_2.render(str(text), 1, colors.WHITE)
                sc.blit(close_pr_text, ((screen_resolution[0] // 2) - 415, (screen_resolution[1] // 2) - 180))
                text = "НЕТ - нажмите 'Esc'         да - нажмите 'Enter'"
                close_pr_text = font_2_.render(str(text), 1, colors.LIGHT_GREEN)
                sc.blit(close_pr_text, ((screen_resolution[0] // 2) - 330, (screen_resolution[1] // 2) - 130))
                pygame.display.update()

                if keyboard.is_pressed('enter'): is_Window_open = False; _is_close_this_window_for_this_play = False; save(file_for_save[0]); os.system('Colner FI L.exe')
                if keyboard.is_pressed('esc'): _is_close_this_window_for_this_play = False; event_2_sound.play(); time.sleep(sleep_time_pres_button * 4); pygame.mixer.music.unpause()

        elif event.type == anim_timer and (keyboard.is_pressed(butN.P_up) or keyboard.is_pressed(butN.P_up_alt)) and not keyboard.is_pressed(butN.P_right) and not keyboard.is_pressed(butN.P_left): player.im_stat = 'F'; is_down = False
        #elif event.type == anim_timer and (keyboard.is_pressed(butN.P_up) or keyboard.is_pressed(butN.P_up_alt)) and not keyboard.is_pressed(butN.P_right) and not keyboard.is_pressed(butN.P_left): player.im_stat = 'F'

        elif event.type == anim_timer and keyboard.is_pressed(butN.P_down): is_down = True;  player.im_stat = 'D';

        elif event.type == anim_timer and keyboard.is_pressed(butN.P_right) and not keyboard.is_pressed(butN.P_boost) and is_down: player.im_stat = 'D'
        elif event.type == anim_timer and keyboard.is_pressed(butN.P_left) and not keyboard.is_pressed(butN.P_boost) and is_down: player.im_stat = 'D'
        elif event.type == anim_timer and keyboard.is_pressed(butN.P_right) and not keyboard.is_pressed(butN.P_boost):
            if player.im_stat == 'F':
                player.im_stat = 'R1'
            elif player.im_stat == 'R1':
                player.im_stat = 'R2'
            elif player.im_stat == 'R2':
                player.im_stat = 'R3'
            elif player.im_stat == 'R3':
                player.im_stat = 'R4'
            elif player.im_stat == 'R4':
                player.im_stat = 'R1'
            else:
                player.im_stat = 'F'
        elif event.type == anim_timer and keyboard.is_pressed(butN.P_left) and not keyboard.is_pressed(butN.P_boost):
            #player.rect.x -= player.speed
            if player.im_stat == 'F':
                player.im_stat = 'L1'
            elif player.im_stat == 'L1':
                player.im_stat = 'L2'
            elif player.im_stat == 'L2':
                player.im_stat = 'L3'
            elif player.im_stat == 'L3':
                player.im_stat = 'L4'
            elif player.im_stat == 'L4':
                player.im_stat = 'L1'
            else:
                player.im_stat = 'F'
        elif event.type == anim_timer_max and keyboard.is_pressed(butN.P_right) and keyboard.is_pressed(butN.P_boost) and player.stamina > 0 and not is_down:
            if player.im_stat == 'F':
                player.im_stat = 'R1'
            elif player.im_stat == 'R1':
                player.im_stat = 'R2'
            elif player.im_stat == 'R2':
                player.im_stat = 'R3'
            elif player.im_stat == 'R3':
                player.im_stat = 'R4'
            elif player.im_stat == 'R4':
                player.im_stat = 'R1'
            else:
                player.im_stat = 'F'
        elif event.type == anim_timer_max and keyboard.is_pressed(butN.P_left) and keyboard.is_pressed(butN.P_boost) and player.stamina > 0 and not is_down:
            #player.rect.x -= player.speed
            if player.im_stat == 'F':
                player.im_stat = 'L1'
            elif player.im_stat == 'L1':
                player.im_stat = 'L2'
            elif player.im_stat == 'L2':
                player.im_stat = 'L3'
            elif player.im_stat == 'L3':
                player.im_stat = 'L4'
            elif player.im_stat == 'L4':
                player.im_stat = 'L1'
            else:
                player.im_stat = 'F'

        elif event.type == player_sound_timer and keyboard.is_pressed(butN.P_right) and not keyboard.is_pressed(butN.P_boost): walk_sound.play()
        elif event.type == player_sound_timer and keyboard.is_pressed(butN.P_left) and not keyboard.is_pressed(butN.P_boost): walk_sound.play()
        elif event.type == player_sound_timer_boost and keyboard.is_pressed(butN.P_right) and keyboard.is_pressed(butN.P_boost) and player.stamina > 0: walk_sound.play()
        elif event.type == player_sound_timer_boost and keyboard.is_pressed(butN.P_left) and keyboard.is_pressed(butN.P_boost) and player.stamina > 0: walk_sound.play()

        elif (keyboard.is_pressed(butN.P_left) or keyboard.is_pressed(butN.P_right)) and (event.type == stamina_timer and keyboard.is_pressed(butN.P_boost) and player.stamina > 0): player.stamina -= 1;
        elif (not (keyboard.is_pressed(butN.P_left) or keyboard.is_pressed(butN.P_right))) and (event.type == stamina_timer and not keyboard.is_pressed(butN.P_boost) and player.stamina < 100): player.stamina += 1;
        elif event.type == cloud_update_timer: cloud_uplate()
        elif event.type == pygame.MOUSEBUTTONDOWN and is_edit_world:
            if event.button == 1:
                old_mouse_pos = pygame.mouse.get_pos()




        player.anim(PlayerClass.ANIMA_PLAYER[player.im_stat])


    if player.rect.right >= screen_resolution[0] and is_world[0] == koll_worlds_[0] - 1:
        iiiii = True
        while iiiii:
            sc.fill(colors.WHITE)
            text = "Поздравляю ты прошёл уровень до конца!"
            close_pr_text = font_2.render(str(text), 1, colors.BLUE)
            sc.blit(close_pr_text, ((screen_resolution[0] // 2) - 415, (screen_resolution[1] // 2) - 180))
            text = "Заработанные монеты зачислены на ваш счёт.   Пройди новые уровни с сайта Colden I "
            close_pr_text = font_2_.render(str(text), 1, colors.LIGHT_BLUE)
            sc.blit(close_pr_text, ((screen_resolution[0] // 2) - 600, (screen_resolution[1] // 2) - 130))
            text = "Начать сначала - нажмите 'Enter'          Выйти из игры - нажмите 'Esc'"
            close_pr_text = font_2_.render(str(text), 1, colors.LIGHT_BLUE)
            sc.blit(close_pr_text, ((screen_resolution[0] // 2) - 500, (screen_resolution[1] // 2) - 90))
            pygame.display.update()

            if keyboard.is_pressed('enter'):

                Main_save = Reader('gamedata/saves/save.dat')
                end_levels = Main_save.read_int('<end_livels>') + 1
                MOney = Main_save.read_int('<money>') + player.money
                Main_save.write(('<end_livels>', '<money>'),(end_levels, MOney), start_text = "Colner Fi  Colden I GAME - save - Colden I GAME  Colner Fi")

                player.live = 100
                is_world[0] = 0
                player.stamina = 90
                player.money = 0
                save(file_for_save[0])
                load_level(config_start_le.read('<load_level>'))
                create_obj_list(level_worlds[is_world[0]])
                repl_sound.play()
                iiiii = False

            if keyboard.is_pressed('esc'):

                Main_save = Reader('gamedata/saves/save.dat')
                end_levels = Main_save.read_int('<end_livels>') + 1
                MOney = Main_save.read_int('<money>') + player.money
                Main_save.write(('<end_livels>', '<money>'),(end_levels, MOney), start_text = "Colner Fi  Colden I GAME - save - Colden I GAME  Colner Fi")

                player.live = 100
                is_world[0] = 0
                player.stamina = 90
                player.money = 0
                save(file_for_save[0])
                repl_sound.play()
                time.sleep(1)
                os.system('Colner FI L.exe')
                quit()

    if player.rect.right >= screen_resolution[0] and is_world[0] < koll_worlds_[0] - 1:
        player.rect.x = screen_resolution[0] // 2
        is_world[0] += 1
        save(file_for_save[0])
        create_obj_list(level_worlds[is_world[0]])
    if player.rect.left <= 0 and is_world[0] > 0:
        player.rect.x = screen_resolution[0] // 2
        is_world[0] -= 1
        save(file_for_save[0])
        create_obj_list(level_worlds[is_world[0]])

    if player.live > 100: player.live = 100; live_max_sound.play(); save(file_for_save[0])
    if player.live <= 0:
        game_over_sound.play()
        _is_game_over_this_player_ = True
        while _is_game_over_this_player_:
            sc.fill(colors.DARK_RED)
            text = "Персонаж погиб под вашим управлением."
            close_pr_text = font_2.render(str(text), 1, colors.LIGHT_RED)
            sc.blit(close_pr_text, ((screen_resolution[0] // 2) - 415, (screen_resolution[1] // 2) - 180))
            text = "Начать сначала - нажмите 'Enter'          Выйти из игры - нажмите 'Esc'"
            close_pr_text = font_2_.render(str(text), 1, colors.LIGHT_BLUE)
            sc.blit(close_pr_text, ((screen_resolution[0] // 2) - 500, (screen_resolution[1] // 2) - 130))
            pygame.display.update()

            if keyboard.is_pressed('enter'):
                player.live = 100
                is_world[0] = 0
                player.stamina = 90
                player.money = 0
                save(file_for_save[0])
                load_level(config_start_le.read('<load_level>'))
                create_obj_list(level_worlds[is_world[0]])
                repl_sound.play()
                _is_game_over_this_player_ = False

            if keyboard.is_pressed('esc'):
                player.live = 100
                is_world[0] = 0
                player.stamina = 90
                player.money = 0
                save(file_for_save[0])
                is_Window_open = False
                _is_game_over_this_player_ = False
                repl_sound.play()
                time.sleep(1)
                os.system('Colner_FI_L.exe')



    block_all = pygame.sprite.spritecollide(player_[0], obst_group, False)
    player.GND = ground
    for i in block_all:
        if pygame.sprite.collide_rect(player_[0], i):
            if i.rect.top + player.grav * 2 > player.rect.bottom and i.rect.top + 10 < player.rect.bottom:
                player.rect.bottom = i.rect.top
                player.GND = i.rect.top

            if i.rect.right - player.speed_max - 5 < player.rect.left and i.rect.right > player.rect.left:
                player.rect.left = i.rect.right #+ player.speed // 2

            if i.rect.left + player.speed_max + 5 > player.rect.right and i.rect.left < player.rect.right:
                player.rect.right = i.rect.left #- player.speed // 2

            if i.rect.bottom - 20 < player.rect.top and i.rect.bottom > player.rect.top:
                player.rect.top = i.rect.bottom
                player.is_jamp = False

    block_fizik = pygame.sprite.spritecollide(player_[0], obst_fizik_group, False)
    for i in block_fizik:
        if pygame.sprite.collide_rect(player_[0], i):
            if i.rect.top + player.grav * 2 > player.rect.bottom and i.rect.top + 10 < player.rect.bottom:
                player.rect.bottom = i.rect.top
                player.GND = i.rect.top

            if i.rect.bottom - 20 < player.rect.top and i.rect.bottom > player.rect.top:
                player.rect.top = i.rect.bottom
                player.is_jamp = False

            if i.rect.right - player.speed_max - 1 < player.rect.left and i.rect.right > player.rect.left:
                i.rect.right = player.rect.left
            if i.rect.left + player.speed_max + 1 > player.rect.right and i.rect.left < player.rect.right:
                i.rect.left = player.rect.right


        block_all = pygame.sprite.spritecollide(i, obst_group, False)
        for ob in block_all:
            if pygame.sprite.collide_rect(i, ob):
                if ob.rect.right - 10 < i.rect.left and ob.rect.right > i.rect.left:
                    i.rect.left = ob.rect.right  # + player.speed // 2

                if ob.rect.left + 10 > i.rect.right and ob.rect.left < i.rect.right:
                    i.rect.right = ob.rect.left  # - player.speed // 2

    block_fizik = obst_fizik_group.sprites()
    for i in block_fizik:
        i.move()


    block_uron = pygame.sprite.spritecollide(player_[0], obst_uron_group, False)
    for i in block_uron:
        if pygame.sprite.collide_rect(player_[0], i):
            player.is_jamp = True
            player.grav = player.max_jamp
            if player.im_stat[0] == "R":
                player.rect.x += player.speed_max * 10
            if player.im_stat[0] == "L":
                player.rect.x -= player.speed_max * 10
            if player.im_stat[0] == "F":
                player.rect.y -= player.speed_max * 15
            if player.im_stat[0] == "D":
                player.rect.y -= player.speed_max * 10
            if random.randint(0, 1) == 1: uron_sound.play()
            else: uron_2_sound.play()
            player.live -= i.uron

    block_item = pygame.sprite.spritecollide(player_[0], obst_item_group, True)
    for i in block_item:
        if pygame.sprite.collide_rect(player_[0], i) and not i.is_collected:
            event_sound.play()
            if i.item == 'random':
                if random.randint(0, 1) == 0:
                    player.live += random.randint(4, 9) * i.pow_i
                else:
                    player.money += random.randint(1, 3) * i.pow_i
            elif i.item == 'live': player.live += i.pow_i
            elif i.item == 'money': player.money += i.pow_i
            elif i.item == 'stamina': player.stamina += i.pow_i
            save(file_for_save[0])

    if (keyboard.is_pressed(butN.P_up) or keyboard.is_pressed(butN.P_up_alt))  and not player.is_jamp and player.rect.bottom == player.GND: jamp_sound.play()

    if keyboard.is_pressed('esc'):
        time.sleep(sleep_time_pres_button * 3)
        _is_close_this_window_for_this_play = True
        game_close_sound.play()
        pygame.mixer.music.pause()
        while _is_close_this_window_for_this_play:
            sc.fill(colors.LIGHT_BLUE)
            text = "Вы действительно хотите покинуть игру?"
            close_pr_text = font_2.render(str(text), 1, colors.WHITE)
            sc.blit(close_pr_text, ((screen_resolution[0] // 2) - 415, (screen_resolution[1] // 2) - 180))
            text = "НЕТ - нажмите 'Esc'         да - нажмите 'Enter'"
            close_pr_text = font_2_.render(str(text), 1, colors.LIGHT_GREEN)
            sc.blit(close_pr_text, ((screen_resolution[0] // 2) - 330, (screen_resolution[1] // 2) - 130))
            pygame.display.update()

            if keyboard.is_pressed('enter'): is_Window_open = False; _is_close_this_window_for_this_play = False; save(file_for_save[0]); os.system('Colner FI L.exe')
            if keyboard.is_pressed('esc'): _is_close_this_window_for_this_play = False; event_2_sound.play(); time.sleep(sleep_time_pres_button * 3); pygame.mixer.music.unpause()

    if keyboard.is_pressed(butN.colib_text):
        time.sleep(sleep_time_pres_button)
        is_draw_colin_text = not is_draw_colin_text

    if keyboard.is_pressed(butN.edit_world):
        time.sleep(sleep_time_pres_button)
        is_edit_world = not is_edit_world

    if keyboard.is_pressed(butN.save_button):
        save(file_for_save[0])
        time.sleep(sleep_time_pres_button)

    if keyboard.is_pressed(butN.draw_hud):
        time.sleep(sleep_time_pres_button)
        is_draw_HUD = not is_draw_HUD

    obst_no_coliz_group.draw(sc)
    obst_uron_group.draw(sc)
    obst_group.draw(sc)
    obst_fizik_group.draw(sc)
    obst_item_group.draw(sc)
    obst_item_G_group.draw(sc)
    player.telep(False)


    if is_draw_HUD:
        indi_panel_.updata(sc)
        indi_li.updata(sc)
        indi_st.updata(sc)
        indi_panel.updata(sc)
        if True:
            text = level_name[0] +"  -  " + indi_te[0]
            indi_te_text = font_2__.render(str(text), 1, colors.BLUE)
            sc.blit(indi_te_text, (20, 865))

            indi_mo_text = font_2.render(str(player.money), 1, colors.LIGHT_YELLOW)
            sc.blit(indi_mo_text, (1380, 160))

            if player.live > 75: indi_li.anim('gamedata/texture/indi/li_100.png')
            elif player.live > 50: indi_li.anim('gamedata/texture/indi/li_75.png')
            elif player.live > 25: indi_li.anim('gamedata/texture/indi/li_50.png')
            elif player.live > 15: indi_li.anim('gamedata/texture/indi/li_25.png')
            elif player.live > 0: indi_li.anim('gamedata/texture/indi/li_0.png')

            if player.stamina > 75: indi_st.anim('gamedata/texture/indi/st_100.png')
            elif player.stamina > 50: indi_st.anim('gamedata/texture/indi/st_75.png')
            elif player.stamina > 25: indi_st.anim('gamedata/texture/indi/st_50.png')
            elif player.stamina > 15: indi_st.anim('gamedata/texture/indi/st_25.png')
            elif player.stamina > 0: indi_st.anim('gamedata/texture/indi/st_0.png')

    if is_edit_world:
        text = "EDIT WORLD (v-0.1) - " + "mouse pos: " + str(pygame.mouse.get_pos()) + " | old mouse pos: " + str(old_mouse_pos) + " | X=" + str(pygame.mouse.get_pos()[0] - old_mouse_pos[0]) + " | Y=" + str(pygame.mouse.get_pos()[1] - old_mouse_pos[1])
        edit_world_text = font_1.render(str(text), 1, colors.BLUE)
        pygame.draw.rect(sc,colors.WHITE, (old_mouse_pos[0], old_mouse_pos[1], pygame.mouse.get_pos()[0] - old_mouse_pos[0], pygame.mouse.get_pos()[1] - old_mouse_pos[1]))
        sc.blit(edit_world_text, (5, 120))
        if keyboard.is_pressed('alt+up'): player.rect.y -=1; time.sleep(sleep_time_pres_button//2)
        if keyboard.is_pressed('alt+down'): player.rect.y += 1; time.sleep(sleep_time_pres_button//2)
        if keyboard.is_pressed('alt+right'): player.rect.x += 1; time.sleep(sleep_time_pres_button//2)
        if keyboard.is_pressed('alt+left'): player.rect.x -= 1; time.sleep(sleep_time_pres_button//2)
        player.update_(sc)
    else:
        player.update(sc)
    if is_draw_colin_text:
        pygame.draw.rect(sc, colors.BLACK, player.rect, 5)

        for i in obst_group.sprites():
            pygame.draw.rect(sc, colors.LIGHT_YELLOW, i.rect, 2)
        for i in obst_uron_group.sprites():
            pygame.draw.rect(sc, colors.LIGHT_RED, i.rect, 2)
        for i in obst_item_group.sprites():
            pygame.draw.rect(sc, colors.BLUE, i.rect, 3)
        for i in obst_no_coliz_group.sprites():
            pygame.draw.rect(sc, colors.WHITE, i.rect, 1)
        for i in obst_fizik_group.sprites():
            pygame.draw.rect(sc, colors.LIGHT_GREEN, i.rect, 3)

        text = "Версия: " + VERSION +"  [grav = " + str(player.grav) + "  |  player: " + str(player.rect) + "  |  gnd: "+str(player.GND) \
        + "]    {World: " + str(is_world[0]+1) + " / " + str(koll_worlds_[0]) + "}    (live=" + str(player.live) + " | money=" + str(player.money) + " | stamina: " + str(player.stamina) + ")  "
        colib_text = font_1.render(str(text), 1, colors.BLACK)
        sc.blit(colib_text, (5, 5))


    pygame.display.update()
    clock.tick(FPS)

quit()