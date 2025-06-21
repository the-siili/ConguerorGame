import random
import settings
import time
from amath import Vec2
import os

def create_borders(map_size):
    map_size = map_size


    render_grid = [[" " for i in range(1, map_size.x)]for i in range(1, map_size.y)]

    nations = {}
    occupied_points = set()
    colors = [(255, 255, 0, 100), (0, 255, 255, 100), (255, 0, 255, 100), (0, 0, 255, 100), (255, 0, 0, 100),(0, 255, 0, 100)]
    for i in range(random.randint(4, 6)):
        new_point = Vec2(random.randint(2, map_size.x-3),random.randint(2, map_size.y-3))
        nations[i] = (set([new_point]), set(), colors[i], new_point)

        for p_p in [Vec2(new_point.x+1, new_point.y), 
                    Vec2(new_point.x-1, new_point.y),
                    Vec2(new_point.x, new_point.y+1),
                    Vec2(new_point.x, new_point.y-1)]:
            if p_p.x in range(1, map_size.x) and \
                p_p.y in range(1, map_size.y) and \
                p_p not in occupied_points and \
                p_p not in nations[i][1]:
                
                nations[i][1].add(p_p)

        occupied_points.add(new_point)

    #print(nations)

    while True:
        point_added = False
        for area in nations.values():
            if len(area[1]) == 0:
                continue
            b = False
            new_point = random.choice([i for i in area[1]])
            while new_point in occupied_points:
                area[1].remove(new_point)
                if len(area[1]) == 0:
                    b = True
                    break
                new_point = random.choice([i for i in area[1]])

            if b: continue
            
            point_added = True

            area[0].add(new_point)
            for p_p in [Vec2(new_point.x+1, new_point.y), 
                Vec2(new_point.x-1, new_point.y),
                Vec2(new_point.x, new_point.y+1),
                Vec2(new_point.x, new_point.y-1)]:
                if p_p.x in range(1, map_size.x) and \
                    p_p.y in range(1, map_size.y) and \
                    p_p not in occupied_points and \
                    p_p not in area[0]:
                    area[1].add(p_p)
            occupied_points.add(new_point)
        
        if point_added == False:
            break

        # os.system('clear')
        # for y in range(len(render_grid)):
        #     for x in range(len(render_grid[1])):
        #         owner = ""
        #         for i in nations.keys():
        #             if Vec2(x, y) in nations[i][0]: 
        #                 owner = i
        #         render_grid[y][x] = f"{owner}"

        # for y in render_grid:
        #     for x in y:
        #         print(x, end=" ")
        #     print()
        # time.sleep(0.05)
    
    for i in nations.keys():
        nations[i] = {
            "occupied_points":nations[i][0],
            "color":nations[i][2],
            "capitol_coords":nations[i][3]
        }

    return nations

    # os.system('clear')
    # for y in range(len(render_grid)):
    #     for x in range(len(render_grid[1])):
    #         owner = " "
    #         for i in nations.keys():
    #             if Vec2(x, y) in nations[i][0]: 
    #                 owner = i
    #         render_grid[y][x] = f"{owner}"

    # for y in render_grid:
    #     for x in y:
    #         print(x, end=" ")
    #     print()

#create_borders(Vec2(64, 32))