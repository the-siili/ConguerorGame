import pygame_gui
import pygame
from amath import Vec2
from renderer import Renderer
from object import Object
from input import Input

class Castle(Object):
    def __init__(self, pos):
        super().__init__(pos, Vec2(1, 1))
        self.render_layer = 2
        self.info_panel = None
        self.info_panel_X = None
    
    def update(self):
        if self.info_panel != None and self.info_panel_X.check_pressed():
            self.close_info()


    def render(self):
        Renderer.render_world_texture(Renderer.surfaces["capitol"], self.pos-Vec2(1, 1), self.scale)
    
    def open_info(self):
        print("hi")
        button_layout_rect = pygame.Rect(0, 0, 200, 300)
        button_layout_rect.topright = (0, 0)
        self.info_panel = pygame_gui.elements.UIPanel(relative_rect=button_layout_rect, 
                                                        manager=Renderer.ui_manager,
                                                        anchors={'right': 'right',
                                                                'top': 'top'})
        button_layout_rect = pygame.Rect(0, 0, 30, 30)
        button_layout_rect.topright = (0, 0)
        self.info_panel_X = pygame_gui.elements.UIButton(relative_rect=button_layout_rect,
                                                        text='X',
                                                        manager=Renderer.ui_manager,
                                                        container=self.info_panel,
                                                        anchors={'right': 'right',
                                                                'top': 'top'})
        
    def close_info(self):
        self.info_panel_X.remove(self.info_panel_X.groups())
        self.info_panel_X = None
        self.info_panel.remove(self.info_panel.groups())
        self.info_panel = None