import streamlit as st
import sqlite3
import pandas as pd
import numpy as np
import datetime

st.set_page_config(layout="wide")
st.title("⚠ Predictive Risk Intelligence")
st.caption("Island-Wide Environmental Stability Monitoring Engine")

# ---------------------------------------
# LOAD DATABASE
# ---------------------------------------

conn = sqlite3.connect("cases.db")

try:
    df = pd.read_sql_query("SELECT * FROM cases", conn)
except:
    df = pd.DataFrame()

conn.close()

if df.empty:
    st.info("No case data available yet.")
    st.stop()

# ---------------------------------------
# BASIC PREPROCESSING
# ---------------------------------------

df["timestamp"] = pd.to_datetime(df["timestamp"])
df["severity"] = pd.to_numeric(df["severity"], errors="coerce")
df["risk_score"] = pd.to_numeric(df["risk_score"], errors="coerce")

df = df.sort_values("timestamp")

# ---------------------------------------
# ENVIRONMENTAL STABILITY INDEX
# ---------------------------------------

avg_risk = df["risk_score"].mean()
stability_index = round(100 - (avg_risk * 25), 2)

col1, col2, col3 = st.columns(3)

col1.metric("Average Risk Score", round(avg_risk, 2))
col2.metric("Environmental Stability Index", stability_index)
col3.metric("Total Incidents Recorded", len(df))

st.divider()

# ---------------------------------------
# TREND ANALYSIS
# ---------------------------------------

df["rolling_risk"] = df["risk_score"].rolling(window=5, min_periods=1).mean()

st.subheader("📈 Risk Trend Over Time")
st.line_chart(df.set_index("timestamp")["rolling_risk"], width="stretch")

# ---------------------------------------
# ANOMALY DETECTION (Z-SCORE METHOD)
# ---------------------------------------

mean_risk = df["risk_score"].mean()
std_risk = df["risk_score"].std()

if std_risk == 0:
    z_score = 0
else:
    z_score = (df["risk_score"].iloc[-1] - mean_risk) / std_risk

st.subheader("🧠 Anomaly Detection")

if z_score < 0.5:
    st.success("Environmental Condition: Stable")
elif z_score < 1.0:
    st.warning("Environmental Condition: Watch Level")
elif z_score < 2.0:
    st.warning("Environmental Condition: Escalating")
else:
    st.error("Environmental Condition: Critical Anomaly Detected")

st.metric("Current Z-Score", round(z_score, 2))

st.divider()

# ---------------------------------------
# ESCALATION PROBABILITY ESTIMATION
# ---------------------------------------

critical_cases = df[df["status"].str.contains("CRITICAL", na=False)]
escalation_probability = round((len(critical_cases) / len(df)) * 100, 2)

st.subheader("🚨 Escalation Probability")

st.metric("Probability of High-Risk Escalation (%)", escalation_probability)

if escalation_probability > 40:
    st.error("High Escalation Risk Detected")
elif escalation_probability > 20:
    st.warning("Moderate Escalation Risk")
else:
    st.success("Low Escalation Risk")

st.divider()

st.caption("Predictive Intelligence Engine – OceanLens Infrastructure")