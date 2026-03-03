import streamlit as st
import pandas as pd

st.title(" Executive Environmental Overview")

# Load dataset
df = pd.read_csv("data/oceanlens_beach_observations_v1.csv")

# Basic Encoding
df["tourist_density"] = df["tourist_density"].map({
    "Low": 0,
    "Medium": 1,
    "High": 2
}).fillna(1)

df["garbage_type"] = df["garbage_type"].astype("category").cat.codes

# Risk Score
df["risk_score"] = (
    df["severity_level"] * 0.6 +
    df["garbage_type"] * 0.3 +
    df["tourist_density"] * 0.1
)

# KPIs
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Observations", len(df))
col2.metric("Average Risk Score", round(df["risk_score"].mean(), 2))
col3.metric("High Severity Cases", len(df[df["severity_level"] == 3]))
col4.metric("Max Risk Score", round(df["risk_score"].max(), 2))

st.divider()

# Region Environmental Index
def detect_region(lat):
    if lat < 12.5:
        return "South Andaman"
    elif lat < 13.2:
        return "Middle/North Andaman"
    else:
        return "Extended Island"

df["region"] = df["latitude"].apply(detect_region)

region_index = 100 - (df.groupby("region")["risk_score"].mean() * 30)

st.subheader("📊 Regional Environmental Stability Index")

st.dataframe(region_index.round(2))

import plotly.express as px

st.divider()

# Risk Distribution
st.subheader(" Risk Score Distribution")

fig = px.histogram(
    df,
    x="risk_score",
    nbins=20,
    title="Risk Score Spread Across Observations",
    color_discrete_sequence=["#FF4B4B"]
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# Severity Breakdown
st.subheader(" Severity Level Breakdown")

severity_counts = df["severity_level"].value_counts().sort_index()

fig2 = px.bar(
    x=severity_counts.index,
    y=severity_counts.values,
    labels={"x": "Severity Level", "y": "Number of Cases"},
    title="Severity Distribution",
    color=severity_counts.index,
)

st.plotly_chart(fig2, use_container_width=True)

st.divider()

# AI-style Insight Generator
st.subheader(" Automated Environmental Insight")

highest_region = region_index.idxmin()

st.info(
    f"⚠️ {highest_region} is currently showing the lowest environmental stability score. "
    "Immediate risk mitigation and waste management reinforcement is recommended."
)