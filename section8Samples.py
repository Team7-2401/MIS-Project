import pandas as pd
import sampleGen
import os

print("starting to generate tests")
df = pd.DataFrame(columns=['Test', 'Vertices', 'Edge Probability', 'filename'])

print("first batch")
# empty graph, one vertex, 5 vertices, and 50 vertices
emptyGraph = sampleGen.generate_graph(0, 0.4)
oneVertex = sampleGen.generate_graph(1, 0.4)
fiveVertices = sampleGen.generate_graph(5, 0.4)
fiftyVertices = sampleGen.generate_graph(50, 0.4)

#Graph with no edges
graphNoEdges = sampleGen.generate_graph(5, 0)

#Graph disconnected
graphDisconnected = sampleGen.generate_graph(5, 0.4, connected=False)

#Graph with all edges
graphAllEdges = sampleGen.generate_graph(10, 1)

graphs = [emptyGraph, oneVertex, fiveVertices, fiftyVertices, graphNoEdges, graphDisconnected, graphAllEdges]
names = ["emptyGraph", "oneVertex", "fiveVertices", "fiftyVertices", "graphNoEdges", "graphDisconnected", "graphAllEdges"]

# Save the graphs

if not os.path.exists("8"):
    os.makedirs("8")

for graph, name in zip(graphs, names):
    with open(f"8/{name}.txt", "w") as f:
        f.write("graph= { \n")
        for node, neighbors in graph.items():
            f.write(f"\t{node}: {neighbors}\n")
        f.write("}\n")
