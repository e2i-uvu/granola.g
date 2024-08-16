import streamlit as st

import os
import json

from openai import OpenAI

from datetime import datetime

# --- tool stuff --- #


def stream_response():

    response = st.session_state.gpt["client"].chat.completions.create(
        model=st.session_state.gpt["model"],
        messages=st.session_state.gpt["system_message"]
        + st.session_state.gpt["messages"],
        stream=True,
    )

    completion = ""
    for chunk in response:
        delta = chunk.choices[0].delta

        if delta and delta.content:
            completion += delta.content
            yield delta.content

    st.session_state.gpt["messages"].append(
        {"role": "assistant", "content": completion}
    )


respond = {
    "name": "respond",
    "func": stream_response,
    "tool": {
        "type": "function",
        "function": {
            "name": "respond",
            "description": "Respond to the user",
        },
    },
}


def build_new_team(project_name: str, project_type: str, total_employees: int):
    st.toast(f"New {project_type} Project!\nName: {project_name}, {total_employees}")


create_team = {
    "name": "create_team",
    "func": build_new_team,
    "tool": {
        "type": "function",
        "function": {
            "name": "create_team",
            "strict": True,
            "description": "Create team description",  # TODO:
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
                        "enum": ["Tech", "Marketing"],
                    },
                    "total_employees": {
                        "type": "number",
                        "description": "The total number of employees needed for a team, between 3 and 6",
                    },
                },
                "required": ["project_name", "project_type", "total_employees"],
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
"""


if "gpt" not in st.session_state:
    st.session_state.gpt = {
        "client": OpenAI(api_key=os.environ.get("OPENAI_API_KEY")),
        "model": "gpt-4o-mini",
        "system_message": [{"role": "system", "content": SYSTEM_MESSAGE}],
        "messages": [],
        # "tools": TOOLS,
        "tools": {
            t.get("name"): {"tool": t.get("tool"), "func": t.get("func")} for t in TOOLS
        },
    }


def moderate(query: str):

    mod = st.session_state.gpt["client"].moderations.create(input=query)

    # log results if flagged
    for r in mod.results:
        if r.flagged:
            # logging here
            return True

    return False


def ai(query: str = ""):

    if query:
        if moderate(query):
            return "I'm sorry, I can't help you with that."

    st.session_state.gpt["messages"].append({"role": "user", "content": query})

    st.session_state.status.update(label="Thinking...", state="running")

    response = st.session_state.gpt["client"].chat.completions.create(
        model=st.session_state.gpt["model"],
        messages=st.session_state.gpt["system_message"]
        + st.session_state.gpt["messages"],
        # tools=st.session_state.gpt["tools"],
        tools=[t.get("tool") for t in st.session_state.gpt["tools"].values()],
        tool_choice="required",
    )

    # st.write(response.choices[0].message.content)
    # st.write(response.choices[0].message)
    for tool_call in response.choices[0].message.tool_calls:
        function_name = tool_call.function.name

        function_args = json.loads(tool_call.function.arguments)

        # function_response = st.session_state.gpt["tools"][function_name]["func"](
        #     **function_args
        # )

        try:
            if function_name == "respond":
                st.session_state.status.update(label="Responding...")

            for r in st.session_state.gpt["tools"][function_name]["func"](
                **function_args
            ):
                yield r

        except:  # catch tools that don't work
            pass

        finally:  # add to messages

            st.session_state.status.update(label="Waiting", state="complete")

    # if query:
    #     yield ai()


def render_messages():
    for message in st.session_state.gpt["messages"]:
        st.chat_message(name=message["role"]).markdown(message["content"])


st.title("AI Chat :brain:")
col1, col2 = st.columns(2, vertical_alignment="bottom")

with col1:
    if st.button("New Chat", use_container_width=True):
        st.session_state.gpt["messages"] = []

with col2:
    st.session_state.status = st.status(label="Waiting", state="complete")

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
