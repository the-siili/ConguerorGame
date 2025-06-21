# Example file showing a basic pygame "game loop"
import pygame
import pygame_gui
import math

from game import Game
from input import Input
from world import World
from object import Object
from renderer import Renderer, Camera


from settings import MAP_SIZE, WINDOW_SIZE, COORD_MULTIPLIER, WINDOW_FLAGS
from amath import Vec2





def main():
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode(tuple(WINDOW_SIZE), WINDOW_FLAGS)
    ui_manager = pygame_gui.UIManager(tuple(WINDOW_SIZE))
    clock = pygame.time.Clock()
    delta_time = clock.tick(60)
    running = True
    Renderer.initialize(screen, ui_manager)

    Game.start()
    while running:
        Game.get_input()
        Game.update(delta_time)

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("black")

        Game.render()
        
        pygame.display.update()
        delta_time = clock.tick(60)  # limits FPS to 60

    pygame.quit()





main()