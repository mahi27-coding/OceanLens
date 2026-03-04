import pandas as pd
import sqlite3

print("OceanLens Environmental Risk Trend Analysis Starting...\n")

# Connect to database
conn = sqlite3.connect("cases.db")

# Load cases
df = pd.read_sql_query("SELECT timestamp, risk_score FROM cases", conn)

conn.close()

# Check if data exists
if df.empty:
    print("No environmental data available.")
else:

    # Convert timestamp
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Extract date
    df["date"] = df["timestamp"].dt.date

    # Calculate daily average risk
    trend = df.groupby("date")["risk_score"].mean()

    print("Daily Environmental Risk Trend:\n")
    print(trend)

    # Calculate Environmental Stability Index
    avg_risk = df["risk_score"].mean()

    stability_index = 100 - (avg_risk * 30)

    print("\nEnvironmental Stability Index:", round(stability_index,2))

    if stability_index > 70:
        status = "Healthy Environment"
    elif stability_index > 50:
        status = "Moderate Environmental Pressure"
    else:
        status = "Critical Environmental Risk"

    print("Environmental Status:", status)