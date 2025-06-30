import pygame_gui
import pygame
from input import Input
from renderer import Renderer, Camera
from amath import Vec2
import buildings
from settings import WINDOW_SIZE
import soldiers 

#HANDLES THE PLAYER FUNCTIONS
#THIS IS ONLY AN INITIATOR FOR THE GAME FUNCTIONS
#BUT ALL NATION ACTIONS FOR EXAMPLE BUILDING SHOULD BE INSIDE THE NATION CLASS


#global
class Player():
    nation = None
    world = None
    in_action = False

    active_ui_panel = None

    building_placer = None

    selected_soldiers = None

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

        #HANDLE CAMERA MOVEMENT THROUGH MOUSE
        if Input.mouse_button_down("right"):
            Camera.move(Input.mouse_world_movement())

        if self.building_placer != None: return

        #HANDLES OPENING BUILDING AND OBJECT MENUS AND INFO PANELS
        if Input.mouse_button_pressed("left"):
            if self.selected_soldiers != None:
                self.selected_soldiers.set_destination(Input.mouse_world_pos_rounded())
                self.selected_soldiers = None
                self.in_action = False



            point = self.world.world_points[Input.mouse_world_pos_rounded()]
            if  point["current_object"] != None and not self.in_action:
                if issubclass(type(point["current_object"]) ,buildings.Building) and point["current_object"].finished:
                    if self.active_ui_panel != None:
                        self.active_ui_panel.close()

                    self.active_ui_panel = point["current_object"].control_panel if point["current_object"].nation == self.nation else point["current_object"].information_panel
                    self.active_ui_panel.open()
                elif type(point["current_object"]) == soldiers.Soldiers:
                    self.selected_soldiers = point["current_object"]
                    self.in_action = True

        
            


        #SHOWS INFORMATION ABOUT THE OBJECT THAT THE CURSOR IS HOVERING OVER
        point = self.world.world_points[Input.mouse_world_pos_rounded()]

        if point["current_object"] != None:
            if type(point["current_object"]) is buildings.Castle or \
                type(point["current_object"]) is buildings.Village or\
                type(point["current_object"]) is soldiers.Soldiers:
                self.info_text.set_text(point["current_object"].name)
            else:
                self.info_text.set_text(point["current_object"].type_str)
        else:
            self.info_text.set_text(point["terrain_type"])



    @classmethod
    def render(self):
        #RENDERS THE GRID CIRCLES FOR THE MOUSE
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

            print(self.world.world_points[mouse_pos]["speed"])
        
        self.nation.render_border()
