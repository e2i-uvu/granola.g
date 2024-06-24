import streamlit as st
import requests

backend = "http://go_server:8080/"

st.title("Interview App")

id = st.text_input("Enter your UVU ID:")
if st.button("Submit"):
    response = requests.post(
        backend + "interviewStart", json={"uvuid": int(id)})
    if response.status_code == 200:
        data = response.json()
        st.write(data)
    else:
        st.write("Error: Unable to fetch message" + str(response.status_code))
