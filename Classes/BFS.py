from collections import deque
from haversine import haversine, Unit
from models.FindTime import findTime

class BFS:
    def __init__(self, graph, model, tod):
        self.graph = graph
        self.model = model
        self.tod = tod

    def NodeByID(self, node_id):
        return next((node for node in self.graph.nodes if node.id == node_id), None)

    def BreadthFirstSearch(self, origin, destination, max_paths=5):
        queue = deque()
        queue.append((origin, [origin], 0))
        # found_paths = []

        visited = set()

        while queue : #and len(found_paths) < max_paths
            current, path, total_cost = queue.popleft()


            if current.id in visited:
                continue
            visited.add(current.id)

            if current.id == destination.id:
                # found_paths.append((path, total_cost)
                print(f"Path found: {[node.id for node in path]} with total cost: {total_cost}")
                return path, total_cost
                

            for neighbor in current.neighbours:
                if neighbor.id not in [node.id for node in path]:  # Prevent cycles

                    locationAdd = self.graph.usingAddress(current, neighbor)
                    if not locationAdd:
                        continue

                    time_to_neighbor = findTime(locationAdd, self.model, current, neighbor, self.tod)
                    new_path = path + [neighbor]
                    new_cost = total_cost + time_to_neighbor

                    queue.append((neighbor, new_path, new_cost))
        return None, None
