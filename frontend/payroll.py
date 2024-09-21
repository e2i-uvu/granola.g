"""Payroll stuff"""

import streamlit as st

import pandas as pd
from io import BytesIO

from datetime import datetime


def process_tims(df: pd.DataFrame) -> pd.DataFrame:
    """
    Takes in csv from tims and cleans up the data.
    """
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]  # Clean data
    df["POSN"] = df["POSN"].str[-2:]
    df = df.dropna(how="all")

    return df


def process_key(df: pd.DataFrame) -> pd.DataFrame:
    """
    Takes in a `key` as a pandas dataframe
    if an employees position number is 0, or unset
    the value of `00` as a string is used
    """

    def get_posn(val: str):
        try:
            num_val = float(val)
            if num_val == 0:
                return "00"
            else:
                return str(num_val)[-2:]
        except ValueError:
            return "99"

    df = df.dropna(how="all")
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]  # Clean data
    df["UVID"] = df["UVID"].astype(int)
    df = df.rename(columns={"Position Number": "POSN"})
    df = df.rename(columns={"Team/Index Number": "TEAM"})
    df["POSN"] = df["POSN"].apply(get_posn)

    return df


def merge_data(tims: pd.DataFrame, key: pd.DataFrame) -> dict:

    # combined = pd.merge(key, tims, how="left", on=["UVID", "POSN"], indicator=True)
    combined = pd.merge(key, tims, how="outer", on=["UVID", "POSN"], indicator=True)

    ordering = ["UVID", "LAST", "FIRST", "Name", "POSN", "DATE", "HOURS", "TEAM"]
    # ordering_plus = [
    #     "UVID",
    #     "LAST",
    #     "FIRST",
    #     "Name",
    #     "POSN",
    #     "DATE",
    #     "HOURS",
    #     "TEAM",
    #     "_merge",
    # ]

    combined_both = combined[combined["_merge"] == "both"]
    combined_both["TEAM"] = combined_both["TEAM"].fillna("UNKNOWN PAYROLL")

    # combined_left = combined[combined["_merge"] == "left_only"]

    combined_right = combined[combined["_merge"] == "right_only"]
    combined_right["TEAM"] = combined_right["TEAM"].fillna("UNKNOWN TIMS")

    combined_total = pd.concat([combined_both, combined_right])

    # st.dataframe(combined[ordering_plus])
    # st.dataframe(combined_left[ordering_plus])
    # st.dataframe(combined_right[ordering_plus])
    # st.dataframe(combined_both[ordering_plus])
    # st.dataframe(combined_total[ordering_plus])

    return {team: info for team, info in combined_total.groupby("TEAM")[ordering]}


# --- UI ---
st.title("Payroll Reports :material/local_atm:")
st.write("---")

col1, col2 = st.columns(2)

with col1:
    tims = st.file_uploader(
        "TIMS Payroll Data",
        type="csv",
        accept_multiple_files=True,
        help="This is the csv imported from TIMS, only csv files are supported",
    )

with col2:
    key = st.file_uploader(
        "Payroll Positions",
        type="csv",
        help="This is the excel doc (converted to csv) of who is on which team, only csv files are supported",
    )

st.write("---")

if tims is not None and key is not None:

    if len(tims) > 1:
        for t in tims:
            t.seek(0)

        dfs = [process_tims(pd.read_csv(f)) for f in tims]
        processed_tims = pd.concat(dfs, axis=0)

    else:
        tims = tims[0]
        tims.seek(0)
        tims = pd.read_csv(tims)
        processed_tims = process_tims(tims)

    key.seek(0)
    key = pd.read_csv(key)
    processed_key = process_key(key)

    teams = merge_data(tims=processed_tims, key=processed_key)

    # DEBUG
    # st.dataframe(processed_key)
    # st.dataframe(processed_tims)
    # st.dataframe(teams)
    # st.write("---")

    # summary = pd.DataFrame(
    #     {t: d.groupby(["UVID", "Name"])["HOURS"].sum() for t, d in teams.items()}
    # )

    summary = []
    for t, d in teams.items():
        total_hours = d["HOURS"].sum()
        summary.append({"TEAM": t, "TOTAL HOURS": total_hours})

    summary_df = pd.DataFrame(summary)
    summary_df["TOTAL HOURS"] = summary_df["TOTAL HOURS"].map("{:,.2f}".format)
    summary_df_transpose = summary_df.set_index("TEAM").T

    st.dataframe(
        summary_df_transpose,
        use_container_width=True,
        hide_index=True,
        # column_config=st.column_config.NumberColumn(label=None, step=1, format="%d.2f"),
    )  # , format="%.2f")
    st.bar_chart(summary, x="TEAM", y="TOTAL HOURS")

    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        for team, info in teams.items():
            # info = info.astype(str)
            info.to_excel(writer, sheet_name=team, index=False)
            info.groupby(["UVID", "Name"])["HOURS"].sum().to_frame(
                name="TOTAL HOURS"
            ).to_excel(writer, sheet_name=team, startrow=len(info) + 3, index=True)

    current_date = datetime.now()
    formatted_date = current_date.strftime("%m-%d-%y")

    team_names = list(teams.keys())

    st.write("---")

    col1, col2, col3 = st.columns([1, 2, 1], vertical_alignment="bottom")

    col1.download_button(
        label="Download Full Spreadsheet",
        data=output.getvalue(),
        file_name=f"{formatted_date}-e2i-tims-report.xlsx",
        help="Get fancy excel sheet, file name is formatted as the current date",
        type="primary",
        use_container_width=True,
    )

    team_selection = col2.multiselect(
        label="Select Team(s)",
        options=team_names,
        default=None,
        help="See more information about each team",
        placeholder="Select Team",
        label_visibility="visible",
    )

    if len(team_selection) >= 1:

        total_hours = 0
        for i in team_selection:
            total_hours += teams[i]["HOURS"].sum()

        st.subheader(f"Total Hours: {total_hours:.2f}")

        selection_df = pd.concat([teams[i] for i in team_selection])

        selection_output = BytesIO()
        with pd.ExcelWriter(selection_output, engine="openpyxl") as writer:
            # selection_df = selection_df.astype(str)
            selection_df.to_excel(writer, index=False)
            selection_df.groupby(["UVID", "Name"])["HOURS"].sum().to_frame(
                name="TOTAL HOURS"
            ).to_excel(writer, startrow=len(selection_df) + 3, index=True)

        current_date = datetime.now()
        formatted_date = current_date.strftime("%m-%d-%y")

        col3.download_button(
            label="Download Spreadsheet for Selected Team(s)",
            data=selection_output.getvalue(),
            file_name=f"{formatted_date}-{'-'.join(team_selection)}-e2i-tims-report.xlsx",
            help="Get fancy excel sheet, file name is formatted as the current date",
            type="primary",
            use_container_width=True,
        )

        selection_df["FULL NAME"] = selection_df["FIRST"] + " " + selection_df["LAST"]
        temp = selection_df.groupby("UVID", as_index=False).agg({"HOURS": "sum"})

        result_df = temp.merge(
            selection_df[["UVID", "FIRST", "LAST", "FULL NAME"]].drop_duplicates(),
            on="UVID",
        )
        result_df = result_df[["FULL NAME", "HOURS"]]

        col1, col2 = st.columns(2)
        col1.bar_chart(
            result_df,
            x="FULL NAME",
            y="HOURS",
            x_label="NAME",
            horizontal=False,
        )
        col2.line_chart(selection_df, x="DATE", y="HOURS", color="FIRST")
