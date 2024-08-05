import os
from typing import Callable
from dotenv import load_dotenv
import logging

def set_basic_state() -> tuple[str,str,str,str]:
    load_dotenv()
    logging.basicConfig(filename = "test.log", level = logging.INFO)
    return os.getenv("BACKEND"), os.getenv("USERNAME"), os.getenv("PASSWORD"), {"Content-Type": "application/json"}


def test_request(logger: str, request_function: Callable, data: dict[str,str], expected_status_code:int, case: str) -> None:
    status = request_function(data)
    if status == expected_status_code:
        logger.info("Sucessfully fails " + case)#ok_message)
    else:
        logger.warning(str(status) + " Does not fail " + case)#error_message)



