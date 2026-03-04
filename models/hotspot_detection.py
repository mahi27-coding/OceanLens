import pandas as pd
import sqlite3
from sklearn.cluster import DBSCAN

print("OceanLens Pollution Hotspot Detection Starting...\n")

# Connect to database
conn = sqlite3.connect("cases.db")

# Read cases
df = pd.read_sql_query("SELECT latitude, longitude FROM cases", conn)

conn.close()

# Check if cases exist
if df.empty:
    print("No reports found in database. Please submit reports first.")
else:

    print("Loaded Reports:", len(df))

    coords = df[["latitude","longitude"]]

    # Apply clustering
    clustering_model = DBSCAN(eps=0.05, min_samples=2)

    clusters = clustering_model.fit_predict(coords)

    df["cluster"] = clusters

    print("\nCluster Results:\n")
    print(df)

    # Detect hotspots
    hotspots = df[df["cluster"] != -1]

    print("\nDetected Pollution Hotspots:\n")

    if hotspots.empty:
        print("No hotspots detected yet.")
    else:
        print(hotspots)