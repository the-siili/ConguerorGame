import pygame
from amath import Vec2
from settings import MAP_SIZE, WINDOW_SIZE, COORD_MULTIPLIER

class Camera:
    pos = Vec2(0, 0)
    zoom = 1.0

    @classmethod
    def set_zoom(self, new_zoom):
        self.zoom = pygame.math.clamp(self.zoom+new_zoom, max(WINDOW_SIZE)/min(MAP_SIZE), 2.0)
        self.fix_to_map()
    
    @classmethod
    def fix_to_map(self):
            x_fix_right = pygame.math.clamp(((self.pos.x)+(WINDOW_SIZE.x/COORD_MULTIPLIER)/self.zoom-(MAP_SIZE.x/COORD_MULTIPLIER)), 0, float("inf"))
            x_fix_left = pygame.math.clamp(self.pos.x, -float("inf"), 0)
            x_fix = max(x_fix_right, x_fix_left, key=lambda x:abs(x))
            self.pos.x -= x_fix

            y_fix_right = pygame.math.clamp(self.pos.y+(WINDOW_SIZE.y/COORD_MULTIPLIER)/self.zoom-(MAP_SIZE.y/COORD_MULTIPLIER), 0, float("inf"))
            y_fix_left = pygame.math.clamp(self.pos.y, -float("inf"), 0)
            y_fix = max(y_fix_right, y_fix_left, key=lambda x:abs(x))
            self.pos.y -= y_fix

class Renderer:
    screen = None
    ui_manager = None
    surfaces = None

    @classmethod
    def initialize(self, screen, ui_manager):
        self.ui_manager = ui_manager
        self.screen = screen
        self.surfaces = {
        "capitol": pygame.transform.scale(pygame.image.load("src/res/capitol.png"), (1024//40, 1024//40)),
        "sea": pygame.transform.scale(pygame.image.load("src/res/tex_Water.jpg"), tuple(MAP_SIZE))
    }


    @classmethod
    def render_world_texture(self, texture, pos, scale):
        texture = pygame.transform.scale_by(texture, Camera.zoom)
        self.screen.blit(texture, ((round((pos.x-Camera.pos.x)*COORD_MULTIPLIER*Camera.zoom), 
                                    round((pos.y-Camera.pos.y)*COORD_MULTIPLIER*Camera.zoom)),
                                    (round(scale.x*COORD_MULTIPLIER*Camera.zoom), 
                                    round(scale.y*COORD_MULTIPLIER*Camera.zoom))))
    @classmethod
    def render_screen_texture(self, texture, x, y, w, h):
        self.screen.blit(texture, ((x, y), (w,h)))
    
    @classmethod
    def render_screen_rect(self, rect_coords, color, width):
        pygame.draw.rect(self.screen, color, rect_coords, width)


    @classmethod                                    #make sure to give width in pixels
    def render_world_rect(self, rect_coords, color, width: int):
        x = int((rect_coords[0][0]-Camera.pos.x)*COORD_MULTIPLIER*Camera.zoom)
        y = int((rect_coords[0][1]-Camera.pos.y)*COORD_MULTIPLIER*Camera.zoom)

        w = int(rect_coords[1][1]*COORD_MULTIPLIER*Camera.zoom)
        h = int(rect_coords[1][0]*COORD_MULTIPLIER*Camera.zoom)

        pygame.draw.rect(self.screen, color, ((x,y),(w,h)), width)

    @classmethod                                    #make sure to give width in pixels
    def render_world_line(self, pos1: Vec2, pos2: Vec2, color, width: int):
        x1 = int((pos1.x-Camera.pos.x)*COORD_MULTIPLIER*Camera.zoom)
        y1 = int((pos1.y-Camera.pos.y)*COORD_MULTIPLIER*Camera.zoom)

        x2 = int((pos2.x-Camera.pos.x)*COORD_MULTIPLIER*Camera.zoom)
        y2 = int((pos2.y-Camera.pos.y)*COORD_MULTIPLIER*Camera.zoom)

        pygame.draw.line(self.screen, color, (x1,y1), (x2,y2), round(width*COORD_MULTIPLIER*Camera.zoom))

    @classmethod                                    #make sure to give width in pixels
    def render_world_circle(self, pos: Vec2, radius, color, width: int):
        x = int((pos.x-Camera.pos.x)*COORD_MULTIPLIER*Camera.zoom)
        y = int((pos.y-Camera.pos.y)*COORD_MULTIPLIER*Camera.zoom)

        radius = int(radius*COORD_MULTIPLIER*Camera.zoom)

        pygame.draw.circle(self.screen, color, (x,y), radius, round(width*COORD_MULTIPLIER*Camera.zoom))