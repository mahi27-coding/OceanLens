import pandas as pd

print("🇮🇳 India Coastal State Detection Engine Started...\n")

# ---------------------------------------------------
# Coastal State Bounding Boxes (Simplified Version)
# ---------------------------------------------------

coastal_states = {
    "Andaman & Nicobar Islands": {
        "lat_min": 6.0,
        "lat_max": 14.5,
        "lon_min": 91.0,
        "lon_max": 94.5
    },
    "Tamil Nadu": {
        "lat_min": 8.0,
        "lat_max": 13.5,
        "lon_min": 76.0,
        "lon_max": 80.5
    },
    "Kerala": {
        "lat_min": 8.0,
        "lat_max": 12.8,
        "lon_min": 74.5,
        "lon_max": 77.5
    },
    "Karnataka": {
        "lat_min": 12.0,
        "lat_max": 15.0,
        "lon_min": 74.0,
        "lon_max": 76.5
    },
    "Goa": {
        "lat_min": 14.8,
        "lat_max": 15.8,
        "lon_min": 73.5,
        "lon_max": 74.5
    },
    "Maharashtra": {
        "lat_min": 15.5,
        "lat_max": 20.5,
        "lon_min": 72.5,
        "lon_max": 74.5
    },
    "Gujarat": {
        "lat_min": 20.0,
        "lat_max": 23.5,
        "lon_min": 68.0,
        "lon_max": 72.5
    },
    "Odisha": {
        "lat_min": 18.0,
        "lat_max": 22.5,
        "lon_min": 84.0,
        "lon_max": 88.5
    },
    "West Bengal": {
        "lat_min": 21.0,
        "lat_max": 23.0,
        "lon_min": 87.5,
        "lon_max": 89.5
    }
}

# ---------------------------------------------------
# Detection Function
# ---------------------------------------------------

def detect_coastal_state(latitude, longitude):
    for state, bounds in coastal_states.items():
        if (bounds["lat_min"] <= latitude <= bounds["lat_max"] and
            bounds["lon_min"] <= longitude <= bounds["lon_max"]):
            return state
    return "Non-Coastal or Unknown"

# ---------------------------------------------------
# Example Test
# ---------------------------------------------------

test_lat = 11.62
test_lon = 92.73

detected = detect_coastal_state(test_lat, test_lon)

print(f"Test Coordinates: {test_lat}, {test_lon}")
print("Detected Coastal State:", detected)