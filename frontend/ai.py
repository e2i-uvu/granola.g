import streamlit as st
import pandas as pd
import json

def filter_to_small_df(person):
    small_df_list = []
    key_names = ['name', 'speciality', 'aoi']
    for key in person.keys():
        for column in key_names:
            if key == column:
                small_df_list.append(person[column])
                continue
    return small_df_list


def display_team(team_json):
    team_json_list = []
    team_json_partial = []

    for item in team_json:
        # st.markdown(item)
        for key in item:
            # st.markdown(key)
            team_json_partial.append(filter_to_small_df(item[key]))
            team_json_list.append(item[key])

    
    df = pd.DataFrame(team_json_list)
    df_small = pd.DataFrame(team_json_partial)

    st.dataframe(df)
    st.dataframe(df_small)
    print("\n")
    print(team_json, "\n\n")


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

