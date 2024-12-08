import os
import sampleGen
import random
import pandas as pd

def generateTests(dirname=None, no_of_tests=None, check_size=None, check_prob=None, size=None, prob=None):
    print("Fixed test generator,,,")
    if not dirname:
        dirname = input("Enter the directory name (where the tests will be stored): ")

    # Create the directory
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    df = pd.DataFrame(columns=['Test', 'Vertices', 'Edge Probability', 'filename'])

    # Create the test files
    if (not no_of_tests or not check_size or not check_prob):
        no_of_tests = int(input("Enter the number of tests you want to generate: "))
        check_size = input("Do you want to have a fixed size? (y/n): ")
        check_prob = input("Do you want to have a fixed edge probability? (y/n): ")

    if check_size == 'y':
        if not size:
            size = int(input("Enter the size of the graph: "))
        if check_prob == 'y':
            if not prob:
                prob = float(input("Enter the edge probability: "))
            for i in range(no_of_tests):
                filename = dirname + '/test_' + str(i) + ".txt"
                graph = sampleGen.generate_graph(size, prob)
                df.loc[len(df)] = [i, size, prob, filename]

                #save test
                save_graph(filename, graph)
        else:
            if not prob:
                prob = input("Enter the edge probability range (e.g. 0,1): ").split(',')
            for i in range(no_of_tests):
                filename = dirname + '/test_' + str(i) + ".txt"
                graph = sampleGen.generate_graph(size, random.uniform(float(prob[0]), float(prob[1])))
                df.loc[len(df)] = [i, size, prob, filename]

                #save test
                save_graph(filename, graph)
    else:
        if not size:
            size = input("Enter the size range (e.g. 10,100): ").split(',')
        if check_prob == 'y':
            if not prob:
                prob = float(input("Enter the edge probability: "))
            for i in range(no_of_tests):
                filename = dirname + '/test_' + str(i) + ".txt"
                graph = sampleGen.generate_graph(random.randint(int(size[0]), int(size[1])), prob)
                df.loc[len(df)] = [i, size, prob, filename]

                #save test
                save_graph(filename, graph)
        else:
            if not prob:
                prob = input("Enter the edge probability range (e.g. 0,1): ").split(',')
            for i in range(no_of_tests):
                filename = dirname + '/test_' + str(i) + ".txt"
                graph = sampleGen.generate_graph(random.randint(int(size[0]), int(size[1])), random.uniform(float(prob[0]), float(prob[1])))
                df.loc[len(df)] = [i, size, prob, filename]

                #save test
                save_graph(filename, graph)

    df.to_csv(dirname + '/test_info.csv', index=False)


def save_graph(filename, graph):
    with open(filename, 'w') as f:
        f.write(str(len(graph)) + '\n')
        f.write("graph= {\n")
        for node, neighbors in graph.items():
            f.write("\t{node} : {neighbors}\n")
        f.write("}\n")


if __name__ == '__main__':
    generateTests()
