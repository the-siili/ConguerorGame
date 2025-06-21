# Example file showing a basic pygame "game loop"
import pygame
import pygame_gui
import math

from game import Game
from input import Input
from object import Object
from renderer import Renderer, Camera
from input import Input

from settings import MAP_SIZE, WINDOW_SIZE, COORD_MULTIPLIER, WINDOW_FLAGS
from amath import Vec2
from engine_data import EngineData




screen = None
clock = None
delta_time = None
running = True
current_scene = None


def start():
    pygame.init()
    global screen
    screen = pygame.display.set_mode(tuple(WINDOW_SIZE), WINDOW_FLAGS)
    global clock
    clock = pygame.time.Clock()
    global delta_time
    delta_time = clock.tick(60)
    global running
    running = True

    Renderer.initialize(screen)
    Input.initialize(Renderer.ui_manager)

    global current_scene
    current_scene = Game()

    EngineData.current_scene = current_scene
    #print(EngineData.current_scene)
    update_engine_data()
    current_scene.start()
    

def gameloop():
    print("hello")
    while running:
        
        update_engine_data()
        
        Input.update_inputs()
        
        current_scene.update()
        global delta_time
        Renderer.ui_manager.update(delta_time)
        
        # fill the screen with a color to wipe away anything from last frame
        screen.fill("black")

        current_scene.render()
        Renderer.ui_manager.draw_ui(Renderer.screen)

        pygame.display.update()
        delta_time = clock.tick(60)  # limits FPS to 60

        Input.clean_inputs()

    pygame.quit()

def update_engine_data():
    #EngineData.current_scene = current_scene
    #EngineData.delta_time = delta_time
    pass

def load_scene(scene):
    current_scene = scene

def get_current_scene():
    return current_scene

start()
gameloop()