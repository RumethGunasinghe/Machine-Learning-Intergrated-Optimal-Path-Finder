import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Classes.Node import Node
from Classes.Graph import Graph
from models.FindTime import findTime

class GBFS:
    def __init__(self, graph , model , tod):
        self.tod = tod
        self.inputModel = model
        self.graph = graph
        self.open_list = []
        self.closed_list = []

    def reconstruct_path(self,current_node):
        path = []
        path.append(current_node) 
        while True:
            next_Node = current_node.parent
            path.append(next_Node)
            current_node = next_Node
            if current_node.parent == None:
                break
        return list(reversed(path))

    # def heuristic(self, node_id1, node_id2):
    #     node1 = next((n for n in self.graph.nodes if n.id == node_id1), None)
    #     node2 = next((n for n in self.graph.nodes if n.id == node_id2), None)
    #     if node1 and node2:
    #         return haversine((node1.latitude, node1.longitude),( node2.latitude, node2.longitude))
    #     return float('inf')

    def find_path(self, start_id, goal_id):
        start = next((node for node in self.graph.nodes if node.id == start_id), None)
        goal = next((node for node in self.graph.nodes if node.id == goal_id), None)

        
        if not start or not goal:
            print("Start or goal node not found")
            return []

        for node in self.graph.nodes:
            # node.g = float('inf')
            node.f = float('inf')
            node.parent = None

        # start.g = 0
        start.f = self.graph.heuristic(start.id, goal.id)

        self.open_list = [start]
        self.closed_list = []
        print(f"Open List is {[n.id for n in self.open_list]}")
        print(f"Cllosed List is {[n.id for n in self.closed_list]}")
        print(" ")
        print(" ")
        


        while self.open_list:
            # print([n.id for n in self.open_list])
            self.open_list.sort(key=lambda node: node.f)
            print(f"resort afterwards =  {[n.id for n in self.open_list]}")
            # if(self.open_list[0] not in current_node.neighbours):
            current_node = self.open_list.pop(0)
            #we dont need the previous neighbours because the sorting wont actually give you the closest node since it  depends on the time ffs
            print(f"moved into {current_node.id} ")
            print(f"removed the moved node from Open List = {[n.id for n in self.open_list]}")

            # print(current_node)
            if current_node.id == goal.id:
                return self.reconstruct_path(current_node)

            self.closed_list.append(current_node)
            print(f"added the moved node into Closed List = {[n.id for n in self.closed_list]}")
            for neighbour in current_node.neighbours:
                if neighbour in self.closed_list:
                    continue
                locationAdd = self.graph.usingAddress(current_node, neighbour )
                print(f"from node {current_node.id} looking at node {neighbour.id} via {locationAdd}")

                if locationAdd == None:  #BUGFIX
                    print("No traffic data were given for the selected road/node. so the node will be dropped as an option")
                    self.closed_list.append(current_node)
                    continue
                else : 
                    # finding the g onyl for the sake of to reach the goal and NOT for the algorithm. wont compare the tentative_g < neighbour.g: 
                    tentative_g = current_node.g + findTime(locationAdd, self.inputModel , current_node , neighbour, self.tod)
                    neighbour.g = tentative_g
                    neighbour.f = self.graph.heuristic(neighbour.id, goal.id)
                    neighbour.parent = current_node

                    if neighbour not in self.open_list:
                        self.open_list.append(neighbour)
                        print(f"adding the available option into open list =  {[n.id for n in self.open_list]}")
            

        return None



