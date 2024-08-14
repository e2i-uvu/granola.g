import streamlit as st

import os
import json

from openai import OpenAI

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

# add tools here like "create team" see below
# https://platform.openai.com/docs/guides/function-calling

# --- tool stuff --- #


TOOLS = [respond]

# TODO: improve
SYSTEM_MESSAGE = """
You are an assistant for the E2i Program at Utah Valley University (UVU).
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


def ai(query: str = ""):

    st.session_state.gpt["messages"].append({"role": "user", "content": query})

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

        for r in st.session_state.gpt["tools"][function_name]["func"](**function_args):
            yield r

        # ahh idk what to do here

        # if function_args:
        #     # function_resp = eval(f"{function_name}({function_args})")
        #     for i in eval(f"{function_name}({function_args})"):
        #         yield i
        # else:
        #     # function_resp = eval(f"{function_name}()")
        #     for i in eval(f"{function_name}()"):
        #         yield i

        # st.write(tool_call)
        # st.write(function_resp)

    # if query:
    #     yield ai()


def render_messages():
    for message in st.session_state.gpt["messages"]:
        st.chat_message(name=message["role"]).markdown(message["content"])


st.title("AI Chat")
st.write("---")

render_messages()
if user_input := st.chat_input("Send a message"):

    st.chat_message("user").markdown(user_input)

    with st.chat_message("assistant"):

        # st.chat_message("assistant").write_stream(stream_response(user_input))
        st.write_stream(ai(user_input))
