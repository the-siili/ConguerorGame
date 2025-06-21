import pygame
import random
from object import Object
from renderer import Renderer
from amath import Vec2
from settings import REAL_MAP_SIZE, COORD_MULTIPLIER
from input import Input
from castle import Castle
import game

class Nation(Object):
    def __init__(self, world, id, occupied_points, color, capitol_coords):
        self.world = world
        self.id = id
        self.occupied_points = occupied_points
        self.color = color
        self.capitol_coords = capitol_coords


        self.render_layer = 1

        def find_border_coords():

            border_points = set()
            for i in self.occupied_points:
                if (i + Vec2(0, 1) not in self.occupied_points and i.y+1 in range(1, REAL_MAP_SIZE.y))  or\
                    (i + Vec2(0, -1) not in self.occupied_points and i.y -1 in range(1, REAL_MAP_SIZE.y)) or\
                    (i + Vec2(1, 0) not in self.occupied_points and i.x + 1 in range(1, REAL_MAP_SIZE.x)) or\
                    (i + Vec2(-1, 0) not in self.occupied_points and i.x -1 in range(1, REAL_MAP_SIZE.x)):# or\
                    #(i + Vec2(1, 1) not in self.occupied_points and i.y + 1 in range(1, REAL_MAP_SIZE.y) and i.x + 1 in range(1, REAL_MAP_SIZE.x)) or\
                    #(i + Vec2(1, -1) not in self.occupied_points and i.y - 1 in range(1, REAL_MAP_SIZE.y) and i.x + 1 in range(1, REAL_MAP_SIZE.x)) or\
                    #(i + Vec2(-1, -1) not in self.occupied_points and i.y - 1 in range(1, REAL_MAP_SIZE.y) and i.x - 1 in range(1, REAL_MAP_SIZE.x)) or\
                    #(i + Vec2(-1, 1) not in self.occupied_points  and i.y + 1 in range(1, REAL_MAP_SIZE.y) and i.x - 1 in range(1, REAL_MAP_SIZE.x)):
                    border_points.add(i)
            return border_points

        self.border_points = find_border_coords()


        self.castles = set()

        self.build_castle(random.choice(list(self.occupied_points)))

    
    def render(self):
        def render_border():
            lines = set()
            for coord in self.border_points:
                Renderer.render_world_circle(coord, 0.80, self.color, 0)

                calc_vectors = [Vec2(0, -1), 
                                Vec2(1, -1),
                                Vec2(1, 0),
                                Vec2(1, 1), 
                                Vec2(0, 1),
                                Vec2(-1, 1), 
                                Vec2(-1, 0), 
                                Vec2(-1, -1)]
                for vec in calc_vectors:
                    if coord+vec in self.border_points and (coord+vec, coord) not in lines:
                        Renderer.render_world_line(coord, coord+vec, self.color, 2)
                        lines.add((coord, coord+vec))

                        #break

        if Input.mouse_world_pos_rounded() in self.occupied_points:
            render_border()

        Renderer.render_world_texture(Renderer.surfaces["capitol"], self.capitol_coords-Vec2(0.5, 0.5), Vec2(1, 1))
    

    def build_castle(self, coords: Vec2):
        if coords in self.occupied_points:
            new_castle = Castle(coords)
            self.castles.add(new_castle)
            self.world.world_points[coords]["current_object"] = new_castle
            game.Game.spawn_object(new_castle)