"""
Entrypoint for the streamlit frontend
"""

import streamlit as st
import sys

try:
    if sys.argv[1] == "dev":
        st.session_state["dev"] = True
    else:
        st.session_state["dev"] = False

except IndexError:
    st.session_state["dev"] = False


st.title("Team Building")

st.logo(
    image="./static/innovation-academy-logo-side.png",
    link="https://www.uvu.edu/innovation/e2i/",
    icon_image="./static/uvu-logo.png",
)

# can add pages here
pages = {
    "Teams": [
        st.Page("interview.py", title="Interview"),
        st.Page("employees.py", title="Employee Info"),
        st.Page("teams.py", title="Team Building", default=False),
        st.Page("chat.py", title="AI Chat"),
    ],
}

pg = st.navigation(pages, position="sidebar")
pg.run()
