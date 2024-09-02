import streamlit as st

import os
import json
import toml

import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

from openai import OpenAI

from datetime import datetime

from ai import display_team


load_dotenv()
backend = os.getenv("BACKEND")
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

# --- tool stuff --- #s

ai_config = toml.load("./ai.toml")


def test():
    st.toast("test successful")


respond = {
    "name": "test",
    "local": True,
    "func": test,
    "tool": {
        "type": "function",
        "function": {
            "name": "test",
            "description": "Call this function if the user is testing",
        },
    },
}


def build_new_team(
    # project_name: str, project_type: str, employees: list, total_employees: int
    request_json: str,
):
    # st.toast(
    #     f"New {project_type} Project!\nName: {
    #         project_name}, {total_employees}, {employees}"
    # )

    r = requests.get(
        backend + "teams", json=request_json, auth=HTTPBasicAuth(username, password)
    )

    if r.status_code == 200:
        # Successful request
        response_data = r.json()
        print(response_data)
    else:
        # Handle the error
        print(f"Error: {r.status_code}")

    return "Sucess!"


employee_types = [
    "Full stack",
    "Frontend",
    "Backend",
    "Database",
    "Embedded",
    "Game Development",
]

project_types = ai_config["project_types"]
employee_types = ai_config["employee_types"]


create_team = {
    "name": "create_team",
    "local": False,
    "func": build_new_team,
    "tool": {
        "type": "function",
        "function": {
            "name": "create_team",
            "strict": True,
            "description": """Create team or project based on description provided by user.
            Created teams should have the proper skills and the necessary amount of each employee
            to complete the project. Assume the Project manager is already chosen.""",
            "parameters": {
                "type": "object",
                "properties": {
                    "project_name": {
                        "type": "string",
                        "description": "The name of the team or project",
                    },
                    "project_type": {
                        "type": "string",
                        "description": "The type of project",
                        "enum": project_types,
                    },
                    "employees": {
                        "type": "array",
                        "description": """List of employees needed to successfully complete the project.
                        Decide what combination and amount of each employee is needed by infering from
                        the user's description. Do not explicitly ask to user to provide the specific
                        roles/types.""",
                        "items": {
                            "type": "object",
                            "properties": {
                                "employee": {
                                    "type": "string",
                                    "enum": employee_types,
                                    "description": """Type of employee needed to complete the project.""",
                                },
                                "amount": {
                                    "type": "number",
                                    "description": "The total number of this type of employee needed",
                                },
                            },
                            "required": [
                                "employee",
                                "amount",
                            ],
                            "additionalProperties": False,
                        },
                    },
                    "total_employees": {
                        "type": "number",
                        "description": "The total number of employees needed for a team, between 3 and 6",
                    },
                },
                "required": [
                    "project_name",
                    "project_type",
                    "total_employees",
                    "employees",
                ],
                "additionalProperties": False,
            },
        },
    },
}

# add tools here like "create team" see below
# https://platform.openai.com/docs/guides/function-calling

# --- tool stuff --- #


TOOLS = [respond, create_team]


# formatted_time = datetime.now().strftime("%H:%M on %A, %Y-%m-%d")

SYSTEM_MESSAGE = f"""# Instructions

* The current date and time is {datetime.now().strftime('%H:%M on %A, %Y-%m-%d')}
* You are an assistant for the E2i Program at Utah Valley University (UVU).
* You responses are formatted in github flavored markdown, with an occasional emoji.
* Respond with concise and effective messages and a bright, upbeat and confident tone.

## Tools

Ask clarifying questions before calling tools if needed.
"""


if "gpt" not in st.session_state:
    st.session_state.gpt = {
        "client": OpenAI(api_key=os.environ.get("OPENAI_API_KEY")),
        "model": "gpt-4o-mini",
        "system_message": [{"role": "system", "content": SYSTEM_MESSAGE}],
        "messages": [],
        "tools": {
            t.get("name"): {
                "tool": t.get("tool"),
                "func": t.get("func"),
                "local": t.get("local"),
            }
            for t in TOOLS
        },
    }


def moderate(query: str):

    mod = st.session_state.gpt["client"].moderations.create(input=query)
    for r in mod.results:  # log results if flagged
        if r.flagged:  # TODO: logging here
            return True

    return False


def ai(query: str = ""):

    if query:
        if moderate(query):
            return "I'm sorry, I can't help you with that."

    st.session_state.gpt["messages"].append({"role": "user", "content": query})

    # st.session_state.status.update(label="Thinking...", state="running")

    response = st.session_state.gpt["client"].chat.completions.create(
        model=st.session_state.gpt["model"],
        messages=st.session_state.gpt["system_message"]
        + st.session_state.gpt["messages"],
        tools=[t.get("tool") for t in st.session_state.gpt["tools"].values()],
        tool_choice="auto",
        stream=True,
    )

    completion = ""
    tool_calls = []
    for chunk in response:  # handle response
        delta = chunk.choices[0].delta

        if delta and delta.content:
            completion += delta.content
            yield delta.content

        elif delta and delta.tool_calls:  # handle tools
            for tool in delta.tool_calls:

                if len(tool_calls) <= tool.index:
                    tool_calls.append(
                        {
                            "id": "",
                            "type": "function",
                            "function": {"name": "", "arguments": ""},
                        }
                    )

                tc = tool_calls[tool.index]

                if tool.id:
                    tc["id"] += tool.id

                if tool.function.name:
                    tc["function"]["name"] += tool.function.name

                if tool.function.arguments:
                    tc["function"]["arguments"] += tool.function.arguments

    if tool_calls:

        st.session_state.gpt["messages"].append(
            {"role": "assistant", "content": completion, "tool_calls": tool_calls}
        )

        for tc in tool_calls:
            function_name = tc["function"]["name"]

            # normally surround in try except, gonna try without it

            print(tc["function"]["arguments"])  # for testing only

            if st.session_state.gpt["tools"][function_name]["local"]:

                if tc["function"]["arguments"]:
                    function_args = json.loads(tc["function"]["arguments"])
                else:
                    function_args = {}

                function_response = st.session_state.gpt["tools"][function_name][
                    "func"
                ](**function_args)

            else:

                function_args_json = tc["function"]["arguments"]

                function_response = st.session_state.gpt["tools"][function_name][
                    "func"
                ](function_args_json)

            # TODO: give better value back to ai
            # call backend here to get team

            st.session_state.gpt["messages"].append(
                {
                    "tool_call_id": tc["id"],
                    "role": "tool",
                    "name": function_name,
                    "content": str(function_response),
                }
            )

    if completion:
        st.session_state.gpt["messages"].append(
            {"role": "assistant", "content": completion}
        )

    # if query: # recursive
    #     yield ai()


def render_messages():
    for message in st.session_state.gpt["messages"]:
        if not message["content"]:
            continue

        elif message["role"] == "tool":
            continue

        else:
            st.chat_message(name=message["role"]).markdown(message["content"])

        # TODO: @Guts this is where we will put the selector

        # TODO: also need to not render tool calls

    with st.chat_message("assistant"):
        display_team(
            [
                {
                    0: {
                        "id": "E001",
                        "name": "Alice Johnson",
                        "email": "alice.johnson@uvu.edu",
                        "uvid": "U12345678",
                        "degreepercent": 85,
                        "teambefore": True,
                        "speciality": "Software Engineering",
                        "major": "Computer Science",
                        "majoralt": "Mathematics",
                        "aoi": "Artificial Intelligence",
                        "social": 5,
                        "statuss": 1,
                    }
                },
                {
                    1: {
                        "id": "E002",
                        "name": "Bob Smith",
                        "email": "bob.smith@uvu.edu",
                        "uvid": "U87654321",
                        "degreepercent": 90,
                        "teambefore": False,
                        "speciality": "Data Analysis",
                        "major": "Information Systems",
                        "majoralt": "Statistics",
                        "aoi": "Big Data",
                        "social": 7,
                        "status": 2,
                    }
                },
                {
                    2: {
                        "id": "E003",
                        "name": "Catherine Lee",
                        "email": "catherine.lee@uvu.edu",
                        "uvid": "U11223344",
                        "degreepercent": 75,
                        "teambefore": True,
                        "speciality": "Cybersecurity",
                        "major": "Computer Science",
                        "majoralt": "Criminal Justice",
                        "aoi": "Network Security",
                        "social": 6,
                        "status": 1,
                    }
                },
                {
                    3: {
                        "id": "E004",
                        "name": "David Brown",
                        "email": "david.brown@uvu.edu",
                        "uvid": "U44332211",
                        "degreepercent": 80,
                        "teambefore": False,
                        "speciality": "Project Management",
                        "major": "Business Administration",
                        "majoralt": "Management",
                        "aoi": "Agile Methodologies",
                        "social": 8,
                        "status": 2,
                    }
                },
                {
                    4: {
                        "id": "E005",
                        "name": "Eva Green",
                        "email": "eva.green@uvu.edu",
                        "uvid": "U55667788",
                        "degreepercent": 95,
                        "teambefore": True,
                        "speciality": "Machine Learning",
                        "major": "Computer Engineering",
                        "majoralt": "Data Science",
                        "aoi": "Deep Learning",
                        "social": 9,
                        "status": 1,
                    }
                },
                {
                    5: {
                        "id": "E006",
                        "name": "Frank White",
                        "email": "frank.white@uvu.edu",
                        "uvid": "U99887766",
                        "degreepercent": 70,
                        "teambefore": False,
                        "speciality": "Web Development",
                        "major": "Information Technology",
                        "majoralt": "Graphic Design",
                        "aoi": "Frontend Development",
                        "social": 4,
                        "status": 2,
                    }
                },
            ]
        )  # testing


st.title("AI Chat :brain:")
col1, col2 = st.columns(2, vertical_alignment="bottom")

with col1:
    if st.button("New Chat", use_container_width=True):
        st.session_state.gpt["messages"] = []

# with col2:
# st.session_state.status = st.status(label="Waiting", state="complete")

if st.session_state.user["role"] == "developer":
    with st.popover("Messages", use_container_width=True):
        st.json(st.session_state.gpt["messages"])

st.write("---")

render_messages()
if user_input := st.chat_input("Send a message"):

    st.chat_message("user").markdown(user_input)

    with st.chat_message("assistant"):

        # st.chat_message("assistant").write_stream(stream_response(user_input))
        st.write_stream(ai(user_input))

        # st.rerun()
