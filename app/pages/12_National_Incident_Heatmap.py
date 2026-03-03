import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from sklearn.cluster import DBSCAN
import numpy as np

st.title(" National Coastal Intelligence & Clustering")

# -----------------------------------
# LOAD DATA
# -----------------------------------
conn = sqlite3.connect("cases.db")
df = pd.read_sql_query("SELECT * FROM cases", conn)
conn.close()

if df.empty:
    st.warning("No incident data available yet.")
    st.stop()

# -----------------------------------
# BASIC HEATMAP
# -----------------------------------
st.subheader("📍 Incident Density Heatmap")

fig = px.density_mapbox(
    df,
    lat="latitude",
    lon="longitude",
    z="severity",
    radius=20,
    center=dict(lat=20, lon=78),
    zoom=4,
    mapbox_style="open-street-map",
    height=600
)

st.plotly_chart(fig, width="stretch")

# -----------------------------------
# DBSCAN CLUSTERING
# -----------------------------------
st.subheader(" Spatial Cluster Detection")

coordinates = df[["latitude", "longitude"]].values

# DBSCAN parameters:
# eps controls cluster radius
# min_samples controls minimum cases per cluster
db = DBSCAN(eps=0.5, min_samples=3).fit(coordinates)

df["cluster"] = db.labels_

# -1 means noise (not in cluster)
clusters = df[df["cluster"] != -1]

if clusters.empty:
    st.success("No significant spatial clusters detected yet.")
else:
    cluster_summary = clusters.groupby("cluster").agg(
        total_cases=("case_id", "count"),
        avg_severity=("severity", "mean"),
        avg_risk_score=("risk_score", "mean")
    ).reset_index()

    st.dataframe(cluster_summary, width="stretch")

    st.subheader("📌 Cluster Map View")

    cluster_map = px.scatter_mapbox(
        clusters,
        lat="latitude",
        lon="longitude",
        color="cluster",
        size="severity",
        zoom=5,
        mapbox_style="open-street-map",
        height=600
    )

    st.plotly_chart(cluster_map, width="stretch")

# -----------------------------------
# MICRO RED-ZONE DETECTION
# -----------------------------------
st.subheader("🚨 Micro Red-Zone Detection")

if not clusters.empty:
    critical_clusters = cluster_summary[
        (cluster_summary["total_cases"] >= 3) &
        (cluster_summary["avg_severity"] >= 2)
    ]

    if critical_clusters.empty:
        st.success("No micro-level critical clusters detected.")
    else:
        st.error("⚠ Critical Geographic Clusters Identified")
        st.dataframe(critical_clusters, width="stretch")