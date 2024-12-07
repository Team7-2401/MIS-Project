def validate_independent_set(graph, independent_set):
    """
    Validate whether a given set is an independent set.
    :param graph: Dictionary representing the adjacency list of the graph {node: [neighbors]}.
    :param independent_set: Set of vertices representing the independent set.
    :return: Boolean result indicating whether it is a valid independent set.
    """
    for vertex in independent_set:
        # Check if any neighbor of the vertex is also in the independent set
        for neighbor in graph.get(vertex, []):
            if neighbor in independent_set:
                return False
    return True
