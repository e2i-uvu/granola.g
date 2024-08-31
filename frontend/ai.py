import streamlit as st
import pandas as pd
import json
from json_data_CAN_DELETE_LATER import json_example_data


def filter_to_small_df(person, key_names=['name', 'speciality', 'aoi']):
    small_df_list = []
    for key in person.keys():
        for column in key_names:
            if key == column:
                small_df_list.append(person[column])
                break
    return small_df_list


def display_team(team_json):
    team_json_list = []
    team_json_partial = []
    example_team_json_list = []

    for item in team_json:
        for key in item:
            team_json_partial.append(filter_to_small_df(item[key]))
            team_json_list.append(item[key])
            example_team_json_list.append(filter_to_small_df(item[key], ['uvid', 'name', 'speciality', 'aoi']))

    
    df = pd.DataFrame(team_json_list)
    df_small = pd.DataFrame(team_json_partial)
    df_example = pd.DataFrame(example_team_json_list)

    df_small.columns = ['Name', 'Specialty', 'Area of Interest']
    df_example.columns = ['uvid', 'name', 'speciality', 'Area of Interest']


    st.dataframe(df_small, hide_index=True)
    if st.button('Edit'):
        edit_dialog(df_example)

def get_exact_matches(input_str, data):
    exact_matches = []
    for item in data:
        person = list(item.values())[0]
        if person['name'].lower().startswith(input_str.lower()):
            exact_matches.append(item)
    return exact_matches

def get_partial_matches(input_str, data):
    partial_matches = []
    for item in data:
        person = list(item.values())[0]
        if input_str.lower() in person['name'].lower() and not person['name'].lower().startswith(input_str.lower()):
            partial_matches.append(item)
    return partial_matches

@st.dialog("Edit Data", width="large")
def edit_dialog(df):
    st.write("Something")
    st.dataframe(df, hide_index=True)
    # df.insert(0, 'Remove', False).

    name = st.text_input("Name")

    if name:
        exact_matches = get_exact_matches(name, json_example_data)

        partial_matches = get_partial_matches(name, json_example_data)
        
        filtered_data = exact_matches + partial_matches
        filtered_data = filtered_data[:5]

        if filtered_data:
            # st.write("Top 5 relevant names:")
            for person in filtered_data:
                st.write(list(person.values())[0]['name'])
        
        else:
            st.write("No relevant names found.")

    if st.button("Save"):
        st.write(f"Saved {name}")



# import streamlit as st
# import pandas as pd

# def display_data_editor(data):
#     df = pd.DataFrame(data)

#     if 'Remove' not in df.columns:
#         df.insert(0, 'Remove', False)


# def display_team(team_json):
#     if 'team_data' not in st.session_state:
#         st.session_state['team_data'] = team_json

#     initial_data = pd.DataFrame(st.session_state['team_data'])
#     if 'Remove' not in initial_data.columns:
#         initial_data.insert(0, 'Remove', False)

#     st.session_state['team_data'] = initial_data.to_dict('records')

#     container = st.empty() # this holds the data_editor container

#     try:
#         if st.session_state['team_data']:
#             edited_df = container.data_editor(st.session_state['team_data'])
#         else:
#             container.write("Team is empty")

#         if st.button('Edit'):
#             st.session_state['team_data'] = edited_df

#             st.session_state['team_data'] = [row for row in st.session_state['team_data'] if not row['Remove']]

#             if st.session_state['team_data']:
#                 container.data_editor(st.session_state['team_data'])
#             else:
#                 container.write("Team is empty")

#     except st.errors.DuplicateWidgetID:
#         st.toast("No Changes detected")

   

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