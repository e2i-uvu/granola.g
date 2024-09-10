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

    # tj = [j for i, j in team_json.itmes()]

    df = pd.DataFrame(team_json_list)

    if 'main_df' not in st.session_state:
        st.session_state.main_df = df

    column_configuration = {
        "id": None, "email": None, "degreepercent": None, "teambefore": None,
        "major": None, "majoralt": None, "social": None, "status": None
    }

    main_df_container = st.empty()
    main_df_container.dataframe(st.session_state.main_df, hide_index=True, column_config=column_configuration)

    column1, column2, column3 = st.columns([1, 1, 5], vertical_alignment='bottom')

    with column1:
        if st.button('Edit', use_container_width=True):
            edit_dialog(st.session_state.main_df, main_df_container, column_configuration)
    
    with column2:
        if st.button('Submit', use_container_width=True):
            st.toast('Submitted!')
            print(st.session_state.main_df)
            print(type(st.session_state.main_df))
    
    df_json = st.session_state.main_df.to_json(orient='records')
    st.json(df_json)

@st.dialog("Edit Data", width="large")
def edit_dialog(df, main_df_container, column_configuration):
    if 'Remove' not in st.session_state.main_df.columns:
        st.session_state.main_df.insert(0, 'Remove', False)

    edited_df = st.data_editor(st.session_state.main_df, hide_index=True, column_config=column_configuration)

    col1, col2 = st.columns([3, 1], vertical_alignment='bottom')

    with col2:
        if st.button('Save'):
            updated_df = edited_df[edited_df['Remove'] == False].drop(columns=['Remove'])
            st.session_state.main_df = updated_df

            if 'selected_row' in st.session_state:
                st.session_state.main_df = pd.concat([st.session_state.main_df, st.session_state.selected_row]).drop_duplicates().reset_index(drop=True)
                del st.session_state.selected_row

            main_df_container.dataframe(st.session_state.main_df, hide_index=True, column_config=column_configuration)
            st.session_state.selected_rows = []
            selected_options = False
            st.rerun()

    add_members(df, col1, main_df_container, column_configuration)

def add_members(df, col1, main_df_container, column_configuration):
    all_options = []
    for item in json_example_data:
        for key in item:
            all_options.append(item[key])

    df = pd.DataFrame(all_options) 
    temp_df = df
    temp_df['display'] = temp_df['name'] + ' -- (' + temp_df['speciality'] + ')'
    all_options = temp_df['display'].tolist()

    with col1:
        selected_options = st.multiselect(
            'Select team members to Add:',
            (all_options),
            default=None,
            placeholder='Begin typing to add...'
        )

    if selected_options:
        selected_df = df[df['display'].isin(selected_options)]

        if 'selected_rows' not in st.session_state:
            st.session_state.selected_rows = []

        selected_df.drop(columns=['display'], inplace=True)

        st.session_state.selected_rows.append(selected_df)


        combined_selected_df = pd.concat(st.session_state.selected_rows).drop_duplicates().reset_index(drop=True)
        st.session_state.selected_row = combined_selected_df

        st.dataframe(selected_df, hide_index=True, column_config=column_configuration)

