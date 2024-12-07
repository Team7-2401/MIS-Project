class DisassembleAlgorithm:
    def __init__(self, graph):
        """
        Initialize the algorithm with the input graph.
        :param graph: Dictionary representing the adjacency list of the graph {node: [neighbors]}.
        """
        self.graph = graph
        self.independent_set = set()
        self.alpha = 0

    def update_adjacency_matrix(self, graph, vertices_to_remove):
        """
        Update the adjacency matrix by removing the given vertices and their edges.
        :param graph: The current graph (adjacency list).
        :param vertices_to_remove: List of vertices to remove.
        :return: Updated adjacency list.
        """
        for vertex in vertices_to_remove:
            if vertex in graph:
                # Remove vertex and its neighbors
                neighbors = graph.pop(vertex, [])
                for neighbor in neighbors:
                    if neighbor in graph:
                        graph[neighbor] = [n for n in graph[neighbor] if n != vertex]
        return graph

    def disassemble(self):
        """
        Implements the Disassemble Algorithm to find the maximal independent set.
        :return: The maximal independent set (I*) and its cardinality (alpha).
        """
        # Step 1: Work on a copy of the graph to preserve the original
        remaining_graph = {node: list(neighbors) for node, neighbors in self.graph.items()}

        for i in self.graph:
            # Step 2: Initialize independent set for this iteration
            current_set = set()
            remaining_graph = {node: list(neighbors) for node, neighbors in self.graph.items()}

            # Add initial vertex and its neighbors if feasible
            current_set.add(i)
            neighbors = remaining_graph.pop(i, [])
            remaining_graph = self.update_adjacency_matrix(remaining_graph, neighbors)

            while remaining_graph:
                # Step 3: Find vertex with maximum degree
                max_degree_vertex = max(remaining_graph, key=lambda v: len(remaining_graph[v]))

                # Add max degree vertex and its neighbors if feasible
                current_set.add(max_degree_vertex)
                neighbors = remaining_graph.pop(max_degree_vertex, [])
                remaining_graph = self.update_adjacency_matrix(remaining_graph, neighbors)

            # Post-processing: Add vertices that do not make the solution infeasible
            for vertex, neighbors in self.graph.items():
                if vertex not in current_set and all(neighbor not in current_set for neighbor in neighbors):
                    current_set.add(vertex)

            # Step 4: Check if the new independent set is larger
            if len(current_set) > self.alpha:
                self.independent_set = current_set
                self.alpha = len(current_set)

        return self.independent_set, self.alpha