import pygame

from input import Input
from world import World
from object import Object
from renderer import Renderer, Camera


from settings import MAP_SIZE, WINDOW_SIZE, COORD_MULTIPLIER, WINDOW_FLAGS
from amath import Vec2


class Game:
    screen = None
    objects = []
    #8 render layers exist
    render_layers = [[],[],[],[],[],[],[],[]]
    last_L_mouse_pos = Vec2(0, 0)
    delta_time = 0
    

    @classmethod
    def start(self):
        self.spawn_object(World())

        for obj in self.objects:
            obj.start()
    @classmethod
    def get_input(self):
        Input.update_inputs()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEWHEEL:
                Camera.set_zoom(event.y*0.1)
            Renderer.ui_manager.process_events(event)

        if Input.mouse_button_down("right") == False:
            self.last_L_mouse_pos = Input.mouse_screen_pos()
        else:
            Camera.pos += Vec2((self.last_L_mouse_pos.x-Input.mouse_screen_pos().x)/Camera.zoom/COORD_MULTIPLIER,
                                (self.last_L_mouse_pos.y-Input.mouse_screen_pos().y)/Camera.zoom/COORD_MULTIPLIER)
            Camera.fix_to_map()

            self.last_L_mouse_pos = Input.mouse_screen_pos()

    @classmethod
    def update(self, delta_time):
        Renderer.ui_manager.update(delta_time)
        for obj in self.objects:
            obj.update()
    @classmethod
    def render(self):
        for layer in self.render_layers:
            for obj in layer:
                obj.render()
        Renderer.ui_manager.draw_ui(Renderer.screen)
        

    @classmethod
    def spawn_object(self, obj):
        self.objects.append(obj)
        if 0 > obj.render_layer >= len(self.render_layers):
            raise ValueError(f"Invalid render layer not between {0, len(self.render_layers)}: {obj}")
        self.render_layers[obj.render_layer].append(obj)

