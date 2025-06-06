from collections import deque
from haversine import haversine, Unit
from models.FindTime import findTime

class HillClimbing:
    def __init__(self, graph, model, tod):
        self.graph = graph
        self.model = model
        self.tod = tod

    def NodeByID(self, node_id):
        return next((node for node in self.graph.nodes if node.id == node_id), None)

    def HillClimbingSearch(self, origin, destination):
        current = origin
        path = [current]
        total_time = 0
        
        while current.id != destination.id:
            neighbors = current.neighbours
            best_neighbor = None
            best_cost = float('inf')
            best_time = float("inf")

            # choose neighbor with least cost
            for neighbor in neighbors:
                if neighbor.id not in [node.id for node in path]:  # Avoid cycles
                    locationAdd = self.graph.usingAddress(current, neighbor)
                    if not locationAdd:
                        continue
                    
                    # Calculate the cost to the neighbor
                    time_to_neighbor = findTime(locationAdd, self.model, current, neighbor, self.tod )
                    cost_to_neighbour = self.graph.heuristic(neighbor.id, destination.id) #distance
                    new_time = total_time + time_to_neighbor
                    
                    # Choose the best neighbor (the one with the least travel time)
                    if cost_to_neighbour < best_cost:
                        best_cost = cost_to_neighbour
                        best_time = new_time
                        best_neighbor = neighbor

            # stuck in local maxima
            if best_neighbor is None:
                return path, total_time

            # go to best neighbor
            current = best_neighbor
            path.append(current)
            total_time = best_time

        print(f"Path found: {[node.id for node in path]} with total ETA: {total_time}")
        return path, total_time
