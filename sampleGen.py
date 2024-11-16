import random
import json

def generate_graph(num_vertices, edge_prob=None, num_edges=None, graph_type="undirected",
                   allow_self_loops=False, connected=True, seed=None,
                   output_format="adjacency_list"):
    """
    Generates a random graph based on specified parameters.
    
    Parameters:
    - num_vertices (int): Number of vertices in the graph.
    - edge_prob (float): Probability of creating an edge between two vertices (used if num_edges is None).
    - num_edges (int): Exact number of edges to create (overrides edge_prob).
    - graph_type (str): "undirected" (default) or "directed".
    - allow_self_loops (bool): Whether self-loops are allowed (default False).
    - connected (bool): Ensure the graph is connected (default True).
    - seed (int): Random seed for reproducibility (default None).
    
    Returns:
    - Graph representation in adjacency list format.
    """
    # Set random seed for reproducibility
    if seed is not None:
        random.seed(seed)
    
    # Initialize the graph structure
    adjacency_list = {i: [] for i in range(1, num_vertices + 1)}
    
    # Helper to add edges
    def add_edge(u, v):
        if v not in adjacency_list[u]:
            adjacency_list[u].append(v)
            if graph_type == "undirected" and u != v:
                adjacency_list[v].append(u)
    
    # Generate edges
    edges = set()
    if num_edges is not None:
        # Generate exact number of edges
        while len(edges) < num_edges:
            u, v = random.randint(1, num_vertices), random.randint(1, num_vertices)
            if not allow_self_loops and u == v:
                continue
            edges.add((u, v) if graph_type == "undirected" and u > v else (v, u))
    else:
        # Use edge probability to generate edges
        for u in range(1, num_vertices + 1):
            for v in range(1, num_vertices + 1):
                if not allow_self_loops and u == v:
                    continue
                if random.random() <= edge_prob:
                    edges.add((u, v) if graph_type == "undirected" and u > v else (v, u))
    
    # Add edges to the graph
    for u, v in edges:
        add_edge(u, v)
    
    # Ensure connectedness if required
    if connected:
        # Create a spanning tree to connect all vertices
        for i in range(2, num_vertices + 1):
            u = random.randint(1, i - 1)
            add_edge(u, i)
    
    # Return the adjacency list 
    return adjacency_list

