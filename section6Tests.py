import heuristic
import pandas as pd
import os
import time
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='6/logs.log')

def main():
    df = pd.read_csv("./6/results.csv")

    results = pd.DataFrame(columns=['Test', 'Vertices', 'Edge Probability', 'filename', 'time', 'Independent Set Size'])

    sample = df.sample(n=5, random_state=2)
    #print(sample)

    generalTime = time.time()

    for index, row in df.iterrows():
        graph, no_of_vertices = read_and_parse_graph(row['filename'])

        if no_of_vertices != row['Vertices']:
            print("Parser failure")
            exit()

        #---------------timed block----------------
        start = time.time()

        algorithm = heuristic.DisassembleAlgorithm(graph)
        independent_set, alpha = algorithm.disassemble()

        end = time.time()
        #---------------timed block----------------

        results.loc[len(results)] = [row['Test'], no_of_vertices, row['Edge Probability'], row['filename'], end-start, len(independent_set)]

        print("Test:", row['Test'], "Vertices:", no_of_vertices,"Time:", end-start, "Independent Set Size:", len(independent_set))
        logging.info("Test: %s, Vertices: %s, Time: %s, Independent Set Size: %s", row['Test'], no_of_vertices, end-start, len(independent_set))


    print("Total time:", time.time()-generalTime)

    results.to_csv("./6/results_test.csv", index=False)

def read_and_parse_graph(filename):
    """
    function reads the file and parses the graph into an adjaceny list
    """
    graph = {}
    with open("./" + filename) as f:
        content = f.readlines()

    no_of_vertices = int(content[0].strip())
    for i in range(2, len(content)-1):
        vertex = content[i].strip().split(":")
        edges = parse_list(vertex[1])
        graph[int(vertex[0].strip())] = edges

    return graph, no_of_vertices

def parse_list(listAsString):
    """
    function parses the list from the string
    """
    listAsString = listAsString.replace("[", "").replace("]", "").strip()
    
    if listAsString == "":
        return []

    listAsInt = listAsString.split(", ")
    if listAsInt[0] == "":
        return []
    else:
        return [int(i) for i in listAsInt]

    return listAsInt

if __name__ == "__main__":
    main()
