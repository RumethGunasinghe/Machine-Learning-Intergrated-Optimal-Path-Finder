from flask import Flask, render_template, request, url_for
from Classes.Graph import Graph
from Classes.AStar import AStar
from Classes.GBFS import GBFS
from Classes.DFS import DFS
from Classes.BFS import BFS
from Classes.IDDFS import IDDFS
from Classes.HillClimbing import HillClimbing
from mapDraw import draw_interactive_map
import os
import shutil

app = Flask(__name__)
STATIC_FOLDER = "static"
EMPTY_MAP = os.path.join(STATIC_FOLDER, "empty_map.html")
MAP_WITH_PATH = os.path.join(STATIC_FOLDER, "map.html")

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    map_file = "empty_map.html"  # default
    graph = Graph()
    node_ids = [str(n.id) for n in graph.nodes]
    if request.method == "POST":
        algorithm = request.form["algorithm"]
        model = int(request.form["model"])
        origin = request.form["origin"]
        destination = request.form["destination"]
        time_of_day = request.form["time"]


        node1 = next((n for n in graph.nodes if str(n.id) == origin), None)
        node2 = next((n for n in graph.nodes if str(n.id) == destination), None)

        print(f"Origin is {origin}")

        
        if not node1 or not node2:
            result = {"error": "Origin or destination node not found."}
        elif node1 == node2:
            result = {"error": "Both Origin and Destination IDs are same"}
        else:
            if algorithm == "AStar":
                astar = AStar(graph, model, time_of_day)
                path = astar.find_path(node1.id, node2.id)
                if path:
                    eta = node2.g + (0.5 * len(path))
                    draw_interactive_map(graph.nodes, path, file_path=MAP_WITH_PATH)
                    result = {
                        "Search Algorithm" : algorithm,
                        "Data Model" :model,
                        "Origin" : origin,
                        "Destination" : destination,
                        "path": [n.id for n in path],
                        "eta": eta
                    }
                    map_file = "map.html"  # show path map
                else:
                    result = {
                        "Search Algorithm" : algorithm,
                        "Data Model" :model,
                        "Origin" : origin,
                        "error": f"Goal {node2.id} couldn't be reached from origin {node1.id}"}

            if algorithm == "GBFS":
                gbfs = GBFS(graph, model, time_of_day)
                path = gbfs.find_path(node1.id, node2.id)
                if path:
                    eta = node2.g + (0.5 * len(path))
                    draw_interactive_map(graph.nodes, path, file_path=MAP_WITH_PATH)
                    result = {
                        "Search Algorithm" : algorithm,
                        "Data Model" :model,
                        "Origin" : origin,
                        "Destination" : destination,
                        "path": [n.id for n in path],
                        "eta": eta
                    }
                    map_file = "map.html"  # show path map
                else:
                    result = {
                        "Search Algorithm" : algorithm,
                        "Data Model" :model,
                        "Origin" : origin,
                        "error": f"Goal {node2.id} couldn't be reached from origin {node1.id}"}

            if algorithm == "DFS":
                dfs = DFS(graph, model, time_of_day )
                start = dfs.NodeByID(int(origin))
                goal = dfs.NodeByID(int(destination))
                path, cost = dfs.DepthFirstSearch(start, goal)

                if path:
                    eta = cost + (0.5 * len(path))
                    draw_interactive_map(graph.nodes, path, file_path=MAP_WITH_PATH)
                    result = {
                        "Search Algorithm" : algorithm,
                        "Data Model" :model,
                        "Origin" : origin,
                        "Destination" : destination,
                        "path": [n.id for n in path],
                        "eta": eta
                    }
                    map_file = "map.html"  # show path map
                else:
                    result = {
                        "Search Algorithm" : algorithm,
                        "Data Model" :model,
                        "Origin" : origin,
                        "error": f"Goal {node2.id} couldn't be reached from origin {node1.id}"}

            if algorithm == "CUS1":
                iddfs = IDDFS(graph, model, time_of_day)
                start = iddfs.NodeByID(int(origin))
                goal = iddfs.NodeByID(int(destination))
                path, cost, maxDepth = iddfs.IDDFS(start, goal, graph.GetMaxDepth(start))

                if path:
                    eta = cost + (0.5 * len(path))
                    draw_interactive_map(graph.nodes, path, file_path=MAP_WITH_PATH)
                    result = {
                        "Search Algorithm" : algorithm + " - IDDFS",
                        "Data Model" :model,
                        "Origin" : origin,
                        "Destination" : destination,
                        "path": [n.id for n in path],
                        "eta": eta,
                        "Max Depth": maxDepth
                    }
                    map_file = "map.html"  # show path map
                else:
                    result = {
                        "Search Algorithm" : algorithm,
                        "Data Model" :model,
                        "Origin" : origin,
                        "error": f"Goal {node2.id} couldn't be reached from origin {node1.id}"}

            if algorithm == "BFS":
                bfs = BFS(graph, model, time_of_day)
                path , cost = bfs.BreadthFirstSearch(node1, node2)

                if path:
                    eta = cost + (0.5 * len(path))
                    draw_interactive_map(graph.nodes, path, file_path=MAP_WITH_PATH)
                    result = {
                        "Search Algorithm" : algorithm,
                        "Data Model" :model,
                        "Origin" : origin,
                        "Destination" : destination,
                        "path": [n.id for n in path],
                        "eta": eta
                    }
                    map_file = "map.html"  # show path map
                else:
                    result = {
                        "Search Algorithm" : algorithm,
                        "Data Model" :model,
                        "Origin" : origin,
                        "error": f"Goal {node2.id} couldn't be reached from origin {node1.id}"}

            if algorithm == "CUS2":
                hillClimbing = HillClimbing(graph, model, time_of_day)
                path , cost = hillClimbing.HillClimbingSearch(node1, node2)
                if path[-1] != node2:
                    eta = cost + (0.5 * len(path))
                    draw_interactive_map(graph.nodes, path, file_path=MAP_WITH_PATH)
                    result = {
                        "error": f"Goal {node2.id} couldn't be reached from origin {node1.id}",
                        "Search Algorithm" : algorithm + " - HillClimbing",
                        "Data Model" :model,
                        "Origin" : origin,
                        "Destination" : destination,
                        "Got Stuck at" : path[-1].id,
                        "path up to reached goal": [n.id for n in path],
                        "eta": eta
                    }
                    map_file = "map.html"  # show path map
                else:
                    eta = cost + (0.5 * len(path))
                    draw_interactive_map(graph.nodes, path, file_path=MAP_WITH_PATH)
                    result = {
                        "Search Algorithm" : algorithm + " - HillClimbing",
                        "Data Model" :model,
                        "Origin" : origin,
                        "Destination" : destination,
                        "path": [n.id for n in path],
                        "eta": eta
                    }
                    map_file = "map.html"  # show path map




    return render_template("index.html", result=result, map_file=map_file, node_ids=node_ids)


if __name__ == "__main__":
    # On first run, generate empty map if not exists
    if not os.path.exists(EMPTY_MAP):
        draw_interactive_map([], path=None, file_path=EMPTY_MAP)

    app.run(debug=True)