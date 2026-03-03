import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🛰️ Island-Wide Environmental Risk Intelligence")

# -------------------------
# Load Dataset
# -------------------------
df = pd.read_csv("data/oceanlens_beach_observations_v1.csv")

# -------------------------
# Encode Features
# -------------------------
df["tourist_density"] = df["tourist_density"].map({
    "Low": 0,
    "Medium": 1,
    "High": 2
}).fillna(1)

df["garbage_type"] = df["garbage_type"].astype("category").cat.codes

# -------------------------
# Risk Score Calculation
# -------------------------
df["risk_score"] = (
    df["severity_level"] * 0.6 +
    df["garbage_type"] * 0.3 +
    df["tourist_density"] * 0.1
)

# -------------------------
# Sidebar Filters
# -------------------------
st.sidebar.header("🔍 Map Filters")

severity_filter = st.sidebar.multiselect(
    "Select Severity Levels",
    options=sorted(df["severity_level"].unique()),
    default=sorted(df["severity_level"].unique())
)

filtered_df = df[df["severity_level"].isin(severity_filter)]

# -------------------------
# Auto Center Map
# -------------------------
center_lat = filtered_df["latitude"].mean()
center_lon = filtered_df["longitude"].mean()

st.subheader("🌍 Live Geospatial Risk Mapping")

fig = px.scatter_mapbox(
    filtered_df,
    lat="latitude",
    lon="longitude",
    color="risk_score",
    size="risk_score",
    hover_data={
        "severity_level": True,
        "risk_score": True
    },
    color_continuous_scale="Inferno",
    zoom=6,
    height=650
)

fig.update_layout(
    mapbox_style="carto-darkmatter",
    mapbox_center={"lat": center_lat, "lon": center_lon},
    margin={"r": 0, "t": 0, "l": 0, "b": 0}
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# -------------------------
# Live Risk Metrics
# -------------------------
col1, col2, col3 = st.columns(3)

col1.metric("Filtered Observations", len(filtered_df))
col2.metric("Average Risk", round(filtered_df["risk_score"].mean(), 2))
col3.metric("High Risk Zones", len(filtered_df[filtered_df["risk_score"] > 1.8]))

# -------------------------
# Smart Risk Alert System
# -------------------------
highest_risk = filtered_df["risk_score"].max()

if highest_risk > 1.9:
    st.error("🚨 Critical Risk Zone Detected – Immediate Response Required")
elif highest_risk > 1.5:
    st.warning("⚠️ Elevated Risk Zones Present")
else:
    st.success("✅ Risk Levels Within Monitoring Threshold")

st.success("Geospatial Environmental Intelligence Engine Active")