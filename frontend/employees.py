import streamlit as st
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()
backend = os.getenv("BACKEND")
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

st.title("Employees")

option = st.selectbox('Select one',
                      ('Select an option', 'hire', 'status', 'fire')
                      )

# st.write(f'You selected: {option}')
if option != 'Select an option':
    if option == 'hire':
        st.write('You are hiring this person')
        r = requests.get(backend + "hire",
                         auth=HTTPBasicAuth(username, password))
        if (r.status_code != 200):
            st.text("The world is dying")
            st.text(r.status_code)
        else:
            data = r.json()
            df = pd.DataFrame(data)
            st.data_editor(df)
    elif option == 'status':
        st.write('Here is the status')
        r = requests.get(backend + "status",
                         auth=HTTPBasicAuth(username, password))
        if (r.status_code != 200):
            st.text("The world is dying")
            st.text(r.status_code)
        else:
            st.json(r.json())
    elif option == 'fire':
        st.write('Congratulations! You have been fired!')


# TODO: Guts this will be the status page for current employees
# Including hiring and firing as we talked about today

# [
# 0:{
# "pid":2
# "uvuid":10955272
# "name":"Henry"
# "lang":"Golang"
# "aoi":"Anything"
# "cancode":true
# "enjoyment":4
# "social":6
# "score":1
# }
# 1:{
# "pid":3
# "uvuid":10810570
# "name":"Guts"
# "lang":"Python"
# "aoi":"Front End"
# "cancode":false
# "enjoyment":2
# "social":10
# "score":6
# }
# ]