import pygame_gui
import pygame
from object import Object
from renderer import Renderer
from amath import Vec2
from input import Input
import random

from settings import BUILDING_SIZES, WINDOW_SIZE, BUILDING_COSTS, CASTLE_NAMES
from engine_data import EngineData

from ui_panels import CapitolControlPanel, CapitolInformationPanel, CastleControlPanel

from player import Player
from soldiers import Soldiers

#INFORMATION PANELS SHOW ENEMY NATION BUILDINGS INFORMATION
#CONTROL PANELS SHOW PLAYERS NATION BUILDINGS INFO AND CONTROLS



class Building(Object):
    def __init__(self, pos, scale, nation, texture_key, information_panel, control_panel, build_time, production_time):
        super().__init__(pos, scale)
        self.nation = nation
        self.render_layer = 2
        self.occupied_points = set()
        self.texture_key = texture_key

        self.water_side = False

        self.information_panel = information_panel
        self.control_panel = control_panel



        self.type_str = "NULL"
        self.__build_start_time = EngineData.game_time
        self.__build_time = build_time

        self.finished = False

        self.production_time = production_time
        self.__last_production_time = EngineData.game_time+self.__build_time

    def start(self):
        for y in range(round(-self.scale.y/2), int(self.scale.y/2)+1):
            for x in range(round(-self.scale.x/2), int(self.scale.x/2)+1):
                self.occupied_points.add(self.pos+Vec2(x, y))
                self.nation.world.world_points[self.pos+Vec2(x, y)]["current_object"] = self

                #for ny in range(-1, 2):
                    #for nx in range(-1, 2):
                        #if self.pos+Vec2(x, y)+Vec2(nx, ny) in self.nation.world.world_points:
                            #if self.nation.world.world_points[self.pos+Vec2(x, y)+Vec2(nx, ny)]["terrain_type"] == "water":
                                #self.nation.world.path_finding_grid[self.pos+Vec2(x, y)].append((self.pos+Vec2(x, y)+Vec2(nx, ny), 0.5))


    def update(self):
        
        if not self.finished and EngineData.game_time - self.__build_start_time >= self.__build_time:
            self.finished = True
        if not self.finished: return
        
        if self.information_panel.is_open:
            self.information_panel.update()
        if self.control_panel.is_open:
            self.control_panel.update()
        
        if EngineData.game_time-self.__last_production_time >= self.production_time:
            self.produce()
            self.__last_production_time = EngineData.game_time

    def render(self):
        if self.finished: 
            Renderer.render_world_texture(self.texture_key, self.pos, self.scale, centered=True)
        else:
            Renderer.render_world_texture("Construction", self.pos, self.scale, centered=True)
        
        if Input.mouse_world_pos_rounded() in self.occupied_points:
            for i in self.occupied_points:
                Renderer.render_world_circle(i, 0.4, self.nation.color, 1)
    def open_info(self):
        pass
    def close_info(self):
        pass
    def destroy(self):
        pass

    def produce(self):
        self.update_information()

    def update_information(self):
        self.information_panel.update_information()
        self.control_panel.update_information()

class BuildingPlacer(Object):
    def __init__(self, building):
        super().__init__(Input.mouse_world_pos_rounded(), building.scale)
        self.can_place = False
        self.render_layer = 3
        self.building = building
    
    def update(self):
        #THE ORDER OF THESE 2 ARE IMPORTANT
        #IF YOU CAN PLACE THE THING AFTER MOVING ON LOW FRAME RATE MIGHT BE
        #POSSIBLE TO PLACE OUTSIDE NATION BORDERS
        #THIS IS BECUASE THE "can place" VARIABLE IS SET IN RENDER AFTER THE UPDATE
        if Input.mouse_button_pressed("left") and self.can_place:
            self.build_building()
        self.pos = Input.mouse_world_pos_rounded()

        #THIS MUST BE AT THE END OF THE UPDATE BECAUSE OF PREVIUS COMMENT
        self.can_place = True


    def render(self):
        #RENDERS THE GRID CIRCLES FOR THE MOUSE
        mouse_pos = Input.mouse_world_pos_rounded()
        for y in range(round(-self.scale.y/2), int(self.scale.y/2)+1):
            for x in range(round(-self.scale.x/2), int(self.scale.x/2)+1):
                vec = Vec2(x, y)
                if mouse_pos+vec in self.building.nation.occupied_points and self.building.nation.world.world_points[mouse_pos+vec]["current_object"] == None:
                    Renderer.render_world_circle(mouse_pos+vec, 0.3, (0, 255, 0), 0)
                else:
                    self.can_place = False
                    Renderer.render_world_circle(mouse_pos+vec, 0.3, (255, 0, 0), 0)



    def build_building(self):
        if self.building.nation.money-BUILDING_COSTS[self.building.type_str]["money"] >= 0 and\
        self.building.nation.wood-BUILDING_COSTS[self.building.type_str]["wood"] >= 0 and\
        self.building.nation.minerals-BUILDING_COSTS[self.building.type_str]["minerals"] >= 0:

            self.building.pos = Input.mouse_world_pos_rounded()
            EngineData.current_scene.spawn_object(self.building)
            self.building.start()

        #removes self
        Player.building_placer = None
        EngineData.current_scene.remove_object(self)

class Capitol(Building):
    def __init__(self, pos, nation):
        super().__init__(pos, Vec2(BUILDING_SIZES["Capitol"], BUILDING_SIZES["Capitol"]), nation, "Capitol", \
            CapitolInformationPanel(self), CapitolControlPanel(self), 0, 5)
        self.type_str = "Capitol"
    
    def produce(self):
        #print(self.nation.name,": produced")
        self.nation.money += 100
        self.nation.wood += 50
        self.nation.minerals += 50
        #the parent class handles updating the UI
        super().produce()

class Castle(Building):
    def __init__(self, pos, nation):
        super().__init__(pos, Vec2(BUILDING_SIZES["Castle"], BUILDING_SIZES["Castle"]), nation, "Castle", \
            CapitolInformationPanel(self), CastleControlPanel(self), 1.0, 5)
        self.type_str = "Castle"
        self.name = f"Castle Of Sir. {random.choice(CASTLE_NAMES)}"
        self.money = 0
        self.wood = 0
        self.minerals = 0

        self.soldiers = 0

        self.production_rate = 1
    
    def start(self):
        super().start()
        self.nation.money -= BUILDING_COSTS["Castle"]["money"]
        self.nation.wood -= BUILDING_COSTS["Castle"]["wood"]
        self.nation.minerals -= BUILDING_COSTS["Castle"]["minerals"]
        self.soldiers = 10
    
    def produce(self):
        self.add(-int(10*self.production_rate*1.2), 
                -int(10*self.production_rate*1.2),
                -int(10*self.production_rate*1.2),
                int(5*self.production_rate))
        super().produce()
    
    def add(self, money=0, wood=0, minerals=0, soldiers=0):
        self.money += money
        self.wood += wood
        self.minerals += minerals
        self.soldiers += soldiers
        
        #TAKES RESOURCES FROM THE NATION IF CANT AFFORD BY SELF
        if self.money < 0:
            self.nation.money -= abs(self.money)
            self.money = 0
        if self.wood < 0:
            self.nation.wood -= abs(self.wood)
            self.wood = 0
        if self.minerals < 0:
            self.nation.minerals -= abs(self.minerals)
            self.minerals = 0
        self.update_information()
        self.nation.capitol.update_information()


    def spawn_soldiers(self, amount, destination):
        self.soldiers -= amount
        fixed_amount = amount
        if self.soldiers < 0:
            fixed_amount = amount-abs(self.soldiers)
            self.soldiers = 0

        EngineData.current_scene.spawn_object(Soldiers(self.pos+Vec2(0, round(self.scale.y/2)+1), fixed_amount, self.nation, destination))

class Village(Building):
    def __init__(self, pos, castle, nation):
        super().__init__(pos, Vec2(BUILDING_SIZES["Village"], BUILDING_SIZES["Village"]), nation, "Village", \
            CapitolInformationPanel(self), CastleControlPanel(self), 10.0, 5)
        self.castle = castle
        self.type_str = "Village"
        self.name = f"Village Of {self.castle.name[10:]}"
        self.money = 0
        self.wood = 0
        self.minerals = 0

        self.soldiers = 0

        self.production_rate = 1
    
    def start(self):
        super().start()
        self.castle.add(
            -BUILDING_COSTS["Village"]["money"],
            -BUILDING_COSTS["Village"]["wood"],
            -BUILDING_COSTS["Village"]["minerals"]
        )

        self.soldiers = 5


    def produce(self):
        self.castle.add(10, 10, 10)

        super().produce()