import streamlit as st
import pandas as pd

def display_data_editor(data):

    df = pd.DataFrame(data)

    if 'Remove' not in df.columns:
        df.insert(0, 'Remove', False)

    return st.data_editor(df.to_dict('records'))

def display_team(team_json):
    if 'team_data' not in st.session_state:
        st.session_state['team_data'] = team_json

    initial_data = pd.DataFrame(st.session_state['team_data'])
    if 'Remove' not in initial_data.columns:
        initial_data.insert(0, 'Remove', False)

    st.session_state['team_data'] = initial_data.to_dict('records')

    data_editor_placeholder = st.empty() # this holds the data_editor container

    if st.session_state['team_data']:
        edited_df = data_editor_placeholder.data_editor(st.session_state['team_data'])
    else:
        data_editor_placeholder.write("Team is empty")

    if st.button('Save'):
        st.session_state['team_data'] = edited_df

        st.session_state['team_data'] = [row for row in st.session_state['team_data'] if not row['Remove']]

        if st.session_state['team_data']:
            data_editor_placeholder.data_editor(st.session_state['team_data'])
        else:
            data_editor_placeholder.write("Team is empty")
