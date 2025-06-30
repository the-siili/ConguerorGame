from object import Object
from renderer import Renderer
from engine_data import EngineData
from amath import Vec2
import math
import heapq
from numba import jit
import dijkstra

class Soldiers(Object):
    def __init__(self, pos, soldier_amount, nation, destination):
        super().__init__(pos, Vec2(1, 1))
        self.render_layer = 4

        self.soldier_amount = soldier_amount
        self.nation = nation

        self.name = "Soldiers Of "+self.nation.name

        self.speed = 4

        self.current_destination = destination
        self.graph = self.nation.world.path_finding_graph.copy()

        self.point = Vec2(round(self.pos.x), round(self.pos.y))
        self.current_path = dijkstra.shortest_path(self.graph, (int(self.point.x), int(self.point.y)), (int(self.current_destination.rounded().x), int(self.current_destination.rounded().y)))
        


        self.boat_point = None
        self.boat_water_point = None



    def start(self):
        self.nation.world.world_points[self.point]["current_object"] = self
    
    def calculate_path(self):
        pass

    
    def update(self):
        
        self.point = self.pos.rounded()
        self.nation.world.world_points[self.point]["current_object"] = self
        if self.current_path != None:
            path_vec = Vec2(self.current_path[-1][0], self.current_path[-1][1])
            d = (path_vec-self.pos)
            m = math.sqrt((d.x**2+d.y**2))

            direction = d/m

            self.pos += d/m*EngineData.game_delta_time*self.speed*(1/self.nation.world.world_points[self.point]["speed"])

            if self.point == path_vec:
                self.current_path.pop(-1)

                if len(self.current_path) == 0:
                    self.current_path = None
                else:
                    self.nation.world.world_points[self.point]["current_object"] = None
                    self.nation.world.world_points[Vec2(self.current_path[-1][0], self.current_path[-1][1])]["current_object"] = self

        #if self.current_path != None:
            #print(self.current_path[-1])


    def set_destination(self, destination):
        self.current_destination = destination
        self.current_path = dijkstra.shortest_path(self.graph, (int(self.pos.rounded().x), int(self.pos.rounded().y)), (int(self.current_destination.rounded().x), int(self.current_destination.rounded().y)))
        #if self.current_path != None:
        #    print(self.current_path)

    def render(self):
        if self.current_path != None and self.nation.world.world_points[Vec2(self.current_path[-1][0], self.current_path[-1][1])]["terrain_type"] == "water":
            Renderer.render_world_texture("Boat", self.pos, self.scale, True)
        elif self.pos.rounded() == self.current_destination.rounded():
            Renderer.render_world_texture("Tent", self.pos.rounded(), self.scale, True)
        else:
            Renderer.render_world_texture("Soldiers", self.pos, self.scale, True, offset=Vec2(0, -1))


        if self.boat_water_point != None:
            Renderer.render_world_texture("Boat", self.boat_water_point, self.scale, True)

    def shortest_path(self, start, end):
        # Priority queue: stores tuples of (distance, vertex)
        graph = self.graph
        queue = [(0, start)]
        # Dictionary to track the shortest known path to each node
        distances = {node: float('inf') for node in graph}
        distances[start] = 0
        # Dictionary to reconstruct the path
        previous_nodes = {node: None for node in graph}

        while queue:
            current_distance, current_node = heapq.heappop(queue)

            # Stop if we reached the destination
            if current_node == end:
                break

            # Skip if we already found a better path
            if current_distance > distances[current_node]:
                continue

            for neighbor, weight in graph[current_node]:
                distance = current_distance + weight

                # Update the shortest path to the neighbor
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous_nodes[neighbor] = current_node
                    heapq.heappush(queue, (distance, neighbor))
        
        # Reconstruct path
        path = []
        current = end
        while current is not None:
            path.append(current)
            current = previous_nodes[current]

        if distances[end] == float('inf'):
            return None
        return path