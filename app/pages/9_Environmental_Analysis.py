import sys
import os

# Allow Python to see project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

from models.alert_engine import generate_environmental_alerts
from models.email_alert import send_email_alert


# Page Title
st.title("Environmental Intelligence Analysis")

st.write("Run OceanLens environmental analytics models.")


# Session state
if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False


# Run Models Button
if st.button("Run Environmental Analysis"):

    st.session_state.analysis_done = True

    st.write("Running Risk Prediction Model...")
    import models.risk_prediction_model
    st.success("Risk Prediction Complete")

    st.write("Running Hotspot Detection...")
    import models.hotspot_detection
    st.success("Hotspot Detection Complete")

    st.write("Running Risk Trend Analysis...")
    import models.risk_trend_analysis
    st.success("Risk Trend Analysis Complete")

    st.write("Running Environmental Anomaly Detection...")
    import models.anomaly_engine
    st.success("Anomaly Detection Complete")


# After models run
if st.session_state.analysis_done:

    st.subheader("Environmental Monitoring Dashboard")

    # Load dataset
    df = pd.read_csv("data/oceanlens_beach_observations_v1.csv")


    # Metrics
    col1, col2, col3 = st.columns(3)

    total_incidents = len(df)
    high_risk = len(df[df["severity_level"] >= 3])
    avg_severity = round(df["severity_level"].mean(), 2)

    col1.metric("Total Incidents", total_incidents)
    col2.metric("High Severity Cases", high_risk)
    col3.metric("Average Severity", avg_severity)


    # Alert System
    st.subheader("Environmental Alert System")

    alerts = generate_environmental_alerts(df)

    st.write(f"Total Alerts Generated: {len(alerts)}")


    if len(alerts) == 0:

        st.success("No environmental alerts detected")

    else:

        for alert in alerts:

            if alert["type"] == "CRITICAL":

                st.markdown(
                f"""
                <div style="
                background:#8b0000;
                padding:15px;
                border-radius:8px;
                color:white;
                font-size:18px;
                font-weight:bold;
                ">
                ⚠ CRITICAL ALERT — {alert["message"]}
                </div>
                """,
                unsafe_allow_html=True
                )

                # Email alert simulation
                send_email_alert(alert["message"])

            elif alert["type"] == "WARNING":

                st.markdown(
                f"""
                <div style="
                background:#b8860b;
                padding:12px;
                border-radius:8px;
                color:white;
                font-size:16px;
                ">
                ⚠ WARNING — {alert["message"]}
                </div>
                """,
                unsafe_allow_html=True
                )


    # Environmental Risk Heatmap
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


        popup_text = f"""
        Severity Level: {severity}
        """

        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=8,
            color=color,
            fill=True,
            fill_opacity=0.7,
            popup=popup_text
        ).add_to(m)


    st_folium(m, width=900, height=500)


    # Legend
    st.markdown(
    """
    ### Heatmap Legend
    🟢 Low Risk  
    🟠 Moderate Risk  
    🔴 High Environmental Risk
    """
    )


    # Download dataset
    st.download_button(
        label="Download Environmental Dataset",
        data=df.to_csv(index=False),
        file_name="oceanlens_environment_data.csv",
        mime="text/csv"
    )