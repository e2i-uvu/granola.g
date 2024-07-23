"""
Entrypoint for the streamlit frontend
"""

import streamlit as st
import sys

VERSION = 0.1

if "role" not in st.session_state:
    st.session_state.role = None

ROLES = [None, "Requester", "Responder", "Admin"]

def login():
    st.header("Log in")

    role = st.selectbox("Choose your role", ROLES)

    if st.button("Log in"):
        st.session_state.role = role
        st.rerun()

def logout():
    st.session_state.role = None
    st.rerun()

try:
    if sys.argv[1] == "dev":
        st.session_state["dev"] = True
    else:
        st.session_state["dev"] = False

except IndexError:
    st.session_state["dev"] = False


def style(filename: str = "./styles/main.css"):
    """Hide default style. Additionally add custom styles"""
    with open(filename, "r") as f:
        css = f.read()
    return f"<style>{css}</style>"


st.set_page_config(
    page_title="E2i",
    page_icon=":material/school:",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        # TODO: Guts take a look at this
        # ./styles/main.css hides this,
        # but maybe we should add these
        "Get Help": "https://www.extremelycoolapp.com/help",
        "Report a bug": "https://www.extremelycoolapp.com/bug",
        "About": "# This is a header. This is an *extremely* cool app!",
    },
)


# any UI elements in this file will be rendered
# on every page of the streamlit app

# st.title("Team Building")s is an *


# st.markdown(style(), unsafe_allow_html=True)


st.logo(
    image="./static/innovation-academy-logo-side-green.png",
    link="https://www.uvu.edu/innovation/e2i/",
    icon_image="./static/uvu-logo-cropped-green.png",
)

# can add pages here
pages = {
    "Info": [
        st.Page("about.py", title="About", icon=":material/info:", default=False),
        st.Page("guide.py", title="How to", icon=":material/help:"),
    ],
    "Teams": [
        st.Page("interview.py", title="Interview", icon=":material/person_add:"),
        st.Page("employees.py", title="Employees", icon=":material/groups:"),
        st.Page(
            "teams.py",
            title="Team Building",
            icon=":material/reduce_capacity:",
        ),
        st.Page("chat.py", title="AI Chat", icon=":material/chat:"),
    ],
    "For Development": [st.Page("stdataframe.py", title="jsonToDataFrame"),
                        st.Page("myAvailability.py", title="My Availability")],
}

st.sidebar.caption(f"Version: :green-background[{VERSION}]")

pg = st.navigation(pages, position="sidebar")
pg.run()
