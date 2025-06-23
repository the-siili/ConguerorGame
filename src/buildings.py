import pygame_gui
import pygame

from object import Object
from renderer import Renderer
from amath import Vec2
from input import Input

from settings import BUILDING_SIZES, WINDOW_SIZE

#INFORMATION PANELS SHOW ENEMY NATION BUILDINGS INFORMATION
#CONTROL PANELS SHOW PLAYERS NATION BUILDINGS INFO AND CONTROLS

class Building(Object):
    def __init__(self, pos, scale, nation, texture_key, information_panel, control_panel):
        super().__init__(pos, scale)
        self.nation = nation
        self.render_layer = 2
        self.occupied_points = set()
        self.texture_key = texture_key

        self.information_panel = information_panel
        self.control_panel = control_panel

        self.type_str = "NULL"

        
        

        for y in range(round(-self.scale.y/2), int(self.scale.y/2)+1):
            for x in range(round(-self.scale.x/2), int(self.scale.x/2)+1):
                self.occupied_points.add(pos+Vec2(x, y))
                self.nation.world.world_points[pos+Vec2(x, y)]["current_object"] = self

    
    def start(self):
        pass
    def update(self):
        if self.information_panel.is_open:
            self.information_panel.update()
        if self.control_panel.is_open:
            self.control_panel.update()

    def render(self):
        Renderer.render_world_texture(self.texture_key, self.pos, self.scale, centered=True)
        if Input.mouse_world_pos_rounded() in self.occupied_points:
            for i in self.occupied_points:
                Renderer.render_world_circle(i, 0.4, self.nation.color, 1)
    def open_info(self):
        pass
    def close_info(self):
        pass
    def construct(self):
        pass
    def destroy(self):
        pass

class InformationPanel():
    def __init__(self, owner):
        self.owner = owner
        self.background_panel = None
        self.type_label = None
        self.close_btn = None
        self.is_open = False

    def open(self):
        self.type = self.owner.type_str
        background_layout_rect = pygame.Rect(0, 0, WINDOW_SIZE.x, 200)
        background_layout_rect.bottomleft = (0, 0)
        self.background_panel = pygame_gui.elements.UIPanel(relative_rect=background_layout_rect,
                                                        manager=Renderer.ui_manager,
                                                        anchors={'bottom': 'bottom',
                                                                    'centerx':'centerx'},
                                                        starting_height=0)

        name_label_layout_rect = pygame.Rect(0, 0, 353, 30)
        name_label_layout_rect.topleft = (0, 0)
        name = f"""{self.type} Of {self.owner.nation.name}""" #Power: {len(self.owner.nation.occupied_points)
        self.type_label = pygame_gui.elements.UILabel(relative_rect=name_label_layout_rect,
                                                    text=name, manager=Renderer.ui_manager,
                                                    container=self.background_panel,
                                                    anchors={'left': 'left',
                                                            'top':'top'})
        close_btn_layout_rect = pygame.Rect(0, 0, 40, 40)
        close_btn_layout_rect.topright = (0, 0)
        self.close_btn = pygame_gui.elements.UIButton(relative_rect=close_btn_layout_rect,
                                                    text="X", 
                                                    manager=Renderer.ui_manager,
                                                    container=self.background_panel,
                                                    anchors={'right': 'right',
                                                            'top':'top'})
        self.is_open = True
    def close(self):
        self.background_panel.kill()
        self.type_label = None
        self.is_open = False
    
    def update(self):
        if self.close_btn.check_pressed():
            self.close()
            print("hellooo")

class ControlPanel():
    def __init__(self, owner):
        self.owner = owner
        self.is_open = False

    def open(self):
        self.is_open = True
    def close(self):
        self.background_panel = None
        self.type_label = None
        self.is_open = False

    def update(self):
        pass

class Capitol(Building):
    def __init__(self, pos, nation):
        super().__init__(pos, Vec2(BUILDING_SIZES["capitol"], BUILDING_SIZES["capitol"]), nation, "capitol", \
            CapitolInformationPanel(self), CapitolControlPanel(self))
        self.type_str = "Capitol"

class CapitolInformationPanel(InformationPanel):
    def __init__(self, owner):
        super().__init__(owner)

class CapitolControlPanel(ControlPanel):
    def __init__(self, owner):
        super().__init__(owner)

