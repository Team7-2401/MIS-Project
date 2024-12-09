import pandas as pd
import matplotlib.pyplot as plt

# Read results from the main directory
results_file = "./results.csv"
df = pd.read_csv(results_file)

# Extract the necessary columns for plotting
vertices = df["Vertices"]
time = df["time"]

# Generate the scatter plot
plt.figure(figsize=(10, 6))
plt.scatter(vertices, time, alpha=0.7)
#plt.yscale("log")  # Logarithmic scale for time
plt.title("Performance of Heuristic Algorithm")
plt.xlabel("Number of Vertices")
plt.ylabel("Time (s)")
plt.grid(True, which="both", linestyle="--", linewidth=0.5)

# Save the scatter plot to the `plots` directory
output_plot = "./plots/heuristic_performance.png"
plt.savefig(output_plot, dpi=300)
plt.close()

print(f"Scatter plot saved to {output_plot}")
