import streamlit as st
import requests
from requests.auth import HTTPBasicAuth
import json


st.title("build quick n dirty team")
st.caption("almost there")

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


if st.button("Create Team"):
    r = requests.get(
        st.session_state.backend["url"] + "teams",
        json=json.dumps(test_data),
        auth=HTTPBasicAuth(
            st.session_state.backend["username"], st.session_state.backend["password"]
        ),
    )

    if r.status_code == 200:

        st.header("Response from backend")

        to_send = r.json()
        # BUG: error ^^^ is here. the `r.json()` method returns a python dictionary
        # Additionally, I tried `r.text` which just returns a string of the response
        # and that is a Json Parse Error, unexpected end of data at line 1 column 1

        st.json(to_send)
        st.success("success")

        new_r = requests.post(
            st.session_state.backend["url"] + "teams",
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
