import pygame as pg


size = (2560, 1440)
FPS = 144
GOAL_TALLY = {'pico': 0, 'goliath': 0}

pg.font.init()
main_font = pg.font.SysFont('garamond', 55, True)
win_font = pg.font.SysFont('garamond', 120, True)
win_subfont = pg.font.SysFont('garamond', 60, True)