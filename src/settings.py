from amath import Vec2
import pygame

WINDOW_FLAGS = 0
#WINDOW_FLAGS = pygame.FULLSCREEN|pygame.SCALED
MAP_SIZE = Vec2(4096, 2048)
WINDOW_SIZE = Vec2(800, 600)
COORD_MULTIPLIER = MAP_SIZE.x//512

REAL_MAP_SIZE = Vec2(MAP_SIZE.x//COORD_MULTIPLIER, MAP_SIZE.y//COORD_MULTIPLIER)

NATION_AMOUNT = Vec2(6, 9)


MAP_COLORS = {
        "wetland":{
                "normal":[(117, 72, 4, 255)],
                "desert":[(240, 191, 117, 255)],
                "tundra":[(129, 164, 179, 255)]
                },
        "planes":{
                "normal":[(73, 107, 22, 255), (70, 100, 18, 255)],
                "desert":[(196, 140, 55, 255), (196, 135, 41, 255)],
                "tundra":[(191, 191, 191, 255), (204, 204, 204, 255)]
        },
        "forest":{
                "normal":[(32, 92, 40, 255), (34, 56, 16, 255), (52, 56, 16, 255)],
                "desert":[(55, 156, 19, 255), (26, 94, 2, 255), (0, 61, 9, 255)],
                "tundra":[(191, 191, 191, 255), (204, 204, 204, 255), 
                         (191, 191, 191, 255), (204, 204, 204, 255), 
                         (191, 191, 191, 255), (204, 204, 204, 255), (77, 36, 3, 255),]
        },
        "mountain1":{
                "normal":[(78, 79, 77, 255)],
                "desert":[(143, 125, 71, 255)],
                "tundra":[(128, 128, 128, 255)]
        },
        "mountain2":{
                "normal":[(98, 89, 97, 255)],
                "desert":[(112, 98, 55, 255)],
                "tundra":[(173, 173, 173, 255)]
        },
        "mountain3":{
                "normal":[(110, 115, 115, 255)],
                "desert":[(84, 75, 48, 255)],
                "tundra":[(204, 204, 204, 255)]
        },
        "mountaintop":{
                "normal":[(191, 191, 191, 255)],
                "desert":[(189, 179, 149, 255)],
                "tundra":[(189, 179, 149, 255)]
        }
}


BUILDING_SIZES = {
        "capitol":9
}