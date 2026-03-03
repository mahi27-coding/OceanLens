import streamlit as st
import pandas as pd
import sqlite3
from sklearn.cluster import DBSCAN

st.title("🌍 Environmental Intelligence Core")

# ---------------------------
# Load Historical Dataset
# ---------------------------
df_base = pd.read_csv("data/oceanlens_beach_observations_v1.csv")

df_base["tourist_density"] = df_base["tourist_density"].map({
    "Low": 0,
    "Medium": 1,
    "High": 2
})
df_base["tourist_density"] = df_base["tourist_density"].fillna(1)

df_base = df_base[["latitude", "longitude", "severity_level", "tourist_density"]]

# ---------------------------
# Load Live Field Reports
# ---------------------------
try:
    conn = sqlite3.connect("cases.db")
    new_cases = pd.read_sql_query("SELECT * FROM cases", conn)
    conn.close()

    if not new_cases.empty:
        new_cases = new_cases.rename(columns={
            "severity": "severity_level"
        })

        new_cases["tourist_density"] = 1

        df_live = new_cases[["latitude", "longitude", "severity_level", "tourist_density"]]

        df = pd.concat([df_base, df_live], ignore_index=True)
    else:
        df = df_base

except:
    df = df_base

# ---------------------------
# Clustering
# ---------------------------
coords = df[["latitude", "longitude"]].values

db = DBSCAN(eps=0.02, min_samples=3)
df["cluster"] = db.fit_predict(coords)

# DO NOT remove noise
# (we allow all points to influence risk)

# ---------------------------
# Adaptive Risk
# ---------------------------
df["adaptive_risk_score"] = (
    0.5 * df["severity_level"] +
    0.3 * df["tourist_density"]
)

# ---------------------------
# Stability Index
# ---------------------------
stability_index = 100 - (df["adaptive_risk_score"].mean() * 20)

st.metric("Environmental Stability Index", round(stability_index, 2))

# ---------------------------
# Status Classification
# ---------------------------
if stability_index >= 75:
    status = "Stable"
    color = "🟢"
elif stability_index >= 60:
    status = "Moderate Risk"
    color = "🟡"
else:
    status = "Critical Condition"
    color = "🔴"

st.subheader(f"{color} Environmental Status: {status}")

# ---------------------------
# Cluster Priority Ranking
# ---------------------------
cluster_risk = (
    df.groupby("cluster")["adaptive_risk_score"]
    .mean()
    .sort_values(ascending=False)
)

st.subheader("📊 Cluster Priority Ranking")
st.dataframe(cluster_risk.reset_index())

highest_cluster = cluster_risk.index[0]
st.success(f"Highest Priority Cluster: {highest_cluster}")