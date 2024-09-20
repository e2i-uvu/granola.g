import streamlit as st
import requests
import json


from ai import display_team


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

            # print(tc["function"]["arguments"])  # for testing only

            if st.session_state.gpt["tools"][function_name]["local"]:

                if tc["function"]["arguments"]:
                    function_args = json.loads(tc["function"]["arguments"])
                else:
                    function_args = {}

                function_response = st.session_state.gpt["tools"][function_name][
                    "func"
                ](**function_args)

            else:
                function_response = st.session_state.gpt["tools"][function_name][
                    "func"
                ](tc["function"]["arguments"])

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

    # display_team(suggested_team) this will replace what is 3 lines down


col1, col2 = st.columns([2, 1], vertical_alignment="bottom")
col1.title("AI Chat :brain:")

with col2:
    if st.button("New Chat", use_container_width=True):
        st.session_state.gpt["messages"] = []

if st.session_state.user["role"] == "developer":
    with st.popover("Messages", use_container_width=True):
        st.json(st.session_state.gpt["messages"])

st.caption("Keep in mind AI responses may be inaccurate.")

st.write("---")

render_messages()
if user_input := st.chat_input("Send a message"):

    st.chat_message("user").markdown(user_input)

    with st.chat_message("assistant"):

        # st.chat_message("assistant").write_stream(stream_response(user_input))
        st.write_stream(ai(user_input))
