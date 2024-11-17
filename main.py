import os
import pandas as pd
import random
import bruteForce
import sampleGen
import visualize
import time

def main():
    # Create the plots and samples directory if they doesn't exist
    if not os.path.exists("plots"):
        os.makedirs("plots")
    if not os.path.exists("samples"):
        os.makedirs("samples")


    # Create pandas dataframe to store the results
    df = pd.DataFrame(columns=["Sample Number", "Vertices", "Edge Probability", "time", "Independent Set Size"])

    # Generate the samples
    num_graph = int(input("Enter the number of graphs you want to generate: "))
    choice = input("Do you want to generate the samples with random vertix counts and probablities? (y/n): ")

    sampleVertixSizes = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 100, 150, 200, 250, 300, 350]

    if choice == "n":
        # Generate the sample
        num_vertices = int(input("Enter the number of vertices: "))
        edge_prob = float(input("Enter the edge probability: "))
        graph = sampleGen.generate_graph(num_vertices, edge_prob)
    else:
        range_vertices = input("Enter the range of vertices (start, end): ").split(",")
        range_prob = input("Enter the range of edge probability [0, 1](start, end): ").split(",")


    for i in range(num_graph):

        if choice == "y":
            num_vertices = random.randint(int(range_vertices[0]), int(range_vertices[1]))
            edge_prob = random.uniform(float(range_prob[0]), float(range_prob[1]))
        
        start = time.time()
        graph = sampleGen.generate_graph(num_vertices, edge_prob)
        # Find MIS
        independent_set = bruteForce.maximum_independent_set(graph)
        end = time.time()

        # Add the result to the dataframe
        df.loc[len(df)] = [i+1, num_vertices, edge_prob, end-start, len(independent_set)]
        # Save the result
        with open(f"samples/sample_{i+1}.txt", "w") as f:
            f.write(f"Graph: \n")
            for node, neighbors in graph.items():
                f.write(f"\t{node}: {neighbors}\n")
            f.write(f"\nIndependent Set: {independent_set}\n")
            f.write(f"\nMaximum Independent Set Size: {len(independent_set)}\n")
        
        # Make the graph and save it
        visualize.visualize_graph(graph, independent_set, filename=f"sample_{i+1}")

    # Save the results to a csv file
    df.to_csv("results.csv", index=False)

if __name__ == "__main__":
    main()
