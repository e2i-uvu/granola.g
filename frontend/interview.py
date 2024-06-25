import streamlit as st
import requests

backend = "http://go_server:8080/"

st.title("Interview App")

id = st.text_input("Enter your UVU ID:")
if st.button("Submit"):
    response = requests.post(
        backend + "interviewStart", json={"uvuid": id})
    if response.status_code == 200:
        data = response.json()
        st.write(data)
    else:
        st.write(str(response.reason) + str(response.status_code))
