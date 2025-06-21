import noise
import numpy as np
from PIL import Image
import random
import pygame
import math
import opensimplex
from settings import MAP_SIZE

def generate_map():
    seed = random.randint(0, 999999)
    print(seed)
    shape = MAP_SIZE
    scale = 2.0
    octaves = 10
    persistence = 0.55
    lacunarity = 2.0

    world = np.zeros([shape.y, shape.x])

    max_n = max(shape)


    for x in range(shape.x):
        for y in range(shape.y):
            world[x][y] = noise.snoise2(x/max_n*scale, 
                                        y/max_n*scale,
                                        octaves=octaves, 
                                        persistence=persistence, 
                                        lacunarity=lacunarity, 
                                        #repeatx=shape.x, 
                                        #repeaty=shape.y,
                                        base=seed)


    im = Image.new(mode="RGBA", size=(shape.y, shape.x))  
    a = np.asarray(im)
    pixelsNew = im.load()
    for y, line in enumerate(world):
        for x, v in enumerate(line):
            if world[y][x] < -0.05:
                pixelsNew[x,y] = (0, 0, 0, 0)
            elif -0.05 <= world[y][x] < -0.03:
                pixelsNew[x,y] = (148, 141, 101, 255)

            elif -0.03 <= world[y][x] < 0.1:
                pixelsNew[x,y] = random.choice([(73, 107, 22, 255), (70, 100, 18, 255)])
            elif 0.1 <= world[y][x] < 0.16:

                pixelsNew[x,y] = random.choice([(32, 92, 40, 255), (34, 56, 16, 255), (52, 56, 16, 255)])
            elif 0.16 <= world[y][x] < 0.2:
                pixelsNew[x,y] = random.choice([(73, 107, 22, 255), (70, 100, 18, 255)])
            
            elif 0.2 <= world[y][x] < 0.25:
                pixelsNew[x,y] = (78, 79, 77, 255)
            elif 0.25 <= world[y][x] < 0.27:
                pixelsNew[x,y] = (98, 89, 97, 255)
            elif 0.27 <= world[y][x] < 0.4:
                pixelsNew[x,y] = (78, 79, 77, 255)
            elif 0.4 <= world[y][x] < 1.0:
                pixelsNew[x,y] = (209, 209, 209, 255)
    #im.save("test.png")
    return pygame.image.fromstring(
        im.tobytes(), 
        im.size, 
        im.mode).convert_alpha()