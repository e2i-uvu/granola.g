import streamlit as st
import requests
from requests.auth import HTTPBasicAuth
import json


st.title("build quick n dirty team")

test_data = {
    "project_name": "Video Game and Website",
    "project_type": "Tech",
    "employees": [
        {"employee": "Game dev", "amount": 2},
        {"employee": "Frontend", "amount": 2},
        {"employee": "Web dev", "amount": 1},
    ],
    "total_employees": 5,
}

st.json(test_data)


create_team = st.button("Create Team")
if create_team:
    r = requests.get(
        st.session_state.backend["url"] + "employees",
        json=json.dumps(test_data),
        auth=HTTPBasicAuth(
            st.session_state.backend["username"], st.session_state.backend["password"]
        ),
    )

    if r.status_code == 200:

        st.header("Response from backend")

        to_send = r.json()
        st.json(r.json())
        st.success("success")

        new_r = requests.post(
            st.session_state.backend["url"] + "employees",
            json=to_send,
            auth=HTTPBasicAuth(
                st.session_state.backend["username"],
                st.session_state.backend["password"],
            ),
        )

        if new_r.status_code == 200:

            st.header("Response from backend")

            recieved = new_r.json()
            st.json(recieved)
            st.success("success")

        else:

            st.error(
                f"Failed. Status code: {
                     r.status_code}"
            )

    else:
        st.error(
            f"Failed. Status code: {
                 r.status_code}"
        )
