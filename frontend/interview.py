import streamlit as st
import requests
from dotenv import load_dotenv
import os

load_dotenv()
backend = os.getenv("BACKEND")

st.title("Interview App")

if "data" not in st.session_state:
    id = st.text_input("Enter your UVU ID:")
    if st.button("Submit"):
        response = requests.post(
            backend + "interviewStart", json={"uvuid": str(id)}, headers={"Content-Type": "application/json"})
        if response.status_code == 200:
            data = response.json()
            st.session_state["data"] = data
        else:
            st.write(str(response.reason) + " " + str(response.status_code))
else:
    data = st.session_state["data"]
    with st.form(key="interviewForm"):
        q1 = st.text_input("Fibonacci Sequence")
        q2 = st.text_input("Game Engine Library")
        if st.form_submit_button("Submit"):
            data["q1"] = q1
            data["q2"] = q2
            st.dataframe(data, use_container_width=True)
            post = requests.post(backend + "path/to/update/db",
                                 json=data, headers={"Content-Type": "application/json"})

st.title("2nd Portion")

second_id = st.text_input("Enter UVU ID for 2nd Portion:")
if st.button("Submit 2nd Portion"):
    response = requests.post(
        backend + "interviewStart", json={"uvuid": str(second_id)}, headers={"Content-Type": "application/json"})
    if response.status_code == 200:
        second_data = response.json()
        st.json(second_data)
    else:
        st.write(str(response.reason) + " " + str(response.status_code))
