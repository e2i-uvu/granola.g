"""
Entrypoint for the streamlit frontend
"""

from numpy import place
import streamlit as st
import sys

VERSION = 0.101

try:
    if sys.argv[1] == "dev":
        st.session_state["dev"] = True
        st.session_state.user = {
            "id": 11111111,
            "name": "Stinky Developer",
            "role": "developer",
        }
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
        "Get Help": None,  # url
        "Report a bug": None,  # url
        "About": f"""# E2i Hub
        Version: {VERSION} """,
    },
)

st.markdown(style(), unsafe_allow_html=True)

st.logo(
    image="./static/innovation-academy-logo-side-green.png",
    link="https://www.uvu.edu/innovation/e2i/",
    icon_image="./static/uvu-logo-cropped-green.png",
)


if "user" not in st.session_state:
    st.session_state.user = {"id": None, "name": None, "role": None}

ROLES = [None, "student", "admin", "developer"]


def login():
    st.header("Log in")

    def check_password():
        """Insert secure password checking here"""
        pass

    st.text_input(
        label="Username / UVID",
        disabled=True,  # remove upon implementation
        max_chars=8,
        placeholder="Username / UVID",
        label_visibility="hidden",
    )
    st.text_input(
        label="Password",
        disabled=True,  # remove upon implementation
        type="password",
        on_change=check_password,
        key="password",
        placeholder="Password",
        label_visibility="hidden",
    )
    st.caption("Username and Password currently not needed")

    # TODO: Will change to username and password
    col1, col2 = st.columns([3, 1], vertical_alignment="bottom")
    role = col1.selectbox(
        label="Choose your role (temporary)",
        placeholder="Choose your role (temporary)",
        options=ROLES,
        label_visibility="visible",
    )

    if col2.button("Log in", use_container_width=True):
        st.session_state.user["role"] = role
        # st.session_state.user["role"] = "admin"
        st.rerun()


def logout():
    st.session_state.user["role"] = None
    st.rerun()


# any UI elements in this file will be rendered
# on every page of the streamlit app

# st.sidebar.caption(f"Version: :green-background[{VERSION}]")

account_pages = [
    st.Page(logout, title="Log out", icon=":material/logout:"),
    st.Page(
        "availability.py",
        title="My Availability",
        icon=":material/calendar_month:",
        default=(st.session_state.user["role"] == "student"),
    ),
]

info_pages = [
    st.Page(
        "about.py",
        title="About",
        icon=":material/info:",
        # default=(st.session_state.user["role"] == "student"),
    ),
    st.Page("guide.py", title="How to", icon=":material/help:"),
]

teams_pages = [
    st.Page(
        "interview.py",
        title="Interview",
        icon=":material/person_add:",
        default=(st.session_state.user["role"] == "developer"),
    ),
    st.Page(
        "employees.py",
        title="Employees",
        icon=":material/groups:",
        default=(st.session_state.user["role"] == "admin"),
    ),
    st.Page(
        "teams.py",
        title="Team Building",
        icon=":material/reduce_capacity:",
    ),
    st.Page("chat.py", title="AI Chat", icon=":material/chat:"),
]

dev_pages = [
    st.Page("stdataframe.py", title="jsonToDataFrame"),
    st.Page("myAvailability.py", title="My Availability"),
]

pages = {}

if st.session_state.user["role"] in ["student", "admin", "developer"]:
    pages["Info"] = info_pages
    # pg = st.navigation({"Account": account_pages} | pages)

if st.session_state.user["role"] in ["admin", "developer"]:
    pages["Teams"] = teams_pages

if st.session_state.user["role"] == "developer":
    pages["Development"] = dev_pages


if len(pages) > 0:
    pg = st.navigation({"Profile": account_pages} | pages)

else:
    pg = st.navigation([st.Page(login)])

# pg = st.navigation(pages, position="sidebar")
pg.run()
# print(st.session_state)
