import pygame_gui
import pygame

from object import Object
from renderer import Renderer
from amath import Vec2
from input import Input

from settings import BUILDING_SIZES, WINDOW_SIZE
from engine_data import EngineData
import buildings
from player import Player

class ControlPanel():
    def __init__(self, owner):
        self.owner = owner
        self.background_panel = None
        self.close_btn = None
        self.is_open = False

    def open(self):
        background_layout_rect = pygame.Rect(0, 0, WINDOW_SIZE.x, 200)
        background_layout_rect.bottomleft = (0, 0)
        self.background_panel = pygame_gui.elements.UIPanel(relative_rect=background_layout_rect,
                                                        manager=Renderer.ui_manager,
                                                        anchors={'bottom': 'bottom',
                                                                    'centerx':'centerx'},
                                                        starting_height=0)
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
    
    def update_information(self):
        pass


class InformationPanel():
    def __init__(self, owner):
        self.owner = owner
        self.background_panel = None
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
    
    def update_information(self):
        pass

class CapitolInformationPanel(InformationPanel):
    def __init__(self, owner):
        super().__init__(owner)
        self.power_label = None
        self.name_label = None
    def __create_ui_elements(self):
        name_label_layout_rect = pygame.Rect(0, 0, 353, 30)
        name_label_layout_rect.topleft = (0, 0)
        name = f"""{self.type} Of {self.owner.nation.name}""" #Power: {len(self.owner.nation.occupied_points)
        self.type_label = pygame_gui.elements.UILabel(relative_rect=name_label_layout_rect,
                                                    text=name, manager=Renderer.ui_manager,
                                                    container=self.background_panel,
                                                    anchors={'left': 'left',
                                                            'top':'top'})
        power_label_layout_rect = pygame.Rect(0, 0, 353, 20)
        power_label_layout_rect.topleft = (0, 25)
        power = f"""Power: {self.owner.nation.power}"""
        self.power_label = pygame_gui.elements.UILabel(relative_rect=power_label_layout_rect,
                                                    text=power, manager=Renderer.ui_manager,
                                                    container=self.background_panel,
                                                    anchors={'left': 'left',
                                                            'top':'top'})
    def open(self):
        super().open()
        self.__create_ui_elements()
    
    def update_information(self):
        if self.background_panel != None:
            self.power_label.set_text(f"""Power: {self.owner.nation.power}""")

class CapitolControlPanel(ControlPanel):
    def __init__(self, owner):
        super().__init__(owner)
        self.name_label = None
        self.power_label = None
        self.honor_label = None
        self.money_label = None
        self.wood_label = None
        self.mineral_label = None
        self.build_panel = None
        self.castle_btn  = None


    def __create_ui_elements(self):
        #CREATES INFORMATION LABELS
        name_label_layout_rect = pygame.Rect(0, 0, 353, 30)
        name_label_layout_rect.topleft = (0, 0)
        name = f"""{self.owner.type_str}""" #Power: {len(self.owner.nation.occupied_points)
        self.name_label = pygame_gui.elements.UILabel(relative_rect=name_label_layout_rect,
                                                    text=name, manager=Renderer.ui_manager,
                                                    container=self.background_panel,
                                                    anchors={'left': 'left',
                                                            'top':'top'})



        power_label_layout_rect = pygame.Rect(0, 0, 353, 20)
        power_label_layout_rect.topleft = (0, 25)
        power = f"""Power: {self.owner.nation.power}"""
        self.power_label = pygame_gui.elements.UILabel(relative_rect=power_label_layout_rect,
                                                    text=power, manager=Renderer.ui_manager,
                                                    container=self.background_panel,
                                                    anchors={'left': 'left',
                                                            'top':'top'})

        honor_label_layout_rect = pygame.Rect(0, 0, 353, 20)
        honor_label_layout_rect.topleft = (0, 50)
        honor = f"""Honor: {self.owner.nation.honor}"""
        self.honor_label = pygame_gui.elements.UILabel(relative_rect=honor_label_layout_rect,
                                                    text=honor, manager=Renderer.ui_manager,
                                                    container=self.background_panel,
                                                    anchors={'left': 'left',
                                                            'top':'top'})

        money_label_layout_rect = pygame.Rect(0, 0, 353, 20)
        money_label_layout_rect.topleft = (0, 75)
        money = f"""Money: {self.owner.nation.money}"""
        self.money_label = pygame_gui.elements.UILabel(relative_rect=money_label_layout_rect,
                                                    text=money, manager=Renderer.ui_manager,
                                                    container=self.background_panel,
                                                    anchors={'left': 'left',
                                                            'top':'top'})

        wood_label_layout_rect = pygame.Rect(0, 0, 353, 20)
        wood_label_layout_rect.topleft = (0, 100)
        wood = f"""Wood: {self.owner.nation.wood}"""
        self.wood_label = pygame_gui.elements.UILabel(relative_rect=wood_label_layout_rect,
                                                    text=wood, manager=Renderer.ui_manager,
                                                    container=self.background_panel,
                                                    anchors={'left': 'left',
                                                            'top':'top'})

        mineral_label_layout_rect = pygame.Rect(0, 0, 353, 20)
        mineral_label_layout_rect.topleft = (0, 125)
        mineral = f"""Minerals: {self.owner.nation.minerals}"""
        self.mineral_label = pygame_gui.elements.UILabel(relative_rect=mineral_label_layout_rect,
                                                    text=mineral, manager=Renderer.ui_manager,
                                                    container=self.background_panel,
                                                    anchors={'left': 'left',
                                                            'top':'top'})
    
        #CREATES BUILD PANEL AND BUTTONS
        build_panel_layout_rect = pygame.Rect(0, 0, WINDOW_SIZE.x-200, 200)
        build_panel_layout_rect.topleft = (200, 25)
        self.build_panel = pygame_gui.elements.UIPanel( relative_rect=build_panel_layout_rect,
                                                        manager=Renderer.ui_manager,
                                                        container=self.background_panel,
                                                        anchors={'top': 'top',
                                                                    'left':'left'},
                                                        starting_height=0)
        
        castle_btn_layout_rect = pygame.Rect(0, 0, 64, 64)
        castle_btn_layout_rect.topleft = (0, 0)
        
        self.castle_btn = pygame_gui.elements.UIButton( relative_rect=castle_btn_layout_rect,
                                                        text='',  # No text, just the image
                                                        manager=Renderer.ui_manager,
                                                        container = self.build_panel,
                                                        object_id=pygame_gui.core.ObjectID(class_id="@build_button",
                                                                                            object_id="#castle_button"))
        
    def update(self):
        super().update()
        if self.castle_btn.check_pressed():
            Player.building_placer = buildings.BuildingPlacer(buildings.Castle(Vec2(0, 0), self.owner.nation))
            EngineData.current_scene.spawn_object(Player.building_placer)
            self.castle_btn.pressed = False
            self.background_panel.kill()

    def open(self):
        super().open()
        self.__create_ui_elements()
    
    def update_information(self):
        if self.background_panel != None:
            self.power_label.set_text(f"""Power: {self.owner.nation.power}""")
            self.money_label.set_text(f"""Money: {self.owner.nation.money}""")
            self.honor_label.set_text(f"""Honor: {self.owner.nation.honor}""")
            self.wood_label.set_text(f"""Wood: {self.owner.nation.wood}""")
            self.mineral_label.set_text(f"""Minerals: {self.owner.nation.minerals}""")



class CastleInformationPanel(InformationPanel):
    def __init__(self, owner):
        super().__init__(owner)
        self.soldier_label = None
        self.name_label = None
    def __create_ui_elements(self):
        name_label_layout_rect = pygame.Rect(0, 0, 353, 30)
        name_label_layout_rect.topleft = (0, 0)
        name = f"""{self.type} Of {self.owner.nation.name}""" #Power: {len(self.owner.nation.occupied_points)
        self.type_label = pygame_gui.elements.UILabel(relative_rect=name_label_layout_rect,
                                                    text=name, manager=Renderer.ui_manager,
                                                    container=self.background_panel,
                                                    anchors={'left': 'left',
                                                            'top':'top'})
        soldier_label_layout_rect = pygame.Rect(0, 0, 353, 20)
        soldier_label_layout_rect.topleft = (0, 25)
        power = f"""Soldiers: {self.owner.soldiers}"""
        self.soldier_label = pygame_gui.elements.UILabel(relative_rect=soldier_label_layout_rect,
                                                    text=power, manager=Renderer.ui_manager,
                                                    container=self.background_panel,
                                                    anchors={'left': 'left',
                                                            'top':'top'})
    def open(self):
        super().open()
        self.__create_ui_elements()
    
    def update_information(self):
        if self.background_panel != None:
            self.power_label.set_text(f"""Soldiers: {self.owner.soldiers}""")


class CastleControlPanel(ControlPanel):
    def __init__(self, owner):
        super().__init__(owner)
        self.money_label = None
        self.wood_label = None
        self.mineral_label = None
        self.soldiers_label = None
        self.build_panel = None
        self.village_btn  = None
        self.soldiers_btn  = None


    def __create_ui_elements(self):
        #CREATES INFORMATION LABELS


        name_label_layout_rect = pygame.Rect(0, 0, 353, 30)
        name_label_layout_rect.topleft = (0, 0)
        name = f"""{self.owner.name}""" #Power: {len(self.owner.nation.occupied_points)
        self.name_label = pygame_gui.elements.UILabel(relative_rect=name_label_layout_rect,
                                                    text=name, manager=Renderer.ui_manager,
                                                    container=self.background_panel,
                                                    anchors={'left': 'left',
                                                            'top':'top'})



        money_label_layout_rect = pygame.Rect(0, 0, 353, 20)
        money_label_layout_rect.topleft = (0, 25)
        money = f"""Money: {self.owner.money}"""
        self.money_label = pygame_gui.elements.UILabel(relative_rect=money_label_layout_rect,
                                                    text=money, manager=Renderer.ui_manager,
                                                    container=self.background_panel,
                                                    anchors={'left': 'left',
                                                            'top':'top'})

        wood_label_layout_rect = pygame.Rect(0, 0, 353, 20)
        wood_label_layout_rect.topleft = (0, 50)
        wood = f"""Wood: {self.owner.wood}"""
        self.wood_label = pygame_gui.elements.UILabel(relative_rect=wood_label_layout_rect,
                                                    text=wood, manager=Renderer.ui_manager,
                                                    container=self.background_panel,
                                                    anchors={'left': 'left',
                                                            'top':'top'})

        mineral_label_layout_rect = pygame.Rect(0, 0, 353, 20)
        mineral_label_layout_rect.topleft = (0, 75)
        mineral = f"""Minerals: {self.owner.minerals}"""
        self.mineral_label = pygame_gui.elements.UILabel(relative_rect=mineral_label_layout_rect,
                                                    text=mineral, manager=Renderer.ui_manager,
                                                    container=self.background_panel,
                                                    anchors={'left': 'left',
                                                            'top':'top'})
        
        soldiers_label_layout_rect = pygame.Rect(0, 0, 353, 20)
        soldiers_label_layout_rect.topleft = (0, 125)
        soldiers = f"""Soldiers: {self.owner.soldiers}"""
        self.soldiers_label = pygame_gui.elements.UILabel(relative_rect=soldiers_label_layout_rect,
                                                    text=soldiers, manager=Renderer.ui_manager,
                                                    container=self.background_panel,
                                                    anchors={'left': 'left',
                                                            'top':'top'})
    
        #CREATES BUILD PANEL AND BUTTONS
        build_panel_layout_rect = pygame.Rect(0, 0, WINDOW_SIZE.x-200, 200)
        build_panel_layout_rect.topleft = (200, 25)
        self.build_panel = pygame_gui.elements.UIPanel( relative_rect=build_panel_layout_rect,
                                                        manager=Renderer.ui_manager,
                                                        container=self.background_panel,
                                                        anchors={'top': 'top',
                                                                    'left':'left'},
                                                        starting_height=0)
        
        village_btn_layout_rect = pygame.Rect(0, 0, 64, 64)
        village_btn_layout_rect.topleft = (0, 0)
        self.village_btn = pygame_gui.elements.UIButton( relative_rect=village_btn_layout_rect,
                                                        text='',  # No text, just the image
                                                        manager=Renderer.ui_manager,
                                                        container = self.build_panel,
                                                        object_id=pygame_gui.core.ObjectID(class_id="@build_button",
                                                                                            object_id="#village_button"))
        soldiers_btn_layout_rect = pygame.Rect(0, 0, 64, 64)
        soldiers_btn_layout_rect.topleft = (128, 0)
        self.soldiers_btn = pygame_gui.elements.UIButton( relative_rect=soldiers_btn_layout_rect,
                                                        text='',  # No text, just the image
                                                        manager=Renderer.ui_manager,
                                                        container = self.build_panel,
                                                        object_id=pygame_gui.core.ObjectID(class_id="@build_button",
                                                                                            object_id="#village_button"))
        
    def update(self):
        super().update()
        if self.village_btn.check_pressed():
            Player.building_placer = buildings.BuildingPlacer(buildings.Village(Vec2(0, 0), self.owner, self.owner.nation))
            EngineData.current_scene.spawn_object(Player.building_placer)
            self.village_btn.pressed = False
            self.background_panel.kill()

        if self.soldiers_btn.check_pressed():
            self.owner.spawn_soldiers(5, self.owner.pos+Vec2(0, round(self.owner.scale.y/2)+1))
            self.soldiers_btn.pressed = False
            self.background_panel.kill()

    def open(self):
        super().open()
        self.__create_ui_elements()
    
    def update_information(self):
        if self.background_panel != None:
            self.money_label.set_text(f"""Money: {self.owner.money}""")
            self.wood_label.set_text(f"""Wood: {self.owner.wood}""")
            self.mineral_label.set_text(f"""Minerals: {self.owner.minerals}""")
            self.soldiers_label.set_text(f"""Soldiers: {self.owner.soldiers}""")