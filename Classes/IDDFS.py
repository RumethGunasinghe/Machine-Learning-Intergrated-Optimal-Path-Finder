from models.FindTime import findTime

class IDDFS:
    def __init__(self, graph, model, TOD):
        self.graph = graph
        self.model = model
        self.TOD = TOD

    def NodeByID(self, node_id):
        return next((node for node in self.graph.nodes if node.id == node_id), None)

    def DepthLimit(self, origin, destination, limit, path, seen, totalCost):
        print(f"At node {origin.id}, depth limit = {limit}, cost = {totalCost}")

        if origin.id in seen:
            return None, float('inf')

        seen.add(origin.id)
        path.append(origin)

        if origin.id == destination.id:
            return list(path), totalCost  

        if limit <= 0:
            path.pop()
            return None, float('inf')

        for neighbor in origin.neighbours:
            if neighbor.id not in seen:
                locationAdd = self.graph.usingAddress(origin, neighbor)
                if not locationAdd:
                    print(f"no address between {origin.id} and {neighbor.id}, skipping it")
                    continue

                timeToNeighbor = findTime(locationAdd, self.model, origin, neighbor, self.TOD)
                newTotal = totalCost + timeToNeighbor

                resultPath, resultCost = self.DepthLimit(neighbor, destination, limit - 1, path, seen, newTotal)
                if resultPath:
                    return resultPath, resultCost

        path.pop()
        return None, float('inf')

    def IDDFS(self, origin, destination, maxDepth):
        for depth in range(maxDepth + 1):
            print(f"depth = {depth}")
            seen = set()
            path = []
            resultPath, cost = self.DepthLimit(origin, destination, depth, path, seen, 0)

            if resultPath:
                print("node found")
                print(", ".join(str(n.id) for n in resultPath))
                print(f"total cost {cost}")
                return resultPath, cost, depth

        print("no path found")
        return None, float("inf"), maxDepth
