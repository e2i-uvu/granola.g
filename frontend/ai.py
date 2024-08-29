import streamlit as st
import json
import pandas as pd


def display_team(team_json):
    st.json(team_json)

    # st.data_editor(team_json)

    df = pd.DataFrame(team_json)
    df.insert(0, 'Remove', False)
    df.insert(1, 'Image', '<img src="assets/minus_icon.jpg"')
    st.data_editor(df.to_dict('records'))
