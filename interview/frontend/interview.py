import streamlit as st
import requests

st.title("Interview App")

id = st.text_input("Enter your UVU ID:")
if st.button("Submit"):
    response = requests.get(f"http://go_server:8080/{id}")
    if response.status_code == 200:
        data = response.json()
        st.write(data["name"], data["lang"], data["aoi"])
    else:
        st.write("Error: Unable to fetch message")
