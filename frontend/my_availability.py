import streamlit as st
import pandas as pd
import numpy as np

st.title("My Availability")

time_slots = pd.date_range("07:00", "22:00", freq="30min").strftime("%I:%M %p")


data = {
    "Monday": [False] * len(time_slots),
    "Tuesday": [False] * len(time_slots),
    "Wednesday": [False] * len(time_slots),
    "Thursday": [False] * len(time_slots),
    "Friday": [False] * len(time_slots),
    "Saturday": [False] * len(time_slots),
    "Sunday": [False] * len(time_slots),
}

df = pd.DataFrame(data, index=time_slots)

st.data_editor(df, height=1125, width=1000)
