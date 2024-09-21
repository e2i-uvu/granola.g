import streamlit as st
import pandas as pd

if "main_df" not in st.session_state:
    st.session_state.main_df = [{'id': 'R_1kL1ZzUZg70h7bf', 'name': 'Emily Burch', 'email': '10875611@uvu.edu', 'uvid': '', 'degreepercent': 95, 'teambefore': True, 'speciality': 'Tech/Computer Science', 'major': 'Software Engineering', 'majoralt': '', 'aoi': 'Fullstack, Frontend, Backend, ', 'social': 11, 'status': 0}, {'id': 'R_1ARWFFvLGiSsbGI', 'name': 'Michael Short', 'email': '10894737@uvu.edu', 'uvid': '', 'degreepercent': 46, 'teambefore': False, 'speciality': 'Tech/Computer Science', 'major': 'Computer Science', 'majoralt': '', 'aoi': 'Database, Backend, Embedded, Game, Frontend, Fullstack, ', 'social': 10, 'status': 0}, {'id': 'R_6ifg0379tg04Hzv', 'name': 'Noah Potter', 'email': '10954749@uvu.edu', 'uvid': '', 'degreepercent': 91, 'teambefore': False, 'speciality': 'Tech/Computer Science', 'major': 'Software Engineering', 'majoralt': '', 'aoi': 'Frontend, Backend, ', 'social': 12, 'status': 0}, {'id': 'R_5mU8mEtyJQ8Qr3e', 'name': 'Brippney Vargas', 'email': '11023340@uvu.edu', 'uvid': '', 'degreepercent': 67, 'teambefore': False, 'speciality': 'Tech/Computer Science', 'major': 'Computer Science', 'majoralt': '', 'aoi': 'Game, Fullstack, Backend, Frontend, ', 'social': 8, 'status': 0}, {'id': 'R_13TtUjWjZlBi71L', 'name': 'David Rowley', 'email': '10861208@uvu.edu', 'uvid': '', 'degreepercent': 90, 'teambefore': False, 'speciality': 'Tech/Computer Science', 'major': 'Computer Science', 'majoralt': '', 'aoi': 'Frontend, Game, Fullstack, Database, Backend, ', 'social': 7, 'status': 0}, {'id': 'R_7fZzZ53fQ4aMUCJ', 'name': 'Hyomin Cha', 'email': '10994542@uvu.edu', 'uvid': '', 'degreepercent': 98, 'teambefore': False, 'speciality': 'Tech/Computer Science', 'major': 'Computer Science', 'majoralt': '', 'aoi': 'Fullstack, Frontend, Database, ', 'social': 12, 'status': 0}]

df = pd.DataFrame(st.session_state.main_df)

for row in st.session_state.main_df:
    if "Remove" not in row.keys():
        print('no remove')

st.markdown(st.session_state.main_df[0]['id'])
# if "Remove" not in st.session_state.main_df.columns:
#     st.session_state.main_df.insert(0, "Remove", False)

st.data_editor(
        st.session_state.main_df,
        key="data_editor",
        # on_change=callback,
        hide_index=True,
        # column_config=column_configuration,
        disabled = ('name', 'uvid', 'speciality', 'aoi')
)