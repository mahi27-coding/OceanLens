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

# ---------------------------------------------------
# HEADER WITH LIVE CLOCK
# ---------------------------------------------------

col1, col2 = st.columns([4,1])

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

# ---------------------------------------------------
# LOAD DATABASE
# ---------------------------------------------------

def load_cases():
    try:
        conn = sqlite3.connect("cases.db")
        df = pd.read_sql_query("SELECT * FROM cases", conn)
        conn.close()
        return df
    except:
        return pd.DataFrame()

df = load_cases()

# ---------------------------------------------------
# SYSTEM STATUS STRIP
# ---------------------------------------------------

st.markdown("### System Status")

colA, colB, colC, colD = st.columns(4)

total_cases = len(df)

if not df.empty:
    avg_risk = round(df["risk_score"].mean(), 2)
    high_severity = len(df[df["severity"] == 3])
else:
    avg_risk = 0
    high_severity = 0

with colA:
    st.metric("Total Incidents", total_cases)

with colB:
    st.metric("High Severity Cases", high_severity)

with colC:
    st.metric("Average Risk Score", avg_risk)

with colD:
    if avg_risk > 1.8:
        st.error("System Status: CRITICAL")
    elif avg_risk > 1.4:
        st.warning("System Status: WATCH")
    else:
        st.success("System Status: STABLE")

st.divider()

# ---------------------------------------------------
# ANDAMAN LIVE INCIDENT MAP
# ---------------------------------------------------

st.markdown("### Live Incident Map — Andaman & Nicobar")

fig = go.Figure()

if not df.empty:
    color_map = {
        1: "green",
        2: "yellow",
        3: "red"
    }

    for severity in df["severity"].unique():
        filtered = df[df["severity"] == severity]

        fig.add_trace(go.Scattermapbox(
            lat=filtered["latitude"],
            lon=filtered["longitude"],
            mode="markers",
            marker=go.scattermapbox.Marker(
                size=12,
                color=color_map.get(severity, "blue")
            ),
            name=f"Severity {severity}"
        ))

fig.update_layout(
    mapbox=dict(
        style="open-street-map",
        center=dict(lat=11.8, lon=92.7),
        zoom=6
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

st.plotly_chart(fig, width="stretch")

st.divider()

# ---------------------------------------------------
# RECENT INCIDENTS TABLE
# ---------------------------------------------------

st.markdown("### Recent Incident Reports")

if not df.empty:
    st.dataframe(
        df.sort_values("timestamp", ascending=False).head(10),
        width="stretch"
    )
else:
    st.info("No incident reports available.")