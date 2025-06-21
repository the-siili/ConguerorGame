import pygame
from object import Object
from renderer import Renderer
from amath import Vec2
from settings import REAL_MAP_SIZE


class Nation(Object):
    def __init__(self, id, occupied_points, color, capitol_coords):
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
                    (i + Vec2(-1, 0) not in self.occupied_points and i.x -1 in range(1, REAL_MAP_SIZE.x)) or\
                    (i + Vec2(1, 1) not in self.occupied_points and i.y + 1 in range(1, REAL_MAP_SIZE.y) and i.x + 1 in range(1, REAL_MAP_SIZE.x)) or\
                    (i + Vec2(1, -1) not in self.occupied_points and i.y - 1 in range(1, REAL_MAP_SIZE.y) and i.x + 1 in range(1, REAL_MAP_SIZE.x)) or\
                    (i + Vec2(-1, -1) not in self.occupied_points and i.y - 1 in range(1, REAL_MAP_SIZE.y) and i.x - 1 in range(1, REAL_MAP_SIZE.x)) or\
                    (i + Vec2(-1, 1) not in self.occupied_points  and i.y + 1 in range(1, REAL_MAP_SIZE.y) and i.x - 1 in range(1, REAL_MAP_SIZE.x)):
                    border_points.add(i)
            return border_points

        self.border_points = find_border_coords()


    
    def render(self):
        for coord in self.border_points:
            Renderer.render_world_circle(coord, 0.25, self.color, 0)
            for i in range(-1, 2, 2):
                if coord+Vec2(0, i) in self.border_points:
                    Renderer.render_world_line(coord, coord+Vec2(0, i), self.color, 3)
                if coord+Vec2(i, 0) in self.border_points:
                    Renderer.render_world_line(coord, coord+Vec2(i, 0), self.color, 3)
        Renderer.render_world_texture(Renderer.surfaces["capitol"], self.capitol_coords-Vec2(0.5, 0.5), Vec2(1, 1))
    