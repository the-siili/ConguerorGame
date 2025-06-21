import noise
import numpy as np
from perlin_numpy import (
    generate_perlin_noise_2d, generate_fractal_noise_2d
)

from PIL import Image
import random
import pygame
import math
import opensimplex
from settings import MAP_SIZE
from amath import Vec2

def generate_map():
    seed = random.randint(0, 999999)
    print(seed)
    shape = MAP_SIZE
    frequency = 2
    octaves = 8
    persistence = 0.5
    lacunarity = 2

    world = generate_fractal_noise_2d((shape.x, shape.y), 
                                        (frequency*2, frequency), 
                                        octaves=octaves,
                                        persistence=persistence,
                                        lacunarity=lacunarity,
                                        tileable=(True, True))


    im = Image.new(mode="RGBA", size=(shape.x, shape.y))  
    a = np.asarray(im)
    pixelsNew = im.load()
    for y, line in enumerate(world):
        for x, v in enumerate(line):
            if world[y][x] < -0.14:
                pixelsNew[y,x] = (0, 0, 0, 0)
            elif -0.14 <= world[y][x] < -0.1:
                pixelsNew[y,x] = (148, 141, 101, 255)

            elif -0.1 <= world[y][x] < 0.1:
                pixelsNew[y,x] = random.choice([(73, 107, 22, 255), (70, 100, 18, 255)])
            elif 0.1 <= world[y][x] < 0.25:

                pixelsNew[y,x] = random.choice([(32, 92, 40, 255), (34, 56, 16, 255), (52, 56, 16, 255)])
            elif 0.25 <= world[y][x] < 0.35:
                pixelsNew[y,x] = random.choice([(73, 107, 22, 255), (70, 100, 18, 255)])
            
            elif 0.35 <= world[y][x] < 0.4:
                pixelsNew[y,x] = (78, 79, 77, 255)
            elif 0.4 <= world[y][x] < 0.45:
                pixelsNew[y,x] = (98, 89, 97, 255)
            elif 0.45 <= world[y][x] < 0.7:
                pixelsNew[y,x] = (78, 79, 77, 255)
                
            elif 0.7 <= world[y][x]:
                pixelsNew[y,x] = (209, 209, 209, 255)
    
    
    im.save("test.png")
    return pygame.image.fromstring(
        im.tobytes(), 
        im.size, 
        im.mode).convert_alpha()