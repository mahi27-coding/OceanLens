# -------------------------------
# SAFE MATPLOTLIB BACKEND (Mac Fix)
# -------------------------------
import matplotlib
matplotlib.use("TkAgg")

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.cluster import DBSCAN

print("Island-Wide Environmental Intelligence Infrastructure Started...\n")

# -------------------------------
# LOAD DATASET
# -------------------------------
df = pd.read_csv("data/oceanlens_beach_observations_v1.csv")

# -------------------------------
# ENCODE FEATURES
# -------------------------------
df["tourist_density"] = df["tourist_density"].map({
    "Low": 0,
    "Medium": 1,
    "High": 2
})

df["tourist_density"] = df["tourist_density"].fillna(1)
df["garbage_type"] = df["garbage_type"].astype("category").cat.codes

# -------------------------------
# TRAIN SEVERITY MODEL
# -------------------------------
X = df[["latitude", "longitude", "tourist_density", "garbage_type"]]
y = df["severity_level"]

model = LogisticRegression(max_iter=1000)
model.fit(X, y)

df["predicted_severity"] = model.predict(X)

# -------------------------------
# APPLY CLUSTERING
# -------------------------------
coords = df[["latitude", "longitude"]].values
db = DBSCAN(eps=0.002, min_samples=4)
df["cluster"] = db.fit_predict(coords)

df_clean = df[df["cluster"] != -1].copy()

# -------------------------------
# RISK SCORE CALCULATION
# -------------------------------
df_clean["risk_score"] = (
    df_clean["predicted_severity"] * 0.6 +
    df_clean["garbage_type"] * 0.3 +
    df_clean["tourist_density"] * 0.1
)

# -------------------------------
# REGION DETECTION
# -------------------------------
def detect_region(lat):
    if lat < 12.5:
        return "South Andaman Node"
    elif lat < 13.2:
        return "Middle/North Andaman Node"
    else:
        return "Extended Island Node"

df_clean["region_node"] = df_clean["latitude"].apply(detect_region)

# -------------------------------
# RESPONSE TIME LOGIC
# -------------------------------
def response_time(score):
    if score > 1.8:
        return "2 Hours (Emergency)"
    elif score > 1.4:
        return "24 Hours (Routine)"
    else:
        return "72 Hours (Monitoring)"

df_clean["estimated_response_time"] = df_clean["risk_score"].apply(response_time)

# -------------------------------
# REGION ENVIRONMENTAL INDEX
# -------------------------------
region_index = 100 - (df_clean.groupby("region_node")["risk_score"].mean() * 30)

print("=== REGION ENVIRONMENTAL INDEX ===")
print(region_index.round(2))

# -------------------------------
# CLUSTER RISK RANKING
# -------------------------------
cluster_risk = df_clean.groupby("cluster")["risk_score"].mean().sort_values(ascending=False)

print("\n=== CLUSTER RISK RANKING ===")
print(cluster_risk)

print("\nHighest Priority Cluster:", cluster_risk.index[0])

print("\n=== SAMPLE INFRASTRUCTURE CASES ===")
print(df_clean[[
    "predicted_severity",
    "cluster",
    "risk_score",
    "region_node",
    "estimated_response_time"
]].head())

# -------------------------------
# ISLAND STABILITY SCORE
# -------------------------------
island_score = 100 - (df_clean["risk_score"].mean() * 30)

print("\n=== ISLAND ENVIRONMENTAL STABILITY SCORE ===")
print("Overall Stability Index:", round(island_score, 2))

# -------------------------------
# HEATMAP VISUALIZATION
# -------------------------------
plt.figure(figsize=(10,7))

scatter = plt.scatter(
    df_clean["longitude"],
    df_clean["latitude"],
    c=df_clean["risk_score"],
    cmap="inferno",
    s=80,
    edgecolors="black"
)

plt.colorbar(scatter, label="Environmental Risk Score")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title("Andaman & Nicobar Environmental Risk Intelligence Map")
plt.grid(alpha=0.2)
plt.tight_layout()

# Save image instead of only showing (safer on Mac)
plt.savefig("models/risk_map.png")

print("\nRisk map saved as models/risk_map.png")

plt.show()