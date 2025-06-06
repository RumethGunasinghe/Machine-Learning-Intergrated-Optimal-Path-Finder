# AI Route-Finding System — COS30019 Assignment 2

## 📌 Overview

This Python project implements a route-finding agent that uses several classical search algorithms to find an optimal or valid path from a given origin to one or more destination nodes on a 2D graph.

The graph is specified in a simple `.txt` file format, and the program supports command-line execution for batch testing.

---

## 🧠 Supported Algorithms

| Category      | Method | Description |
|---------------|--------|-------------|
| Uninformed    | `dfs`  | Depth-First Search |
|               | `bfs`  | Breadth-First Search |
| Informed      | `gbfs` | Greedy Best-First Search |
|               | `astar`| A* Search |
| Custom        | `cus1` | Custom uninformed strategy (optional) |
|               | `cus2` | Custom informed strategy (optional) |

---

## 📁 Project Structure
Assignment2/
├── main.py # Entry point of the program
├── graph.py # Graph structure and data models
├── algorithms.py # DFS, BFS, GBFS, A*, etc.
├── importData.py # Parses input.txt into graph format
├── input.txt # Example input file (can be replaced)
└── README.md # This file


---

## 🧾 Input File Format

The input file (e.g., `input.txt`) should follow this format:
Nodes:
1: (4,1)
2: (2,2)
...

Edges:
(2,1): 4
(3,1): 5
...

Origin:
2

Destinations:
5; 4


---

## ▶️ How to Run
### Use the command line to run the script:

```BASH
python search.py <filename> <method>
Example:
python search.py input.txt astar
```
### Or use the bat file


Expected Output (when path is found):
```BASH
input.txt astar
5 9
2 → 3 → 5
```

Where:
5 is the reached goal
9 is the number of nodes created (expanded or generated)
The path shows how to go from origin to the destination

🖥 Requirements
Python 3.6+
Standard Library only (no external packages required)

🛠 Developer Notes
Paths are found toward any destination node (first one reached optimally).
If multiple nodes are equal in cost, the smaller node ID is chosen first.
If nodes are equal in all aspects, expand them in insertion (chronological) order.

🧪 Testing
You can test multiple algorithms by calling each one separately:

bash
Copy
Edit
python main.py input.txt bfs
python main.py input.txt dfs
python main.py input.txt gbfs
python main.py input.txt astar