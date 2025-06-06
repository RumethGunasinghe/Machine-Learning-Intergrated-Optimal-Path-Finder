from importData import importData
from node import Node
from graph import Graph
import algorithms
import sys




if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python main.py <c> <method>")
        sys.exit(1)

    filename = sys.argv[1]
    method = sys.argv[2].lower()

    nodes, edges, start, goals = importData(filename)
    nodeDF = Node(start, start)
    graphObj = Graph( nodes, edges, start, goals)

    if method == "as":
        algorithms.As(graphObj)
    elif method == "gbfs":
        algorithms.GBFS(graphObj)
    elif method == "dfs":
        algorithms.DFS(nodeDF, graphObj)
    elif method == "cus1":
        algorithms.cus1(nodeDF, graphObj)
    # elif method == "cus2":
    #     algorithms.cus2(graphObj)
    #elif method == "bfs":
    #     algorithms.BFS(graphObj)
    else:
        print(f"Unknown method: {method}")


#uncommment to run inside the IDE

# nodes, edges, start, goals = importData(filename)
# nodeDF = Node(start, start)
# graphObj = Graph( nodes, edges, start, goals)

# algorithms.As(graphObj)
# algorithms.GBFS(graphObj)
# algorithms.DFS(nodeDF, graphObj)
# algorithms.cus1(nodeDF, graphObj)
# algorithms.BFS(graphObj)
# algorithms.cus2(graphObj)