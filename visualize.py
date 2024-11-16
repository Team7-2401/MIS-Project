import networkx as nx
import matplotlib.pyplot as plt

def visualize_graph(graph, independent_set=None, filename="sample"):
    """
    Visualizes the graph using NetworkX and Matplotlib.
    
    Parameters:
    - graph: dict, adjacency list representation of the graph
    - independent_set: list, (optional) vertices in the maximum independent set to highlight
    """
    # Create a NetworkX graph from the adjacency list
    G = nx.Graph()
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            G.add_edge(node, neighbor)

    # Set up node colors
    node_colors = []
    for node in G.nodes():
        if independent_set and node in independent_set:
            node_colors.append("lightgreen")  # Highlight independent set nodes
        else:
            node_colors.append("lightblue")

    # Draw the graph
    pos = nx.spring_layout(G)  # Spring layout for aesthetics
    plt.figure(figsize=(8, 6))
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color=node_colors,
        node_size=800,
        font_size=10,
        edge_color="gray"
    )
    plt.title("Graph Visualization" + (" with Maximum Independent Set" if independent_set else ""))

    #Save the plot into plots folder
    plt.savefig(f'plots/{filename}.png', dpi=300)
    #plt.show()

