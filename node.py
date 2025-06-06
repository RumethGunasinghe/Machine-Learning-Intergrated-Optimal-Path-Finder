class Node:
    def __init__(self, node_id, position):
        self.id = node_id
        self.position = position
        self.g = float('inf')
        self.f = float('inf')
        self.parent = None
        self.seen = set()
        self.h = 0



