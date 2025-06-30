import noise
import numpy as np
import time

from numba import jit

from perlin_numpy import (
    generate_perlin_noise_2d, generate_fractal_noise_2d
)

from PIL import Image
import random
import pygame
import math
import opensimplex
from amath import Vec2



def generate_map(map_size, map_colors):
    seed = random.randint(0, 999999)
    print("map being generated")
    shape = map_size
    frequency = 2
    octaves = 8
    persistence = 0.7
    lacunarity = 2
    
    # #DEBBUGGING ONLY
    # im = Image.open(r"src/res/test_map.png")
    # return pygame.image.fromstring(
    #     im.tobytes(), 
    #     im.size, 
    #     im.mode).convert_alpha()
    # #DEBBUGGING ONÖLY

    t = time.time()
    np.random.seed(random.randint(0, 999999))
    #GENERATE FRACTAL NOISE FOR THE BASE WORLD
    world = generate_fractal_noise_2d((shape.x, shape.y), 
                                        (frequency*2, frequency), 
                                        octaves=octaves,
                                        persistence=persistence,
                                        lacunarity=lacunarity,
                                        tileable=(False, False))
    #GENERATE FRACTAL NOISE FOR THE GRADIENT MASK 
    #USED TO MAKE THE CONTINENT BORDERS MORE NATURAL
    mask = generate_fractal_noise_2d((shape.x, shape.y), 
                                        (frequency*2, frequency), 
                                        octaves=6,
                                        persistence=persistence,
                                        lacunarity=lacunarity,
                                        tileable=(False, False))
    #print("Noise generation: ", time.time()-t)

    #t = time.time()
    #CIRCLE GRADIENT TO MAKE SURE THE EDGES OF THE MAP ARE ONLY WATER
    grad = circular_gradient(shape, radius=1, inner=0, outer=2, gamma=10)


    color_line = [random.randint(-10, 10) for i in range(shape.y)]


    im = Image.new(mode="RGBA", size=(shape.x, shape.y))  
    a = np.asarray(im)
    pixelsNew = im.load()
    #LOOPING THROUGH ALL THE PIXELS IN THE IMAGE
    for y, line in enumerate(world):
        for x, v in enumerate(line):
            #ADDING TO GETHER THE PIXELS BASE WORLD, AND MASK GRADIENT TO MAKE A CONTINENT
            world[y][x] = (world[y][x]+1)/2+(mask[y][x]-grad[x][y])

            

            #DEBBUGGING
            t = time.time()
            xm = x+math.sin(x*y)*10
            ym = math.sin(y/20)*8

            #CHOOSES THE BIOM OF THE PIXEL
            biome = "normal"
            if  xm < (shape.y*0.2)+ym \
                or xm > (shape.y*0.80)+ym:
                biome = "tundra"
            elif (shape.y*0.4)+ym < xm < shape.y*0.6+ym:
                biome = "desert"

            #CHOOSES THE CORRECT TERRAIN COLOR FOR THE PIXEL using the give map color set
            #USUALLY THE MAP COLOR IS TAKEN FROM "settings.MAP_COLORS"
            if world[y][x] < 0.3: #or mask[y, x] == False:
                pixelsNew[y,x] = (0, 0, 0, 0)
            elif 0.3 <= world[y][x] < 0.37:
                pixelsNew[y,x] = random.choice(map_colors["wetland"][biome])

            elif 0.37 <= world[y][x] < 0.47:
                pixelsNew[y,x] = random.choice(map_colors["planes"][biome])
            elif 0.47 <= world[y][x] < 0.75:
                pixelsNew[y,x] = random.choice(map_colors["forest"][biome])
            elif 0.75 <= world[y][x] < 1:
                pixelsNew[y,x] = random.choice(map_colors["planes"][biome])
            
            elif 1 <= world[y][x] < 1.2:
                pixelsNew[y,x] = random.choice(map_colors["mountain1"][biome])
            elif 1.2 <= world[y][x] < 1.3:
                pixelsNew[y,x] = random.choice(map_colors["mountain2"][biome])
            elif 1.3 <= world[y][x] < 1.4:
                pixelsNew[y,x] = random.choice(map_colors["mountain3"][biome])
                
            elif 1.4 <= world[y][x]:
                pixelsNew[y,x] = random.choice(map_colors["mountaintop"][biome])

    #print("Rest: ", time.time()-t)
    #im.save("test_map.png")
    #print("map fully generated")
    return pygame.image.fromstring(
        im.tobytes(), 
        im.size, 
        im.mode).convert_alpha()

def circular_gradient(size, inner=0.0, outer=1.0, radius=None, gamma=1.0):
    """
    Generate adjustable circular (radial) gradient.
    
    Args:
        size    : int, image will be size × size pixels.
        inner   : float or tuple, value/color at the center.
        outer   : float or tuple, value/color at the edges.
        radius  : float, maximum radius (in normalized coords). Defaults to 1.0.
        gamma   : float, exponent for fall-off curve (>0), controls sharpness.

    Returns:
        numpy.ndarray with shape:
          – (size, size) for grayscale
          – (size, size, 3) for RGB
          – (size, size) for alpha mask when alpha=True
    """
    ax = np.linspace(-1, 1, size.x)
    ay = np.linspace(-1, 1, size.y)
    xx, yy = np.meshgrid(ax, ay)
    r = np.sqrt(xx**2 + yy**2)
    maxr = radius if radius is not None else 1.0
    r = np.clip(r / maxr, 0, 1)
    # Apply gamma curve
    r = r ** gamma

    return r * outer + (1 - r) * inner


