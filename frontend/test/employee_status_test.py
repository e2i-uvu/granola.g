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
backend, username, password, _ = testutils.set_basic_state()

#module_logger = logging.getLogger("employee_statusHandler_Test")

def employee_status(url: str = "status"):
    request = requests.get(
            backend + url,
            auth = HTTPBasicAuth(username,password)
    )
    return request.status_code

def test_employee_status(url: str = "status"):
    # NOTE: Should I test the status_code or also the structure of the contents?
    module_logger = logging.getLogger(f"{url.title()}_Test")
    if employee_status(url) == 200:
        module_logger.info(f"succesfully returns data.")
    else:
        module_logger.error(f"fails to return data.")

def run_tests():
    test_employee_status("status")
    test_employee_status("hire")
    test_employee_status("fire")


if __name__ == "__main__":
    run_tests()

