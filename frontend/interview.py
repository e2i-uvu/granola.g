import streamlit as st
import requests

backend = "http://go_server:8080/"

st.title("Interview App")

if "data" not in st.session_state:
    id = st.text_input("Enter your UVU ID:")
    if st.button("Submit"):
        response = requests.post(
            backend + "interviewStart", json={"uvuid": id})
        if response.status_code == 200:
            data = response.json()
            st.session_state["data"] = data

        else:
            st.write(str(response.reason) + str(response.status_code))
else:
    data = st.session_state["data"]
    with st.form(key="interviewForm"):
        q1 = st.text_input("Fibonnaci Sequence")
        q2 = st.text_input("Game Engine Library")
        if st.form_submit_button("Submit"):
            data["q1"] = q1
            data["q2"] = q2
            st.dataframe(data, use_container_width=True)
