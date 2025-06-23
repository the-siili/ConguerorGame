import pygame
import random
import math
from object import Object
from renderer import Renderer
from amath import Vec2
from settings import REAL_MAP_SIZE, COORD_MULTIPLIER, MAP_SIZE, BUILDING_SIZES
from input import Input
from buildings import Capitol
import game
from engine_data import EngineData

#instance
class Nation(Object):
    def __init__(self, world, id, occupied_points, color, name):
        self.world = world
        self.id = id
        self.occupied_points = occupied_points
        self.color = color
        self.name = name
        border_surface = pygame.Surface(tuple(MAP_SIZE), pygame.SRCALPHA).convert_alpha()
        border_surface.fill((0, 0, 0, 0))
        Renderer.add_surface(f"border{self.id}", border_surface)
        self.render_layer = 1

        def find_border_coords():

            border_points = set()
            water_border_points = set()
            check_vecs = [Vec2(0, 1), Vec2(0, -1), Vec2(1, 0), Vec2(-1, 0)]
            for i in self.occupied_points:
                for vec in check_vecs:
                    if i + vec not in self.occupied_points and i+vec in self.world.world_points.keys():
                        if self.world.world_points[i+vec]["terrain_type"] == "water":
                            water_border_points.add(i)
                        border_points.add(i)

            return border_points, water_border_points

        
        self.border_points, self.water_border_points = find_border_coords()
        self.update_borders()

        def generate_capitol():
            for point in self.occupied_points:
                possible_place = True
                for y in range(int(-BUILDING_SIZES["capitol"]/2), int(BUILDING_SIZES["capitol"]/2)+1):
                    for x in range(int(-BUILDING_SIZES["capitol"]/2), int(BUILDING_SIZES["capitol"]/2)+1):
                        if point+Vec2(x, y) not in self.occupied_points:
                            possible_place = False
                            break
                    if possible_place == False:
                        break

                if possible_place:
                    return Capitol(point, self)    
            return None

        self.capitol = generate_capitol()

            #if nation doesnt have enough space for a capitol the nation creation in world will not add it to the game
        #this will be triggered if after the next for loop the nations capitol is still "None"
        if self.capitol == None:
            return

        EngineData.current_scene.spawn_object(self.capitol)
        for point in self.occupied_points:
            self.world.world_points[point]["nation"] = self
        
        #NATION ATTRIBUTES
        self.money = 1000
        self.wood = 1000
        self.minerals = 1000
        self.honor = 1000
        self.power = len(self.occupied_points)

        
    
    def render(self):
        if Input.mouse_world_pos_rounded() in self.occupied_points:
            self.render_border()
    
    def render_border(self):
        Renderer.render_world_texture(f"border{self.id}", Vec2(0, 0), REAL_MAP_SIZE)

    def update_borders(self):
        lines = set()
        for coord in self.border_points:
            #Renderer.render_world_circle(coord, 0.40, self.color, 0)

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
                    pygame.draw.aaline(Renderer.get_surface(f"border{self.id}"), self.color, tuple(coord*COORD_MULTIPLIER), tuple((coord+vec)*COORD_MULTIPLIER),  8)
                    lines.add((coord, coord+vec))
        Renderer.update_surface(f"border{self.id}")
        #update the power stat
        self.power = len(self.occupied_points)


    def build_castle(self, coords: Vec2):
        if coords in self.occupied_points:
            new_castle = Castle(coords)
            self.castles.add(new_castle)
            self.world.world_points[coords]["current_object"] = new_castle
            
            EngineData.current_scene.spawn_object(new_castle)