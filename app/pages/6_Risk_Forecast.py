import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.title("🔮 Coastal Risk Forecast Intelligence Engine")

# --------------------------------------------------
# Load Dataset
# --------------------------------------------------
df = pd.read_csv("data/oceanlens_beach_observations_v1.csv")

# Encode tourist density first (needed for risk calculation)
df["tourist_density_encoded"] = df["tourist_density"].map({
    "Low": 1,
    "Medium": 1.5,
    "High": 2
}).fillna(1)

# Recompute risk score (since it is not stored in CSV)
df["risk_score"] = (
    df["severity_level"] * 0.6 +
    df["tourist_density_encoded"] * 0.4
)

# --------------------------------------------------
# Simulated Time Index (since dataset has no timestamp)
# --------------------------------------------------
np.random.seed(42)
df["day"] = np.random.randint(1, 31, size=len(df))

# Compute Daily Average Risk
daily_risk = df.groupby("day")["risk_score"].mean().reset_index()
daily_risk = daily_risk.sort_values("day")

# --------------------------------------------------
# Rolling Trend
# --------------------------------------------------
daily_risk["rolling_mean"] = daily_risk["risk_score"].rolling(window=5).mean()

st.subheader("📈 Historical Risk Trend (Simulated 30 Days)")

fig_trend = go.Figure()

fig_trend.add_trace(go.Scatter(
    x=daily_risk["day"],
    y=daily_risk["risk_score"],
    mode="lines+markers",
    name="Daily Risk"
))

fig_trend.add_trace(go.Scatter(
    x=daily_risk["day"],
    y=daily_risk["rolling_mean"],
    mode="lines",
    name="5-Day Rolling Average"
))

fig_trend.update_layout(
    xaxis_title="Day",
    yaxis_title="Average Risk Score",
    title="Risk Trend Over Time"
)

st.plotly_chart(fig_trend, use_container_width=True)

st.divider()

# --------------------------------------------------
# 30-Day Forecast Projection
# --------------------------------------------------
st.subheader("🔮 30-Day Risk Projection")

x = daily_risk["day"]
y = daily_risk["risk_score"]

coefficients = np.polyfit(x, y, 1)
trend_line = np.poly1d(coefficients)

future_days = np.arange(31, 61)
future_risk = trend_line(future_days)

forecast_df = pd.DataFrame({
    "day": np.concatenate([x, future_days]),
    "risk": np.concatenate([y, future_risk]),
    "type": ["Historical"] * len(x) + ["Forecast"] * len(future_days)
})

fig_forecast = px.line(
    forecast_df,
    x="day",
    y="risk",
    color="type",
    title="Projected Coastal Risk (Next 30 Days)"
)

st.plotly_chart(fig_forecast, use_container_width=True)

st.divider()

# --------------------------------------------------
# Escalation Risk Probability
# --------------------------------------------------
st.subheader("⚠ Escalation Probability Estimation")

latest_risk = daily_risk["risk_score"].iloc[-1]

if latest_risk > 1.8:
    escalation_level = "HIGH"
    color = "red"
elif latest_risk > 1.4:
    escalation_level = "MODERATE"
    color = "orange"
else:
    escalation_level = "LOW"
    color = "green"

st.markdown(f"""
### Current Escalation Level:  
<span style='color:{color}; font-size:24px; font-weight:bold;'>{escalation_level}</span>
""", unsafe_allow_html=True)

st.success("Forecast Engine Active – Predictive Monitoring Running")