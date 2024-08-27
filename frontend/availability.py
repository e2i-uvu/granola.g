import streamlit as st
import pandas as pd

st.title("My Availability")

time_slots = [
    "07:00 AM",
    "07:30 AM",
    "08:00 AM",
    "08:30 AM",
    "09:00 AM",
    "09:30 AM",
    "10:00 AM",
    "10:30 AM",
    "11:00 AM",
    "11:30 AM",
    "12:00 PM",
    "12:30 PM",
    "01:00 PM",
    "01:30 PM",
    "02:00 PM",
    "02:30 PM",
    "03:00 PM",
    "03:30 PM",
    "04:00 PM",
    "04:30 PM",
    "05:00 PM",
    "05:30 PM",
    "06:00 PM",
    "06:30 PM",
    "07:00 PM",
    "07:30 PM",
    "08:00 PM",
    "08:30 PM",
    "09:00 PM",
    "09:30 PM",
    "10:00 PM",
]

# Default data where all checkboxes are set to False
default_data = {
    "Mon": [False] * len(time_slots),
    "Tue": [False] * len(time_slots),
    "Wed": [False] * len(time_slots),
    "Thu": [False] * len(time_slots),
    "Fri": [False] * len(time_slots),
    "Sat": [False] * len(time_slots),
    "Sun": [False] * len(time_slots),
}

# Initialize the DataFrame in session state if not already present
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(default_data, index=time_slots)

# Use the DataFrame from session state
df = st.session_state.df

col0, col1, col2, col3 = st.columns([0.55, 0.2, 0.2, 0.15], vertical_alignment="bottom")

with col0:
    options = st.multiselect(
        "Select Days to apply these times",
        ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    )

with col1:
    start_time = st.selectbox("Start time", time_slots)

with col2:
    end_time = st.selectbox("End time", time_slots)

with col3:
    if st.button("Save"):
        start_idx = time_slots.index(start_time)
        end_idx = time_slots.index(end_time)
        if start_idx > end_idx:
            st.error("Start time must be before end time.")
        else:
            for day in options:
                df.loc[time_slots[start_idx : end_idx + 1], day] = True

        # Save the updated DataFrame back to session state
        st.session_state.df = df

        # Print the updated DataFrame as JSON to the terminal
        print(df.to_json())

# Generate custom checkboxes for each cell
for time in time_slots:
    cols = st.columns([1, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5], gap="small")
    cols[0].text(time)
    for i, day in enumerate(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]):
        label = f"{time}_{day}"
        checked = cols[i + 1].checkbox(
            label, value=df.loc[time, day], key=label, label_visibility="collapsed"
        )
        if checked != df.loc[time, day]:
            df.loc[time, day] = checked
            st.session_state.df = df

# Display the updated DataFrame
st.write(df)

