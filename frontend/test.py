import streamlit as st
import requests
from requests.auth import HTTPBasicAuth


st.title("build quick n dirty team")
st.caption("almost there")

test_data = {
    "project_name": "Video Game and Website",
    "project_type": "Tech",
    "employees": [
        {"employee": "Game", "amount": 2},
        {"employee": "Frontend", "amount": 2},
        {"employee": "Backend", "amount": 1},
    ],
    "total_employees": 5,
}

test_post = {
    "project_name": "Video Game and Website",
    "project_type": "Tech",
    "employees": [
        {"employee": "r_jnhdfa9d8asdoifh89"},
        {"employee": "r_jnhdfa9d8nfbkjvnsk"},
        {"employee": "r_jnhdhi890u98dsuyfg"},
    ],
}


st.json(test_data)


if st.button("Create Team"):
    r = requests.get(
        st.session_state.backend["url"] + "teams",
        json=test_data,
        auth=HTTPBasicAuth(
            st.session_state.backend["username"], st.session_state.backend["password"]
        ),
    )

    if r.status_code == 200:

        st.header("Response from backend")

        to_send = test_post

        st.json(r.json())
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
