import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
import pytz
import plotly.graph_objects as go

st.set_page_config(
    page_title="OceanLens Command Center",
    layout="wide"
)

# =========================================================
# HEADER WITH LIVE CLOCK
# =========================================================

col1, col2 = st.columns([4, 1])

with col1:
    st.markdown("""
        <h2 style='margin-bottom:0px;'>OceanLens Command Center</h2>
        <span style='font-size:14px;color:gray;'>
        Andaman & Nicobar Environmental Intelligence Infrastructure
        </span>
    """, unsafe_allow_html=True)

with col2:
    ist = pytz.timezone("Asia/Kolkata")
    now = datetime.now(ist)
    st.markdown(f"""
        <div style='text-align:right; font-size:14px; color:#00b3b3;'>
        {now.strftime("%d %b %Y | %H:%M:%S")} IST
        </div>
    """, unsafe_allow_html=True)

st.divider()

# =========================================================
# LOAD DATABASE
# =========================================================

def load_cases():
    try:
        conn = sqlite3.connect("cases.db")
        df = pd.read_sql_query("SELECT * FROM cases", conn)
        conn.close()
        return df
    except:
        return pd.DataFrame()

df = load_cases()

# =========================================================
# KPI PANELS (3 PANELS)
# =========================================================

st.markdown("### Operational Overview")

if not df.empty:
    total_cases = len(df)
    avg_risk = round(df["risk_score"].mean(), 2)
    high_severity = len(df[df["severity"] == 3])
else:
    total_cases = 0
    avg_risk = 0
    high_severity = 0

col1, col2, col3 = st.columns(3)

def kpi_panel(title, value, border_color):
    st.markdown(f"""
        <div style="
            border: 2px solid {border_color};
            padding: 20px;
            border-radius: 8px;
            background-color: #111827;
        ">
            <div style="font-size:13px; color:gray; letter-spacing:1px;">
                {title}
            </div>
            <div style="font-size:36px; font-weight:bold; margin-top:5px;">
                {value}
            </div>
        </div>
    """, unsafe_allow_html=True)

with col1:
    kpi_panel("TOTAL INCIDENTS", total_cases, "#00b3b3")

with col2:
    kpi_panel("HIGH SEVERITY CASES", high_severity, "#ff4c4c")

with col3:
    kpi_panel("AVERAGE RISK SCORE", avg_risk, "#ffaa00")

st.divider()

# =========================================================
# FULL WIDTH COMMAND STATUS STRIP
# =========================================================

if avg_risk > 1.8:
    strip_color = "#8B0000"
    strip_message = "CRITICAL — Immediate Intervention Required"
elif avg_risk > 1.4:
    strip_color = "#b8860b"
    strip_message = "WATCH — Elevated Environmental Risk"
else:
    strip_color = "#006400"
    strip_message = "STABLE — Monitoring Active"

st.markdown(f"""
    <div style="
        background-color: {strip_color};
        padding: 14px;
        border-radius: 6px;
        font-weight: 500;
        font-size: 15px;
        text-align: center;
        letter-spacing: 0.5px;
    ">
        SYSTEM STATUS: {strip_message}
    </div>
""", unsafe_allow_html=True)

st.divider()

# =========================================================
# LIVE INCIDENT MAP
# =========================================================

st.markdown("### Live Incident Map — Andaman & Nicobar")

fig = go.Figure()

if not df.empty:

    color_map = {
        1: "#00ff99",
        2: "#ffaa00",
        3: "#ff4c4c"
    }

    for severity in df["severity"].unique():
        filtered = df[df["severity"] == severity]

        fig.add_trace(go.Scattermapbox(
            lat=filtered["latitude"],
            lon=filtered["longitude"],
            mode="markers",
            marker=go.scattermapbox.Marker(
                size=12,
                color=color_map.get(severity, "#00b3b3")
            ),
            name=f"Severity {severity}"
        ))

fig.update_layout(
    mapbox=dict(
        style="carto-darkmatter",
        center=dict(lat=11.8, lon=92.7),
        zoom=6.7
    ),
    margin={"r":0,"t":0,"l":0,"b":0},
    height=550,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=0.01,
        xanchor="right",
        x=0.99
    )
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# =========================================================
# RECENT INCIDENTS TABLE
# =========================================================

st.markdown("### Recent Incident Reports")

if not df.empty:
    st.dataframe(
        df.sort_values("timestamp", ascending=False).head(10),
        use_container_width=True
    )
else:
    st.info("No incident reports available.")