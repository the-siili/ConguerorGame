import random
import settings
import time
from amath import Vec2
import os

def create_borders(map_size, amount_of_nations):
    map_size = map_size


    render_grid = [[" " for i in range(1, map_size.x)]for i in range(1, map_size.y)]

    nations = {}
    occupied_points = set()
    colors = [(230, 25, 75, 255),
                (60, 180, 75, 255),
                (255, 225, 25, 255),
                (0, 170, 250, 255),
                (245, 130, 48, 255),
                (145, 30, 180, 255),
                (70, 240, 240, 255),
                (240, 50, 230, 255),
                (210, 245, 60, 255),
                (250, 190, 190, 255),
                (250, 190, 190, 255)]
    names = ["Valoria",
            "Kingdom Of Sweidor",
            "Karthwyn",
            "Empire Of Emberhold ",
            "Orrenmark",
            "Zevaran Expanse ",
            "Thornsworn Dynasty",
            "Kingdom Of Drelmore",
            "The Fyrholt Sultanate",
            "Shadowmere",
            "Shadowmere"]
    #GENERATES THE STARTING POINT FOR NEW NATIONS
    for i in range(amount_of_nations):
        new_point = Vec2(random.randint(int(map_size.x*0.25), int(map_size.x-map_size.x*0.25)),random.randint(int(map_size.y*0.25), int(map_size.y-map_size.y*0.25)))
        nations[i] = (set([new_point]), set(), colors[i], new_point, names[i])

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
    #ALGORITHM THAT MAKES ALL THE NATIONS EXPAND FROM STARTING POSITIONS EQUALLY
    #GIVES NICE FAKE NATION BORDERS
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
    
    #TRANSLATES THE NATIONS INTO A MORE READABLE FORM
    for i in nations.keys():
        nations[i] = {
            "occupied_points":nations[i][0],
            "color":nations[i][2],
            "capitol_coords":nations[i][3],
            "name":nations[i][4]
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

#create_borders(Vec2(64, 64), 10)