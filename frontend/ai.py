import streamlit as st
import pandas as pd

def display_data_editor(data):

    df = pd.DataFrame(data)

    if 'Remove' not in df.columns:
        df.insert(0, 'Remove', False)


def display_team(team_json):
    if 'team_data' not in st.session_state:
        st.session_state['team_data'] = team_json

    initial_data = pd.DataFrame(st.session_state['team_data'])
    if 'Remove' not in initial_data.columns:
        initial_data.insert(0, 'Remove', False)

    st.session_state['team_data'] = initial_data.to_dict('records')

    data_editor_placeholder = st.empty() # this holds the data_editor container

    try:
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

    except st.errors.DuplicateWidgetID:
        st.toast("No Changes detected")

# Next steps:
# Rename placeholder and other values
# Create a text input box
# Create a dummy person's list
# Search by name
# Toggle to search by UVID
# automatically pull up anything that matches the string input
# Create an add button and the multi-select will allow for multiple people to be selected at a time

