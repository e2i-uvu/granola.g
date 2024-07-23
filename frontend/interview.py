import streamlit as st
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os
import time

# when a UVUID is pressed the first time have it go to the next screen
# allow functionality so that you can hit the enter button which will also trigger the submit button
# when all of the enjoyment and other info has been entered correctly, the submit button will return the user to the original screen
# (this has something to do with the session state)

load_dotenv()
backend = os.getenv("BACKEND")
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

st.title("Interview App")


if "IDs_entered" not in st.session_state:
    st.session_state.IDs_entered = []

if "data" not in st.session_state:
    if st.session_state.IDs_entered != []:
        st.write("Interview form submitted succesfully.")
        st.write(st.session_state.IDs_entered)
    id = st.text_input("Enter your UVU ID:")
    if st.button("Submit"):
        response = requests.post(
            backend + "interviewStart", json={"uvuid": str(id)}, headers={"Content-Type": "application/json"})
        if response.status_code == 200:
            st.session_state["data"] = response.json()
            time.sleep(0.01) # this allows time for the sessionstate to update before making the page reload
            st.rerun() # reload the current page (these two line fix the submit button having to be pushed twice)
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
            post = requests.post(
                backend + "interviewFinish", auth=HTTPBasicAuth(username, password),
                json=interview_data, headers={"Content-Type": "application/json"})
            if post.status_code == 200:
                st.write(post.status_code)
                st.session_state.IDs_entered.append(int(st.session_state["data"]["uvuid"]))
                del st.session_state["data"]
                time.sleep(0.01)
                st.rerun()
            else:
                st.write(post.status_code)
                st.write("There was an error in the submission.")
