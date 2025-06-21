import pygame
import random
from map_generator import generate_map
from object import Object
from renderer import Renderer
from amath import Vec2
from settings import COORD_MULTIPLIER, REAL_MAP_SIZE
from input import Input
from border_creation import create_borders
from nation import Nation
import game
from player import Player

class World(Object):
    def __init__(self):
        super().__init__(Vec2(0, 0), Vec2(0, 0))

        self.backround_sea = Renderer.surfaces["sea"]
        self.surface = generate_map()

        self.world_points = {}
        def match_color_to_terrain(color):
            if color == (0, 0, 0, 0): return "water"
            elif color == (148, 141, 101, 255): return "coast"
            elif color == (73, 107, 22, 255) or color == (70, 100, 18, 255): return "flatland"
            elif color == (32, 92, 40, 255) or color ==  (34, 56, 16, 255) or color ==  (52, 56, 16, 255): return "forest"
            elif color == (78, 79, 77, 255) or color == (98, 89, 97, 255): return "mountain"
            elif color == (209, 209, 209, 255): return "mountaintop"

        for y in range(REAL_MAP_SIZE.y):
            for x in range(REAL_MAP_SIZE.x):
                color = self.surface.get_at((x*COORD_MULTIPLIER, y*COORD_MULTIPLIER))[:4]
                terrain_type = match_color_to_terrain(color)
                self.world_points[Vec2(x, y)] = {"terrain_type":terrain_type,
                                                "current_object":None}


        self.sea_area = set()
        nations = create_borders()
        for nation in nations.keys():
            to_remove = set()
            for coord in nations[nation]["occupied_points"]:
                try:
                    if self.surface.get_at((round(coord.x*COORD_MULTIPLIER), round(coord.y*COORD_MULTIPLIER)))[:4] == (0, 0, 0, 0):
                        to_remove.add(coord)
                except: pass
            for coord in to_remove:
                self.sea_area.add(coord)
                nations[nation]["occupied_points"].remove(coord)

            nations[nation]["capitol_coords"] = random.choice(list(nations[nation]["occupied_points"]))
        
        self.nations = [Nation(self, key, value["occupied_points"], value["color"], value["capitol_coords"]) for key, value in nations.items()]
        for nation in self.nations: game.Game.spawn_object(nation)

        Player.initialize(random.choice(self.nations), self)

    def add_graphic_to_grid(x, y, graphic):
        self.grid[y][x][2] = graphic
    def remove_graphic_from_grid(x, y, graphic):
        self.grid[y][x][2] = 0

    def render(self):
        #screen.blit(self.surface, (self.x-self.game.cam_pos[0], self.y-self.game.cam_pos[1], 0, 0))
        Renderer.render_world_texture(self.backround_sea, self.pos, self.scale)
        Renderer.render_world_texture(self.surface, self.pos, self.scale)


