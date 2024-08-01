
import streamlit as st
import pandas as pd
import numpy as np

st.title("My Availability")


data = {
    "Monday": False,
    "Tuesday": False,
    "Wednesday": False,
    "Thursday": False,
    "Friday": False,
    "Saturday": False,
    "Sunday": False,
}

df = pd.DataFrame(data, index = ["7:00 am", "7:30 am", "8:00 am"])

st.data_editor(df)  # Same as st.write(df)