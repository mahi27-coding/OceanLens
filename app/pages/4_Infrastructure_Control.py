import streamlit as st
import sqlite3
import pandas as pd

st.title(" Island Infrastructure Control Center")

# -----------------------------
# Load Case Data
# -----------------------------
conn = sqlite3.connect("cases.db")
df = pd.read_sql_query("SELECT * FROM cases", conn)
conn.close()

if df.empty:
    st.warning("No active environmental cases available.")
    st.stop()

# -----------------------------
# INFRASTRUCTURE CAPACITY SETTINGS
# -----------------------------
TOTAL_UNITS = 15  # total waste response teams available

node_case_count = df.groupby("region")["case_id"].count().reset_index()
node_case_count.columns = ["region", "total_cases"]

# Simulated deployment rule
node_case_count["units_required"] = node_case_count["total_cases"].apply(lambda x: max(1, x // 3))
node_case_count["units_required"] = node_case_count["units_required"].astype(int)

total_required = node_case_count["units_required"].sum()
remaining_units = TOTAL_UNITS - total_required

# -----------------------------
# DISPLAY METRICS
# -----------------------------
col1, col2, col3 = st.columns(3)

col1.metric("Total Response Units", TOTAL_UNITS)
col2.metric("Units Currently Required", total_required)
col3.metric("Remaining Capacity", remaining_units)

st.divider()

# -----------------------------
# NODE DEPLOYMENT TABLE
# -----------------------------
st.subheader("📍 Deployment Distribution by Island Node")

st.dataframe(node_case_count, width="stretch")

st.divider()

# -----------------------------
# AUTOMATIC ESCALATION LOGIC
# -----------------------------
st.subheader("🚨 Deployment Recommendation Engine")

high_pressure_nodes = node_case_count[node_case_count["total_cases"] >= 5]

if not high_pressure_nodes.empty:
    st.error("High Pressure Zones Detected")
    st.dataframe(high_pressure_nodes[["region", "total_cases", "units_required"]], width="stretch")
else:
    st.success("Infrastructure capacity stable across all nodes.")