"""
Main file of the game.

This module is to run directly from the command line. For more information,
please see README.md.

    Typical usage example:

        python3 pico-and-goliath/main.py

"""
import sys
import pygame as pg
import pygame_menu as pg_menu
from pygame_menu import sound
from src.collision_engine import CollisionEngine
from src.disks import Pico, Goliath, Ball
from src.goals import Goal
from src.music import Sounds
from src.settings import size, FPS, GOAL_TALLY, main_font, win_font, win_subfont


class PicoAndGoliath:
    """
    Encapsulates all data and control flow for Pico and Goliath.

    Provides a structured way to interface with the data for the entire game.
    Contains the main game loop, pygame window, and objects for the goals,
    Pico, Goliath, and the ball. Contains the physics-engine interactions
    as well.

    """

    def __init__(self):
        """
        Inits the game with all necessary player objects and pygame window.

        Initializes pygame, fps clock, and window at the top level.

        Initialized objects:
            -Pico
            -Goliath
            -Ball
            -Goal (2)
            -Sounds
            -CollisionEngine

        """
        pg.init()
        self.fps_clock = pg.time.Clock()
        self.window = pg.display.set_mode(size, pg.FULLSCREEN)
        self.icon = pg.image.load("images/ball.png").convert()
        self.background = pg.image.load('images/background.png')
        pg.display.set_caption("David_Goliath_Soccer")
        pg.display.set_icon(self.icon)

        self.pico = Pico([size[0]/4, size[1]/2])
        self.goliath = Goliath([3*size[0]/4, size[1]/2])
        self.ball = Ball([size[0]/2, size[1]/2])
        self.goal1 = Goal('left')
        self.goal2 = Goal('right')
        self.sounds = Sounds()
        self.collision_engine = CollisionEngine()

    def game_flow(self, volume: tuple, running: bool = True):
        """
        Main game flow of the program using pygame.

        Every iteration of the loop corresponds 1:1 with a frame. Every frame,
        the object attributes are updated, and the pygame window is blitted
        with the object images. The game ends when either player scores thrice.

        Args:
            volume (tuple[float, float]): Contains the volume setting for
                background music and sound effects.
            running (bool, optional): Boolean controlling game flow.
                Defaults to True.

        """
        # Background music is queued and looped
        pg.mixer.music.set_volume(volume[0])
        self.sounds.set_volume(volume[1])
        while running:
            self.window.blit(self.background, (0, 0))
            self.main_event_handler(pg.event.get())
            for player in self.pico, self.goliath:
                player.key_down(pg.key.get_pressed())

            # Updates the agents' vectors and blits window
            self.update_agents([self.pico, self.goliath, self.ball, self.goal1, self.goal2])
            self.update_window(self.window, [self.pico, self.goliath, self.ball, self.goal1, self.goal2])

            self.collision_engine.disk_collision(self.pico, self.ball, volume[1])
            self.collision_engine.disk_collision(self.goliath, self.ball, volume[1])
            self.render_score()

            # Check for ball's collision with goal, then proceed round
            if self.collision_engine.goal_collision(self.ball, self.goal1):
                self.sounds.goal_effects[0].play()
                self.proceed_round('goliath')
            elif self.collision_engine.goal_collision(self.ball, self.goal2):
                self.sounds.goal_effects[0].play()
                self.proceed_round('pico')

            # Fills the new frame with the background, redraws disk, and updates screen.
            pg.display.update()
            self.fps_clock.tick(FPS)

    def main_event_handler(self, events: list):
        """
        Checks the pygame events for any button presses and quit events.

        Args:
            events (list): Contains all current events defined by pygame.
        """
        for event in events:
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit(0)
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                main_menu.mainloop(self.window)

    def render_score(self):
        """
        Renders Pico and Goliath's score to their corners on the screen.

        Creates a pygame text object that contains the players score in the
        form of an f-string, then blits it to the main game winow.

        """
        pico_score = main_font.render(f"Pico Score: {GOAL_TALLY['pico']}", 1, (0, 0, 0))
        goliath_score = main_font.render(f"Goliath Score: {GOAL_TALLY['goliath']}", 1, (0, 0, 0))
        self.window.blit(pico_score, (10, 10))
        self.window.blit(goliath_score, (size[0] - 390, 10))

    def update_agents(self, agents: list):
        """
        Calls physics-engine methods on all agents in the game.

        Calls the acclerate (update position), boundary_check (check position),
        update_hitbox (updates rectangular position), and speed_check (keeps 
        velocity vectors under maximum speed) methods on all agents.

        The provided agents are:
            -Pico
            -Goliath
            -Goal (2)

        Args:
            agents (list): Contains objects for all updatable agents.

        """
        for agent in agents:
            try:
                agent.accelerate()
                agent.boundary_check()
                agent.update_hitbox()
                agent.speed_check()
            except AttributeError:
                continue

    def update_window(self, window: any, objects: list):
        """
        Blits all agents onto the pygame window from a list.

        Accepts a list of agents to be blitted onto the pygame window.
        This method should be called after self.update_agents() is called
        in order to make sure physics-engine functions properly.

        Args:
            window (pg): Pygame window the images should be blitted onto.
            objects (list): Contains agents who have a blittable image as
                an attribute.
        """
        for object in objects:
            window.blit(object.image, (object.position[0], object.position[1]))

    def proceed_round(self, winner: str):
        """
        Tallies the score and proceeds the round by resetting agents.

        This method should be called after a collision is detected using the
        collision engine object. Agents in the class namespace are updated
        using their intial position attribute. If either player has 3 points,
        the main loop is broken and the end_screen loop is entered.

        Args:
            winner (str): Name of the player who has scored.

        """
        GOAL_TALLY[winner] += 1
        for object in self.pico, self.goliath, self.ball:
            object.position[0] = object.initial_position[0]
            object.position[1] = object.initial_position[1]
            object.velocity = [0, 0]
        
        for player in 'pico', 'goliath':
            if GOAL_TALLY[player] >= 3:
                self.render_score()
                self.sounds.impact_effects['win'].play()
                self.end_screen(player)
        pg.time.wait(500)

    def end_screen(self, winner: str, running: bool = True):
        """
        Displays the winner of the game and proceeds to end-game loop.

        This method should only be called after one player scores 3 points,
        thus triggering the end-game. Contains the end-game loop which checks
        for RETURN to return to main menu, and ESCAPE which quits the program.

        Args:
            winner (str): Name of the winner of the game to be displayed.
            running (bool, optional): Controls the end game loop iteration.
                Defaults to True.

        """
        while running:
            self.end_event_handler(pg.event.get())

            color = (0, 0, 150) if winner == 'pico' else (150, 0, 0)
            position = ((size[0]/4 - 300, size[1]/2 - 400) 
                        if winner == 'pico'
                        else (3*size[0]/4 - 420, size[1]/2 - 400))
            win_text = win_font.render(f'{winner.capitalize()} Wins!', 1, color)
            return_text = win_subfont.render('Press RETURN to play again',
                                            1, (150, 0, 150))
            exit_text = win_subfont.render('Press ESCAPE to quit',
                                            1, (150, 0, 150))
            self.window.blit(win_text, position)
            self.window.blit(return_text, (position[0] + 10, position[1] + 120))
            self.window.blit(exit_text, (position[0] + 10, position[1] + 180))
            pg.display.update()
            self.fps_clock.tick(FPS)
        
    def end_event_handler(self, events: list):
        """
        Event handler for end-game loop to check for user input.

        Checks for keyboard input outlined in self.end_screen() documentation.
        Triggers main_menu or pygame.quit() depending on user key press.

        Args:
            events (list): Contains the current events defined by pygame.

        """
        for event in events:
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit(1)
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                pg.quit()
                sys.exit(1)
            if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                GOAL_TALLY['pico'] = 0
                GOAL_TALLY['goliath'] = 0
                main_menu.mainloop(game.window)


pg.mixer.music.load('sounds/background.ogg')
pg.mixer.music.set_volume(.03)
pg.mixer.music.play(loops=-1)
game = PicoAndGoliath()

background_volume = .3
effects_volume = .3

# ----------------------------------- MENU ------------------------------------
def quit():
    """
    Defines procedure to quit the game.

    Menu sound effect is played upon final mouse-press, pygame is uninitialized,
    and program is exited with exit code 0.

    """
    game.sounds.menu_effects[0].play()
    pg.quit()
    sys.exit(0)

DIMENSIONS = {
    'height': 650,
    'width': 800
}
ABOUT = (
    'Pico and Goliath',
    'By: Chinar Joshi',
    'Email: chinarjoshi7@gmail.com'
)
CONTROLS = (
    'WASD: Move Pico',
    'ARROW KEYS: Move Goliath',
    'ESCAPE: Pause menu'
)
STRATEGY_GUIDE = (
    'Rules of the game:',
    'Play as Pico (left side) or Goliath (right side)',
    'The object of the game is to hit the ball into either goal that is',
    'constantly moving. First player to 3 points wins. For more information,',
    'go to: https://github.com/chinarjoshi/pico-and-goliath',
    'Good luck!'
)
back = 'Return to main menu'

theme = pg_menu.themes.THEME_DARK.copy()
font = pg_menu.font.FONT_FRANCHISE
theme.widget_font = font
theme.widget_font_size = 50
theme.title_font = font
theme.title_font_size = 90

# PLAY MENU
play_menu = pg_menu.Menu(
    height=DIMENSIONS['height'],
    width=DIMENSIONS['width'],
    title='Play Menu',
    theme=theme
)
play_menu.add_button('Start', game.game_flow, (background_volume, effects_volume))

# HELP MENU
help_menu = pg_menu.Menu(
    height=DIMENSIONS['height'],
    width=DIMENSIONS['width'],
    title='Help',
    theme=theme
)

# CONTROLS MENU
controls_menu = pg_menu.Menu(
    height=DIMENSIONS['height'],
    width=DIMENSIONS['width'],
    title='Controls',
    theme=theme
)
for item in CONTROLS:
    controls_menu.add_label(item, font_size=40)
controls_menu.add_button(back, pg_menu.events.BACK)

play_menu.add_button('Controls', controls_menu)
play_menu.add_button(back, pg_menu.events.BACK)

# ABOUT MENU
about_menu = pg_menu.Menu(
    height=DIMENSIONS['height'],
    width=DIMENSIONS['width'],
    title='About',
    theme=theme
)
for item in ABOUT:
    about_menu.add_label(item, font_size=40)
about_menu.add_button(back, pg_menu.events.BACK)

# STRATEGY MENU
strategy_menu = pg_menu.Menu(
    height=DIMENSIONS['height'],
    width=DIMENSIONS['width'],
    title='Strategy Guide',
    theme=theme
)
for item in STRATEGY_GUIDE:
    strategy_menu.add_label(item, align=pg_menu.locals.ALIGN_LEFT, font_size=35)
strategy_menu.add_button(back, pg_menu.events.BACK)
help_menu.add_button('Controls', controls_menu)
help_menu.add_button('About', about_menu)
help_menu.add_button('Strategy Guide', strategy_menu)
help_menu.add_button(back, pg_menu.events.BACK)

# SETTINGS MENU
settings_menu = pg_menu.Menu(
    height=DIMENSIONS['height'],
    width=DIMENSIONS['width'],
    theme=theme,
    title='Settings'
)

def change_background_volume(value, volume):
    """Changes background music volume based on menu interaction."""
    background_volume = volume

def change_effects_volume(value, volume):
    """Changes sound effects volume based on menu interaction."""
    effects_volume = volume

settings_menu.add_selector('Background music volume: ',
                        [('10%', .1),
                        ('20%', .2),
                        ('30%', .3),
                        ('40%', .4),
                        ('50%', .5),
                        ('60%', .6),
                        ('70%', .7),
                        ('80%', .8),
                        ('90%', .9),
                        ('100%', 1)],
                        onchange=change_background_volume,
                        selector_id='select_background_volume')
settings_menu.add_selector('Sound effects volume: ',
                        [('10%', .1),
                        ('20%', .2),
                        ('30%', .3),
                        ('40%', .4),
                        ('50%', .5),
                        ('60%', .6),
                        ('70%', .7),
                        ('80%', .8),
                        ('90%', .9),
                        ('100%', 1)],
                        onchange=change_effects_volume,
                        selector_id='select_effects_volume')
settings_menu.add_button(back, pg_menu.events.BACK)

# MAIN MENU
main_menu = pg_menu.Menu(
    height=DIMENSIONS['height'],
    width=DIMENSIONS['width'],
    theme=theme,
    title='Pico and Goliath'
)

main_menu.add_button('Play', play_menu)
main_menu.add_button('Help', help_menu)
main_menu.add_button('Settings', settings_menu)
main_menu.add_button('Quit', pg_menu.events.EXIT)

engine = sound.Sound()
engine.set_sound(sound.SOUND_TYPE_CLICK_MOUSE, 'sounds/menu_select.ogg')
main_menu.set_sound(engine, recursive=True)

if __name__ == '__main__':
    main_menu.mainloop(game.window)
