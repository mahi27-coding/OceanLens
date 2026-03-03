import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.title("🧠 Strategic Coastal Risk Scenario Simulator")

st.markdown("""
Simulate environmental policy decisions and compare projected coastal risk
under baseline vs reform conditions.
""")

st.divider()

st.sidebar.header("⚙️ Policy Reform Controls")

tourist_pressure = st.sidebar.slider(
    "Tourist Density Impact",
    0.5, 2.0, 1.0, 0.1,
    key="tourist_slider"
)

waste_management_efficiency = st.sidebar.slider(
    "Waste Management Efficiency",
    0.5, 2.0, 1.0, 0.1,
    key="waste_slider"
)

enforcement_strength = st.sidebar.slider(
    "Environmental Enforcement Strength",
    0.5, 2.0, 1.0, 0.1,
    key="enforcement_slider"
)

climate_stress = st.sidebar.slider(
    "Climate Stress Multiplier",
    0.5, 2.0, 1.0, 0.1,
    key="climate_slider"
)

st.divider()

np.random.seed(42)
base_risk = np.random.normal(loc=1.6, scale=0.25, size=120)

baseline_risk = base_risk

reform_risk = (
    base_risk
    * tourist_pressure
    * climate_stress
    / (waste_management_efficiency * enforcement_strength)
)

df = pd.DataFrame({
    "Baseline Risk": baseline_risk,
    "Reform Risk": reform_risk
})

baseline_avg = df["Baseline Risk"].mean()
reform_avg = df["Reform Risk"].mean()

risk_delta = baseline_avg - reform_avg
improvement_percent = (risk_delta / baseline_avg) * 100

col1, col2, col3 = st.columns(3)

col1.metric("Baseline Avg Risk", round(baseline_avg, 3))
col2.metric("Reform Avg Risk", round(reform_avg, 3))
col3.metric("Risk Reduction %", f"{improvement_percent:.2f}%")

st.divider()

st.subheader("📊 Risk Distribution Comparison")

comparison_df = df.melt(var_name="Scenario", value_name="Risk Score")

fig = px.histogram(
    comparison_df,
    x="Risk Score",
    color="Scenario",
    barmode="overlay",
    opacity=0.6,
    nbins=20
)

fig.update_layout(template="plotly_dark")

st.plotly_chart(fig, width="stretch")

st.divider()

st.subheader("🚨 Strategic Impact Assessment")

if improvement_percent > 20:
    st.success("Significant Risk Mitigation Achieved – Reform Highly Effective")
elif improvement_percent > 10:
    st.info("Moderate Risk Reduction – Policy Improvement Recommended")
elif improvement_percent > 0:
    st.warning("Minor Risk Improvement – Strengthen Enforcement Strategy")
else:
    st.error("Risk Escalation Detected – Immediate Policy Correction Required")

st.success("Scenario Engine Active • Comparative Policy Intelligence Enabled")

# ---------------------------------------
# MONTE CARLO SIMULATION
# ---------------------------------------

st.divider()
st.subheader("📈 Probabilistic Risk Projection (Monte Carlo Simulation)")

simulation_runs = 1000

simulated_means = []

for _ in range(simulation_runs):
    noise = np.random.normal(1, 0.05, size=120)
    simulated = (
        base_risk
        * tourist_pressure
        * climate_stress
        * noise
        / (waste_management_efficiency * enforcement_strength)
    )
    simulated_means.append(np.mean(simulated))

simulated_means = np.array(simulated_means)

expected_risk = simulated_means.mean()
lower_bound = np.percentile(simulated_means, 2.5)
upper_bound = np.percentile(simulated_means, 97.5)

escalation_probability = np.mean(simulated_means > baseline_avg) * 100

col1, col2, col3 = st.columns(3)

col1.metric("Expected Risk", round(expected_risk, 3))
col2.metric("95% Confidence Interval", f"{lower_bound:.2f} - {upper_bound:.2f}")
col3.metric("Escalation Probability", f"{escalation_probability:.2f}%")

fig_mc = px.histogram(
    simulated_means,
    nbins=30,
    title="Monte Carlo Distribution of Projected Risk"
)

fig_mc.update_layout(template="plotly_dark")

st.plotly_chart(fig_mc, width="stretch")

if escalation_probability > 50:
    st.error("High Probability of Risk Escalation Under Current Reform")
elif escalation_probability > 20:
    st.warning("Moderate Escalation Risk – Strengthen Policy Parameters")
else:
    st.success("Low Escalation Probability – Reform Strategy Stable")

st.divider()
st.subheader("📄 Executive Policy Summary")

summary_text = f"""
Under the current reform configuration, the projected average coastal risk is **{expected_risk:.2f}** 
with a 95% confidence interval between **{lower_bound:.2f} and {upper_bound:.2f}**.

The probability of environmental risk escalation relative to baseline conditions is estimated at 
**{escalation_probability:.1f}%**.

Based on the stochastic simulation results, the reform strategy is classified as 
{'high risk and requires immediate recalibration.' if escalation_probability > 50 
 else 'moderately stable but requires monitoring.' if escalation_probability > 20 
 else 'operationally stable under current parameters.'}
"""

st.markdown(summary_text)


# ---------------------------------------
# SCENARIO ARCHIVE SYSTEM
# ---------------------------------------

st.divider()
st.subheader("📁 Scenario Archive & Policy Ranking")

if "scenario_history" not in st.session_state:
    st.session_state.scenario_history = []

if st.button("💾 Save Current Reform Scenario"):

    scenario_data = {
        "Tourist Pressure": tourist_pressure,
        "Waste Efficiency": waste_management_efficiency,
        "Enforcement Strength": enforcement_strength,
        "Climate Stress": climate_stress,
        "Reform Avg Risk": reform_avg,
        "Risk Reduction %": improvement_percent,
        "Escalation Probability %": escalation_probability
    }

    st.session_state.scenario_history.append(scenario_data)
    st.success("Scenario Saved Successfully")

if st.session_state.scenario_history:

    history_df = pd.DataFrame(st.session_state.scenario_history)

    st.markdown("### 📊 Saved Reform Scenarios")
    st.dataframe(history_df)

    # Rank scenarios by lowest reform risk
    best_scenario = history_df.sort_values("Reform Avg Risk").iloc[0]

    st.markdown("### 🏆 Best Reform Configuration Identified")

    st.success(
        f"""
        Best Scenario Achieves Avg Risk: {best_scenario['Reform Avg Risk']:.2f}
        with Escalation Probability: {best_scenario['Escalation Probability %']:.1f}%
        """
    )

    # ---------------------------------------
# POLICY RECOMMENDATION ENGINE
# ---------------------------------------

st.divider()
st.subheader("🤖 Automated Policy Recommendation Engine")

if escalation_probability > 50:
    recommendation = """
    Increase Waste Management Efficiency above 1.5  
    Strengthen Environmental Enforcement above 1.6  
    Consider reducing Tourist Density Impact below 1.2  
    """
elif escalation_probability > 20:
    recommendation = """
    Moderate improvement required.  
    Focus on enforcement tightening and waste efficiency upgrades.  
    """
else:
    recommendation = """
    Current reform configuration is stable.  
    Maintain monitoring and periodic stress testing.  
    """

st.info(recommendation)