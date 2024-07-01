import streamlit as st
import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()
backend = os.getenv("BACKEND")

st.title("Interview App")

if "data" not in st.session_state:
    id = st.text_input("Enter your UVU ID:")
    if st.button("Submit"):
        response = requests.post(
            backend + "interviewStart", json={"uvuid": str(id)}, headers={"Content-Type": "application/json"})
        if response.status_code == 200:
            st.session_state["data"] = response.json()
        else:
            st.write(str(response.reason) + " " + str(response.status_code))
else:
    with st.form(key="interviewForm"):
        st.write(f"Name: {st.session_state["data"]["name"]}")
        st.write(f"UVU ID: {st.session_state["data"]["uvuid"]}")
        q1 = st.checkbox("Can code")
        q2 = int(st.number_input("Enjoyment", min_value=1, max_value=10, value=5))
        q3 = int(st.number_input("Social", min_value=1, max_value=10, value=5))
        if st.form_submit_button("Submit"):
            interview_data = json.dumps(dict(fkuser=st.session_state["data"]["pid"], cancode=q1, enjoyment=q2, social=q3))
            # I doubt request.post works. Blame on 
            post = requests.post(backend + "path/to/update/db",
                                 json=interview_data, headers={"Content-Type": "application/json"})
            if post.status_code == 200:
                st.write(post.status_code)
                st.write("Interview form submitted succesfully.")
            else:
                st.write(post.status_code)
                st.write("There was an error in the submission.")

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
