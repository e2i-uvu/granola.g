# #this is where my function goes that returns the 

# import streamlit as st

# import toml

# USERS = "./.streamlit/users.toml"

# # TODO: So after reading the docs, we can't update `secrets.toml`
# # and work with the updates without restarting the app.
# # So I am thinking we might as well just change the file

# user_data = toml.load(USERS)

# st.header("Users")

# with st.form("verification", border=False):
#     modified_user_data = st.data_editor(
#         user_data,
#         column_config={
#             "id": st.column_config.NumberColumn("UVID", disabled=True, format="%i"),
#             "verified": st.column_config.CheckboxColumn(
#                 "Verified?",
#                 help="Select to allow access",
#                 default=False,
#             ),
#         },
#         # disabled
#         use_container_width=True,
#         hide_index=True,
#     )
#     submitted = st.form_submit_button(
#         "Process Changes", type="primary", use_container_width=True
#     )
#     if submitted:
#         with open(USERS, "w") as f:
#             toml.dump(modified_user_data, f)

#         st.toast("success")

import streamlit as st
import json

def display_team(team_json):
    # st.markdown(
    #     f"{team_json}This now should appear on screen"
    # )
    st.json(team_json)
    st.data_editor(team_json)

    print(team_json)