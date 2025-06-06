import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Classes.Node import Node
from Classes.Location import Location 
from haversine import haversine, Unit

class Graph:
    def __init__(self):
        df = pd.read_csv("csv/locationSummary.csv")
        self.nodes = []

        # Group by SCATS Number
        grouped = df.groupby("SCATS Number")

        for scat_number, group in grouped:
            node = Node(scat_number)  # create a Node with this SCATS Number

            # Add each location to the Node
            for _, row in group.iterrows():
                locationObj = Location(name=row["Location"], latitude=row["NB_LATITUDE"],  longitude=row["NB_LONGITUDE"], direction=row["Direction"], located_on=row["LocatedOn#street"], compared_to=row["DirectionComparedTo"])
                node.locations.append(locationObj)

            ##BUGFIX BUGFIX - if commented - Will be ignored as neighbours
            # if node == next((n for n in self.nodes if n.id == 970), None)  #only node 970 is located on HIGH STREET_ROAD and it converts into HIGH_ST inbetween 970 and 2846. they wont be recognized as neighbours even though they are in tthe same road since the road names are different for both nodes. 
            #     for location in node.locations:
            #         if location.located_on == "HIGH STREET_RD":
            #             location.located_on = "HIGH_ST"
  
            node.latitude = node.locations[0].latitude
            node.longitude = node.locations[0].longitude
            
            self.nodes.append(node)  # add the fully populated Node to the graph

            for location in node.locations:
                if location.located_on not in node.assoRoadsWithNodes:
                    node.assoRoadsWithNodes[location.located_on] = [] #list to save the road names and their nodes

                 # If the road key doesn't exist, initialize an empty list
                if location.located_on not in node.assoRoadsWithDirections:
                    node.assoRoadsWithDirections[location.located_on] = [] #list to save road names and their directions

                # Only add the direction if it's not already added
                if location.direction not in node.assoRoadsWithDirections[location.located_on]:
                    node.assoRoadsWithDirections[location.located_on].append(location.direction)  #appending the directions into roads in the list

            # print("done1")
            # for key, value_list in node.assoRoadsWithNodes.items():
            #     print(f"{key}: {value_list}")
            # print(" ")


        ##BUGFIX BUGFIX
        self.nodes.remove(next((n for n in self.nodes if n.id == 4266), None)) #BUG FIX : to remove the node with 0,0 coordinates

        for nodeSelected in self.nodes:  # to find the other nodes that are in the same roads that were connected to the specific road
            for node in self.nodes:
                # if node != nodeSelected:    #will be adding the selected node into the list as well
                    for key1 in nodeSelected.assoRoadsWithNodes:
                        for key2 in node.assoRoadsWithNodes:
                            if key2 == key1:
                                if node not in nodeSelected.assoRoadsWithNodes[key1]:
                                    nodeSelected.assoRoadsWithNodes[key1].append(node)     #{'HIGH_ST': [2846, 3001, 3662, 4030, 4321]}


        self.buildNeighbours()
        
    def buildNeighbours(self):
        latDirections = ['N','S','NW','SW','NE','SE']
        lonDirections = ['W', 'E']
        for node in self.nodes:
            for key,value in node.assoRoadsWithNodes.items():
                orderedNodes = []
                if len(value) == 1:  #if no nodes available other than the selected node on the road = no neighbours on that road
                    continue
                else: #if theres one  or more nodes other than the selected node 
                    if any(direction in node.assoRoadsWithDirections[key] for direction in latDirections):
                        orderedNodes = sorted( value, key=lambda node: node.latitude)
                    else:
                        orderedNodes = sorted(value , key=lambda node : node.longitude)
                        
                    #if the selected node is the corner node means there will be only one edge in either of the side

                    if node == orderedNodes[0]:
                        if self.heuristic(orderedNodes[0].id, orderedNodes[1].id) < 6: #BUGFIX
                            node.neighbours.append(orderedNodes[1])
                    elif node == orderedNodes[-1]:
                        if self.heuristic(orderedNodes[-1].id, orderedNodes[-2].id) < 6:  #BUGFIX
                            node.neighbours.append(orderedNodes[-2])
                    else: #if the node is in the middle and we have to get both edges from each side
                        if self.heuristic(orderedNodes[orderedNodes.index(node)-1].id, node.id) < 6:   #BUGFIX
                            node.neighbours.append(orderedNodes[orderedNodes.index(node)-1])
                        if self.heuristic(orderedNodes[orderedNodes.index(node)+1].id, node.id) < 6:   #BUGFIX
                            node.neighbours.append(orderedNodes[orderedNodes.index(node)+1])

                    for neighbour in node.neighbours: #checking whether all the neighbours are reachable with AVAILABLE traffic data
                        if (self.usingAddress(node, neighbour) is not None) and (self.usingAddress(neighbour, node) is not None):
                            continue
                        else:
                            node.neighbours.remove(neighbour) #will have to remove the neighbour if there are no traffic data available to calc the costs to travel


    def usingAddress(self,currentNode, nextNode): #to get the location address of the camera to get the traffic flow the road that path gonna use 
        latDirections = ['N','S','NW','SW','NE','SE']
        latInc = ['N', 'NW', 'NE']
        latDec = ['S', 'SW', 'SE']

        for key,value in currentNode.assoRoadsWithNodes.items():
            if nextNode.id in [node.id for node in value]:
                if any(item in latDirections for item in currentNode.assoRoadsWithDirections[key]):
                    if currentNode.latitude < nextNode.latitude :
                        for location in currentNode.locations:
                            if location.located_on == key and (location.direction in latInc):
                                return (location.name)
                    else :
                        for location in currentNode.locations:
                            if location.located_on == key and (location.direction in latDec):
                                return (location.name)
                else:
                    if currentNode.longitude < nextNode.longitude :
                        for location in currentNode.locations:
                            if location.located_on == key and location.direction=='E':
                                return (location.name)
                    else :
                        for location in currentNode.locations:
                            if location.located_on == key and location.direction=='W':
                                return (location.name)

    def GetMaxDepth(self, start_node):
        def dfs(node, seen):
            seen.add(node.id)
            #finding max depth through dfs starting at the passed in start node, so every max depth is a calc by starting node
            max_depth = 0
            for neighbor in node.neighbours:
                if neighbor.id not in seen:
                    depth = dfs(neighbor, seen.copy())
                    max_depth = max(max_depth, depth)
            return 1 + max_depth 

        return dfs(start_node, set())

    def heuristic(self, node_id1, node_id2):
        node1 = next((n for n in self.nodes if n.id == node_id1), None)
        node2 = next((n for n in self.nodes if n.id == node_id2), None)
        if node1 and node2:
            return haversine((node1.latitude, node1.longitude),( node2.latitude, node2.longitude))
        return float('inf')


                

# graphobj = Graph()
# node =  next((n for n in graphobj.nodes if n.id == 2200), None)

# for location in node.locations:
#     print (location.located_on)
#     print(location.direction)





# ##To test all the neighbours are reachable with available traffic details.
# graph = Graph()
# for node in graph.nodes:
#     for neighbour in node.neighbours:
#         if (graph.usingAddress(node, neighbour)== None) or (graph.usingAddress(neighbour, node) == None):
#             print(f"from {node.id} to {neighbour.id} : {graph.usingAddress(node, neighbour)} ")
#             print(f"from {neighbour.id} to {node.id} : {graph.usingAddress(neighbour, node)} ")
#             print( " ")



##To return the location address name
# node1 = next((n for n in graph.nodes if n.id == 970), None)
# node2 = next((n for n in graph.nodes if n.id == 2000), None)

# if node1 and node2:
#     graph.usingAddress(node1, node2)
# else:
#     print("One or both nodes not found in graph.")




###print test1 for nodes and edges
# for node  in graph.nodes:
#     if not node.neighbours :
#         print(f"Node id : {node.id} -> No edges are connected")
#         # print(" ")
#     else:
#         print(f"Node id : {node.id} -> Edges : {[edge.id for edge in node.neighbours]}") 
#         # print(" ")




###print test2  for


# for node in graph.nodes:
#     print(f"Node id = {node.id} ")
#     for location in node.locations:
#         print(f" road : {location.located_on} : {location.direction}")
#     for key , value in node.assoRoadsWithNodes.items():
#         print(f"{key} :{node.assoRoadsWithDirections[key]}  : {[node.id for node in value]}")
#     print(" ")

        
# #output
# Node id = 4270
#  road : GLENFERRIE_RD : N
#  road : RIVERSDALE_RD : E
#  road : GLENFERRIE_RD : S
#  road : RIVERSDALE_RD : W
# GLENFERRIE_RD :['N', 'S']  : [4270, 4324]
# RIVERSDALE_RD :['E', 'W']  : [4270, 4272]


# #To print all the details
# for node in graph.nodes:
#     print(f"Node ID: {node.id}")
#     print(f"Latitude: {node.latitude}")
#     print(f"Longitude: {node.longitude}")
#     print(f"Neighbours: {[n.id if n else None for n in node.neighbours]}")
#     print(f"Associated Roads with Nodes:")
#     for key, value in node.assoRoadsWithNodes.items():
#         print(f"  {key} : {[n.id for n in value]}")
#     print(f"Associated Roads with Directions:")
#     for key, directions in node.assoRoadsWithDirections.items():
#         print(f"  {key} : {directions}")
#     print(" ")
#     print("details of Associated Locations around the node")
#     for location in node.locations:
#         print(f"Name: {location.name}")
#         print(f"Located on: {location.located_on}")
#         print(f"Latitude: {location.latitude}")
#         print(f"Longitude: {location.longitude}")
#         print(f"Direction: {location.direction}")
#         print(f"Compared to: {location.compared_to}")
#         print(" ")
#     print(" ")
#     print(" ")
#     print(" ")

#     print(" ")


##output
# Node ID: 4821
# Latitude: -37.81285
# Longitude: 145.00849
# Neighbours: []
# Associated Roads with Nodes:
#   WALMER_ST : [4821]
#   VICTORIA_ST : [4821]
#   BURNLEY_ST : [4821]
# Associated Roads with Directions:
#   WALMER_ST : ['N']
#   VICTORIA_ST : ['E', 'W']
#   BURNLEY_ST : ['S']

# details of Associated Locations around the node
# Name: WALMER_ST N OF VICTORIA_ST
# Located on: WALMER_ST
# Latitude: -37.81285
# Longitude: 145.00849
# Direction: N
# Compared to: VICTORIA_ST

# Name: VICTORIA_ST E OF BURNLEY_ST
# Located on: VICTORIA_ST
# Latitude: -37.81293
# Longitude: 145.00865
# Direction: E
# Compared to: BURNLEY_ST

# Name: BURNLEY_ST S OF VICTORIA_ST
# Located on: BURNLEY_ST
# Latitude: -37.81312
# Longitude: 145.00844
# Direction: S


#To print the above output
# with open("node_output.txt", "w", encoding="utf-8") as f:
#     for node in graph.nodes:
#         print(f"Node ID: {node.id}", file=f)
#         print(f"Latitude: {node.latitude}", file=f)
#         print(f"Longitude: {node.longitude}", file=f)
#         print(f"Neighbours: {[n.id if n else None for n in node.neighbours]}", file=f)
#         print(f"Associated Roads with Nodes:", file=f)
#         for key, value in node.assoRoadsWithNodes.items():
#             print(f"  {key} : {[n.id for n in value]}", file=f)
#         print(f"Associated Roads with Directions:", file=f)
#         for key, directions in node.assoRoadsWithDirections.items():
#             print(f"  {key} : {directions}", file=f)
#         print(" ", file=f)
#         print("details of Associated Locations around the node", file=f)
#         for location in node.locations:
#             print(f"Name: {location.name}", file=f)
#             print(f"Located on: {location.located_on}", file=f)
#             print(f"Latitude: {location.latitude}", file=f)
#             print(f"Longitude: {location.longitude}", file=f)
#             print(f"Direction: {location.direction}", file=f)
#             print(f"Compared to: {location.compared_to}", file=f)
#             print(" ", file=f)
#         print("\n\n\n", file=f)
