import streamlit as st
import pandas as pd
import json
from json_data_CAN_DELETE_LATER import json_example_data

def display_team(team_json):
    team_json_list = []
    team_json_partial = []
    example_team_json_list = []

    for item in team_json:
        for key in item:
            team_json_partial.append(item[key])
            team_json_list.append(item[key])
            example_team_json_list.append(item[key])

    df = pd.DataFrame(team_json_list)

    if 'main_df' not in st.session_state:
        st.session_state.main_df = df

    column_configuration = {
        "id": None, "email": None, "degreepercent": None, "teambefore": None,
        "major": None, "majoralt": None, "social": None, "status": None
    }

    main_df_container = st.empty()
    main_df_container.dataframe(st.session_state.main_df, hide_index=True, column_config=column_configuration)

    if st.button('Edit'):
        edit_dialog(st.session_state.main_df, main_df_container, column_configuration)

@st.dialog("Edit Data", width="large")
def edit_dialog(df, main_df_container, column_configuration):
    if 'Remove' not in st.session_state.main_df.columns:
        st.session_state.main_df.insert(0, 'Remove', False)

    edited_df = st.data_editor(st.session_state.main_df, hide_index=True, column_config=column_configuration)

    col1, col2 = st.columns([2.5, 1], vertical_alignment='bottom')

    with col2:
        if st.button('Save'):
            updated_df = edited_df[edited_df['Remove'] == False].drop(columns=['Remove'])
            st.session_state.main_df = updated_df

            if 'selected_row' in st.session_state:
                st.session_state.main_df = pd.concat([st.session_state.main_df, st.session_state.selected_row]).drop_duplicates().reset_index(drop=True)
                del st.session_state.selected_row

            main_df_container.dataframe(st.session_state.main_df, hide_index=True, column_config=column_configuration)

    add_members(df, col1, main_df_container, column_configuration)

def add_members(df, col1, main_df_container, column_configuration):
    all_options = []
    for item in json_example_data:
        for key in item:
            all_options.append(item[key])

    df = pd.DataFrame(all_options)
    all_options = df['name'].tolist()

    with col1:
        selected_option = st.selectbox(
            'Select team members to Add:',
            (all_options),
            index=None,
            placeholder='None'
        )

    if selected_option:
        st.session_state.selected_option = selected_option
        selected_df = df[df['name'] == selected_option]

        if 'selected_rows' not in st.session_state:
            st.session_state.selected_rows = []

        st.session_state.selected_rows.append(selected_df)

        combined_selected_df = pd.concat(st.session_state.selected_rows).drop_duplicates().reset_index(drop=True)
        st.session_state.selected_row = combined_selected_df

        st.dataframe(selected_df, hide_index=True, column_config=column_configuration)



# TODO still need to Make the 'Save' button actually add names into the st.empty container
# TODO Add an 'Add' Button next to the 'Save' button that will add right next to name to the edit data dsataframe
# TODO Make the editable dataframe into an st.empty
# formatting for each dataframe...

   

# Next steps:
# Create a text input box
# Create a dummy person's list
# Search by name
# Toggle to search by UVID
# automatically pull up anything that matches the string input
# Create an add button and the multi-select will allow for multiple people to be selected at a time

#dialogue - maybe just a checkbox and st.markdown next to it
# (hopefully no submit button is necessary)
#popover (maybe just use this?)
# ()

# just use dataFrame instead of dataeditor, get rid of remove column
# add an edit button that brings up the dialogue box