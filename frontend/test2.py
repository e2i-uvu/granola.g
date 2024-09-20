import streamlit as st
import requests
from requests.auth import HTTPBasicAuth
import json
import os
from ai import display_team

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
    display_team(  # FIX: remove
        [
            {
                0: {
                    "id": "E001",
                    "name": "Alice Johnson",
                    "email": "alice.johnson@uvu.edu",
                    "uvid": "U12345678",
                    "degreepercent": 85,
                    "teambefore": True,
                    "speciality": "Software Engineering",
                    "major": "Computer Science",
                    "majoralt": "Mathematics",
                    "aoi": "Artificial Intelligence",
                    "social": 5,
                    "status": 1,
                }
            },
            {
                1: {
                    "id": "E002",
                    "name": "Bob Smith",
                    "email": "bob.smith@uvu.edu",
                    "uvid": "U87654321",
                    "degreepercent": 90,
                    "teambefore": False,
                    "speciality": "Data Analysis",
                    "major": "Information Systems",
                    "majoralt": "Statistics",
                    "aoi": "Big Data",
                    "social": 7,
                    "status": 2,
                }
            },
            {
                2: {
                    "id": "E003",
                    "name": "Catherine Lee",
                    "email": "catherine.lee@uvu.edu",
                    "uvid": "U11223344",
                    "degreepercent": 75,
                    "teambefore": True,
                    "speciality": "Cybersecurity",
                    "major": "Computer Science",
                    "majoralt": "Criminal Justice",
                    "aoi": "Network Security",
                    "social": 6,
                    "status": 1,
                }
            },
            {
                3: {
                    "id": "E004",
                    "name": "David Brown",
                    "email": "david.brown@uvu.edu",
                    "uvid": "U44332211",
                    "degreepercent": 80,
                    "teambefore": False,
                    "speciality": "Project Management",
                    "major": "Business Administration",
                    "majoralt": "Management",
                    "aoi": "Agile Methodologies",
                    "social": 8,
                    "status": 2,
                }
            },
            {
                4: {
                    "id": "E005",
                    "name": "Eva Green",
                    "email": "eva.green@uvu.edu",
                    "uvid": "U55667788",
                    "degreepercent": 95,
                    "teambefore": True,
                    "speciality": "Machine Learning",
                    "major": "Computer Engineering",
                    "majoralt": "Data Science",
                    "aoi": "Deep Learning",
                    "social": 9,
                    "status": 1,
                }
            },
            {
                5: {
                    "id": "E006",
                    "name": "Frank White",
                    "email": "frank.white@uvu.edu",
                    "uvid": "U99887766",
                    "degreepercent": 70,
                    "teambefore": False,
                    "speciality": "Web Development",
                    "major": "Information Technology",
                    "majoralt": "Graphic Design",
                    "aoi": "Frontend Development",
                    "social": 4,
                    "status": 2,
                }
            },
        ]
    )  # testing

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
