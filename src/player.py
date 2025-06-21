from input import Input
from renderer import Renderer
from amath import Vec2

class Player():
    nation = None
    world = None
    in_action = False
    @classmethod
    def initialize(self, nation, world):
        self.nation = nation
        self.world = world

    @classmethod
    def update(self):
        if Input.mouse_button_pressed("left") and not self.in_action:
            #self.nation.build_castle(Input.mouse_world_pos_rounded())
            point = self.world.world_points[Input.mouse_world_pos_rounded()]
            if point["current_object"] != None:
                point["current_object"].open_info()
            else:
                print(point["terrain_type"])

    
    @classmethod
    def render(self):
        calc_vectors = [Vec2(0, 0),
                Vec2(0, -1), 
                Vec2(1, -1),
                Vec2(1, 0),
                Vec2(1, 1), 
                Vec2(0, 1),
                Vec2(-1, 1), 
                Vec2(-1, 0), 
                Vec2(-1, -1)]

        for vec in calc_vectors:
            mouse_pos = Input.mouse_world_pos_rounded()
            Renderer.render_world_circle(mouse_pos+vec, 0.3, (255, 255, 255), 0)
