import pandas as pd
import sqlite3
import numpy as np

print("Advanced Environmental Anomaly Engine Started...\n")

# -----------------------------
# Load Historical Baseline
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

print("Baseline Mean Risk:", round(baseline_mean, 3))
print("Baseline Std Dev:", round(baseline_std, 3))

# -----------------------------
# Load Live Reports
# -----------------------------
try:
    conn = sqlite3.connect("cases.db")
    df_live = pd.read_sql_query("SELECT * FROM cases", conn)
    conn.close()

    if not df_live.empty:
        df_live["live_risk"] = (
            0.6 * df_live["severity"] +
            0.3
        )

        current_mean = df_live["live_risk"].mean()

    else:
        current_mean = baseline_mean

except:
    current_mean = baseline_mean

print("\nCurrent Mean Risk:", round(current_mean, 3))

# -----------------------------
# Z-Score Anomaly Detection
# -----------------------------
if baseline_std == 0:
    z_score = 0
else:
    z_score = (current_mean - baseline_mean) / baseline_std

print("Z-Score:", round(z_score, 3))

# -----------------------------
# Classification
# -----------------------------
if z_score < 0.5:
    status = "🟢 Normal"
elif z_score < 1.0:
    status = "🟡 Watch"
elif z_score < 2.0:
    status = "🟠 Escalating"
else:
    status = "🔴 Critical Environmental Anomaly"

print("\nEnvironmental Status:", status)