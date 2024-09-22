"""
Entrypoint for the streamlit frontend
"""

import streamlit as st

import toml
import hmac
import re
import os

from dotenv import load_dotenv

from openai import OpenAI

from ai import SYSTEM_MESSAGE, TOOLS


VERSION = 1.000
MODEL = "gpt-4o-mini"
USERS = "./.streamlit/users.toml"


def style(filename: str = "./styles/main.css"):
    """Hide default style. Additionally add custom styles"""
    with open(filename, "r") as f:
        css = f.read()
    return f"""<style>\n{css}\n</style>"""


# --- Setup session state --- #

st.session_state.mobile_pat = re.compile(r"[mM]obile|iPhone|iPad|iPod|Android|webOS")

if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "user" not in st.session_state:
    st.session_state.user = {
        "id": None,
        "first": None,
        "last": None,
        # "name": None,
        "role": None,
        "mobile": False,
    }


if "gpt" not in st.session_state:
    st.session_state.gpt = {
        "client": OpenAI(api_key=os.environ.get("OPENAI_API_KEY")),
        "model": MODEL,
        "system_message": [{"role": "system", "content": SYSTEM_MESSAGE}],
        "messages": [],
        "tools": {
            tool.get("name"): {
                "tool": tool.get("tool"),
                "func": tool.get("func"),
                "local": tool.get("local"),
            }
            for tool in TOOLS
        },
    }

if "layout" not in st.session_state:
    if st.session_state.mobile_pat.search(st.context.headers["User-Agent"]):
        st.session_state.user["mobile"] = True
        st.session_state.layout = "wide"
    else:
        st.session_state.layout = "centered"

if "backend" not in st.session_state:
    # NOTE: Can use like the rest, example:
    # `st.session_state.backend["url"]` -> backend url

    # TODO: This moves the environment variables into the session_state
    # But we should maybe also move the functions, and possibly even look
    # into streamlit connections:
    # https://docs.streamlit.io/develop/api-reference/connections/st.connection
    load_dotenv()
    st.session_state.backend = {
        "url": os.getenv("BACKEND"),
        "username": os.getenv("USERNAME"),
        "password": os.getenv("PASSWORD"),
    }

# --- Setup session state --- #

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
    # link="https://www.uvu.edu/innovation/e2i/",
    link=None,
    icon_image="./static/uvu-logo-cropped-green.png",
)


# ROLES = [None, "student", "admin", "developer"]
ROLES = [None, "student", "admin"]


def check_password(role) -> bool:
    """Returns `True` if the user had the correct password."""

    def password_entered(role) -> None:
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

    uvid = st.text_input(
        label="Username / UVID",
        # disabled=True,  # remove upon implementation
        max_chars=8,
        # placeholder="Username / UVID",
        label_visibility="visible",
    )

    if uvid:  # and st.session_state.user["id"] is not None:

        users = toml.load(USERS)

        for user in users["users"]:
            if str(user["id"]) == uvid:

                if not user["verified"]:
                    st.warning("Waiting for verification", icon=":material/hourglass:")
                    # TODO: Add cookies here
                    # to stop spamming
                    st.stop()

                if not check_password(user["role"]):
                    st.session_state.attempts += 1
                    # TODO: Add cookies here
                    # just to stop bad actors
                    st.stop()

                st.session_state.user["id"] = user["id"]
                # st.session_state.user["name"] = user["name"]
                st.session_state.user["first"] = user["first"]
                st.session_state.user["last"] = user["last"]
                st.session_state.user["role"] = user["role"]
                st.rerun()

            # else:
        with st.form("register-new-uvid", clear_on_submit=True):

            st.subheader("UVID Not Found")
            st.write("Register")
            col1, col2 = st.columns(2)

            first = col1.text_input("First Name")
            last = col2.text_input("Last Name")

            role = st.selectbox(
                label="Choose your role",
                placeholder="Choose your role",
                options=ROLES,
                label_visibility="visible",
            )

            submitted = st.form_submit_button("Update map")
            if submitted:
                with open(USERS, "a") as f:
                    f.write(
                        f"""
[[users]]
id = {uvid}
first = "{first}"
last = "{last}"
role = "{role}"
verified = false
"""
                    )
                st.rerun()


def logout():  # need to be careful to reset session_state
    """Logs the user out of the website,
    reset some parts of session_state"""

    if "password_correct" in st.session_state:
        del st.session_state["password_correct"]

    if "gpt" in st.session_state:
        del st.session_state.gpt

    if "first_login" in st.session_state:
        del st.session_state.first_login

    st.session_state.user["role"] = None
    st.rerun()


# any UI elements in this file will be rendered
# on every page of the streamlit app

# st.sidebar.caption(f"Version: :green-background[{VERSION}]")

account_pages = [
    st.Page(logout, title="Log out", icon=":material/logout:"),
    #    st.Page(
    # "availability.py",
    # title="My Availability",
    #        icon=":material/calendar_month:",
    #        default=(st.session_state.user["role"] == "student"),
    #    ),
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
    st.Page(
        "overview.py",  # "employees.py",
        title="Overview",  # "Employees",
        icon=":material/groups:",
        # default=(st.session_state.user["role"] == "admin"),
    ),
    st.Page(
        "teams.py",
        title="Team Builder",
        icon=":material/reduce_capacity:",
    ),
]

admin_pages = [
    st.Page("payroll.py", title="Payroll", icon=":material/local_atm:"),
    st.Page("file_upload.py", title="Qualtrics Upload", icon=":material/folder:"),
    st.Page("users.py", title="Verification", icon=":material/verified:"),
]

dev_pages = [
    # st.Page("my_availability.py", title="My Availability"),
    st.Page("sessionstate.py", title="Session State", icon=":material/settings:"),
    st.Page("test.py", title="Test Build Team"),
    # st.Page("users.py", title="Verification", icon=":material/verified:"),
]

pages = {}

if st.session_state.user["role"] in ["admin", "developer"]:
    pages["Teams"] = teams_pages
    pages["Admin"] = admin_pages

if st.session_state.user["role"] == "developer":
    pages["Development"] = dev_pages


if len(pages) > 0:
    pg = st.navigation({"Profile": account_pages} | pages)

    if "first_login" not in st.session_state:
        st.session_state.first_login = True

    if st.session_state.first_login:
        st.toast(f"Welcome {st.session_state.user['first']}!", icon=":material/login:")
        st.session_state.first_login = False

else:
    pg = st.navigation([st.Page(login)])


if not st.session_state.user["mobile"]:

    # Dynamically change to wide if going to payroll page
    if pg.title == "Payroll" or pg.title == "Overview":
        if st.session_state.layout == "centered":
            st.session_state.layout = "wide"
            st.rerun()

    else:
        if st.session_state.layout == "wide":
            st.session_state.layout = "centered"
            st.rerun()


pg.run()
