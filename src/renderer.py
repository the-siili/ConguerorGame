import pygame
import pygame_gui
import pygame_shaders
from amath import Vec2
from settings import MAP_SIZE, WINDOW_SIZE, COORD_MULTIPLIER, MAP_COLORS, REAL_MAP_SIZE
from map_generator import generate_map

#global
class Camera:
    pos = Vec2(0, 0)
    #start from 1.0 because i dont fucking know man id doesnt work otherwise
    #hours spent debugging: 1
    zoom = 1.0

    @classmethod
    def set_zoom(self, new_zoom):
        if new_zoom < 0:
            self.zoom = pygame.math.clamp(self.zoom+0.25, 1.0, 2.0)
        else:
            self.zoom = pygame.math.clamp(self.zoom-0.25, 1.0, 2.0)
        self.fix_to_map()
    
    @classmethod
    def fix_to_map(self):
            x_fix_right = pygame.math.clamp(((self.pos.x)+(WINDOW_SIZE.x/COORD_MULTIPLIER)*self.zoom-(MAP_SIZE.x/COORD_MULTIPLIER)), 0, float("inf"))
            x_fix_left = pygame.math.clamp(self.pos.x, -float("inf"), 0)
            x_fix = max(x_fix_right, x_fix_left, key=lambda x:abs(x))
            self.pos.x -= x_fix

            y_fix_right = pygame.math.clamp(self.pos.y+(WINDOW_SIZE.y/COORD_MULTIPLIER)*self.zoom-(MAP_SIZE.y/COORD_MULTIPLIER), 0, float("inf"))
            y_fix_left = pygame.math.clamp(self.pos.y, -float("inf"), 0)
            y_fix = max(y_fix_right, y_fix_left, key=lambda x:abs(x))
            self.pos.y -= y_fix

    @classmethod
    def set_position(self, pos):
            self.pos = pos
            self.fix_to_map()

    @classmethod
    def move(self, direction):
            self.pos += direction
            self.fix_to_map()


#global
class Renderer:
    screen = None
    ui_manager: pygame_gui.UIManager|None = None
    
    original_surfaces = {}
    mip_maps = {}

    @classmethod
    def initialize(self, screen):
        #Settings these only onse because they will exist as the same 
        #till the application quits
        self.ui_manager = pygame_gui.UIManager(tuple(WINDOW_SIZE), 'src/res/ui_themes/default_theme.json')
        self.screen = screen
        self.__add_standard_textures()
        #
        self.reset()
    
    @classmethod
    def __add_standard_textures(self):
        self.add_surface("Soldiers", pygame.transform.scale(pygame.image.load("src/res/soldiers.png"), (16, 24)))
        self.add_surface("Tent", pygame.transform.scale(pygame.image.load("src/res/tent.png"), (16, 16)))
        self.add_surface("Boat", pygame.transform.scale(pygame.image.load("src/res/boat.png"), (24, 16)))
        self.add_surface("Capitol", pygame.transform.scale(pygame.image.load("src/res/capitol.png"), (64, 64)))
        self.add_surface("Castle", pygame.transform.scale(pygame.image.load("src/res/castle.png"), (38, 38)))
        self.add_surface("Village", pygame.transform.scale(pygame.image.load("src/res/village.png"), (24, 24)))
        self.add_surface("Construction", pygame.transform.scale(pygame.image.load("src/res/construction.png"), (38, 38)))
        self.add_surface("Sea", pygame.transform.scale(pygame.image.load("src/res/tex_Water.jpg"), (max(MAP_SIZE), max(MAP_SIZE))))
        

    @classmethod
    def render_world_texture(self, texture_key, pos, scale, centered=False, offset=Vec2(0, 0)):
        center_fix = Vec2(0, 0)
        if centered:center_fix = Vec2(self.mip_maps[texture_key][Camera.zoom].get_width()//2, self.mip_maps[texture_key][Camera.zoom].get_height()//2)
        
        x = round((pos.x+offset.x-Camera.pos.x)*COORD_MULTIPLIER/Camera.zoom)-center_fix.x
        y = round((pos.y+offset.y-Camera.pos.y)*COORD_MULTIPLIER/Camera.zoom)-center_fix.y
        w = round(scale.x*COORD_MULTIPLIER//Camera.zoom)
        h = round(scale.y*COORD_MULTIPLIER//Camera.zoom)
        self.screen.blit(self.mip_maps[texture_key][Camera.zoom], ((x, y),(w, h)))#h
    @classmethod
    def render_screen_texture(self, texture, x, y, w, h):
        self.screen.blit(texture, ((x, y), (w,h)))
    
    @classmethod
    def render_screen_rect(self, rect_coords, color, width):
        pygame.draw.rect(self.screen, color, rect_coords, width)


    @classmethod                                    #make sure to give width in pixels
    def render_world_rect(self, rect_coords, color, width: int):
        x = int((rect_coords[0][0]-Camera.pos.x)*COORD_MULTIPLIER/Camera.zoom)
        y = int((rect_coords[0][1]-Camera.pos.y)*COORD_MULTIPLIER/Camera.zoom)

        w = int(rect_coords[1][1]*COORD_MULTIPLIER/Camera.zoom)
        h = int(rect_coords[1][0]*COORD_MULTIPLIER/Camera.zoom)

        pygame.draw.rect(self.screen, color, ((x,y),(w,h)), width)

    @classmethod                                    #make sure to give width in pixels
    def render_world_line(self, pos1: Vec2, pos2: Vec2, color, width: int):
        x1 = int((pos1.x-Camera.pos.x)*COORD_MULTIPLIER/Camera.zoom)
        y1 = int((pos1.y-Camera.pos.y)*COORD_MULTIPLIER/Camera.zoom)

        x2 = int((pos2.x-Camera.pos.x)*COORD_MULTIPLIER/Camera.zoom)
        y2 = int((pos2.y-Camera.pos.y)*COORD_MULTIPLIER/Camera.zoom)

        pygame.draw.line(self.screen, color, (x1,y1), (x2,y2), round(width*COORD_MULTIPLIER*Camera.zoom))

    @classmethod                                    #make sure to give width in pixels
    def render_world_circle(self, pos: Vec2, radius, color, width: int):
        x = int((pos.x-Camera.pos.x)*COORD_MULTIPLIER/Camera.zoom)
        y = int((pos.y-Camera.pos.y)*COORD_MULTIPLIER/Camera.zoom)

        radius = int(radius*COORD_MULTIPLIER/Camera.zoom)

        pygame.draw.circle(self.screen, color, (x,y), radius, round(width*COORD_MULTIPLIER/Camera.zoom))
    
    @classmethod
    def reset(self):
        #has to be set to 1 for some reason that I dont know why
        Camera.set_zoom(1.0)
        Camera.set_zoom(1.0)
        Camera.set_zoom(1.0)
        Camera.set_zoom(1.0)
        #create a new map and clear the ui manager to be empty so that
        #previous ui elements will all disappear from the screen and memory
        self.add_surface("Land", generate_map(MAP_SIZE, MAP_COLORS))
        self.ui_manager.clear_and_reset()
        

    @classmethod
    def add_surface(self, key, surface):
        self.original_surfaces[key] = surface
        self.update_surface(key)

    #updates a textures mip maps
    #useful for when a generated texture changes, for example the borders
    @classmethod
    def update_surface(self, key):
        #empty the mip_maps so that the old mipmaps for this texture will dissappear from memory
        self.mip_maps[key] = {}
        #creates new mip_maps for the texture
        for i in [1, 1.25, 1.5, 1.75, 2]:
            self.mip_maps[key][i] = pygame.transform.scale_by(self.original_surfaces[key], 1/i)

    #returns the original texture by reference to be changed
    #used for replacing generated textures
    @classmethod
    def get_surface(self, key):
        return self.original_surfaces[key]