import sys
import os
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# Allow Streamlit to find models
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

st.title("Environmental Intelligence Analysis")
st.write("Run OceanLens AI environmental analytics models.")

# -----------------------------
# SESSION STATES
# -----------------------------
if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False

if "model_results" not in st.session_state:
    st.session_state.model_results = []

# -----------------------------
# RUN ANALYSIS BUTTON
# -----------------------------
if st.button("Run Environmental Analysis"):

    st.session_state.analysis_done = True
    st.session_state.model_results = []

    # Run Models
    st.session_state.model_results.append("Running Risk Prediction Model...")
    import models.risk_prediction_model
    st.session_state.model_results.append("Risk Prediction Complete")

    st.session_state.model_results.append("Running Hotspot Detection...")
    import models.hotspot_detection
    st.session_state.model_results.append("Hotspot Detection Complete")

    st.session_state.model_results.append("Running Risk Trend Analysis...")
    import models.risk_trend_analysis
    st.session_state.model_results.append("Risk Trend Analysis Complete")

    st.session_state.model_results.append("Running Environmental Anomaly Detection...")
    import models.anomaly_engine
    st.session_state.model_results.append("Anomaly Detection Complete")

# -----------------------------
# SHOW MODEL RESULTS
# -----------------------------
if st.session_state.analysis_done:

    st.subheader("Model Execution Results")

    for msg in st.session_state.model_results:
        if "Complete" in msg:
            st.success(msg)
        else:
            st.info(msg)

# -----------------------------
# LOAD DATA
# -----------------------------
    df = pd.read_csv("data/oceanlens_beach_observations_v1.csv")

# -----------------------------
# HEATMAP
# -----------------------------
    st.subheader("Environmental Risk Heatmap")

    m = folium.Map(
        location=[df["latitude"].mean(), df["longitude"].mean()],
        zoom_start=8,
        tiles="cartodb dark_matter"
    )

    for _, row in df.iterrows():

        severity = row["severity_level"]

        if severity >= 3:
            color = "red"
        elif severity == 2:
            color = "orange"
        else:
            color = "green"

        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=8,
            color=color,
            fill=True,
            fill_opacity=0.7,
            popup=f"Severity Level: {severity}"
        ).add_to(m)

    st_folium(m, width=900, height=500)