import testGen
import pandas as pd

print("starting to generate tests")
df = pd.DataFrame(columns=['Test', 'Vertices', 'Edge Probability', 'filename'])

for i in range (5, 75, 10):
    print("i:", i)
    data = testGen.generateTests(dirname="7", no_of_tests=20, check_size='y', check_prob='n', size=i, prob=[0.02, 0.6])
    for index, row in data.iterrows():
        df.loc[len(df)] = [row['Test'], row['Vertices'], row['Edge Probability'], row['filename']]

df.to_csv("./7/results.csv", index=False)
