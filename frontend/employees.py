import streamlit as st
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os

load_dotenv()
backend = os.getenv("BACKEND")
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

st.title("Employees")

# TODO: Guts this will be the status page for current employees
# Including hiring and firing as we talked about today


r = requests.get(backend + "hire", auth=HTTPBasicAuth(username, password))
if (r.status_code != 200):
    st.text("The world is dying")
    st.text(r.status_code)
else:
    st.json(r.body)
