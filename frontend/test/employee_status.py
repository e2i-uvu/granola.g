import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os
#import pandas as pd

import logging
import testutils

#load_dotenv()
#backend = os.getenv("BACKEND")
#username = os.getenv("USERAME")
#password = os.getenv("PASSWORD")
backend, username, password, standard_header = testutils.set_basic_state()

#module_logger = logging.getLogger("employee_statusHandler_Test")

def get_employee_status(url: str = "status"):
    request = requests.get(
            backend + url,
            auth = HTTPBasicAuth(username,password)
    )
    return request.status_code

def post_employee_status(url: str, data: dict[str,str]) -> int:
    response = requests.post(
        backend + url,
        auth = HTTPBasicAuth(username, password),
        json = data,
        headers = standard_header
    )
    return response.status_code

def test_get(url: str = "status") -> None:
    # NOTE: Should I test the status_code or also the structure of the contents?
    module_logger = logging.getLogger(f"get_{url.title()}_Test")
    if get_employee_status(url) == 200:
        module_logger.info(f"succesfully returns data.")
    else:
        module_logger.error(f"fails to return data.")


def test_post(url: str, data: dict[str,str]) -> None:
    module_logger = logging.getLogger(f"post_{url.title()}_Test")
    if post_employee_status(url) == 200:
        module_logger.info("successfully returns data.")
    else:
        module_logger.error(f"fails to return data.")


def run_tests():
    test_get("status")
    test_get("hire")
    test_get("fire")

    # Post tests
    post_data: dict[str,str] ={
            {
            "uvuid": "11006941",
            "status": "1"
        }
    }
    test_post("hire")
    test_post("fire")


if __name__ == "__main__":
    run_tests()
