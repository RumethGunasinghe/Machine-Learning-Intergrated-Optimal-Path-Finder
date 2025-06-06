from Classes.Graph import Graph
from Classes.AStar import AStar
from Classes.GBFS import GBFS
from Classes.DFS import DFS
from Classes.BFS import BFS
from Classes.IDDFS import IDDFS
from Classes.HillClimbing import HillClimbing



origin = 970
reachableDest2820 = 2820
unreachableDest2827 = 2827

nodelist = [(origin, reachableDest2820), (origin, unreachableDest2827)]
time_of_day = "Morning"
searchAlgo = ["AStar", "GBFS", "DFS", "BFS", "CUS1", "CUS2"]
model = 3

with open("TESTING.txt", "w", encoding="utf-8") as f:
    for i in nodelist:
        
        for algorithm in searchAlgo:
            node1 = i[0]
            node2 = i[1]
            graph = Graph()
            result = {}

            if algorithm == "AStar":
                astar = AStar(graph, model, time_of_day)
                path = astar.find_path(node1, node2)
                node1 = next((n for n in graph.nodes if n.id == node1), None)
                node2 = next((n for n in graph.nodes if n.id == node2), None)
                if path:
                    eta = node2.g + (0.5 * len(path))
                    result = {
                        "Search Algorithm": algorithm,
                        "Data Model": model,
                        "Origin": node1.id,
                        "Destination": node2.id,
                        "Path": [n.id for n in path],
                        "ETA": eta
                    }
                else:
                    result = {
                        "Search Algorithm": algorithm,
                        "Data Model": model,
                        "Origin": node1.id,
                        "Error": f"Goal {node2.id} couldn't be reached from origin {node1.id}"
                    }

            elif algorithm == "GBFS":
                gbfs = GBFS(graph, model, time_of_day)
                path = gbfs.find_path(node1, node2)
                node1 = next((n for n in graph.nodes if n.id == node1), None)
                node2 = next((n for n in graph.nodes if n.id == node2), None)
                if path:
                    eta = node2.g + (0.5 * len(path))
                    result = {
                        "Search Algorithm": algorithm,
                        "Data Model": model,
                        "Origin": node1.id,
                        "Destination": node2.id,
                        "Path": [n.id for n in path],
                        "ETA": eta
                    }
                else:
                    result = {
                        "Search Algorithm": algorithm,
                        "Data Model": model,
                        "Origin": node1.id,
                        "Error": f"Goal {node2.id} couldn't be reached from origin {node1.id}"
                    }

            elif algorithm == "DFS":
                dfs = DFS(graph, model, time_of_day)
                start = dfs.NodeByID(int(str(node1)))
                goal = dfs.NodeByID(int(str(node2)))
                path, cost = dfs.DepthFirstSearch(start, goal)
                if path:
                    eta = cost + (0.5 * len(path))
                    result = {
                        "Search Algorithm": algorithm,
                        "Data Model": model,
                        "Origin": node1,
                        "Destination": node2,
                        "Path": [n.id for n in path],
                        "ETA": eta
                    }
                else:
                    result = {
                        "Search Algorithm": algorithm,
                        "Data Model": model,
                        "Origin": node1,
                        "Error": f"Goal {node2} couldn't be reached from origin {node1}"
                    }

            elif algorithm == "CUS1":
                iddfs = IDDFS(graph, model, time_of_day)
                start = iddfs.NodeByID(int(str(node1)))
                goal = iddfs.NodeByID(int(str(node2)))
                path, cost, maxDepth = iddfs.IDDFS(start, goal, graph.GetMaxDepth(start))
                if path:
                    eta = cost + (0.5 * len(path))
                    result = {
                        "Search Algorithm": algorithm + " - IDDFS",
                        "Data Model": model,
                        "Origin": node1,
                        "Destination": node2,
                        "Path": [n.id for n in path],
                        "ETA": eta,
                        "Max Depth": maxDepth
                    }
                else:
                    result = {
                        "Search Algorithm": algorithm,
                        "Data Model": model,
                        "Origin": node1,
                        "Error": f"Goal {node2} couldn't be reached from origin {node1}"
                    }

            elif algorithm == "BFS":
                bfs = BFS(graph, model, time_of_day)
                node1 = next((n for n in graph.nodes if n.id == node1), None)
                node2 = next((n for n in graph.nodes if n.id == node2), None)
                path, cost = bfs.BreadthFirstSearch(node1, node2)
                if path:
                    eta = cost + (0.5 * len(path))
                    result = {
                        "Search Algorithm": algorithm,
                        "Data Model": model,
                        "Origin": node1.id,
                        "Destination": node2.id,
                        "Path": [n.id for n in path],
                        "ETA": eta
                    }
                else:
                    result = {
                        "Search Algorithm": algorithm,
                        "Data Model": model,
                        "Origin": node1.id,
                        "Error": f"Goal {node2.id} couldn't be reached from origin {node1.id}"
                    }

            elif algorithm == "CUS2":
                hillClimbing = HillClimbing(graph, model, time_of_day)
                node1 = next((n for n in graph.nodes if n.id == node1), None)
                node2 = next((n for n in graph.nodes if n.id == node2), None)
                path, cost = hillClimbing.HillClimbingSearch(node1, node2)
                if path[-1].id != node2:
                    eta = cost + (0.5 * len(path))
                    result = {
                        "Error": f"Goal {node2} couldn't be reached from origin {node1}",
                        "Search Algorithm": algorithm + " - HillClimbing",
                        "Data Model": model,
                        "Origin": node1.id,
                        "Destination": node2.id,
                        "Got Stuck at": path[-1].id,
                        "Path up to reached goal": [n.id for n in path],
                        "ETA": eta
                    }
                else:
                    eta = cost + (0.5 * len(path))
                    result = {
                        "Search Algorithm": algorithm + " - HillClimbing",
                        "Data Model": model,
                        "Origin": node1.id,
                        "Destination": node2.id,
                        "Path": [n.id for n in path],
                        "ETA": eta
                    }

            # Write result to file
            f.write(f"{'-'*40}\n")
            f.write(f"Test case: {node1} -> {node2} using {algorithm}\n")
            for key, value in result.items():
                f.write(f"{key}: {value}\n")
            f.write(f"{'-'*40}\n\n")
