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


# GET must retrieve:
#   Join table of employees and projects
#   Project table

# test data
employees = [
    {
        "eid": 1,
        "ename": "Pedro",
        "escore": 100,
        "pname": "Windows"
    },
    {
        "eid": 2,
        "ename": "Halfonso",
        "escore": 9000,
        "pname": "ChadLinux"

    },
    {
        "eid": 3,
        "ename": "Pikachu",
        "escore": 25,
        "pname": "IDRobber"
    }
]

projects  = ["Windows", "ChadLinux","IDRobber"]

columnConfig = {
    "eid": st.column_config.Column(label="eid", disabled = True),
    "ename": st.column_config.Column(label="ename", disabled = True),
    "escore": st.column_config.Column(label="escore", disabled = True),
    "pname": st.column_config.SelectboxColumn(label="pname", options = projects)
}

session = HTTPBasicAuth(username, password)
#r = requests.get(backend + _ +, auth=HTTPBASICAuth(username, password))
#raw_data = r.json()

raw_data = pd.DataFrame(employees)

st.title("Team Building")
edited_data = st.data_editor(raw_data, column_config = columnConfig, hide_index = True)

if st.button('Save'):
    filtered_data = edited_data[["eid", "pname"]].to_dict()
    response = requests.post(backend + _,
                             json=filtered_data,
                             auth=session)
    if response.status_code == 200:
        st.success("Changes saved.")
    else:
        st.error("Failure in saving changes.")

if st.button('Reset'):
    pass




