import streamlit as st
import json
import pandas as pd


def display_team(team_json):
    if 'team_data' not in st.session_state:
        st.session_state['team_data'] = team_json
    # st.json(team_json)

    # st.data_editor(team_json)

    df = pd.DataFrame(st.session_state['team_data'])

    if 'Remove' not in df.columns:
        df.insert(0, 'Remove', False)
    # df.insert(1, 'Image2', '<img src="assets/minus_icon.jpg"')
    edited_df = st.data_editor(df.to_dict('records'))

    if st.button('Save'):

        st.session_state['team_data'] = edited_df

        st.session_state['team_data'] = [row for row in st.session_state['team_data'] if not row['Remove']]

        st.success('Changes have been saved!')

        df = pd.DataFrame(st.session_state['team_data'])
        st.data_editor(df.to_dict('records'))
        st.rerun()
