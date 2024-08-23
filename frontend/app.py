"""
Entrypoint for the streamlit frontend
"""

import streamlit as st
import hmac
import sys
import re

VERSION = 0.102

try:
    if sys.argv[1] == "dev":
        st.session_state["dev"] = True
        st.session_state.user = {
            "id": 11111111,
            "name": "Stinky Developer",
            "role": "developer",
        }
        st.session_state["password_correct"] = True
    else:
        st.session_state["dev"] = False

except IndexError:
    st.session_state["dev"] = False


def style(filename: str = "./styles/main.css"):
    """Hide default style. Additionally add custom styles"""
    with open(filename, "r") as f:
        css = f.read()
    return f"<style>{css}</style>"


# if "center" not in st.session_state:
#     layout = "wide"
# else:
#     layout = "centered" if st.session_state.center else "wide"

st.session_state.mobile_pat = re.compile(r"[mM]obile|iPhone|iPad|iPod|Android|webOS")

if "user" not in st.session_state:
    st.session_state.user = {"id": None, "name": None, "role": None, "mobile": False}

if "layout" not in st.session_state:
    if st.session_state.mobile_pat.search(st.context.headers["User-Agent"]):
        st.session_state.user["mobile"] = True
        st.session_state.layout = "wide"
    else:
        st.session_state.layout = "centered"

st.set_page_config(
    page_title="E2i",
    page_icon=":trophy:",  # add e2i logo here
    layout=st.session_state.layout,
    initial_sidebar_state="expanded",
    menu_items={  # currently hidden
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


ROLES = [None, "student", "admin", "developer"]


def check_password(role):
    """Returns `True` if the user had the correct password."""

    def password_entered(role):
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(
            st.session_state["password"],
            st.secrets.passwords[role],
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False

    # Return True if the password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password.
    st.text_input(
        "Password",
        type="password",
        on_change=password_entered,
        args=(role,),
        key="password",
    )
    if "password_correct" in st.session_state:
        st.error("😕 Password incorrect")
    return False


def login():
    st.header("Log in")

    # def check_password():
    #     """Insert secure password checking here"""
    #     pass

    # st.text_input(
    #     label="Username / UVID",
    #     disabled=True,  # remove upon implementation
    #     max_chars=8,
    #     placeholder="Username / UVID",
    #     label_visibility="hidden",
    # )
    # st.text_input(
    #     label="Password",
    #     disabled=True,  # remove upon implementation
    #     type="password",
    #     on_change=check_password,
    #     key="password",
    #     placeholder="Password",
    #     label_visibility="hidden",
    # )

    # st.caption("Username and Password currently not needed")

    # TODO: Will change to username and password
    # col1, col2 = st.columns([3, 1], vertical_alignment="bottom")
    role = st.selectbox(
        label="Choose your role",
        placeholder="Choose your role",
        options=ROLES,
        label_visibility="visible",
    )

    if role == "admin" or role == "developer":
        if not check_password(role):
            st.stop()

    if role is not None:
        st.session_state.user["role"] = role
        st.rerun()


def logout():  # need to be careful to reset session_state
    """Logs the user out of the website,
    reset some parts of session_state"""

    if "password_correct" in st.session_state:
        del st.session_state["password_correct"]

    if "gpt" in st.session_state:
        del st.session_state.gpt

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
        "chat.py",
        title="AI Chat",
        icon=":material/chat:",
        default=(
            st.session_state.user["role"] == "admin"
            or st.session_state.user["role"] == "developer"
        ),
    ),
    # st.Page(
    #     "interview.py",
    #     title="Interview",
    #     icon=":material/person_add:",
    #     default=(st.session_state.user["role"] == "developer"),
    # ),
    st.Page(
        "employees.py",
        title="Employees",
        icon=":material/groups:",
        # default=(st.session_state.user["role"] == "admin"),
    ),
    st.Page(
        "teams.py",
        title="Team Building",
        icon=":material/reduce_capacity:",
    ),
]

admin_pages = [st.Page("payroll.py", title="Payroll", icon=":material/local_atm:")]

dev_pages = [
    st.Page("myAvailability.py", title="My Availability"),
    st.Page("sessionstate.py", title="Session State"),
]

pages = {}

if st.session_state.user["role"] in ["student", "admin", "developer"]:
    pages["Info"] = info_pages
    # pg = st.navigation({"Account": account_pages} | pages)

if st.session_state.user["role"] in ["admin", "developer"]:
    pages["Teams"] = teams_pages
    pages["Admin"] = admin_pages

if st.session_state.user["role"] == "developer":
    pages["Development"] = dev_pages


if len(pages) > 0:
    pg = st.navigation({"Profile": account_pages} | pages)

else:
    pg = st.navigation([st.Page(login)])


if not st.session_state.user["mobile"]:

    # Dynamically change to wide if going to payroll page
    if pg.title == "Payroll":
        if st.session_state.layout == "centered":
            st.session_state.layout = "wide"
            st.rerun()

    else:
        if st.session_state.layout == "wide":
            st.session_state.layout = "centered"
            st.rerun()


pg.run()
