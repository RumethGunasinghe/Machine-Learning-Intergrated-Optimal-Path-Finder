from haversine import haversine, Unit
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.FindTime import findTime
from Classes.Graph import Graph
from Classes.Node import Node
# from Classes.Graph import Graph
class DFS:
    def __init__(self, graph, model, TOD):
        self.graph = graph
        self.TOD = TOD
        self.model = model 

    
    def NodeByID(self, node_id):
        return next((node for node in self.graph.nodes if node.id == node_id), None)
        
    def DepthFirstSearch(self, origin, destination, seen=None, path=None, totalCost=0):
        if seen is None:
            seen = set()
        if path is None:
            path = []

        print(f"currently at node: {origin.id}, total cost = {totalCost}")
        seen.add(origin.id)
        path.append(origin)

        if origin.id == destination.id:
            print(f"goal reached at node {destination.id}")
            print(", ".join(str(n.id) for n in path))
            print(f"total estimated time: {totalCost}")
            return list(path), totalCost  

        for neighbor in origin.neighbours:
            if neighbor.id not in seen:
                locationAdd = self.graph.usingAddress(origin, neighbor)

                if not locationAdd:
                    print(f"no address found between {origin.id} and {neighbor.id}, passing")
                    continue

                time_to_neighbor = findTime(locationAdd, self.model, origin, neighbor, self.TOD)
                new_total = totalCost + time_to_neighbor

                result_path, result_cost = self.DepthFirstSearch(neighbor, destination, seen, path.copy(), new_total
                )

                if result_path:
                    return result_path, result_cost

        path.pop()  
        return None, float("inf")

