import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN

print("Adaptive Environmental Risk Engine Started...")

# Load dataset
df = pd.read_csv("data/oceanlens_beach_observations_v1.csv")

# Convert tourist density to numeric
df["tourist_density"] = df["tourist_density"].map({
    "Low": 0,
    "Medium": 1,
    "High": 2
})

df["tourist_density"] = df["tourist_density"].fillna(1)

# Perform clustering
coords = df[["latitude", "longitude"]].values
db = DBSCAN(eps=0.01, min_samples=4)
df["cluster"] = db.fit_predict(coords)

# Remove noise points
df = df[df["cluster"] != -1].copy()

# Cluster analysis
cluster_summary = df.groupby("cluster").agg({
    "severity_level": "mean",
    "tourist_density": "mean"
}).reset_index()

def classify_cluster(row):
    if row["tourist_density"] > 1.2:
        return "High Tourism Zone"
    elif row["severity_level"] > 2:
        return "Eco-Sensitive Zone"
    else:
        return "Balanced Zone"

cluster_summary["zone_type"] = cluster_summary.apply(classify_cluster, axis=1)

df = df.merge(cluster_summary[["cluster", "zone_type"]], on="cluster")

# Adaptive risk scoring
def adaptive_risk(row):
    if row["zone_type"] == "High Tourism Zone":
        return (0.35 * row["severity_level"] +
                0.45 * row["tourist_density"])
    elif row["zone_type"] == "Eco-Sensitive Zone":
        return (0.5 * row["severity_level"] +
                0.25 * row["tourist_density"])
    else:
        return (0.4 * row["severity_level"] +
                0.3 * row["tourist_density"])

df["adaptive_risk_score"] = df.apply(adaptive_risk, axis=1)

# Environmental Stability Index
stability_index = 100 - (df["adaptive_risk_score"].mean() * 25)

print("\n=== Environmental Stability Index ===")
print(round(stability_index, 2))

# Priority ranking
cluster_risk = df.groupby("cluster")["adaptive_risk_score"].mean().sort_values(ascending=False)

print("\n=== Cluster Priority Ranking ===")
print(cluster_risk)

print("\nHighest Priority Cluster:", cluster_risk.index[0])