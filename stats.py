import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
df = pd.read_csv('results.csv')

# Sort with respect to vector size
df = df.sort_values(by='Vertices')

# Plot the data (scatter plot)
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='Vertices', y='time')
plt.yscale('log')
plt.xlabel('Number of Vertices')
plt.ylabel('Time (s)')
plt.title('Performance of Different Algorithms')
plt.grid()
plt.show()


