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
from dotenv import load_dotenv
import os


def upload_csv() -> list[dict[str, str]]:
    uploadedFile = st.file_uploader(label="Upload file", type=[
                                    "csv"], accept_multiple_files=False)

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
    load_dotenv()

    backend = os.getenv("BACKEND")
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")
    data = upload_csv()

    if data and testing:
        st.write(data)

    url = backend + "employeesIngest"

    # WARNING: Backend still on work. This might not work
    if data:
        #print(data)
        response = requests.post(
            url, auth=HTTPBasicAuth(username, password), 
            headers={"Content-Type": "application/json"}, 
            json=data
        )
        wrtie(response.status_code)


import_csv_data(testing=False)#True)
