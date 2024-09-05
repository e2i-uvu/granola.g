import os
from typing import Callable
from dotenv import load_dotenv
import logging
import typing

import requests
from requests.auth import HTTPBasicAuth

# TypeAliases
code = int
url = str
data = dict[str,str]

def set_basic_state() -> tuple[str,str,str,str]:
    """Load environment variables and other useful state."""
    load_dotenv()
    logging.basicConfig(filename = "test.log", level = logging.INFO)
    return os.getenv("BACKEND"), os.getenv("USERNAME"), os.getenv("PASSWORD"), {"Content-Type": "application/json"}


def get_status_code(url: url, data: data) -> int:
    backend, username, password, standard_headers = set_basic_state()
    response = requests.post(
        backend + url, #json = {"uvuid": data},
        auth=HTTPBasicAuth(username, password),
        json=data,
        headers=standard_headers
    )
    return response.status_code

def test_request(logger: str, data: data, expected_status_code: code, case: str, /, url: url, request_function: Callable[[url,data], code] = get_status_code) -> None:
    if url == None:
        raise TypeError("URL cannot be of NoneType.")

    status: code = request_function(url, data)
    if status == expected_status_code:
        logger.info("Sucessfully fails " + case)#ok_message)
    else:
        logger.warning(str(status) + " Does not fail " + case)#error_message)


