import pygame

from input import Input
import world
from object import Object
from renderer import Renderer, Camera
from player import Player

from settings import MAP_SIZE, WINDOW_SIZE, COORD_MULTIPLIER, WINDOW_FLAGS
from amath import Vec2

#HANDLES THE GAME ISNTANCE AND GAME LOOP
#DOESNT DO MUCH, BUT MAKES SURE THE GAME CAN BE RESET AT ANY MOMENT
#instance
class Game():

    def __init__(self):
        self.objects = []
        #8 render layers exist
        self.render_layers = [[],[],[],[],[],[],[],[]]
        self.delta_time = 0

    def start(self):
        self.spawn_object(world.World())
        for obj in self.objects:
            obj.start()

    def update(self):
        Player.update()
        for obj in self.objects:
            obj.update()

    def render(self):
        for layer in self.render_layers:
            for obj in layer:
                obj.render()
        Player.render()
        
        
        
    def spawn_object(self, obj):
        self.objects.append(obj)
        if obj.render_layer < 0 or obj.render_layer >= len(self.render_layers):
            raise ValueError(f"Invalid render layer not between {0, len(self.render_layers)}: {obj}")
        self.render_layers[obj.render_layer].append(obj)

    def remove_object(self, obj):
        try:
            self.objects.remove(obj)
            self.render_layers[obj.render_layer].remove(obj)
        except:print("ERROR: Trying to remove object that doesnt exist in the scene")

