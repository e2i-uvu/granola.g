import streamlit as st
import pandas as pd

st.title("My Availability")

time_slots = ['07:00 AM', '07:30 AM', '08:00 AM', '08:30 AM', 
              '09:00 AM', '09:30 AM', '10:00 AM', '10:30 AM', '11:00 AM', 
              '11:30 AM', '12:00 PM', '12:30 PM', '01:00 PM', '01:30 PM',
              '02:00 PM', '02:30 PM', '03:00 PM', '03:30 PM', '04:00 PM',
              '04:30 PM', '05:00 PM', '05:30 PM', '06:00 PM', '06:30 PM',
              '07:00 PM', '07:30 PM', '08:00 PM', '08:30 PM', '09:00 PM',
              '09:30 PM', '10:00 PM']

data = {
    "Mon": [False] * len(time_slots),
    "Tue": [False] * len(time_slots),
    "Wed": [False] * len(time_slots),
    "Thu": [False] * len(time_slots),
    "Fri": [False] * len(time_slots),
    "Sat": [False] * len(time_slots),
    "Sun": [False] * len(time_slots),
}
df = pd.DataFrame(data, index=time_slots)

col0, col1, col2, col3 = st.columns([.55, .2, .2, .15], vertical_alignment='bottom')

with col0:
    options = st.multiselect(
        "Select Days to apply these times",
        ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    )

with col1:
    start_time = st.selectbox(
        "Start time",
        time_slots
    )

with col2:
    end_time = st.selectbox(
        "End time",
        time_slots
    ) 

with col3:
    if st.button("Save"):
        start_idx = time_slots.index(start_time)
        end_idx = time_slots.index(end_time)
        if start_idx > end_idx:
            st.error("Start time must be before end time.")
        else:
            for day in options:
                df.loc[start_time:end_time, day] = True

edited_df = st.data_editor(df, height=1125, width=1000)

df.update(edited_df)
