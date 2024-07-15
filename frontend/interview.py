import streamlit as st
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os

load_dotenv()
backend = os.getenv("BACKEND")
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

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
        q1 = str(st.checkbox("Can code"))
        q2 = str(st.number_input("Enjoyment", min_value=1, max_value=10, value=5))
        q3 = str(st.number_input("Social", min_value=1, max_value=10, value=5))

        if st.form_submit_button("Submit"):
            interview_data = {
                'fkuser': str(st.session_state["data"]["pid"]),
                'cancode': q1, 'enjoyment': q2, 'social': q3
            }

            print(interview_data)
            post = requests.post(
                backend + "interviewFinish", auth=HTTPBasicAuth(username, password),
                json=interview_data, headers={"Content-Type": "application/json"})
            if post.status_code == 200:
                st.write(post.status_code)
                st.write("Interview form submitted succesfully.")
            else:
                st.write(post.status_code)
                st.write("There was an error in the submission.")
