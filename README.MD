-------USAGE------

1. RUN the main file on virtual environment with all the requirements installed. (ver 3.10.11)
2. open the local server link which was created and printed on the terminal.
3. Select the input options. and click predict. it may take some time to display the output and reload the map
4. afterwards you can reuse the gui without having to re-run the program.


![Web Application Interface](testing/Screenshot%202025-06-06%20215134.png)
![Web Application Interface](testing/Screenshot%202025-06-06%20215300.png)








# Graph Class README

The `Graph` class is designed to model a network of traffic nodes based on data from a CSV file containing location and road information. This structure is useful for traffic analysis, route planning, and simulation of traffic flow, especially in contexts like SCATS (Sydney Coordinated Adaptive Traffic System) where intersections and roads are represented as nodes and edges. The class organizes nodes, their associated roads, directions, and neighbors to allow efficient navigation and distance calculations.

---

### Initialization and Data Loading (`__init__`)

When a `Graph` object is created, its primary task is to load all node and location data from a CSV file and organize this data into meaningful structures. The constructor reads the CSV, groups locations by their SCATS node numbers, and creates `Node` objects representing each traffic node. Each node is assigned its geographical coordinates (latitude and longitude) based on the first location associated with it.

Besides loading basic data, the constructor builds mappings to relate roads to nodes and to directions, allowing the graph to understand which roads connect which nodes and the possible travel directions on those roads. The method also includes a data-cleanup step to remove invalid nodes, such as nodes with zero coordinates, which might represent bad data entries.

Finally, the constructor calls `buildNeighbours()` to establish neighbor relationships between nodes, essential for pathfinding and traffic flow analysis.

---

### Building Neighbor Relationships (`buildNeighbours`)

Once nodes are loaded, the graph needs to understand how they connect — that is, which nodes are neighbors and can be directly traveled between. The `buildNeighbours()` method uses the road and direction mappings created during initialization to identify neighbors along the same roads.

For each road associated with a node, the method sorts all nodes on that road by their geographic location, considering either latitude or longitude depending on the road’s travel direction. This ordering allows it to identify adjacent nodes along the road.

Nodes at the ends of roads get at most one neighbor, while those in the middle get neighbors on both sides, but only if they are within a reasonable distance threshold (6 km). Additionally, the method verifies that traffic data exists between candidate neighbor nodes by calling `usingAddress()`. If no traffic data is available for a road segment, the neighbor relationship is removed to avoid creating invalid connections.

---

### Verifying Traffic Data on Road Segments (`usingAddress`)

The method `usingAddress(currentNode, nextNode)` checks if there is actual traffic camera data available for the road segment connecting two nodes. It returns the name of the location address associated with that segment if found to feed into data models to get the predicted traffic values of the road that will be used.

This method works by first ensuring both nodes share at least one common road. It then calculates the direction of travel between the nodes by comparing their coordinates and matches this direction with the node’s direction list. If a match is found, it returns the corresponding location name representing a traffic camera address.

If no valid data is found for the segment, the method returns `None`, signaling that the road segment should not be considered connected for traffic data purposes. This check is critical during neighbor-building to ensure the graph only contains edges supported by real traffic information.

---

### Calculating Maximum Depth in the Graph (`GetMaxDepth`)

The `GetMaxDepth(start_node)` method performs a depth-first search starting from a given node to find the longest path reachable without revisiting nodes. This measure of "maximum depth" reflects the maximum number of nodes that can be visited in sequence from the start node.

This recursive method tracks visited nodes to avoid cycles and explores all neighbors, returning the longest depth found plus one for the current node. This functionality is useful in understanding the extent of connectivity and the longest route possible starting from a specific traffic node.

---

### Estimating Distance Between Nodes (`heuristic`)

The `heuristic(node_id1, node_id2)` method provides an estimate of the physical distance between two nodes using their geographic coordinates. It retrieves the nodes by their IDs and applies the Haversine formula to calculate the great-circle distance in kilometers between their latitude and longitude.

If either node ID does not exist in the graph, the method returns infinity (`float('inf')`), indicating an invalid or unreachable distance. This heuristic is typically used in pathfinding algorithms like A* to estimate travel costs between nodes in the graph.

---

In summary, the `Graph` class provides comprehensive support for constructing a traffic node network from raw location data, establishing neighbor relationships with traffic data validation, and performing useful graph operations such as depth measurement and distance estimation, all critical for traffic modeling and routing applications.












# Node Class README

The `Node` class represents a traffic control node (such as an intersection or a traffic signal location) in a traffic network graph. Each node aggregates one or more `Location` objects that provide detailed geographic and traffic-related data for that node. This class forms the fundamental building block of the `Graph` structure used to model traffic flow and route analysis.

---

### Initialization (`__init__`)

When a `Node` instance is created, it requires a unique identifier (`node_id`) to distinguish it within the graph. The constructor initializes several attributes:

- **ID**: A unique identifier for the node.
- **Locations**: An initially empty list to hold associated `Location` objects. These represent different traffic monitoring points or cameras linked to this node.
- **Latitude and Longitude**: These store the geographical coordinates of the node. Initially set to zero but typically assigned based on the first associated `Location`.
- **Neighbours**: A list to hold references to neighboring `Node` objects connected via roads. This is essential for pathfinding and network traversal.
- **Associated Roads with Nodes (`assoRoadsWithNodes`)**: A dictionary mapping road names to lists of nodes on those roads, facilitating road-based navigation.
- **Associated Roads with Directions (`assoRoadsWithDirections`)**: A dictionary mapping roads to the possible travel directions, supporting directional routing.

Additionally, the `Node` class contains fields useful for graph search algorithms like A*:

- **g**: Cost from the start node to this node (default 0).
- **f**: Estimated total cost from start node to goal through this node (initialized to infinity).
- **h**: Heuristic estimate from this node to the goal node.
- **parent**: A reference to the previous node on the optimal path, useful for reconstructing paths after search.
- **seen**: A list to keep track of visited nodes during traversal.
- **path**: A list representing the current path during search.

---

This class serves as the core entity for modeling nodes in traffic networks, storing geographic and connectivity data and supporting algorithms for routing and traffic analysis.










# Location Class README

The `Location` class models a single traffic monitoring point, such as a SCATS detector, camera, or sensor, which is associated with a specific geographic coordinate and traffic direction. Locations are typically aggregated under `Node` objects to form a more complete representation of an intersection or traffic control site within a traffic network graph.

---

### Initialization (`__init__`)

When a `Location` object is instantiated, it accepts the following parameters:

- **name**: The identifier or label for this location (e.g., a SCATS site code). The `.strip()` method is applied to remove any leading/trailing whitespace.
- **latitude**: A float representing the geographic latitude of the location.
- **longitude**: A float representing the geographic longitude of the location.
- **direction**: A string indicating the direction of traffic at this monitoring point (e.g., Northbound, Eastbound, etc.).
- **located_on**: A string representing the name of the road this location is physically situated on. `.strip()` ensures clean formatting.
- **compared_to**: A string describing the relative position or relation of this location to another (e.g., “North of Intersection X”). `.strip()` is used for formatting consistency.

These fields provide a comprehensive view of the spatial and directional context of the location, useful for detailed analysis and pathfinding.

---
