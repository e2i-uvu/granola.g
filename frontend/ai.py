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

        display_team(response_data)
        # have display_team return the whole submitted json, (this is in addition to making the post request)
    else:
        # Handle the error
        print(f"Error: {r.status_code}")

    # TODO: Guts
    # after edits send to same endpoint but as a post request ('Don't use fake data for this')
    # Display team and modal dialog here
    # when submit is hit, we send a post request back to the same endpoint


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
def display_team(team_json):
    team_json_list = []
    team_json_partial = []
    example_team_json_list = []

    # st.markdown(team_json)

    # for item in team_json:
    #     for key in item:
    #         team_json_partial.append(item[key])
    #         team_json_list.append(item[key])
    #         example_team_json_list.append(item[key])

    # tj = [j for i, j in team_json.itmes()]

    df = pd.DataFrame(team_json)

    if "main_df" not in st.session_state:
        st.session_state.main_df = df

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
    # main_df_container.dataframe(
    #     st.session_state.main_df, hide_index=True, column_config=column_configuration
    # )
    edit_dialog(st.session_state.main_df, main_df_container, column_configuration)

    column1, column2, column3 = st.columns([1, 1, 5], vertical_alignment="bottom")

    # with column1:
    #     if st.button("Edit", use_container_width=True):
    #         # display_team()
    #         edit_dialog(
    #             st.session_state.main_df, main_df_container, column_configuration
    #         )

    with column2:
        if st.button("Submit", use_container_width=True):
            # st.toast("Submitted!")
            # TODO: Henry - write post request here
            # POST TO DATABASE HERE:
            # This is where we send back the confirmed team
            df_json = st.session_state.main_df.to_dict(orient="records")
            # st.json(df_json)
            # print(json.dumps(df_json, indent=4))

            r = requests.post(
                st.session_state.backend["url"] + "teams",
                json=json.dumps(df_json),
                auth=HTTPBasicAuth(
                    st.session_state.backend["username"],
                    st.session_state.backend["password"],
                ),
            )
            if r.status_code == 200:
                # st.header("Response from backend")

                recieved = r.json()

                # st.json(recieved)
                # st.success("success")

                print(r.status_code)

            else:
                st.error(
                    f"Failed. Status code: {
                     r.status_code}"
                )
        # add_members(df, col1, main_df_container, column_configuration)


# @st.dialog("Edit Data", width="large")
def edit_dialog(df, main_df_container, column_configuration):
    if "Remove" not in st.session_state.main_df.columns:
        st.session_state.main_df.insert(0, "Remove", False)

    # edited_df = st.data_editor(
    #     st.session_state.main_df, hide_index=True, column_config=column_configuration,
    #     disabled = ('name', 'uvid', 'speciality', 'aoi')
    # )

    main_df_container.data_editor(
        st.session_state.main_df,
        hide_index=True,
        column_config=column_configuration,
    )
    st.success("Nice")

    col1, col2 = st.columns([3, 1], vertical_alignment="bottom")

    with col2:
        if st.button("Save"):
            updated_df = st.session_state.main_df[
                st.session_state.main_df["Remove"] == False
            ]
            # .drop(
            #     columns=["Remove"]
            # )
            # st.session_state.main_df = updated_df
            # st.session_state.main_df = updated_df.drop(columns=["Remove"])

            if "selected_row" in st.session_state:
                st.session_state.main_df = (
                    pd.concat([st.session_state.main_df, st.session_state.selected_row])
                    .drop_duplicates()
                    .reset_index(drop=True)
                )
                del st.session_state.selected_row

            # main_df_container.dataframe(
            #     st.session_state.main_df,
            #     hide_index=True,
            #     column_config=column_configuration,
            # )
            st.session_state.selected_rows = []
            selected_options = False
            # st.rerun()

    add_members(df, col1, main_df_container, column_configuration)


def add_members(df, col1, main_df_container, column_configuration):
    all_options = []
    # TODO: Henry -
    # GET REQUEST FROM DATABASE, SHOULD RETURN JSON INFORMATION OF FROM EVERY PERSON
    # json_example_data = requests.get(... )

    r = requests.get(
        st.session_state.backend["url"] + "employees",
        auth=HTTPBasicAuth(
            st.session_state.backend["username"],
            st.session_state.backend["password"],
        ),
    )
    to_send = ""

    if r.status_code == 200:

        # st.header("Response from backend")

        to_send = r.json()
        # st.json(r.json())
        # st.success("success")

    else:
        st.error(
            f"Failed. Status code: {
                r.status_code}"
        )
    for item in to_send:
        for key in item:
            all_options.append(item[key])

    df = pd.DataFrame(to_send)
    temp_df = df
    temp_df["display"] = temp_df["name"] + " -- (" + temp_df["speciality"] + ")"
    all_options = temp_df["display"].tolist()

    with col1:
        selected_options = st.selectbox(
            "Select team members to Add:",
            (all_options),
            # on_change = auto_update(df, col1, main_df_container, column_configuration),
            # default=None,
            placeholder="Begin typing to add...",
        )


# def auto_update(df, col1, main_df_container, column_configuration):

# if selected_options:
#     selected_df = df[df["display"].isin(selected_options)]

#     if "selected_rows" not in st.session_state:
#         st.session_state.selected_rows = []

#     selected_df.drop(columns=["display"], inplace=True)

#     st.session_state.selected_rows.append(selected_df)

#     combined_selected_df = (
#         pd.concat(st.session_state.selected_rows)
#         .drop_duplicates()
#         .reset_index(drop=True)
#     )
#     st.session_state.selected_row = combined_selected_df

#     st.dataframe(selected_df, hide_index=True, column_config=column_configuration)
# I want to make a tech team with 5 people. We are making a website.
