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


#using globas that are passed to diiferent handlers like the Renderer and EngineData
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

def gameloop():
    while running:

        EngineData.update()
        #DEBBUGING FOR CHANGEING SCENE
        global map_button
        if map_button.check_pressed():
            load_scene(Game())

            #DEBUGGING
            button_layout_rect = pygame.Rect(0, 0, 100, 50)
            button_layout_rect.topright = (0, 0)
            map_button = pygame_gui.elements.UIButton(relative_rect=button_layout_rect,
                                                    text="new map",
                                                    manager=Renderer.ui_manager,
                                                    anchors={'right': 'right',
                                                            'top': 'top'})

        Input.update_inputs()
        current_scene.update()
        Renderer.ui_manager.update(EngineData.delta_time)
        
        
        
        
        # fill the screen with a color to wipe away anything from last frame
        screen.fill("black")

        current_scene.render()
        Renderer.ui_manager.draw_ui(Renderer.screen)

        pygame.display.update()
        clock.tick()  # limits FPS to 60
        #print(clock.get_fps())
        global last_time
        Input.clean_inputs()


        print(clock.get_fps())

    pygame.quit()


def load_scene(scene):
    #reseting renderer, because the surfaces are affected by zoom, this resets that
    
    Renderer.reset()
    new_scene = scene
    EngineData.set_current_scene(new_scene)
    global current_scene
    current_scene = new_scene
    scene.start()

def get_current_scene():
    global current_scene
    return current_scene

start()

cProfile.run("gameloop()", sort="tottime")