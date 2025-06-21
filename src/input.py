import pygame
from amath import Vec2
from settings import COORD_MULTIPLIER
from renderer import Camera

class Input():
    __mouse_states = {
        "left":(False, False, False),
        "right":(False, False, False),
        "middle":(False, False, False),
    }



    @classmethod
    def update_inputs(self):
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
        return Vec2(pygame.mouse.get_pos()[0]/COORD_MULTIPLIER, pygame.mouse.get_pos()[1]/COORD_MULTIPLIER)-Camera.pos
    
    @classmethod
    def mouse_screen_pos(self):
        return Vec2(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
