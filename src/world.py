import pygame
import random

from object import Object
from renderer import Renderer
from amath import Vec2
from settings import COORD_MULTIPLIER, REAL_MAP_SIZE, MAP_SIZE, NATION_AMOUNT, MAP_COLORS
from input import Input
from border_creation import create_borders
from nation import Nation
import game
from player import Player
from engine_data import EngineData
import itertools
#FIX!!!
#IF KNGDOM OF VALOR AKA PLAYERS KINGDOM DOESNT GAIN ANY ARE THE PLAYER WILL BE ASINGE
#THE WRONG NATION AND THATS BAD

#instance
class World(Object):
    def __init__(self):
        super().__init__(Vec2(0, 0), Vec2(0, 0))

        self.backround_sea = Renderer.get_surface("sea")
        self.surface = Renderer.get_surface("land")
        self.world_points = {}
        def match_color_to_terrain(color):
            if color in itertools.chain.from_iterable(list(MAP_COLORS["wetland"].values())): return "wetland"
            elif color in itertools.chain.from_iterable(list(MAP_COLORS["planes"].values())): return "planes"
            elif color in itertools.chain.from_iterable(list(MAP_COLORS["forest"].values())): return "forest"
            elif color in itertools.chain.from_iterable(list(MAP_COLORS["mountain1"].values()) +list(MAP_COLORS["mountain2"].values()) +list(MAP_COLORS["mountain3"].values())): return "mountain"
            elif color in itertools.chain.from_iterable(list(MAP_COLORS["mountaintop"].values())): return "mountaintop"
            else: return "water"

            #print(self.surface.get_width(), self.surface.get_height())
        for y in range(1, REAL_MAP_SIZE.y):
            for x in range(1, REAL_MAP_SIZE.x):
                color = self.surface.get_at((x*COORD_MULTIPLIER, y*COORD_MULTIPLIER))[:4]
                terrain_type = match_color_to_terrain(color)
                #owner = [nation.id for nation in self.nations if Vec2(x, y) in nation.occupied_points][0] if Vec2(x, y) not in self.sea_area else None

                self.world_points[Vec2(x, y)] = {"terrain_type":terrain_type,
                                                "current_object":None,
                                                "nation":None,
                                                }

        self.sea_area = set()
        nations = create_borders(REAL_MAP_SIZE, random.randint(NATION_AMOUNT.x, NATION_AMOUNT.y+1))
        for nation in list(nations.keys()):
            to_remove = set()
            for coord in nations[nation]["occupied_points"]:
                try:
                    if self.surface.get_at((round(coord.x*COORD_MULTIPLIER), round(coord.y*COORD_MULTIPLIER)))[:4] == (0, 0, 0, 0):
                        to_remove.add(coord)
                except: pass
            for coord in to_remove:
                self.sea_area.add(coord)
                nations[nation]["occupied_points"].remove(coord)

            #sometimes the nations fail to gain any land space, in which case they have to be skipped
            if len(nations[nation]["occupied_points"]) == 0:
                del nations[nation]
                continue
        self.nations = []
        for key, value in nations.items():
            new_nation = Nation(self, key, value["occupied_points"], value["color"], value["name"])
            if new_nation.capitol != None:
                self.nations.append(new_nation)
        
        for nation in self.nations: EngineData.current_scene.spawn_object(nation)




        Player.initialize(self.nations[0], self)

    def add_graphic_to_grid(x, y, graphic):
        self.grid[y][x][2] = graphic
    def remove_graphic_from_grid(x, y, graphic):
        self.grid[y][x][2] = 0

    def render(self):
        #screen.blit(self.surface, (self.x-self.game.cam_pos[0], self.y-self.game.cam_pos[1], 0, 0))
        Renderer.render_world_texture("sea", self.pos, self.scale)
        Renderer.render_world_texture("land", self.pos, self.scale)
        

