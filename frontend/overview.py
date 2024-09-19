import streamlit as st
import requests
from requests.auth import HTTPBasicAuth
import pandas as pd

st.title("Overview")

#test_data = [{"id" : "11111111", "name": "Bob", "email": "bob@uvu.edu", "uvid": "111111111", "degreepercent": 99, "teambefore": True, "speciality": "Machine Learning", "major": "Computational Data Science", "aoi": "Artificial Intelligence", "social": 5, "status": 1}]

def encode_status_code(status: str):
    match status:
        case "Hired":
            return 1
        case "Not hired":
            return 0
        case "Fired":
            return -2
        # TODO: Add the rest of the status codes!
        case "":
            return 1#status


def format_DataFrame(data: list[dict[str, str | int | bool]]):
    def decode_status_code(status: int):
        match status:
            case 1:
                st.write(True)
                return "Hired"
            case 0:
                return "Not hired"
            case -1:
                return "Fired"
        # TODO: Add the rest of the status codes!
            case _:
                return "Not hired"

    df = pd.DataFrame(data)

    df["status"] = [decode_status_code(value) for value in df["status"]]#.iloc()]

    # if "id" in df and "pid" not in df:
    #     df["pid"] = df["id"]
    #     del df['id']
    columns_order = ["status"] + [col for col in df.columns if col != "status"]
    df = df[columns_order]
    return df


EMPLOYEE_STATUS_CODE: list[str] = [
    "Fired",
    "Hired",
    "Not hired"
]

EMPLOYEE_COLUMN_CONFIG = {
    "status": st.column_config.SelectboxColumn(label="Status", options=EMPLOYEE_STATUS_CODE),
    "id": st.column_config.Column(label="Employee ID", disabled=True),
    "uvid": st.column_config.Column(label="UVID", disabled=True),
    "name": st.column_config.Column(label="Name", disabled=True),
    "email": st.column_config.Column(label="eMail", disabled=True),
    "degreepercent": st.column_config.Column(label="Degree Percent", disabled=True),
    "teambefore": st.column_config.Column(label="Team Before?", disabled=True),
    "speciality": st.column_config.Column(label="Speciality", disabled=True),
    "major": st.column_config.Column(label="Major", disabled=True),
    "aoi": st.column_config.Column(label="Interest", disabled=True),
    "social": st.column_config.Column(label="Social", disabled=True),
}


def main():
    # NOTE:
    # status + hire + fire + all surveys
    # pending projects + running projects (teams and descriptions)
    options = ("Select an option", "Employees", "Team Projects")
    # TODO: Delete this!
    # old_options = (
    #         "Select an option",
    #         "hire",
    #         "status",
    #         "fire",
    #         "all surveys",
    #         "pending projects",
    #     )
    option = st.selectbox("Select one", options)  # old_options)
    # st.write(f'You selected: {option}')
    if option != "Select an option":
        option_selection(option)


def option_selection(option):
    # if option == "hire":
    #     show_hire()
    # elif option == "status":
    #     show_status()
    # elif option == "fire":
    #     show_fire()
    #     st.write("Congratulations! You have been fired!")
    # elif option == "all surveys":
    #     show_all_surveys()
    # if option == "pending projects":
    #     show_pending_projects()
    match option:
        case "Employees":
            show_status()
        case "Team Projects":
            show_pending_projects()


def show_pending_projects():
    st.write("Here is the status")
    r = requests.get(
        st.session_state.backend["url"] + "project",
        auth=HTTPBasicAuth(
            st.session_state.backend["username"], st.session_state.backend["password"]
        ),
    )
    if r.status_code != 200:
        st.text("The world is dying")
        st.text(r.status_code)
    else:
        # st.json(r.json())
        st.dataframe(pd.DataFrame(r.json()), hide_index=True)


def show_status():
    st.write("Here is the status")
    r = requests.get(
        st.session_state.backend["url"] + "employees",
        auth=HTTPBasicAuth(
            st.session_state.backend["username"], st.session_state.backend["password"]
        ),
    )
    # df = format_DataFrame(test_data) 
    # edited_df = st.data_editor(df, column_config=EMPLOYEE_COLUMN_CONFIG, hide_index=True, use_container_width=True)
    # if st.button("Save Changes"):
    #     edited_df["status"] = edited_df["status"].apply(encode_status_code)
    #     filtered_data = edited_df[["pid", "status"]].to_dict(orient="records")
    #
    #     response = requests.post(
    #         st.session_state.backend["url"] + "status",
    #         json=filtered_data,
    #         auth=HTTPBasicAuth(
    #             st.session_state.backend["username"],
    #             st.session_state.backend["password"],
    #         ),
    #     )
    #     if response.status_code == 200:
    #         st.success("Changes save successfully!")
    #     else:
    #         st.error(
    #             f"Failed to save changes. Status code: {
    #                  response.status_code}"
    #         )
    if r.status_code != 200:
        st.text("The world is dying")
        st.text(r.status_code)
    else:
        # st.json(r.json())
        df = format_DataFrame(r.json())
        # st.dataframe(df, hide_index=True)
        edited_df = st.data_editor(df, column_config=EMPLOYEE_COLUMN_CONFIG, hide_index=True, use_container_width=True)
        if st.button("Save Changes"):
            edited_df["status"] = edited_df["status"].apply(encode_status_code)
            filtered_data = edited_df[["pid", "status"]].to_dict(orient="records")

            # FIX: To Henry: As it is now, the Employee struct sends a string Id and string UVID, but the EmployeeStatus gets an int PID. 

            response = requests.post(
                st.session_state.backend["url"] + "employees",
                json=filtered_data,
                auth=HTTPBasicAuth(
                    st.session_state.backend["username"],
                    st.session_state.backend["password"],
                ),
            )
            if response.status_code == 200:
                st.success("Changes save successfully!")
            else:
                st.error(
                    f"Failed to save changes. Status code: {
                         response.status_code}"
                )

# TODO: Obsolete. Delete this later!!!
# def show_all_surveys():
#     st.write("Here is the status")
#     r = requests.get(
#         st.session_state.backend["url"] + "preinterview",
#         auth=HTTPBasicAuth(
#             st.session_state.backend["username"], st.session_state.backend["password"]
#         ),
#     )
#     if r.status_code != 200:
#         st.text("The world is dying")
#         st.text(r.status_code)
#     else:
#         st.json(r.json())


# TODO: Copy submit button and delete
def show_fire():
    st.write("Here is the status")
    r = requests.get(
        st.session_state.backend["url"] + "fire",
        auth=HTTPBasicAuth(
            st.session_state.backend["username"], st.session_state.backend["password"]
        ),
    )
    if r.status_code != 200:
        st.text("The world is dying")
        st.text(r.status_code)
    else:
        # st.json(r.json())
        df = pd.DataFrame(r.json())

        # NOTE: Generate firing checkbox
        df["status"] = [False for row in df.index]
        columns_order = ["status"] + \
            [col for col in df.columns if col != "status"]
        df = df[columns_order]

        column_config = {
            "status": st.column_config.CheckboxColumn(label="Fire?"),
            "pid": st.column_config.Column(label="PID", disabled=True),
            "uvuid": st.column_config.Column(label="UVUID", disabled=True),
            "name": st.column_config.Column(label="Name", disabled=True),
            "lang": st.column_config.Column(label="Language", disabled=True),
            "aoi": st.column_config.Column(label="Area of Interest", disabled=True),
            "cancode": st.column_config.Column(label="Can Code", disabled=True),
            "enjoyment": st.column_config.Column(label="Enjoyment", disabled=True),
            "social": st.column_config.Column(label="Social", disabled=True),
            "score": st.column_config.Column(label="Score", disabled=True),
        }

        # NOTE: Show Spreadsheet
        edited_df = st.data_editor(
            df, column_config=column_config, hide_index=True)

        # NOTE: Submitting changes
        if st.button("Save Changes"):
            edited_df["status"] = edited_df["status"].apply(
                lambda x: -2 if x == True else 1
            )
            filtered_data = edited_df[["pid", "status"]].to_dict(
                orient="records")

            # st.dataframe(edited_df)

            response = requests.post(
                st.session_state.backend["url"] + "hire",
                json=filtered_data,
                auth=HTTPBasicAuth(
                    st.session_state.backend["username"],
                    st.session_state.backend["password"],
                ),
            )
            if response.status_code == 200:
                st.success("Changes save successfully!")
            else:
                st.error(
                    f"Failed to save changes. Status code: {
                        response.status_code}"
                )


def show_hire():
    r = requests.get(
        st.session_state.backend["url"] + "hire",
        auth=HTTPBasicAuth(
            st.session_state.backend["username"], st.session_state.backend["password"]
        ),
    )
    # FIX: this ->   ^^^^^^^^^^^^^^^^  is broken

    if r.status_code == 400:
        st.text("There is currently no one to hire")
        st.text(r.status_code)
    elif r.status_code != 200:
        st.text("The world is dying")
        st.text(r.status_code)
    else:
        st.write("You are hiring this person")
        data = r.json()
        df = pd.DataFrame(data)

        df["status"] = df["status"].apply(lambda x: x >= 1)
        # ^converts the 'hired' column into boolean values to show up as checkmarks

        if "checkboxes" not in st.session_state:
            st.session_state["checkboxes"] = df["status"].tolist()

        df["status"] = st.session_state["checkboxes"]

        columns_order = ["status"] + \
            [col for col in df.columns if col != "status"]
        df = df[columns_order]
        # ^reorders the columns to put 'hired' column at the front of the list

        column_config = {
            "status": st.column_config.Column(label="Hire"),
            "pid": st.column_config.Column(label="PID", disabled=True),
            "uvuid": st.column_config.Column(label="UVUID", disabled=True),
            "name": st.column_config.Column(label="Name", disabled=True),
            "lang": st.column_config.Column(label="Language", disabled=True),
            "aoi": st.column_config.Column(label="Area of Interest", disabled=True),
            "cancode": st.column_config.Column(label="Can Code", disabled=True),
            "enjoyment": st.column_config.Column(label="Enjoyment", disabled=True),
            "social": st.column_config.Column(label="Social", disabled=True),
            "score": st.column_config.Column(label="Score", disabled=True),
        }

        # NOTE: Show Spreadsheet
        edited_df = st.data_editor(
            df, column_config=column_config, hide_index=True)

        st.session_state["checkboxes"] = edited_df["status"].tolist()

        if st.button("Save Changes"):
            edited_df["status"] = edited_df["status"].apply(
                lambda x: 1 if x else 0)
            filtered_data = edited_df[["pid", "status"]].to_dict(
                orient="records")

            response = requests.post(
                st.session_state.backend["url"] + "hire",
                json=filtered_data,
                auth=HTTPBasicAuth(
                    st.session_state.backend["username"],
                    st.session_state.backend["password"],
                ),
            )
            if response.status_code == 200:
                st.success("Changes save successfully!")
            else:
                st.error(
                    f"Failed to save changes. Status code: {
                        response.status_code}"
                )
                st.write(f"Error: {response.text}")

        if st.button("Show session state"):
            st.write(st.session_state)


main()
# NOTE:
# Read everything in, if the hire is 1, if it is false then it is 0.
# I want the hire box to appear in column 1, and I want it to be a checkbox
#

# copy the submit code for the json post request from interview.py
# check out the session state example that is in interview.py
# nothing should be able to be changed except for the newly added 'hire' checkbox
# if the 'hire' dropdown option is selected and the 'submit button is pressed',
# then a json of the pid and the hire status will be returned

# hire page should sort by the score value
# status pages should sort by the status column
# fire page should can sort as it currently does

# steps:
# add in a hire box on the side of each column of the dataframe
# lock the dataframe so that only the hirebox can be altered
# add in a submit button that will return the pid and hire statuses of each employees


# TODO: Guts this will be the status page for current employees
# Including hiring and firing as we talked about today

# [
# 0:{
# "pid":2[
# 0:{
# "pid":2
# "hire": 0
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
# "hire": 0
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
# "hire": 0
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
# "hire": 0
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
