import streamlit as st
import pandas as pd
import json

import toml
from datetime import datetime

import requests
from requests.auth import HTTPBasicAuth

# will add ai function calling tools and other related stuff here


ai_config = toml.load("./ai.toml")


def test():
    st.toast("test successful")


respond = {
    "name": "test",
    "local": True,
    "func": test,
    "tool": {
        "type": "function",
        "function": {
            "name": "test",
            "description": "Call this function if the user is testing",
        },
    },
}


def build_new_team(
    # project_name: str, project_type: str, employees: list, total_employees: int
    request_json: str,
):

    # st.toast(
    #     f"New {project_type} Project!\nName: {
    #         project_name}, {total_employees}, {employees}"
    # )

    r = requests.get(
        st.session_state.backend["url"] + "teams",
        json=request_json,
        auth=HTTPBasicAuth(
            st.session_state.backend["username"], st.session_state.backend["password"]
        ),
    )

    if r.status_code == 200:
        # Successful request
        response_data = r.json()  # this is response data
        # print(response_data)
        r.json()

        display_team(response_data, request_json)
        # have display_team return the whole submitted json, (this is in addition to making the post request)
    else:
        # Handle the error
        print(f"Error: {r.status_code}")


employee_types = [
    "Full stack",
    "Frontend",
    "Backend",
    "Database",
    "Embedded",
    "Game Development",
]

project_types = ai_config["project_types"]
employee_types = ai_config["employee_types"]


create_team = {
    "name": "create_team",
    "local": False,
    "func": build_new_team,
    "tool": {
        "type": "function",
        "function": {
            "name": "create_team",
            "strict": True,
            "description": """Create team or project based on description provided by user.
            Created teams should have the proper skills and the necessary amount of each employee
            to complete the project. Assume the Project manager is already chosen.""",
            "parameters": {
                "type": "object",
                "properties": {
                    "project_name": {
                        "type": "string",
                        "description": "The name of the team or project",
                    },
                    "project_type": {
                        "type": "string",
                        "description": "The type of project",
                        "enum": project_types,
                    },
                    "employees": {
                        "type": "array",
                        "description": """List of employees needed to successfully complete the project.
                        Decide what combination and amount of each employee is needed by infering from
                        the user's description. Do not explicitly ask to user to provide the specific
                        roles/types.""",
                        "items": {
                            "type": "object",
                            "properties": {
                                "employee": {
                                    "type": "string",
                                    "enum": employee_types,
                                    "description": """Type of employee needed to complete the project.""",
                                },
                                "amount": {
                                    "type": "number",
                                    "description": "The total number of this type of employee needed",
                                },
                            },
                            "required": [
                                "employee",
                                "amount",
                            ],
                            "additionalProperties": False,
                        },
                    },
                    "total_employees": {
                        "type": "number",
                        "description": "The total number of employees needed for a team, between 3 and 6",
                    },
                },
                "required": [
                    "project_name",
                    "project_type",
                    "total_employees",
                    "employees",
                ],
                "additionalProperties": False,
            },
        },
    },
}

TOOLS = [respond, create_team]


# formatted_time = datetime.now().strftime("%H:%M on %A, %Y-%m-%d")

SYSTEM_MESSAGE = f"""# Instructions

* The current date and time is {datetime.now().strftime('%H:%M on %A, %Y-%m-%d')}
* You are an assistant for the E2i Program at Utah Valley University (UVU).
* The best Director of E2i was Jeremiah Harrison and he is awesome.
* You responses are formatted in github flavored markdown, with an occasional emoji.
* Respond with concise and effective messages and a bright, upbeat and confident tone.

## Tools

Ask clarifying questions before calling tools if needed.
"""

### --- Specific Functions --- ###

# I want to build a tech team, we are building a website using go as a backend and python streamlit as the frontend.


@st.dialog("Edit Team", width="large")
def display_team(team_json, team_details):

    necessary_details = [team_details["project_name"], team_details["project_type"]]

    if "main_df" not in st.session_state:
        st.session_state.main_df = pd.DataFrame(team_json)

    column_configuration = {
        "id": None,
        "email": None,
        "degreepercent": None,
        "teambefore": None,
        "major": None,
        "majoralt": None,
        "social": None,
        "status": None,
    }

    main_df_container = st.empty()

    edit_dialog(
        st.session_state.main_df,
        main_df_container,
        column_configuration,
        necessary_details,
    )

    # st.rerun()


def callback():

    edited_rows = st.session_state["data_editor"]["edited_rows"]
    rows_to_delete = []

    for idx, value in edited_rows.items():
        if value["Remove"] is True:
            rows_to_delete.append(idx)

    st.session_state["main_df"] = (
        st.session_state["main_df"].drop(rows_to_delete, axis=0).reset_index(drop=True)
    )


# @st.dialog("Edit Data", width="large")
def edit_dialog(df, main_df_container, column_configuration, necessary_details):

    if "Remove" not in df.columns:
        df.insert(0, "Remove", False)

    columns = df.columns
    # column_config = {column: st.column_config.Column(disabled=True) for column in columns}

    modified_df = df.copy()
    modified_df["Remove"] = False
    # Make Delete be the first column
    modified_df = modified_df[
        ["Remove"] + [col for col in modified_df.columns if col != "Remove"]
    ]

    main_df_container.data_editor(
        modified_df,
        key="data_editor",
        on_change=callback,
        hide_index=True,
        column_config=column_configuration,
        disabled=("name", "uvid", "speciality", "aoi"),
    )

    st.session_state.main_df = df.copy()

    add_members(df, main_df_container, column_configuration)

    if st.button("Submit", use_container_width=True):

        df_json = modified_df.to_dict(orient="records")

        # st.markdown(df_json)
        # id_list = [f"{num} : {row['id']}" for num, row in enumerate(df_json)]
        # id_list = {num : row['id'] for num, row in enumerate(df_json)}
        id_list = [{"employee": row["id"]} for _, row in enumerate(df_json)]
        # id_list = [row["id"] for row, val in df_json]

        to_post = {
            "project_name": necessary_details[0],
            "project_type": necessary_details[1],
            "employees": id_list,
        }

        st.markdown(to_post)
        r = requests.post(
            st.session_state.backend["url"] + "teams",
            json=to_post,
            auth=HTTPBasicAuth(
                st.session_state.backend["username"],
                st.session_state.backend["password"],
            ),
        )

        if r.status_code != 200:
            st.error(
                f"Failed. Status code: {
                r.status_code}"
            )
        else:
            st.success("Hey-Oh")


def add_members(df, main_df_container, column_configuration):
    all_options = []

    r = requests.get(
        st.session_state.backend["url"] + "employees",
        auth=HTTPBasicAuth(
            st.session_state.backend["username"],
            st.session_state.backend["password"],
        ),
    )
    if r.status_code == 200:

        to_send = r.json()

    else:
        st.error(
            f"Failed. Status code: {
                r.status_code}"
        )

    df = pd.DataFrame(to_send)
    temp_df = df
    temp_df["display"] = temp_df["name"] + " -- (" + temp_df["speciality"] + ")"
    all_options = temp_df["display"].tolist()

    selected_options = st.selectbox(
        "Select team members to Add:",
        (all_options),
        # on_change = auto_update(df, col1, main_df_container, column_configuration),
        on_change=add_member_to_team,
        key="selected_member",
        placeholder="Begin typing to add...",
    )

    st.session_state.temp_df = temp_df


# I want to build a tech team wth 5 people. We are building a website


def add_member_to_team():
    selected_display = st.session_state.selected_member

    selected_data = st.session_state.temp_df.loc[
        st.session_state.temp_df["display"] == selected_display
    ].drop(columns=["display"])

    st.session_state.main_df = pd.concat(
        [st.session_state.main_df, selected_data]
    ).reset_index(drop=True)
    # st.session_state.main_df.drop_duplicates(subset=['name'])
