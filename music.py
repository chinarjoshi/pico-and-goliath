import pygame as pg


pg.mixer.init()
class Sounds:
    'Sound effects for the whole program'
    def __init__(self):
        self.menu_effects = (
            pg.mixer.Sound("sounds/menu_select.ogg"),
        )
        self.impact_effects = {
            'pico': pg.mixer.Sound("sounds/pico_impact.ogg"),
            'goliath': pg.mixer.Sound("sounds/goliath_impact.ogg"),
            'win': pg.mixer.Sound("sounds/fanfare.ogg")
        }
        self.goal_effects = (
            pg.mixer.Sound("sounds/goal_impact.ogg"),
        )
    
    def set_volume(self, volume):
        for sound in self.menu_effects + tuple(self.impact_effects.values()):
            pg.mixer.Sound.set_volume(sound, volume)
            pg.mixer.Sound.set_volume(sound, volume)