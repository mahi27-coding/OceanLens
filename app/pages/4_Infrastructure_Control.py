import streamlit as st
import sqlite3
import pandas as pd
import os
import sys

# Allow database import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from database import init_db

st.title("🏗 Island Infrastructure Control Center")

# Always initialize DB first (important for cloud)
init_db()

# Connect to DB
conn = sqlite3.connect("cases.db")

try:
    df = pd.read_sql_query("SELECT * FROM cases", conn)
except:
    df = pd.DataFrame()

conn.close()

# If no cases yet
if df.empty:
    st.info("No infrastructure cases recorded yet.")
else:
    st.subheader("📋 Active Infrastructure Cases")
    st.dataframe(df, width="stretch")