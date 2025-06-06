class Node:
    def __init__(self, node_id, position):
        self.id = node_id
        self.position = position
        self.g = float('inf')
        self.f = float('inf')
        self.parent = None
        self.seen = set()
        self.path = []
        self.h = 0
        

        #for BFS and hill Climbing
        self.node_id = node_id
        self.edges = {}
        
    
    def add_edge(self, neighbor, cost):
        self.edges[neighbor] = cost

    def __repr__(self):
        return f"Node({self.node_id}, ({self.x}, {self.y}), Edges: {self.edges})"


        


