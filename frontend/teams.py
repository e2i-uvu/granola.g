import streamlit as st
from pypdf import PdfReader

st.title("Team Import :material/reduce_capacity:")
st.write("---")

def read_pdf(pdf_file) -> str:
    reader = PdfReader(pdf_file)
    content: str = ""
    for page in reader.pages:
        content += page.extract_text()
    return content

files = st.file_uploader(
    "Project Charter",
    type=["csv", "docx", "pdf"],
    accept_multiple_files=True,
)


if files is not None:
    for file in files:
        # NOTE: project_description is a string containing text form pdf
        project_description: str = read_pdf(file)
