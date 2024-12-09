import bruteForce
from heuristic import DisassembleAlgorithm
import pandas as pd
import os
import time

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

def main():
    df = pd.read_csv("./7/results.csv")

    results=pd.DataFrame(columns=['Test', 'Vertices', 'filename', 'Brute Force', 'Brute Force Time','Heuristic', 'Heuristic Time'])


    sample=df.sample(5,random_state=42)
    for index, rows in df.iterrows():
        print("Test:", rows['Test'])
        print("Vertices:", rows['Vertices'])
        print("filename:", rows['filename'])
        print("")
        graph, nofver= read_and_parse_graph(rows['filename'])

    

        start = time.time()
        bruteForceResult = bruteForce.maximum_independent_set(graph)
        bfResultSize= len(bruteForceResult)
        print("Brute Force Result:", bruteForceResult)
        print("Brute Force Result Size:", bfResultSize)
        end = time.time()
        bfTime = end - start
        print("Brute Force Time:", bfTime)

        start = time.time() 
        algorithm = DisassembleAlgorithm(graph)
        independent_set, alpha = algorithm.disassemble()
        print("Heuristic Result:", independent_set)
        print("Heuristic Result Size:", alpha)
        end = time.time()
        heuristicTime = end - start
        print("Heuristic Time:", heuristicTime)

        results.loc[len(results)] = [rows['Test'], rows['Vertices'], rows['filename'], bfResultSize, bfTime, alpha, heuristicTime]
        if index % 50 == 0:
            results.to_csv("./7/resultest.csv", index=False)
        print("")

    results.to_csv("./7/resultest.csv", index=False)



if __name__ == "__main__":
    main()