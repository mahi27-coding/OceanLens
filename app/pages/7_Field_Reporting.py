import streamlit as st
import os
import uuid
import random
from datetime import datetime
import sys
import sqlite3
from PIL import Image
from pillow_heif import register_heif_opener
import plotly.graph_objects as go
from streamlit_js_eval import streamlit_js_eval

register_heif_opener()

# Allow database import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from database import init_db, save_case

st.set_page_config(layout="wide")
st.title("🏝 Andaman & Nicobar Environmental Field Reporting System")

init_db()

# ---------------------------------------------------
# AUTO LOCATION DETECTION
# ---------------------------------------------------

st.subheader("📡 Auto Location Detection")

browser_location = streamlit_js_eval(
    js_expressions="navigator.geolocation.getCurrentPosition((pos) => pos.coords)",
    key="get_location"
)

latitude = None
longitude = None

if browser_location and isinstance(browser_location, dict):
    latitude = browser_location.get("latitude")
    longitude = browser_location.get("longitude")
    st.success("📍 Live location detected from device GPS.")

# ---------------------------------------------------
# IMAGE UPLOAD + EXIF GPS
# ---------------------------------------------------

uploaded_files = st.file_uploader(
    "Upload Live Camera Image (GPS Enabled)",
    accept_multiple_files=True,
    type=["jpg", "jpeg", "png", "heic"]
)

def extract_gps(image):
    try:
        exif = image.getexif()
        gps_info = exif.get_ifd(34853)

        if not gps_info:
            return None, None

        def convert_to_degrees(value):
            d = value[0][0] / value[0][1]
            m = value[1][0] / value[1][1]
            s = value[2][0] / value[2][1]
            return d + (m / 60.0) + (s / 3600.0)

        lat = convert_to_degrees(gps_info[2])
        if gps_info[1] == "S":
            lat = -lat

        lon = convert_to_degrees(gps_info[4])
        if gps_info[3] == "W":
            lon = -lon

        return lat, lon
    except:
        return None, None

if uploaded_files and latitude is None:
    image = Image.open(uploaded_files[0])
    lat, lon = extract_gps(image)

    if lat and lon:
        latitude = lat
        longitude = lon
        st.success("📷 GPS detected from image metadata.")
    else:
        st.warning("Image has no GPS metadata.")

# ---------------------------------------------------
# MANUAL FALLBACK
# ---------------------------------------------------

if latitude is None:
    latitude = st.number_input("Latitude", value=11.62, format="%.6f")

if longitude is None:
    longitude = st.number_input("Longitude", value=92.73, format="%.6f")

# ---------------------------------------------------
# ISLAND NODE DETECTION
# ---------------------------------------------------

def detect_island_node(lat):
    if lat < 10.5:
        return "Nicobar Node"
    elif lat < 11.6:
        return "Little Andaman Node"
    elif lat < 12.0:
        return "South Andaman Node"
    elif lat < 13.0:
        return "Middle Andaman Node"
    elif lat < 14.5:
        return "North Andaman Node"
    else:
        return "Extended Archipelago Zone"

island_node = detect_island_node(latitude)
st.info(f"Detected Island Node: {island_node}")

# ---------------------------------------------------
# MAP PREVIEW
# ---------------------------------------------------

predicted_severity = random.randint(1, 3)

if predicted_severity == 3:
    marker_color = "red"
elif predicted_severity == 2:
    marker_color = "yellow"
else:
    marker_color = "green"

fig = go.Figure(go.Scattermapbox(
    lat=[latitude],
    lon=[longitude],
    mode='markers',
    marker=go.scattermapbox.Marker(
        size=18,
        color=marker_color
    )
))

fig.update_layout(
    mapbox=dict(
        style="open-street-map",
        center=dict(lat=latitude, lon=longitude),
        zoom=10
    ),
    margin={"r":0,"t":0,"l":0,"b":0},
    height=500
)

st.plotly_chart(fig, width="stretch")

# ---------------------------------------------------
# SUBMIT REPORT (WITH ALERT LOGIC)
# ---------------------------------------------------

if st.button("Submit Report"):

    risk_score = round(random.uniform(1.2, 2.2), 2)

    case_id = "CASE_" + str(uuid.uuid4())[:8]
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 🔴 CRITICAL ALERT LOGIC
    if predicted_severity == 3:
        status = "CRITICAL – DISPATCHED"
    else:
        status = "Monitoring"

    os.makedirs("uploads", exist_ok=True)

    image_paths = []

    if uploaded_files:
        for file in uploaded_files:
            filename = case_id + "_" + file.name
            file_path = os.path.join("uploads", filename)

            with open(file_path, "wb") as f:
                f.write(file.getbuffer())

            image_paths.append(file_path)

    image_string = ",".join(image_paths) if image_paths else None

    case_data = (
        case_id,
        timestamp,
        latitude,
        longitude,
        predicted_severity,
        risk_score,
        island_node,
        "Deploy Island Response Unit",
        status,
        image_string
    )

    save_case(case_data)

    if predicted_severity == 3:
        st.error(f"🚨 CRITICAL ALERT TRIGGERED – Case {case_id} Dispatched")
    else:
        st.success(f"✅ Case {case_id} submitted successfully.")