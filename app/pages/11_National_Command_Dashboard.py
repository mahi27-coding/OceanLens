import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

st.title("🇮🇳 National Coastal Intelligence Command Dashboard")

# -----------------------------
# Load Data
# -----------------------------
try:
    conn = sqlite3.connect("cases.db")
    df = pd.read_sql_query("SELECT * FROM cases", conn)
    conn.close()
except:
    st.error("Unable to connect to database.")
    st.stop()

if df.empty:
    st.warning("No environmental cases reported yet.")
    st.stop()

# -----------------------------
# NATIONAL METRICS
# -----------------------------
total_cases = len(df)
avg_severity = round(df["severity"].mean(), 2)
avg_risk = round(df["risk_score"].mean(), 2)

col1, col2, col3 = st.columns(3)

col1.metric("Total Reported Cases", total_cases)
col2.metric("Average Severity", avg_severity)
col3.metric("Average Risk Score", avg_risk)

st.divider()

# -----------------------------
# ISLAND NODE SUMMARY
# -----------------------------
st.subheader("📊 Island Node Risk Distribution")

node_summary = (
    df.groupby("region")
      .agg(
          total_cases=("case_id", "count"),
          avg_severity=("severity", "mean"),
          avg_risk_score=("risk_score", "mean")
      )
      .reset_index()
)

st.dataframe(node_summary, width="stretch")

# -----------------------------
# BAR CHART
# -----------------------------
fig = px.bar(
    node_summary,
    x="region",
    y="total_cases",
    color="avg_risk_score",
    title="Case Distribution by Island Node",
    color_continuous_scale="Reds"
)

st.plotly_chart(fig, width="stretch")

st.divider()

# -----------------------------
# CRITICAL ZONE DETECTION
# -----------------------------
st.subheader("🚨 Automatic Red-Zone Detection")

critical_zones = node_summary[
    (node_summary["avg_severity"] >= 2.5) |
    (node_summary["avg_risk_score"] >= 1.8)
]

if not critical_zones.empty:
    st.error("Critical Environmental Zones Detected")
    st.dataframe(critical_zones, width="stretch")
else:
    st.success("No Critical Zones Detected")

st.divider()

# -----------------------------
# TREND ANALYSIS
# -----------------------------
st.subheader("📈 Incident Timeline")

df["timestamp"] = pd.to_datetime(df["timestamp"])
timeline = df.groupby(df["timestamp"].dt.date).size().reset_index(name="cases")

fig2 = px.line(
    timeline,
    x="timestamp",
    y="cases",
    markers=True,
    title="Daily Incident Trend"
)

st.plotly_chart(fig2, width="stretch")