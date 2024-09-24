import json
import streamlit as st
from pypdf import PdfReader

st.title("Team Import :material/reduce_capacity:")
st.write("---")

# SYSTEM_MSG = {"role": "system", "content": }


def read_pdf(pdf_file) -> str:
    reader = PdfReader(pdf_file)
    content: str = ""
    for page in reader.pages:
        content += page.extract_text()
    return content


def generate_team(pdf_text):

    response = st.session_state.gpt["client"].chat.completions.create(
        model=st.session_state.gpt["model"],
        messages=[{"role": "user", "content": pdf_text}],
        tools=[t.get("tool") for t in st.session_state.gpt["tools"].values()],
        tool_choice={"type": "function", "function": {"name": "create_team"}},
        stream=False,
    )

    tool_calls = response.choices[0].message.tool_calls

    if tool_calls:
        for tc in tool_calls:
            if tc.function.arguments:
                function_args = json.loads(tc.function.arguments)
            else:
                function_args = {}

            function_response = st.session_state.gpt["tools"][tc.function.name]["func"](
                function_args
            )


files = st.file_uploader(
    "Project Charter",
    type=["csv", "docx", "pdf"],
    accept_multiple_files=True,
)

if st.button("Create Teams", type="primary", use_container_width=True):

    if files is not None:
        for file in files:
            # NOTE: project_description is a string containing text form pdf
            project_description: str = read_pdf(file)
            generate_team(project_description)
