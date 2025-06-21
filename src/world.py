import pygame
import random
from map_generator import generate_map
from object import Object
from renderer import Renderer
from amath import Vec2
from settings import COORD_MULTIPLIER
from input import Input
from border_creation import create_borders
from nation import Nation
import game

class World(Object):
    def __init__(self):
        super().__init__(Vec2(0, 0), Vec2(0, 0))
        self.backround_sea = Renderer.surfaces["sea"]
        self.surface = generate_map()
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
        
        self.nations = [Nation(key, value["occupied_points"], value["color"], value["capitol_coords"]) for key, value in nations.items()]
        for nation in self.nations: game.Game.spawn_object(nation)


    def add_graphic_to_grid(x, y, graphic):
        self.grid[y][x][2] = graphic
    def remove_graphic_from_grid(x, y, graphic):
        self.grid[y][x][2] = 0

    def render(self):
        #screen.blit(self.surface, (self.x-self.game.cam_pos[0], self.y-self.game.cam_pos[1], 0, 0))
        Renderer.render_world_texture(self.backround_sea, self.pos, self.scale)
        Renderer.render_world_texture(self.surface, self.pos, self.scale)


