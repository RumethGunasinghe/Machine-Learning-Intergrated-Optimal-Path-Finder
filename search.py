from importData import importData
from node import Node
from graph import Graph
from graphBFS import GraphBFS
import algorithms
import sys

def printPath(path, filename, method, goalfound):
    if(goalfound == None):
        print("No Path found")
    else:
        number_of_nodes = len(path)
        print(f"{filename} {method}")
        print(f"{goalfound} {number_of_nodes}")
        print(f"{path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python search.py <filename> <method>")
        sys.exit(1)

    filename = sys.argv[1]
    method = sys.argv[2].upper()

    nodes, edges, start, goals = importData(filename)
    graphObj = Graph( nodes, edges, start, goals)

    if method == "AS":
        goalfound, path = algorithms.As(graphObj)
        printPath(path, filename, method, goalfound)

    elif method == "GBFS":
        goalfound, path =  algorithms.GBFS(graphObj)
        printPath(path, filename, method, goalfound)

    elif method == "DFS":
        nodeDF = Node(start, graphObj.nodes[start])
        goalfound, path = algorithms.DFS(nodeDF, graphObj)
        printPath(path, filename, method, goalfound)

    elif method == "BFS":
        graphBFS = GraphBFS.create_graph(nodes, edges)
        goalfound, path = algorithms.BFS(start, goals, graphBFS)
        printPath(path, filename, method, goalfound)

    elif method == "CUS1":
        nodeDFF = Node(start,  graphObj.nodes[start])
        goalfound, path = algorithms.cus1(nodeDFF, graphObj)
        printPath(path, filename, method, goalfound)

    elif method == "CUS2":
        graphBFS = GraphBFS.create_graph(nodes, edges)
        goalfound, path = algorithms.cus2(start, goals, graphBFS)
        printPath(path, filename, method, goalfound)

    else:
        print(f"Unknown method: {method}")
        

#Below is a code for testing. it will run through all 10 input#.txt files 
#through all the search methods and save the output to a text file named as
#search_results.txt


# if __name__ == "__main__":
#     input_files = [f"input{i}.txt" for i in range(1, 11)]
#     methods = ["AS", "GBFS", "DFS", "BFS", "CUS1", "CUS2"]

#     with open("search_results.txt", "w") as f:
#         for filename in input_files:
#             nodes, edges, start, goals = importData(filename)
#             graphObj = Graph(nodes, edges, start, goals)

#             for method in methods:
#                 f.write(f"\nRunning {method} on {filename}\n")

#                 if method == "AS":
#                     goalfound, path = algorithms.As(graphObj)

#                 elif method == "GBFS":
#                     goalfound, path = algorithms.GBFS(graphObj)

#                 elif method == "DFS":
#                     nodeDF = Node(start, graphObj.nodes[start])
#                     goalfound, path = algorithms.DFS(nodeDF, graphObj)

#                 elif method == "BFS":
#                     graphBFS = GraphBFS.create_graph(nodes, edges)
#                     goalfound, path = algorithms.BFS(start, goals, graphBFS)

#                 elif method == "CUS1":
#                     nodeDFF = Node(start, graphObj.nodes[start])
#                     goalfound, path = algorithms.cus1(nodeDFF, graphObj)

#                 elif method == "CUS2":
#                     graphBFS = GraphBFS.create_graph(nodes, edges)
#                     goalfound, path = algorithms.cus2(start, goals, graphBFS)

#                 else:
#                     f.write(f"Unknown method: {method}\n")
#                     continue


#                 if goalfound is None:
#                     f.write("No Path found\n")
#                 else:
#                     number_of_nodes = len(path)
#                     f.write(f"{filename} {method}\n")
#                     f.write(f"{goalfound} {number_of_nodes}\n")
#                     f.write(f"{path}\n")
