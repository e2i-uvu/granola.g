import streamlit as st

st.title("Team Import :material/reduce_capacity:")

files = st.file_uploader(
    "Project Charter",
    type=["csv", "docx", "pdf"],
    accept_multiple_files=True,
)


if files is not None:
    pass
