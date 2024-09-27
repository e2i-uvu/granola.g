import streamlit as st
import random
import json


PLACEHOLDERS = ["Send a message", "I want to build a team..."]


def moderate(query: str):

    mod = st.session_state.gpt["client"].moderations.create(input=query)
    for r in mod.results:  # log results if flagged
        if r.flagged:  # TODO: logging here
            return True

    return False


def ai(query: str = ""):

    if query:
        if moderate(query):
            # return "I'm sorry, I can't help you with that."
            st.error("I'm sorry, I can't help you with that.")
            return "I'm sorry, I can't help you with that."

    st.session_state.gpt["messages"].append({"role": "user", "content": query})

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

            if tc["function"]["arguments"]:
                function_args = json.loads(tc["function"]["arguments"])
            else:
                function_args = {}

            if st.session_state.gpt["tools"][function_name]["local"]:

                # This one unpacks kwargs
                function_response = st.session_state.gpt["tools"][function_name][
                    "func"
                ](**function_args)

            else:

                # This one does not
                function_response = st.session_state.gpt["tools"][function_name][
                    "func"
                ](function_args)

            st.session_state.gpt["messages"].append(
                {
                    "tool_call_id": tc["id"],
                    "role": "tool",
                    "name": function_name,
                    "content": str(function_response),
                }
            )

        # respond again?
        response = st.session_state.gpt["client"].chat.completions.create(
            model=st.session_state.gpt["model"],
            messages=st.session_state.gpt["system_message"]
            + st.session_state.gpt["messages"],
            stream=True,
        )

        completion = ""
        for chunk in response:  # handle response
            delta = chunk.choices[0].delta

            if delta and delta.content:
                completion += delta.content
                yield delta.content

        # st.session_state.gpt["messages"].append(
        #     {"role": "assistant", "content": completion}
        # )

        # if query:  # recursive
        # yield ai()

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


col1, col2 = st.columns([2, 1], vertical_alignment="bottom")
col1.title("AI Chat :material/chat:")

with col2:
    if st.button("New Chat", use_container_width=True):
        st.session_state.gpt["messages"] = []

if st.session_state.user["role"] == "developer":
    with st.popover("Messages", use_container_width=True):
        st.json(st.session_state.gpt["messages"])

st.caption("Keep in mind AI responses may be inaccurate.")

st.write("---")

render_messages()

if user_input := st.chat_input(
    # random.choice(PLACEHOLDERS), key="current_user_message"  # , on_submit=respond
    "Send a message",
    key="current_user_message",  # , on_submit=respond
):

    # st.chat_message("user").markdown(st.session_state.current_user_message)
    st.chat_message("user").markdown(user_input)

    with st.chat_message("assistant"):

        # st.write_stream(ai(st.session_state.current_user_message))
        st.write_stream(ai(user_input))

# if user_input := st.chat_input(random.choice(PLACEHOLDERS)):
# if user_input:
#
#     st.chat_message("user").markdown(st.session_state.current_user_message)
#
#     with st.chat_message("assistant"):
#
#         st.write_stream(ai(st.session_state.current_user_message))
