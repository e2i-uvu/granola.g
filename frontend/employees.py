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
            st.json(r.json)
    elif option == 'status':
        st.write('Here is the status')
    elif option == 'fire':
        st.write('Congratulations! You have been fired!')


# TODO: Guts this will be the status page for current employees
# Including hiring and firing as we talked about today
