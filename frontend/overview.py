import streamlit as st
import requests
from requests.auth import HTTPBasicAuth
import pandas as pd

st.title("Overview")

# NOTE: EMPLOYEES

EMPLOYEE_STATUS_CODE: list[str] = [
    "Assigned",
    "Pending Assignment",
    "Previously on e2i"
]

EMPLOYEE_COLUMN_ORDER: list[str] = [
    "status",
    "uvid",
    "name",
    "email",
    "speciality",
    "teambefore",
    "major",
    "majoralt",
    "degreepercent",
    "aoi",
    "social",
    "id"
]
 
EMPLOYEE_COLUMN_CONFIG = {
    "status": st.column_config.SelectboxColumn(label="Status", disabled=True, options=EMPLOYEE_STATUS_CODE, required=True),
    "id": st.column_config.Column(label="Employee ID", disabled=True),
    "uvid": st.column_config.Column(label="UVID", disabled=True),
    "name": st.column_config.Column(label="Name", disabled=True),
    "email": st.column_config.Column(label="Email", disabled=True),
    "degreepercent": st.column_config.Column(label="Degree Percent", disabled=True),
    "teambefore": st.column_config.Column(label="Team Before?", disabled=True),
    "speciality": st.column_config.Column(label="Speciality", disabled=True),
    "major": st.column_config.Column(label="Major", disabled=True),
    "majoralt": st.column_config.Column(label="Major (Alt)", disabled=True),
    "aoi": st.column_config.Column(label="Interest", disabled=True),
    "social": st.column_config.Column(label="Social", disabled=True),
}

def encode_status_code(status: str):
    match status:
        case "Assigned":
            return 1
        case "Pending Assignment":
            return 0
        case "Previously on e2i":
            return -1

def employee_stats_summary(df: pd.Series | pd.DataFrame) -> dict[str, int|float|str]:
    return {
        "Total Team Members": len(df),
        "Assigned": len([s for s in df.status if s == 1]),
        "Unassigned": len([s for s in df.status if s != 1]),
    }

def format_DataFrame(data: list[dict[str, str | int | bool]]):
    def decode_status_code(status: int):
        match status:
            case 1:
                return "Assigned"
            case 0:
                return "Pending Assignment"
            case -2:
                return "Previously on e2i"

    df = pd.DataFrame(data)
    stats = employee_stats_summary(df)

    df["status"] = [decode_status_code(value) for value in df["status"]]#.iloc()]
    df["degreepercent"] = [f"{value}%" for value in df["degreepercent"]]

    return df, stats

def generate_stats(stats: dict[str, int|float|str]) -> None:
    labels = list(stats.keys())
    values = list(stats.values())
    stat_num: int = len(stats)
    metric_columns = st.columns(stat_num)

    for i in range(stat_num):
        with metric_columns[i]:
            st.metric(labels[i], values[i])

def show_status():
    r = requests.get(
        st.session_state.backend["url"] + "employees",
        auth=HTTPBasicAuth(
            st.session_state.backend["username"], st.session_state.backend["password"]
        ),
    )
    if r.status_code != 200:
        st.text("The world is dying")
        st.text(r.status_code)
    else:

        df, stats = format_DataFrame(r.json())
        generate_stats(stats) 
        edited_df = st.data_editor(
            df, 
            height = 1400,
            column_order=EMPLOYEE_COLUMN_ORDER,
            column_config=EMPLOYEE_COLUMN_CONFIG,
            hide_index=True,
            use_container_width=True
        )

        if st.button("Save Changes"):
            edited_df["status"] = edited_df["status"].apply(encode_status_code)

            # HACK: Backend expects a PID key, not an ID. 
            # Therefore, this funky algorithm
            edited_df["pid"] = edited_df["id"]
            filtered_data = edited_df[["pid", "status"]].to_dict(orient="records")

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

# NOTE: PROJECTS
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

# NOTE: DATA ANALYTICS
def show_analytics():
    pass

# NOTE: main
def main():
    # NOTE:
    # pending projects + running projects (teams and descriptions)
    option = st.selectbox("Select one", ("Select an option", "Employees", "Team Projects", "Analytics"))  # old_options)

    if option != "Select an option":
        match option:
            case "Employees":
                show_status()
            case "Team Projects":
                show_pending_projects()
            case "Analytics":
                show_analytics()

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
