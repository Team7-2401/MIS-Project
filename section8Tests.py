import heuristic
import visualize

names = ["emptyGraph", "oneVertex", "fiveVertices", "fiftyVertices", "graphNoEdges", "graphDisconnected", "graphAllEdges"]

def run_test(graph):
    algorithm = heuristic.DisassembleAlgorithm(graph)
    independent_set, alpha = algorithm.disassemble()
    return independent_set, alpha

def read_and_parse_graph(filename):
    """
    function reads the file and parses the graph into an adjaceny list
    """
    graph = {}
    with open("./" + filename) as f:
        content = f.readlines()

    for i in range(1, len(content)-1):
        vertex = content[i].strip().split(":")
        edges = parse_list(vertex[1])
        graph[int(vertex[0].strip())] = edges

    return graph

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

for graph_name in names:
    try:
        print(f"Running test for {graph_name}")
        graph = read_and_parse_graph(f"8/{graph_name}.txt")
        visualize.visualize_graph(graph, filename=f"{graph_name}_original")
        independent_set, alpha = run_test(graph)
        visualize.visualize_graph(graph, independent_set, filename=f"{graph_name}")
        print("Maximal Independent Set:", independent_set)
        print("Cardinality:", alpha)

        # Save results
        with open(f"8/{graph_name}_results.txt", "w") as f:
            f.write("Maximal Independent Set:\n")
            for vertex in independent_set:
                f.write(f"{vertex}\n")
            f.write(f"Cardinality: {alpha}\n")

        print()
    except Exception as e:
        print(f"Test failed for {graph_name}")
