"""
Defines the music class that contains all audio files of the package.

    Typical usage example:

        sounds = Sounds()
        sounds.impact_effects['pico'].play()

"""
import pygame as pg


pg.mixer.init()
class Sounds:
    """
    Encapsulates sound effects for the whole program.
    """

    def __init__(self):
        """
        Inits the Sounds object with all files from the ./sounds directory.

        Initializes the menu effects, pico/goliath/goal impact effects, and the
        game-ending fanfare.

        """
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
    
    def set_volume(self, volume: int):
        """
        Sets the volume of all sound effects to be played.

        Args:
            volume (int): Volume that the sound effects should play at.

        """
        for sound in self.menu_effects + tuple(self.impact_effects.values()):
            pg.mixer.Sound.set_volume(sound, volume)
            pg.mixer.Sound.set_volume(sound, volume)