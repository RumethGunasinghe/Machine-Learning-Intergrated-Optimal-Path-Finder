from node import Node
import math

class GraphBFS:
    def __init__(self):
        self.nodes = {}

    def add_node(self, node_id, position):
        self.nodes[node_id] = Node(node_id, position)

    def add_edge(self, node1, node2, cost):
        self.nodes[node1].add_edge(node2, cost)

    def get_node(self, node_id):
        return self.nodes.get(node_id, None)
    
    def get_neighbors(self, node_id):
        # This method will return a list of (neighbor_id, cost) tuples
        node = self.get_node(node_id)
        if node:
            return node.edges
        return []

    def create_graph(nodes, edges): #for BSF GRAPH CREATION
        graph = GraphBFS()

        for node_id, (x, y) in nodes.items():
            position = x ,y
            graph.add_node(node_id, position)

        for (from_node, to_node), cost in edges.items():
            graph.add_edge(from_node, to_node, cost)

        return graph

    def heuristic(self,graph, node_id, goal_id):
        node = self.get_node(node_id)
        goal = self.get_node(goal_id)

        x1, y1 = node.position  
        x2, y2 = goal.position
        # Calculate Euclidean distance between nodes
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
