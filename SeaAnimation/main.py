import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from perlin_numpy import generate_fractal_noise_3d
from PIL import Image

np.random.seed(0)
noise = generate_fractal_noise_3d(
    (32, 256, 256), (1, 32, 32), 4, tileable=(True, False, False)
)

fig = plt.figure()
i = 0
for layer in noise:
    im = Image.new(mode="RGBA", size=(256, 256))  
    a = np.asarray(im)
    pixelsNew = im.load()
    for y, line in enumerate(layer):
        for x, v in enumerate(line):
            pixelsNew[y,x] = (0, 0, int(255*layer[y][x]), 255)

    im.save(f"{i}.png")
    i+=1

#animation_3d = animation.ArtistAnimation(fig, images, interval=50, blit=True)
#plt.show()