import streamlit as st
import pandas as pd
import sqlite3
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Early Warning System", layout="wide")

st.title("🚨 Island-Wide Environmental Early Warning System")

# -----------------------------
# Load Baseline Data
# -----------------------------
df_base = pd.read_csv("data/oceanlens_beach_observations_v1.csv")

df_base["tourist_density"] = df_base["tourist_density"].map({
    "Low": 0,
    "Medium": 1,
    "High": 2
}).fillna(1)

df_base["baseline_risk"] = (
    0.6 * df_base["severity_level"] +
    0.3 * df_base["tourist_density"]
)

baseline_mean = df_base["baseline_risk"].mean()
baseline_std = df_base["baseline_risk"].std()

# -----------------------------
# Load Live Reports
# -----------------------------
try:
    conn = sqlite3.connect("cases.db")
    df_live = pd.read_sql_query("SELECT * FROM cases", conn)
    conn.close()

    if not df_live.empty:
        df_live["live_risk"] = (
            0.6 * df_live["severity"] + 0.3
        )
        current_mean = df_live["live_risk"].mean()
    else:
        current_mean = baseline_mean

except:
    current_mean = baseline_mean

# -----------------------------
# Z-Score Calculation
# -----------------------------
if baseline_std == 0:
    z_score = 0
else:
    z_score = (current_mean - baseline_mean) / baseline_std

# -----------------------------
# Status Classification
# -----------------------------
if z_score < 0.5:
    status = "Normal"
    color = "#28a745"
elif z_score < 1.0:
    status = "Watch"
    color = "#ffc107"
elif z_score < 2.0:
    status = "Escalating"
    color = "#fd7e14"
else:
    status = "Critical"
    color = "#dc3545"

# -----------------------------
# Layout
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    st.metric("Baseline Risk Mean", round(baseline_mean, 3))
    st.metric("Current Risk Mean", round(current_mean, 3))
    st.metric("Z-Score Deviation", round(z_score, 3))

with col2:
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=z_score,
        title={"text": "Environmental Anomaly Z-Score"},
        gauge={
            "axis": {"range": [-2, 3]},
            "bar": {"color": color},
            "steps": [
                {"range": [-2, 0.5], "color": "#d4edda"},
                {"range": [0.5, 1], "color": "#fff3cd"},
                {"range": [1, 2], "color": "#ffeeba"},
                {"range": [2, 3], "color": "#f8d7da"}
            ],
        }
    ))

    st.plotly_chart(fig, width="stretch")

# -----------------------------
# Executive Summary
# -----------------------------
st.subheader("📄 Executive Risk Summary")

st.write(f"""
### Environmental Status: **{status}**

The system compares live environmental risk reports against historical baseline data using statistical anomaly detection.

A Z-score close to zero indicates stability. Higher positive deviations indicate abnormal environmental escalation.
""")

if status == "Critical":
    st.error("⚠ Immediate intervention required. Risk deviation exceeds statistical threshold.")
elif status == "Escalating":
    st.warning("⚠ Environmental instability detected. Preventive action advised.")
elif status == "Watch":
    st.info("Monitoring recommended. Slight elevation in risk levels.")
else:
    st.success("System stable. No abnormal environmental escalation detected.")