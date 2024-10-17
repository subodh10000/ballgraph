import igraph as ig
import matplotlib.pyplot as plt

# Function to load edges from a file and count unique nodes
def load_edges(file_path):
    edges = []
    nodes = []
    with open(file_path, 'r') as file:
        for line in file:
            node1, node2 = line.strip().split(';')
            edges.append((int(node1), int(node2)))  # Ensure node identifiers are strings
            nodes.append(int(node1))
            nodes.append(int(node2))
    return edges, len(set(nodes))

# Load edges from the file
file_path = 'connections.txt'
edges, num_nodes = load_edges(file_path)


# Create a graph from the edges and vertices
g = ig.Graph(n=num_nodes, edges=edges, directed=False)

# Plot the graph
# https://python.igraph.org/en/stable/tutorial.html#structural-properties-of-graphs
layout = g.layout_mds() 
fig, ax = plt.subplots()
ig.plot(g, layout=layout, target=ax)
plt.show()

input("Press Enter to exit...")
