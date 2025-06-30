import time


class EngineData:
    current_scene = None


    delta_time = 0.000001

    game_delta_time = 0.00000001
    game_time = 0
    game_time_multiplier = 1

    last_time = time.time()

    @classmethod
    def set_current_scene(self, scene):
        delta_time = 0.001
        game_delta_time = 0.001
        game_time = 0
        game_time_multiplier = 1
        
        self.current_scene = scene

        self.last_time = time.time()


    @classmethod
    def get_current_scene(self, scene):
        return self.current_scene
    
    @classmethod
    def update(self):

        self.delta_time = time.time()-self.last_time
        self.game_delta_time = self.delta_time*self.game_time_multiplier
        self.game_time += self.game_delta_time

        self.last_time = time.time()



