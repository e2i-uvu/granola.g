"""
Entrypoint for the streamlit frontend
"""

import streamlit as st

st.title("Hellow testing")

# can add pages here
pages = {
    "Interview": [
        st.Page("interview.py", title="Interview"),
        st.Page("teams.py", title="Team Building", default=False),
        st.Page("interviewForm.py", title="Interview Form", default=False)
    ]
}

pg = st.navigation(pages, position="sidebar")
pg.run()
