from node import Node
from graph import Graph

def As(Graph):
        while Graph.open_list:
            # print("Open list:", [node.id for node in Graph.open_list])
            # Sort open list based on the f value (best path so far)
            Graph.open_list.sort(key=lambda node: node.f)

            current_node = Graph.open_list.pop(0)
            # print(f"owest f: {current_node.id}, Position: {current_node.position}, f: {current_node.f}")
            print(" ")
 
            if current_node in Graph.goals:
                return reconstruct_path(current_node, Graph.start.id, [g.id for g in Graph.goals] )

            Graph.closed_list.add(current_node.id)

            # Iterate over edges and update neighbors
            for (src, dest), cost in Graph.edges.items():
                if src == current_node.id:
                    neighbor = Graph.nodes[dest]

                    if neighbor.id in Graph.closed_list:
                        continue

                    tentative_g = current_node.g + cost

                    if tentative_g < neighbor.g:
                        neighbor.g = tentative_g
                        neighbor.f = neighbor.g + min(Graph.heuristic(neighbor, goal) for goal in Graph.goals)
                        neighbor.parent = current_node

                        if neighbor not in Graph.open_list:
                            Graph.open_list.append(neighbor)

        print("No path found")
        return ("No path found")

def GBFS(Graph):
    while Graph.open_list:
            # Sort open list based on the f value (best path so far)
            Graph.open_list.sort(key=lambda node: node.f)
            current_node = Graph.open_list.pop(0)

            if current_node in Graph.goals:
                return reconstruct_path(current_node, Graph.start.id, [g.id for g in Graph.goals] )

            Graph.closed_list.add(current_node.id)

            # Iterate over edges and update neighbors
            for (src, dest), cost in Graph.edges.items(): # src is x, dest is y, cost is node_value
                if src == current_node.id: # check for neighbours for a specific node
                    neighbor = Graph.nodes[dest] # neighbour is "absorbing" the attributes of the 'dest' node
                    if neighbor.id in Graph.closed_list: # so it doesn't back track
                        continue
                    tenative_f = min(Graph.heuristic(neighbor, goal) for goal in Graph.goals)
                    # * print(tenative_f)
                    if tenative_f < neighbor.f:
                        neighbor.f = tenative_f
                        neighbor.parent = current_node
                        if neighbor not in Graph.open_list:
                            Graph.open_list.append(neighbor)

    return "No goal found", "No path found"

def DFS(node: Node , graph : Graph):
        print(f" starting node {node.id}")
        node.seen.add(node.id)

        neighbors = graph.import_edges[node.id]
        print(f"neighbors of {node.id}: are {neighbors}")
        
        if any(goal.id == node.id for goal in graph.goals):
            return print(f"node goal reached {node.id}")
        
        else:
            for neighbor in neighbors:
                if neighbor not in node.seen:
                    node.seen.add(neighbor)
                    
                    neighbor_node = Node(neighbor, neighbor)
                    neighbor_node.seen = node.seen
                    return DFS(neighbor_node, graph)


def cus1(node: Node, graph : Graph):
        print(f"starting node {node.id}")
        node.seen.add(node.id)

        depth = 0

        if any(goal.id == node.id for goal in graph.goals):
            return node.id
        
        else:             
            while depth <=  graph.max_depth:
                startingNode = Node(node.id, node.position)
                startingNode.seen = set()

                found =  depthSearch(startingNode, depth, graph.max_depth , graph)
                if found ==  True:
                    return 
                depth += 1

#depth search used for cus1
def depthSearch( node: Node, currentDepth, maxDepth, graph : Graph) -> bool:
        
        print(f"visiting node {node.id} at the depth of {currentDepth}")

        if any(goal.id == node.id for goal in graph.goals):
            print(f"goal found at node {node.id}, at depth of {currentDepth}")
            return True
        
        if currentDepth >= maxDepth:
            print("not found within depth")
            return False
        
        else:
            node.seen.add(node.id)
            for neighbor in graph.import_edges[node.id]:
                if neighbor not in node.seen:
                    neighbor_node = Node(neighbor, neighbor)
                    neighbor_node.seen = node.seen
                    if depthSearch(neighbor_node, currentDepth + 1, maxDepth, graph):
                        return True
            return False

     

def reconstruct_path(node, start, goals):
    path = []
    cheapest_goal = node.id
    while node:
        path.append(node.id)
        node = node.parent
    path = path[::-1]
    print(" ")
    print(f"start : {start}")
    print(f"Goals :  {goals}")
    print(f"Cheapest goal to arrive: {cheapest_goal}")
    print((f"Path :  {path}"))
    print("")