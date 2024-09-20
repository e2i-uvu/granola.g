import streamlit as st
import requests
from requests.auth import HTTPBasicAuth
import json
import os

# Initialize session_state 'backend' if not already set
if 'backend' not in st.session_state:
    st.write('Initializing backend in session state')
    st.session_state['backend'] = {
        "url": os.getenv("BACKEND", ""),
        "username": os.getenv("USERNAME1", ""),
        "password": os.getenv("PASSWORD", ""),
    }

st.title("Build Quick and Dirty Team")

# Correct test data without numbered keys
test_data = {
    "project_name": "Video Game and Website",
    "project_type": "Tech",
    "employees": [
        {"employee": "Game dev", "amount": 2},
        {"employee": "Frontend", "amount": 2},
        {"employee": "Web dev", "amount": 1}
    ],
    "total_employees": 5
}

st.json(test_data)

# Button to create team
create_team = st.button("Create Team")

if create_team:
    # Check if URL, username, and password are set
    if not st.session_state['backend']["url"] or not st.session_state['backend']["username"] or not st.session_state['backend']["password"]:
        st.error("Backend URL, username, or password is not set.")
    else:
        # Make the request to get employees
        try:
            r = requests.get(
                st.session_state['backend']["url"] + "/teams",
                json=test_data,  # Directly pass the correct JSON structure
                auth=HTTPBasicAuth(
                    st.session_state['backend']["username"],
                    st.session_state['backend']["password"]
                ),
            )

            # Print the raw response content for debugging
            st.write("Raw response content:", r.content.decode('utf-8'))

            # Only attempt to parse JSON if the response contains data
            if r.content and r.status_code == 200:
                st.header("Response from backend")
                try:
                    to_send = r.json()  # Attempt to parse JSON
                    st.json(to_send)
                    st.success("Success")

                    # Now post to create the team
                    new_r = requests.post(
                        st.session_state['backend']["url"] + "/teams",
                        json=to_send,  # Send parsed JSON as payload
                        auth=HTTPBasicAuth(
                            st.session_state['backend']["username"],
                            st.session_state['backend']["password"],
                        ),
                    )

                    if new_r.status_code == 200:
                        st.header("Team creation response from backend")
                        received = new_r.json()
                        st.json(received)
                        st.success("Team created successfully")
                    else:
                        st.error(f"Failed to create team. Status code: {new_r.status_code}")
                except json.JSONDecodeError:
                    st.error("Failed to decode JSON from response.")
            else:
                st.error(f"Failed to fetch employees. Status code: {r.status_code} or empty response")

        except Exception as e:
            st.error(f"An error occurred: {e}")
