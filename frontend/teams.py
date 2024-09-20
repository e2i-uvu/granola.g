import streamlit as st

files = st.file_uploader(
    "Project Charter",
    type=["csv", "docx", "pdf"],
    accept_multiple_files=True,
)


if files is not None:
    pass
