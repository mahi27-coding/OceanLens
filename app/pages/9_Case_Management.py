import streamlit as st
from database import fetch_cases, delete_case
import os

st.title("📂 Case Management System")

cases = fetch_cases()

if not cases:
    st.info("No cases found.")
else:
    for case in cases:

        case_id = case[0]

        with st.expander(f"Case ID: {case_id}"):

            st.write(f"Timestamp: {case[1]}")
            st.write(f"Location: ({case[2]}, {case[3]})")
            st.write(f"Severity: {case[4]}")
            st.write(f"Risk Score: {case[5]}")
            st.write(f"Region: {case[6]}")
            st.write(f"Response: {case[7]}")
            st.write(f"Status: {case[8]}")

            if case[9]:
                image_list = case[9].split(",")
                for img in image_list:
                    if os.path.exists(img):
                        st.image(img, width=300)

            if st.button("Delete Case", key=case_id):
                delete_case(case_id)
                st.success("Case deleted.")
                st.rerun()