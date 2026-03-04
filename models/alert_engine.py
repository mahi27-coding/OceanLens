import pandas as pd

def generate_environmental_alerts(data):

    alerts = []

    for _, row in data.iterrows():

        severity = row["severity_level"]

        if severity >= 3:

            alerts.append({
                "type": "CRITICAL",
                "message": "High severity waste accumulation detected",
                "location": (row["latitude"], row["longitude"])
            })

        elif severity == 2:

            alerts.append({
                "type": "WARNING",
                "message": "Moderate waste accumulation detected",
                "location": (row["latitude"], row["longitude"])
            })

    return alerts