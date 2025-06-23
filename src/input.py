import pygame
import pygame_gui
from amath import Vec2
from settings import COORD_MULTIPLIER, WINDOW_SIZE, REAL_MAP_SIZE
from renderer import Renderer, Camera

#global
class Input():
    ui_manager = None
    __mouse_states = {
        "left":(False, False, False),
        "right":(False, False, False),
        "middle":(False, False, False),
    }
    __last_mouse_world_pos = Vec2(0, 0)

    @classmethod
    def initialize(self, ui_manager):
        self.ui_manager = ui_manager
    @classmethod
    def update_inputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEWHEEL:
                Camera.set_zoom(event.y)

            Renderer.ui_manager.process_events(event)
        self.__mouse_states= {
            "left":(pygame.mouse.get_pressed(3)[0], 
                    pygame.mouse.get_pressed(3)[0] and self.__mouse_states["left"][0] == False,
                    pygame.mouse.get_pressed(3)[0] == False and self.__mouse_states["left"][0] == True),

            "right":(pygame.mouse.get_pressed(3)[2], 
                    pygame.mouse.get_pressed(3)[2] and self.__mouse_states["right"][0] == False,
                    pygame.mouse.get_pressed(3)[2] == False and self.__mouse_states["right"][0] == True),
            "middle":(pygame.mouse.get_pressed(3)[1], 
                    pygame.mouse.get_pressed(3)[1] and self.__mouse_states["middle"][0] == False,
                    pygame.mouse.get_pressed(3)[1] == False and self.__mouse_states["middle"][0] == True),
        }

    @classmethod
    def clean_inputs(self):
        self.__last_mouse_world_pos = self.mouse_world_pos()

    @classmethod
    def mouse_button_down(self, button):
        return self.__mouse_states[button][0]
    @classmethod
    def mouse_button_pressed(self, button):
        return self.__mouse_states[button][1]

    @classmethod
    def mouse_button_released(self, button):
        return self.__mouse_states[button][2]

    #BROKEN!! NEEDS CAMERA POSITION SUBTRACTED TO WORK CORRECTLY
    @classmethod
    def mouse_world_pos(self):
        x = (pygame.mouse.get_pos()[0]/COORD_MULTIPLIER*Camera.zoom)+Camera.pos.x
        y = (pygame.mouse.get_pos()[1]/COORD_MULTIPLIER*Camera.zoom)+Camera.pos.y
        return Vec2(x, y)

    @classmethod
    def mouse_world_pos_rounded(self):
        x = pygame.math.clamp(round((pygame.mouse.get_pos()[0]/COORD_MULTIPLIER*Camera.zoom)+Camera.pos.x), 1, REAL_MAP_SIZE.x-1)
        y = pygame.math.clamp(round((pygame.mouse.get_pos()[1]/COORD_MULTIPLIER*Camera.zoom)+Camera.pos.y), 1, REAL_MAP_SIZE.y-1)
        return Vec2(x, y)

    @classmethod
    def mouse_world_movement(self):
        return self.__last_mouse_world_pos-self.mouse_world_pos()
    
    @classmethod
    def mouse_screen_pos(self):
        return Vec2(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

    @classmethod
    def was_ui_button_pressed(self, button):
        return button == self.__ui_last_pressed_button
