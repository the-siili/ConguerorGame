# Example file showing a basic pygame "game loop"
import pygame
import pygame_gui
import pygame_shaders
import math
import time
import cProfile

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
map_button = None

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

    load_scene(Game())

    #DEBUGGING
    button_layout_rect = pygame.Rect(0, 0, 100, 50)
    button_layout_rect.topright = (0, 0)
    global map_button
    map_button = pygame_gui.elements.UIButton(relative_rect=button_layout_rect,
                                                        text="new map",
                                                        manager=Renderer.ui_manager,
                                                        anchors={'right': 'right',
                                                                'top': 'top'})
last_time = 0
def gameloop():
    while running:
        global map_button
        if map_button.check_pressed():
            #initializing renderer, because the surfaces are affected by zoom, this resets that
            Renderer.reset()
            load_scene(Game())

            #DEBUGGING
            button_layout_rect = pygame.Rect(0, 0, 100, 50)
            button_layout_rect.topright = (0, 0)
            map_button = pygame_gui.elements.UIButton(relative_rect=button_layout_rect,
                                                    text="new map",
                                                    manager=Renderer.ui_manager,
                                                    anchors={'right': 'right',
                                                            'top': 'top'})


        
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
        clock.tick()  # limits FPS to 60
        #print(clock.get_fps())
        global last_time
        Input.clean_inputs()
        delta_time = time.time()-last_time
        last_time = time.time()

        print(clock.get_fps())

    pygame.quit()

def update_engine_data():
    global current_scene
    EngineData.set_current_scene(current_scene)

    global delta_time
    EngineData.delta_time = delta_time

def load_scene(scene):
    new_scene = scene
    EngineData.set_current_scene(new_scene)
    global current_scene
    current_scene = new_scene
    scene.start()

def get_current_scene():
    global current_scene
    return current_scene

start()

cProfile.run("gameloop()")