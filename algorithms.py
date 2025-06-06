from node import Node
from graph import Graph
from myQueue import Queue
from graphBFS import GraphBFS



def As(Graph):
        while Graph.open_list:
            # print("Open list:", [node.id for node in Graph.open_list])
            # Sort open list based on the f value (best path so far)
            Graph.open_list.sort(key=lambda node: node.f)

            current_node = Graph.open_list.pop(0)
            # print(f"owest f: {current_node.id}, Position: {current_node.position}, f: {current_node.f}")
  
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
        return None, None

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
    return None, None

def DFS(node: Node, graph: Graph):
    node.seen.add(node.id)
    node.path.append(node.id)

    neighbors = graph.import_edges[node.id]

    if any(goal.id == node.id for goal in graph.goals):
        return (node.id, node.path)

    for neighbor in neighbors:
        if neighbor not in node.seen:
            neighbor_node = Node(neighbor, graph.nodes[neighbor])
            neighbor_node.seen = node.seen.copy()  
            neighbor_node.path = node.path.copy()  
            result = DFS(neighbor_node, graph)
            if result is not None:
                return result
            else:
                 return None, None

def BFS( origin, destinations, graph):
    """Finds the shortest path from origin to any one destination."""
    shortest_path = None
    shortest_cost = float('inf')

    # Iterate over each destination to find the shortest path
    for destination in destinations:
        path, cost = bfs(origin, destination, graph)
        if path and cost < shortest_cost:
            shortest_cost = cost
            shortest_path = path
            goalFound = destination

    if shortest_path:
        return (goalFound, path)
        # print(f"Shortest path from {origin} to one of the destinations {destinations}: {shortest_path}")
        # print(f"Total cost: {shortest_cost}")
    else:
        return None, None
        
def bfs(start, goal, graph):
        queue = Queue()
        queue.enqueue((start, [start], 0))  # (node, path, total_cost)
        visited = set()

        while not queue.is_empty():
            node_id, path, total_cost = queue.dequeue()

            if node_id in visited:
                continue
            visited.add(node_id)

            if node_id == goal:
                return path, total_cost 

            for neighbor, cost in graph.get_node(node_id).edges.items():
                if neighbor not in visited:
                    queue.enqueue((neighbor, path + [neighbor], total_cost + cost))

        return None, float('inf')

def cus1(node: Node, graph : Graph):
        # print(f"starting node {node.id}")
        # node.seen.add(node.id)

        depth = 0

        if any(goal.id == node.id for goal in graph.goals):
            return node.id
        
        else:             
            while depth <=  graph.max_depth:
                startingNode = Node(node.id, node.position)
                startingNode.seen = set()
                node.path.append(startingNode)

                success , goalFound, pathUsed =  depthSearch(startingNode, depth, graph.max_depth , graph)
                if success:
                    return goalFound, pathUsed
                depth += 1
            return None, None

def depthSearch( node: Node, currentDepth, maxDepth, graph : Graph) -> bool:
        
        # print(f"visiting node {node.id} at the depth of {currentDepth}")

        if any(goal.id == node.id for goal in graph.goals):
            # print(f"goal found at node {node.id}, at depth of {currentDepth}")
            node.seen.add(node.id)
            node.path.append(node.id)
            return True, node.id, node.path
        
           
        
        if currentDepth >= maxDepth:
            return False, None, None
        
        else:
            node.seen.add(node.id)
            node.path.append(node.id)
            for neighbor in graph.import_edges[node.id]:
                if neighbor not in node.seen:
                    neighbor_node = Node(neighbor, neighbor)
                    neighbor_node.seen = node.seen
                    neighbor_node.path = node.path
                    success , goalFound, pathUsed = depthSearch(neighbor_node, currentDepth + 1, maxDepth, graph)
                    if success:
                        return True, goalFound, pathUsed 
            return False, None, None 

def cus2(start, goals, graph):
        if isinstance(goals, int):
            goals = [goals]

        best_path = None
        best_cost = float('inf')

        for goal in goals:
            pathFound, goalReached = find_path(start, goal , graph)
            if pathFound:
                cost = calculate_cost(pathFound, graph)
                if cost < best_cost:
                    best_cost = cost
                    best_path = pathFound
                    chosenGoal = goalReached

        if best_path:
            # print(f"Best path chosen: {best_path} with cost {best_cost}")
            return(chosenGoal, best_path)
        else:
            return None, None
        
def find_path( start, goal, graph):
        current = start
        path = [current]
        visited = set()

        while current != goal:
            visited.add(current)
            neighbors = graph.get_neighbors(current)

            # Evaluate all neighbors and sort by heuristic
            current_h = graph.heuristic(graph,current, goal)
            better_neighbors = []

            # Heuristic value debug
            #print(f"Current Node: {current}, Heuristic to goal: {current_h}")

            for neighbor_id, cost in neighbors.items():
                if neighbor_id in visited:
                    continue

                # Calculate the heuristic for the neighbor
                h = graph.heuristic(graph,neighbor_id, goal)

                # Print heuristic value of neightbor
                #print(f"Neighbor: {neighbor_id}, Heuristic: {h}")

                better_neighbors.append((neighbor_id, h))

            if not better_neighbors:
                #print("Reached local minimum or stuck.")
                #print("Partial path:", path)
                return None, None

            # Sort neighbors by heuristic value (best heuristic comes first)
            better_neighbors.sort(key=lambda x: x[1])

            # Select the best neighbor
            best_neighbor = better_neighbors[0][0]
            path.append(best_neighbor)
            current = best_neighbor
        # print(path, goal)
        return (path, goal)

def calculate_cost(path, graph):
        cost = 0
        for i in range(len(path) - 1):
            node = graph.get_node(path[i])
            next_node = graph.get_node(path[i + 1])
            # Get the cost from current node to next node
            cost += node.edges.get(next_node.node_id, float('inf'))
        return cost

def reconstruct_path(node, start, goals):
    path = []
    count = 0
    cheapest_goal = node.id
    while node:
        path.append(node.id)
        count = count + 1
        node = node.parent
    path = path[::-1]
    return(cheapest_goal, path )
    # print(" ")
    # print(f"start : {start}")
    # print(f"Goals :  {goals}")
    # print(f"Cheapest goal to arrive: {cheapest_goal}")
    # print((f"Path :  {path}"))
    # print("")