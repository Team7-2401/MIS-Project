import testGen
import pandas as pd

testGen.generateTests(dirname="testim", no_of_tests=10, check_size='y', check_prob='n', size=10, prob=[0.02, 0.6])

print("starting to generate tests")
df = pd.DataFrame(columns=['Test', 'Vertices', 'Edge Probability', 'filename'])

for i in range (5, 10):
    print("i:", i)
    data = testGen.generateTests(dirname="6", no_of_tests=30, check_size='y', check_prob='n', size=i, prob=[0.02, 0.6])
    for index, row in data.iterrows():
        df.loc[len(df)] = [row['Test'], row['Vertices'], row['Edge Probability'], row['filename']]

df.to_csv("./6/results.csv", index=False)
