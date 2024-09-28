import streamlit as st
import requests
from requests.auth import HTTPBasicAuth
import pandas as pd

# Data Analytics
from copy import copy
import altair as alt
from collections.abc import Callable
#from enum import Enum

st.title("Overview :material/groups:")
st.write("---")

EMPLOYEE_STATUS_CODE: list[str] = [
    "Assigned",
    "Pending Assignment",
    "Previously on e2i"
]

def encode_status_code(status: str):
    match status:
        case "Assigned":
            return 1
        case "Pending Assignment":
            return 0
        case "Previously on e2i":
            return -1

# WARN: Obsolete. overview.py does not send POST requests
def decode_status_code(status: int):
    match status:
        case 1:
            return "Assigned"
        case 0:
            return "Pending Assignment"
        case -1:
            return "Previously on e2i"

def format_DataFrame(data: list[dict[str, str | int | bool]]):
    df = pd.DataFrame(data)

    # NOTE: Parsing:
    df["status"] = [decode_status_code(value) for value in df["status"]]#.iloc()]

    parse_degree = lambda x: [f"{value}%" for value in df[x]]
    parse_prev_team = lambda x: "Yes" if x else "No"

    if "teambefore" in df:
        df["teambefore"] = [parse_prev_team(value) for value in df["teambefore"]]
    else:
        df["prevTeam"] = [parse_prev_team(value) for value in df["prevTeam"]]


    if "degreepercent" in df:
        df["degreepercent"] = parse_degree("degreepercent")
    else:
        df["degree"] = parse_degree("degree")

    return df

def generate_stats(stats: dict[str, int|float|str]| pd.Series) -> None:
    if type(stats) == dict:
        labels = list(stats.keys())
        values = list(stats.values())
        stat_num: int = len(stats)
        metric_columns = st.columns(stat_num)

        for i in range(stat_num):
            with metric_columns[i]:
                if type(values[i]) == pd.Series:
                    values[i] = values[i][0]
                st.metric(labels[i], values[i])

# NOTE: EMPLOYEES

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
    #"id"
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

def employee_stats_summary(df: pd.Series | pd.DataFrame) -> dict[str, int|float|str]:
    return {
        "Total Team Members": len(df),
        "Assigned": len([s for s in df.status if s == 1]),
        "Unassigned": len([s for s in df.status if s != 1]),
    }

def show_status():
    r = requests.get(
        st.session_state.backend["url"] + "employees",
        auth=HTTPBasicAuth(
            st.session_state.backend["username"], st.session_state.backend["password"]
        ),
    )
    if r.status_code == 400:
        st.warning(f"The database is empty!")
    elif r.status_code != 200:
        st.error(f"Error code: {r.status_code}. Contact support.")
        st.toast(f"Error code: {r.status_code}")
    else:
        st.write("---")
        df = format_DataFrame(r.json())
        generate_stats(employee_stats_summary(df)) 
        st.write("---")
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
                st.error( f"Failed to save changes. Status code: {response.status_code}")

# NOTE: PROJECTS

PROJECT_STATUS_CODE: list[str] = [
    "Active",
    "Pending Assignment",
    "Previously on e2i"
]

TEAM_COLUMN_ORDER: list[str] = [
    "pname",
    "ptype",
    "uvid",
    "name",
    "major",
    "majoralt",
    "speciality",
    "degree",
    "status",
    "prevTeam",
    "aoi",
    "social",
    "email",
    #"id"
]

TEAM_COLUMN_CONFIG = {
    "pname": st.column_config.Column(label="Project Name", disabled=True),
    "ptype": st.column_config.Column(label="Project Type", disabled=True),
    "status": st.column_config.SelectboxColumn(label="Status", disabled=True, options=EMPLOYEE_STATUS_CODE, required=True),
    #"id": st.column_config.Column(label="Employee ID", disabled=True),
    "uvid": st.column_config.Column(label="UVID", disabled=True),
    "name": st.column_config.Column(label="Name", disabled=True),
    "email": st.column_config.Column(label="Email", disabled=True),
    "degree": st.column_config.Column(label="Degree Percent", disabled=True),
    "prevTeam": st.column_config.Column(label="Team Before?", disabled=True),
    "speciality": st.column_config.Column(label="Speciality", disabled=True),
    "major": st.column_config.Column(label="Major", disabled=True),
    "majoralt": st.column_config.Column(label="Major (Alt)", disabled=True),
    "aoi": st.column_config.Column(label="Interest", disabled=True),
    "social": st.column_config.Column(label="Social", disabled=True),
}

def team_stats_summary(df: pd.DataFrame) -> dict[str, int|float]:
    return {
        "Teams/Project Number": len(set(df["pname"]))
    }

def show_pending_projects():
    r = requests.get(
        st.session_state.backend["url"] + "project",
        auth=HTTPBasicAuth(
            st.session_state.backend["username"], st.session_state.backend["password"]
        ),
    )
    if r.status_code != 200:
        st.error(f"Error code: {r.status_code}. Contact support.", icon=":material/sad:")
        st.toast(f"Error code: {r.status_code}", icon=":material/sad:")
    else:
        # st.json(r.json())
        df = format_DataFrame(r.json())
        generate_stats(team_stats_summary(df))
        st.write("---")
        st.dataframe(df,
                     height = 14000,
                     use_container_width=True,
                     column_order=TEAM_COLUMN_ORDER,
                     column_config=TEAM_COLUMN_CONFIG,
                     hide_index=True
                     )
        st.write("---")

# NOTE: DATA ANALYTICS

def generate_plots(df, vars: dict[str, str], plot_type: str):
    def _generate_histogram(df, var: str, label: str):
        st.altair_chart(
            alt.Chart(df).mark_bar().encode(
                x=alt.X(var)
                    .title(label)
                    .bin(maxbins=10),
                y=alt.Y("count()").title("Frequency"),
                color=alt.Color("count()",legend=None).title("Frequency")
            ).properties(title=label),
            use_container_width=True
        )

    def _generate_barplot(df, var: str, label: str):
        st.altair_chart(
            alt.Chart(df).mark_bar().encode(
                y=alt.Y(var)
                    .title(label),
                x=alt.X("count()").title("Frequency"),
                color=alt.Color("count()", legend=None).title("Frequency")
            ).properties(title=label),
            use_container_width=True
        )

    generate_plot: Callable

    match plot_type:
        case "barplot":
            generate_plot = _generate_barplot
        case "histogram":
            generate_plot = _generate_histogram

    columns = list(vars.keys())
    labels = list(vars.values())
    vars_num: int = len(vars)
    vars_columns = st.columns(vars_num)

    for i in range(vars_num):
        with vars_columns[i]:
            generate_plot(df, columns[i], labels[i])

def return_joined_majors():
    pass

def show_analytics():
    r_emp = requests.get(
        st.session_state.backend["url"] + "employees",
        auth=HTTPBasicAuth(
            st.session_state.backend["username"], st.session_state.backend["password"]
        )
    )
    r_pro = requests.get(
        st.session_state.backend["url"] + "project",
        auth=HTTPBasicAuth(
            st.session_state.backend["username"], st.session_state.backend["password"]
        )
    )
    if r_emp.status_code == 400 or r_pro.status_code == 400:
        st.warning(f"The database is empty!")
    elif r_emp.status_code != 200:
        st.error(f"Error code: {r_emp.status_code}. Contact support.")
        st.toast(f"Error code: {r_emp.status_code}")
    elif r_pro.status_code != 200:
        st.error(f"Error code: {r_pro.status_code}. Contact support.")
        st.toast(f"Error code: {r_pro.status_code}")
    else:
        st.write("---")
        df_emp = pd.DataFrame(r_emp.json())
        df_pro = pd.DataFrame(r_pro.json())

        statistics: dict[str, dict[str, str|int|float]] = {
            "General" : {
                "Total e2i Members": len(df_emp),
                "Assigned e2i Students": len([s for s in df_emp.status if s == 1]),
                "Unassigned e2i Students": len([s for s in df_emp.status if s != 1]),
                "Returning": len([s for s in df_emp.teambefore if s]),
                "Formed Teams/Active Projects": len(set(df_pro["pname"]))
            },
            "Means" : {
                "Program Overall Social Skills": round(df_emp.social.mean(),2),
                "Social Skills per Team": round(df_pro.groupby("pname").social.mean(),2),
                "Degree Completion Percentage": round(df_emp.degreepercent.mean(), 2),
                "Degree Percentage per Team": round(df_pro.groupby("pname").degree.mean(),2),
                
            },
            "Modes" : {
                "Area of Interest": pd.Series([value for value in df_emp.aoi if value != ""]).mode(),
                "Most Frequent Major": pd.Series([value for value in df_emp.major if value != ""]).mode(),
                "Major (Alt)": pd.Series([value for value in df_emp.majoralt if value != ""]).mode()
            }
        }

        for stat, values in statistics.items():
            st.subheader(stat)
            generate_stats(values)
            st.write("---")

        histogram_variables: dict[str,str] = {
            "degreepercent": "Degree Percent",
            "social": "Social Skills",
        }

        barplot_variables: dict[str,str] = {
            "major": "Major",
            "majoralt": "Major (Alt)"
        }

        generate_plots(df_emp, histogram_variables, "histogram")
        generate_plots(df_emp, barplot_variables, "barplot")


# NOTE: main
def main():
    # NOTE:
    # pending projects + running projects (teams and descriptions)
    option = st.selectbox("Select one", ( "Analytics", "Employees", "Team Projects"))  # old_options)

    if option != "Select an option":
        match option:
            case "Employees":
                show_status()
            case "Team Projects":
                show_pending_projects()
            case "Analytics":
                show_analytics()

main()
st.write("---")
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
