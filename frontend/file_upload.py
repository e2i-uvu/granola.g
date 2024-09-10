"""
    Documentation
    
    Maximum file size depends on streamlit.server.maxUploadSize, and it's defaulted
    to 200MB

    Code doesn't support multiple files.


    Journal:
    Maybe adding support for json?
"""

import streamlit as st
from io import StringIO
import csv
import requests
from requests.auth import HTTPBasicAuth


def upload_csv() -> list[dict[str, str]]:
    uploadedFile = st.file_uploader(
        label="Upload file", type=["csv"], accept_multiple_files=False
    )

    if uploadedFile is not None:
        stringInput = StringIO(uploadedFile.getvalue().decode("utf-8"))
        table = csv.DictReader(stringInput)
        next(table)
        next(table)

        data = []
        for row in table:
            # st.write(row)
            data.append(row)
        return data


def import_csv_data(*, testing=False):

    # NOTE: I have a nice function that can summarize loading up all this data
    # Nice! I like your code 😄 I refactored the backend variables for you
    data = upload_csv()

    if data and testing:
        st.write(data)

    if data:
        # print(data)
        response = requests.post(
            st.session_state.backend["url"] + "/employeesIngest",
            auth=HTTPBasicAuth(
                st.session_state.backend["username"],
                st.session_state.backend["password"],
            ),
            headers={"Content-Type": "application/json"},
            json=data,
        )
        st.write(response.status_code)


import_csv_data()  # True)
