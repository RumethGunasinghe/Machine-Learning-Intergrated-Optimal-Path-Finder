def importData(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    nodes = {}
    edges = {}
    start = None
    goals = []

    section = None

    for line in lines:
        line = line.strip()
        if not line: 
            continue

        if line.startswith("Nodes:"):
            section = "nodes"
            continue
        elif line.startswith("Edges:"):
            section = "edges"
            continue
        elif line.startswith("Origin:"):
            section = "origin"
            continue
        elif line.startswith("Destinations:"):
            section = "destinations"
            continue

        elif section == "nodes":
            parts = line.split(":")
            node_id = int(parts[0].strip())
            x, y = map(int, parts[1].strip().strip("()").split(","))
            nodes[node_id] = (x, y)

        elif section == "edges":
            parts = line.split(":")
            x, y = map(int, parts[0].strip().strip("()").split(","))
            node_value = int(parts[1].strip())
            edges[(x, y)] = node_value
            
        elif section == "origin":
            start = int(line.strip())

        elif section == "destinations":
            goals = list(map(int, line.replace(";", "").split()))

    return nodes, edges, start, goals
