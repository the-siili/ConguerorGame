import noise
import numpy as np
import time
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
    
    #DEBBUGGING ONLY
    im = Image.open(r"src/res/test_map.png")
    return pygame.image.fromstring(
        im.tobytes(), 
        im.size, 
        im.mode).convert_alpha()
    #DEBBUGGING ONÖLY

    t = time.time()
    np.random.seed(random.randint(0, 999999))
    world = generate_fractal_noise_2d((shape.x, shape.y), 
                                        (frequency*2, frequency), 
                                        octaves=octaves,
                                        persistence=persistence,
                                        lacunarity=lacunarity,
                                        tileable=(False, False))
    
    mask = generate_fractal_noise_2d((shape.x, shape.y), 
                                        (frequency*2, frequency), 
                                        octaves=6,
                                        persistence=persistence,
                                        lacunarity=lacunarity,
                                        tileable=(False, False))
    #print("Noise generation: ", time.time()-t)

    #t = time.time()

    grad = circular_gradient(shape, radius=1, inner=0, outer=2, gamma=10)


    color_line = [random.randint(-10, 10) for i in range(shape.y)]


    im = Image.new(mode="RGBA", size=(shape.x, shape.y))  
    a = np.asarray(im)
    pixelsNew = im.load()
    for y, line in enumerate(world):
        for x, v in enumerate(line):
            world[y][x] = (world[y][x]+1)/2+(mask[y][x]-grad[x][y])

            biome = "normal"

            xm = x+math.sin(x*y)*10
            ym = math.sin(y/20)*8
            t = time.time()
            if  xm < (shape.y*0.2)+ym \
                or xm > (shape.y*0.80)+math.sin(y/10)*10:
                biome = "tundra"
            elif (shape.y*0.4)+ym < xm < shape.y*0.6+ym:
                biome = "desert"

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




def generate_blobby_image(
    size=Vec2(256, 256),
    num_blobs=10,
    fade_strength=1,
    blob_size_range=(0.3, 0.7),
    intensity_range=(-1, 5),
    center_bias=0.9,
    global_mask_strength=1,
    blob_shape="circle",
    jaggedness=0.01,  # Controls how jagged the edges are
    seed=None
):
    """
    Generate a grayscale image with semi-random radial blobs, where brightness fades to 0 at the edges of the image.
    Args:
        size : int, size x size output.
        num_blobs : int, number of radial blobs.
        fade_strength: float, controls falloff sharpness of blobs.
        blob_size_range: tuple (min_radius, max_radius), range of blob sizes.
        intensity_range: tuple (min_intensity, max_intensity), range of blob intensities.
        center_bias: float, controls how much blob centers are biased toward the center.
        global_mask_strength: float, controls falloff sharpness of the global radial mask.
        blob_shape: str, shape of the blobs ("circle" or "square").
        jaggedness: float, controls how jagged the edges are.
        seed: int, random seed for reproducibility.
    Returns:
        numpy.ndarray of shape (size, size), values in [0, 1] with edges = 0.
    """
    if seed is not None:
        np.random.seed(seed)

    if global_mask_strength is None:
        global_mask_strength = fade_strength

    image = np.zeros((size.y, size.x), dtype=np.float32)
    ax = np.linspace(-1, 1, size.x)
    ay = np.linspace(-1, 1, size.y)
    xx, yy = np.meshgrid(ax, ay)

    # Initialize Perlin noise for jagged edges
    noise = generate_fractal_noise_2d((512, 512), 
                                        (1, 1), 
                                        octaves=8,
                                        persistence=0.5,
                                        lacunarity=2,
                                        tileable=(False, False))

    for _ in range(num_blobs):
        # Random blob center, more biased toward center
        cx, cy = np.random.uniform(-center_bias, center_bias, size=2)
        radius = np.random.uniform(*blob_size_range)
        intensity = np.random.uniform(*intensity_range)

        # Compute radial distance from blob center
        if blob_shape == "circle":
            r = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
        elif blob_shape == "square":
            r = np.maximum(np.abs(xx - cx), np.abs(yy - cy))
        else:
            raise ValueError("blob_shape must be 'circle' or 'square'")

        # Add noise to the radial distance to make edges jagged
        noise_map = np.zeros_like(r)
        for i in range(size.x):
            for j in range(size.y):
                noise_map[j, i] = noise[j // size.x, i // size.y]
        r = r * (1 + jaggedness * noise_map)

        r = np.clip(r / radius, 0, 1)
        r = r ** fade_strength
        blob = (1 - r) * intensity
        image = np.maximum(image, blob)

    # Apply global radial mask to ensure edges = 0
    global_r = np.sqrt(xx**2 + yy**2)
    global_mask = np.clip(1 - global_r, 0, 1) ** global_mask_strength
    image *= global_mask
    import matplotlib.pyplot as plt
    # Display the image
    plt.imshow(np.clip(image, 0, 1), cmap='gray')
    plt.axis('off')
    plt.title("Blobs with Jagged Edges (Edge = 0)")
    plt.show()

    return np.clip(image, 0, 1)