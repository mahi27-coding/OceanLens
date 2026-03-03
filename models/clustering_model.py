import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN

print("Clustering started...")

# Load dataset
df = pd.read_csv("data/oceanlens_beach_observations_v1.csv")

# Extract coordinates
coords = df[["latitude", "longitude"]].values

# Apply DBSCAN
db = DBSCAN(eps=0.002, min_samples=4)
clusters = db.fit_predict(coords)

# Add cluster labels
df["cluster"] = clusters

print("\nCluster Distribution:")
print(df["cluster"].value_counts())

# Plot clusters
plt.figure(figsize=(8,6))
plt.scatter(df["longitude"], df["latitude"], c=df["cluster"], cmap="rainbow")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title("Environmental Hotspot Clusters")
plt.colorbar(label="Cluster ID")
plt.show()