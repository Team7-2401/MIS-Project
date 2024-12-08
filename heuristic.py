import verify

class DisassembleAlgorithm:
    def __init__(self, graph):
        """
        Initialize the algorithm with the input graph.
        :param graph: Dictionary representing the adjacency list of the graph {node: [neighbors]}.
        """
        self.graph = graph
        self.independent_set = set()
        self.alpha = 0

    def update_adjacency_matrix(self, graph, vertex_to_remove):
        """
        Update the adjacency matrix by removing the given vertices and their edges.
        :param graph: The current graph (adjacency list).
        :param vertex_to_remove: the vertix that should be removed along with its neighbors
        :return: Updated adjacency list.
        """
        neighbors_to_remove = graph.get(vertex_to_remove, [])
        for vertex in neighbors_to_remove:
            if vertex in graph:
                n = graph.pop(vertex, [])
                # update the neighbors of the vertex
                for neighbor in n:
                    if neighbor != vertex_to_remove:
                        graph[neighbor] = [n for n in graph[neighbor] if n != vertex]

        graph.pop(vertex_to_remove, None)

        return graph

    def add_feasible_neighbors(self, graph, vertex, current_set):
        """
        Add feasible neighbors of the given vertex to the current independent set.
        :param graph: The current graph (adjacency list).
        :param vertex: The vertex to consider.
        :param current_set: The current independent set.
        :return: Updated independent set.
        """
        neighbors = graph.get(vertex, [])
        #print("Neighbors:", neighbors)
        for neighbor in neighbors:
            #this condition theorectically guanrantees that additions are independent
            if neighbor not in current_set and all(n not in current_set for n in graph.get(neighbor, [])):
                current_set.add(neighbor)

        # Check if the current set is still a valid independent set, just in case
        for vertex in current_set:
            if vertex in graph:
                graph = self.update_adjacency_matrix(graph, vertex)

        check = verify.validate_independent_set(graph, current_set)
        if not check:
            print("Invalid Independent Set at add_feasible_neighbors")
            return null, null

        return current_set, graph

    def disassemble(self):
        """
        Implements the Disassemble Algorithm to find the maximal independent set.
        :return: The maximal independent set (I*) and its cardinality (alpha).
        """
        # Step 1: Work on a copy of the graph to preserve the original
        remaining_graph = {node: list(neighbors) for node, neighbors in self.graph.items()}

        for i in self.graph:
            #print("Current Vertex:", i)
            # Step 2: Initialize independent set for this iteration
            current_set = set()
            remaining_graph = {node: list(neighbors) for node, neighbors in self.graph.items()}
            #print("Remaining Graph:", remaining_graph)

            # Add initial vertex and its neighbors if feasible
            # TODO: correct this
            # current_set.add(i)
            # neighbors = remaining_graph.pop(i, [])
            # remaining_graph = self.update_adjacency_matrix(remaining_graph, neighbors)
            
            # Add the initial vertex's neighbors to the independent set if feasible
            current_set, remaining_graph = self.add_feasible_neighbors(remaining_graph, i, current_set)
            #print("Current Set:", current_set)
            # Remove the initial vertex and its neighbors from the graph
            #remaining_graph = self.update_adjacency_matrix(remaining_graph, [i])
            #print("Remaining Graph:", remaining_graph)
            
            
            while remaining_graph:
                # Step 3: Find vertex with maximum degree that is not in the independent set
                remaining_no_independent = {node: list(neighbors) for node, neighbors in remaining_graph.items() if node not in current_set}
                #print("Remaining No Independent:", remaining_no_independent)
                max_degree_vertex = max(remaining_no_independent, key=lambda x: len(remaining_no_independent[x]))
                #print("Max Degree Vertex:", max_degree_vertex)

                # Add max degree vertex and its neighbors if feasible
                # TODO: correct this
                # current_set.add(max_degree_vertex)
                # neighbors = remaining_graph.pop(max_degree_vertex, [])
                # remaining_graph = self.update_adjacency_matrix(remaining_graph, neighbors)

                # Add the max degree vertex's neighbors to the independent set if feasible
                current_set, remaining_graph = self.add_feasible_neighbors(remaining_graph, max_degree_vertex, current_set)
                # Remove the max degree vertex and its neighbors from the graph
                #remaining_graph = self.update_adjacency_matrix(remaining_graph, [max_degree_vertex])
                #print("Current Set:", current_set)
                #print("Remaining Graph:", remaining_graph)

                # sanity check
                empty = True
                for vertex in remaining_graph:
                    if (len(remaining_graph[vertex]) != 0):
                        empty = False
                
                if empty:
                    break

            # Post-processing: Add vertices that do not make the solution infeasible
            for vertex, neighbors in self.graph.items():
                if vertex not in current_set and all(neighbor not in current_set for neighbor in neighbors):
                    current_set.add(vertex)

            # Sepcial vertex swapping mechanism
            swapped = False
            for vm in self.graph:
                if vm in current_set:
                    continue
                neighbors_in_set = [n for n in self.graph[vm] if n in current_set]
                
                if (len(neighbors_in_set) == 1):
                    vn = neighbors_in_set[0]

                    # swapping is feasible since its the only neighbor
                    current_set.remove(vn)
                    current_set.add(vm)

                    swapped = True
                    break
                    
            # Step 4: Check if the new independent set is larger
            if len(current_set) > self.alpha:
                self.independent_set = current_set
                self.alpha = len(current_set)

        return self.independent_set, self.alpha



# 
# graph = {
# 	1: [3, 7, 9, 4, 8, 2, 6],
# 	2: [9, 6, 8, 3, 5, 1],
# 	3: [1, 5, 7, 2, 6, 4, 8],
# 	4: [5, 1, 8, 3],
# 	5: [4, 9, 6, 3, 2, 7],
# 	6: [2, 5, 3, 1],
# 	7: [1, 9, 3, 5],
# 	8: [2, 4, 1, 3],
# 	9: [2, 5, 1, 7]
# }
# 
# algorithm = DisassembleAlgorithm(graph)
# independent_set, alpha = algorithm.disassemble()
# print("Maximal Independent Set:", independent_set)
# print("Cardinality:", alpha)
# print("Is Valid MIS:", verify.validate_independent_set(graph, independent_set))
