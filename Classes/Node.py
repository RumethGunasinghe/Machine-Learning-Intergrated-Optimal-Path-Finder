from Classes.Location import Location

class Node:
    def __init__(self, node_id):
        self.id = node_id
        self.locations = []
        self.latitude = float()
        self.longitude = float()
        self.neighbours = []
        self.assoRoadsWithNodes = {}
        self.assoRoadsWithDirections = {}
        
        self.g = 0
        self.f = float('inf')
        self.parent = None
        self.seen = []
        self.path = []
        self.h = 0

    def add_location(self, locationObj):
        self.locations.append(locationObj)
        
    def add_associatedRoads(self, road):
        if road not in self.associatedRoads:
            self.associatedRoads.append(road)

    def add_nodeOnassociatedRoads(self, node):
        self.nodeOnassociatedRoads.append(node)


    # def add_edge(self, neighbor, cost):
    #     self.edges[neighbor] = cost


    def __repr__(self):
        return f"Node({self.id}, Locations: {[location.name for location in self.locations]})"



        


