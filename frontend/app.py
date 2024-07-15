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


# any UI elements in this file will be rendered
# on every page of the streamlit app

# st.title("Team Building")

st.logo(
    image="./static/innovation-academy-logo-side-green.png",
    link="https://www.uvu.edu/innovation/e2i/",
    icon_image="./static/uvu-logo-green.png",
)

# can add pages here
pages = {
    "Teams": [
        st.Page("interview.py", title="Interview", icon=":material/person_add:"),
        st.Page("employees.py", title="Employees", icon=":material/groups:"),
        st.Page(
            "teams.py",
            title="Team Building",
            default=False,
            icon=":material/reduce_capacity:",
        ),
        st.Page("chat.py", title="AI Chat", icon=":material/chat:"),
    ],
}

pg = st.navigation(pages, position="sidebar")
pg.run()
