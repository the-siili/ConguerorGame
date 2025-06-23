import pygame_gui
import pygame
from input import Input
from renderer import Renderer, Camera
from amath import Vec2
import buildings
from settings import WINDOW_SIZE




#global
class Player():
    nation = None
    world = None
    in_action = False

    active_ui_panel = None
    @classmethod
    def initialize(self, nation, world):
        self.nation = nation
        self.world = world

        info_text_layout_rect = pygame.Rect(0, 0, WINDOW_SIZE.x, 30)
        info_text_layout_rect.topleft = (0, 0)
        self.info_text = pygame_gui.elements.UILabel(relative_rect=info_text_layout_rect,
                                                    text="", manager=Renderer.ui_manager,
                                                    anchors={'left': 'left',
                                                            'top':'top'})

    @classmethod
    def update(self):
        if Input.mouse_button_down("right"):
            Camera.move(Input.mouse_world_movement())

        if Input.mouse_button_pressed("left") and not self.in_action:
            point = self.world.world_points[Input.mouse_world_pos_rounded()]
            if  point["current_object"] != None and issubclass(type(point["current_object"]) ,buildings.Building):
                if self.active_ui_panel != None:
                    self.active_ui_panel.close()
                if type(point["current_object"]) == buildings.Capitol:
                    self.active_ui_panel = point["current_object"].information_panel
                    self.active_ui_panel.open()
        
        point = self.world.world_points[Input.mouse_world_pos_rounded()]

        self.info_text.set_text(point["current_object"].type_str if point["current_object"] != None else point["terrain_type"])


    @classmethod
    def render(self):
        calc_vectors = [Vec2(0, 0),
                Vec2(0, -1), 
                Vec2(1, -1),
                Vec2(1, 0),
                Vec2(1, 1), 
                Vec2(0, 1),
                Vec2(-1, 1), 
                Vec2(-1, 0), 
                Vec2(-1, -1)]

        for vec in calc_vectors:
            mouse_pos = Input.mouse_world_pos_rounded()
            if mouse_pos+vec in self.world.world_points.keys():
                Renderer.render_world_circle(mouse_pos+vec, 0.3, (255, 255, 255), 0)
        
        self.nation.render_border()
