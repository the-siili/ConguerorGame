


class EngineData:
    current_scene = None
    delta_time = None

    @classmethod
    def set_current_scene(self, scene):
        self.current_scene = scene
    @classmethod
    def get_current_scene(self, scene):
        return self.current_scene
        