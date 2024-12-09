import bruteForce
from heuristic import DisassembleAlgorithm
import pandas as pd
import os
import time
import threading
from concurrent.futures import ThreadPoolExecutor, TimeoutError

result_lock = threading.Lock()
counter_lock = threading.Lock()

def heuristic_with_timeout(graph, timeout=300):
    """
    Runs the heuristic algorithm with a timeout.
    """
    def run_heuristic():
        algorithm = DisassembleAlgorithm(graph)
        independent_set, alpha = algorithm.disassemble()
        return independent_set, alpha

    with ThreadPoolExecutor() as executor:
        future = executor.submit(run_heuristic)
        try:
            return future.result(timeout=timeout)  # Wait for result or timeout
        except TimeoutError:
            print("Heuristic computation timed out!")
            return None, None  # Return a fallback value if timeout occurs


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

def run_tests(row):
    graph, nofver= read_and_parse_graph(row['filename'])

    start = time.time()
    bruteForceResult = bruteForce.maximum_independent_set(graph)
    bfResultSize= len(bruteForceResult)
    print("Brute Force Result Size:", bfResultSize)
    end = time.time()
    bfTime = end - start
    print("Brute Force Time:", bfTime)

    # start = time.time() 
    # algorithm = DisassembleAlgorithm(graph)
    # independent_set, alpha = algorithm.disassemble()
    # print("Heuristic Result Size:", alpha)
    # end = time.time()
    # heuristicTime = end - start
    # print("Heuristic Time:", heuristicTime)

    # Heuristic
    failed = False
    start = time.time()
    independent_set, alpha = heuristic_with_timeout(graph)
    if alpha is None:  # Handle timeout
        failed = True
    end = time.time()
    heuristicTime = end - start
    print("Heuristic Result Size:", alpha)
    print("Heuristic Time:", heuristicTime)

    if failed:
        print("Heuristic failed!")
        return [row['Test'], row['Vertices'], row['filename'], bfResultSize, bfTime, -1, 0]
    
    global counterG
    with counter_lock: 
        counterG += 1
    print("Counter:", counterG)
    return [row['Test'], row['Vertices'], row['filename'], bfResultSize, bfTime, alpha, heuristicTime]

def run_tests_threading(row, results):
    result = run_tests(row)
    with result_lock:
        results.loc[len(results)] = result
    return

def make_thread(i, df, resultHolder):
    print("Thread:", i)
    results = pd.DataFrame(columns=['Test', 'Vertices', 'filename', 'Brute Force', 'Brute Force Time','Heuristic', 'Heuristic Time'])
    for index, row in df.iterrows():
        if index % 15 == i:
            print("Thread:", i, "Test:", row['Test'], "Vertices:", row['Vertices'])
            results.loc[len(results)] = run_tests(row)
    print("Thread:", i, "finished")
    results.to_csv(f"./7/results_test_intermediate_{i}.csv", index=False)
    resultHolder[i] = results
    return

counterG = 0

results = None

def get_processed():
    # list all the files in 7
    files = os.listdir("./7")
    files = [f for f in files if f.startswith("results_test_intermediate_")]
    processed = pd.DataFrame(columns=['Test', 'Vertices', 'filename', 'Brute Force', 'Brute Force Time','Heuristic', 'Heuristic Time'])

    for file in files:
        df = pd.read_csv(f"./7/{file}")
        processed = pd.concat([processed, df], ignore_index=True)

    return processed


def main():
    df = pd.read_csv("./7/results.csv")

    global results
    results=pd.DataFrame(columns=['Test', 'Vertices', 'filename', 'Brute Force', 'Brute Force Time','Heuristic', 'Heuristic Time'])
    resultHolder = [None]*len(df)

    
    processed = get_processed()

    unprocessed = df[~df['filename'].isin(processed['filename'])]
    print("Unprocessed:", len(unprocessed))

    sample = df.sample(n=40, random_state=2)
    # implement threading
    threads = []
    # for i in range(len(sample)):
    #     print("Thread:", i)
    #     t = threading.Thread(target=run_tests_threading, args=(sample.iloc[i], results))
    #     t.start()
    #     threads.append(t)

    # for t in threads:
    #     print("Joining thread ", t)
    #     t.join()

    for i in range(15):
        t = threading.Thread(target=make_thread, args=(i, df, resultHolder))
        t.start()
        threads.append(t)

    counter = 0
    for t in threads:
        t.join()
        
    for i in range(15):
        if resultHolder[i] is not None:
            results = pd.concat([results, resultHolder[i]], ignore_index=True)

    results.to_csv("./7/results_test_test.csv", index=False)



if __name__ == "__main__":
    main()
