from node import Node
import math
from collections import defaultdict


class Graph:
    def __init__(self, nodes, edges, start, goal):
        self.nodes = {n: Node(n, pos) for n, pos in nodes.items()}
        self.edges = edges
        self.start = self.nodes[start]
        self.goals = [self.nodes[g] for g in goal]

        self.closed_list = set()
        self.open_list = []

        self.open_list.append(self.start)
        self.max_depth = max([value[0] for value in nodes.values()])
        start = self.start
        goals = self.goals

        self.start.g = 0
        self.start.f = min(self.heuristic(start, goal) for goal in goals)

        self.import_edges = defaultdict(list)
        self.buildEdges()

    def buildEdges(self):
        for start, end in self.edges:
            self.import_edges[start].append(end)   


    def heuristic(self, node, goal):
            x1, y1 = node.position  
            x2, y2 = goal.position
            # print(f"Heurist for {goal.id} from {node.id} is : {math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)}")
            return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)