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
    allow_mouse_detection_this_frame = True
    @classmethod
    def initialize(self, ui_manager):
        self.ui_manager = ui_manager
    @classmethod
    def update_inputs(self):
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            #HANDLES THE CAMERA ZOOM
            #SHOULD LATER BE MOVED TO THE PLAYER CLASS
            if event.type == pygame.MOUSEWHEEL:
                Camera.set_zoom(event.y)
            
            Renderer.ui_manager.process_events(event)
        

        self.allow_mouse_detection_this_frame = not Renderer.ui_manager.get_hovering_any_element()

        #GENERATES MOUSE STATES TO DETECT PRESS, RELEASE AND DOWN
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
        self.allow_mouse_detection_this_frame = True
        self.__last_mouse_world_pos = self.mouse_world_pos()

    @classmethod
    def mouse_button_down(self, button):
        return  self.__mouse_states[button][0] and self.allow_mouse_detection_this_frame
    @classmethod
    def mouse_button_pressed(self, button):
        return self.__mouse_states[button][1] and self.allow_mouse_detection_this_frame

    @classmethod
    def mouse_button_released(self, button):
        return self.__mouse_states[button][2] and self.allow_mouse_detection_this_frame

    @classmethod
    def mouse_world_pos(self):
        if not self.allow_mouse_detection_this_frame: return Vec2(1, 1)
        x = (pygame.mouse.get_pos()[0]/COORD_MULTIPLIER*Camera.zoom)+Camera.pos.x
        y = (pygame.mouse.get_pos()[1]/COORD_MULTIPLIER*Camera.zoom)+Camera.pos.y
        return Vec2(x, y)

    @classmethod
    def mouse_world_pos_rounded(self):
        if not self.allow_mouse_detection_this_frame: return Vec2(100, 100)
        x = pygame.math.clamp(round((pygame.mouse.get_pos()[0]/COORD_MULTIPLIER*Camera.zoom)+Camera.pos.x), 1, REAL_MAP_SIZE.x-1)
        y = pygame.math.clamp(round((pygame.mouse.get_pos()[1]/COORD_MULTIPLIER*Camera.zoom)+Camera.pos.y), 1, REAL_MAP_SIZE.y-1)
        return Vec2(x, y)

    @classmethod
    def mouse_world_movement(self):
        return self.__last_mouse_world_pos-self.mouse_world_pos()
    
    @classmethod
    def mouse_screen_pos(self):
        return Vec2(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

