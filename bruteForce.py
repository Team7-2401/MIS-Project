
def findMIS(graph, remaining_vertices, current_set, best_set):
    """
    Backtracking function to find the Maximum Independent Set (MIS)
    graph: dict, adjacency list representation of the graph
    remaining_vertices: list, vertices still to explore
    current_set: list, current independent set being built
    best_set: list, keeps track of the best solution found so far
    """
    # Base case: no more vertices to explore
    if not remaining_vertices:
        if len(current_set) > len(best_set[0]):
            best_set[0] = current_set[:]
        return

    # Choose a vertex to explore
    v = remaining_vertices[0]
    neighbors = graph[v]

    # Case 1: Include v in the independent set
    if all(neighbor not in current_set for neighbor in neighbors):
        current_set.append(v)
        findMIS(
            graph,
            [u for u in remaining_vertices if u != v and u not in neighbors],
            current_set,
            best_set
        )
        current_set.pop()  # Backtrack

    # Case 2: Exclude v from the independent set
    findMIS(graph, remaining_vertices[1:], current_set, best_set)


def maximum_independent_set(graph):
    """
    Wrapper function to initialize variables and call the backtracking function
    graph: dict, adjacency list representation of the graph
    """
    best_set = [[]]  # Use a list to store the best set (mutable reference)
    findMIS(graph, list(graph.keys()), [], best_set)
    return best_set[0]
