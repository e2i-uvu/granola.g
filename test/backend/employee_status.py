import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os
#import pandas as pd

import pytest
#import logging
import testutils

backend, username, password, standard_header = testutils.set_basic_state()

#module_logger = logging.getLogger("employee_statusHandler_Test")

def verify_query_data(data: list[dict[str,str]]) -> None:
    columns: set[str] = {"pid", "uvuid", "name", "lang","aoi", "cancode", "enjoyment", "social","status","score"}
    for row in data:
        if set(row.keys()) != columns:
            return False
    return True

#def get_employee_status(url: str = "status"):
#request = requests.get(
#            backend + url,
#            auth = HTTPBasicAuth(username,password)
#    )
#    return request

def post_employee_status(url: str, data: dict[str,str]) -> int:
    response = requests.post(
        backend + url,
        auth = HTTPBasicAuth(username, password),
        json = data,
        headers = standard_header
    )
    return response.status_code

def eval_get(url: str = "status") -> bool:
    # NOTE: Should I test the status_code or also the structure of the contents?
    module_logger = logging.getLogger(f"get_{url.title()}_Test")

    response = requests.get(
            backend + url,
            auth = HTTPBasicAuth(username,password)
    )

    if response.status_code != 200:
        module_logger.error(f"fails to return data.")
    if not verify_query_data(response.json()):
        module_logger.error(f"returns inconsistent data.")
    else:
        module_logger.info("successfully return data.")
        return True
    return False

    #if get_employee_status(url) == 200:
    #    module_logger.info(f"succesfully returns data.")
    #else:
    #    module_logger.error(f"fails to return data.")


def eval_post(url: str, data: dict[str,str]) -> None:
    module_logger = logging.getLogger(f"post_{url.title()}_Test")
    _eval_post: Callable[[], bool] = lambda x,y,z,url : testutils.test_request(module_logger, x, y, z, url)
    return _eval_post(data, 200, "\b/posts data", url = url)


def run_tests():
    # Post tests
    post_data: dict[str,str] = [
            {
            "uvuid": "11006941",
            "status": "1"
        } ]
    
    # Get data
    assert eval_get("status")
    assert eval_get("hire")
    assert eval_get("fire")

    # Post Data
    assert eval_post("hire", post_data)
    assert eval_post("fire", post_data)

if __name__ == "__main__":
    run_tests()
