import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os

#import pytest
import logging
import testutils
#import time

load_dotenv()
backend = os.getenv("BACKEND")
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
standard_headers = {"Content-Type": "application/json"}

module_logger = logging.getLogger("InterviewFinishHandler_Test")

# TODO: Change parameter from string to dictionary/json

#def test_interviewFinish( data: dict[str,str] #data: str
#def make_interviewFinish_request(data: dict[str,str]) -> int:
def status_code(url: str, data: dict[str,str]) -> int:
    response = requests.post(
        backend + "interviewFinish", #json = {"uvuid": data},
        auth=HTTPBasicAuth(username, password),
        json=data,
        headers=standard_headers
    )
    return response.status_code

#def test_interviewFinish_request(data: dict[str,str], expected_status_code: int, case: str):
#    status = make_interviewFinish_request(data)
#    if status == expected_status_code:
#        module_logger.info("Sucessfully fails " + case)#ok_message)
#    else:
#        module_logger.warning(str(status) + "Does not fail " + case)#error_message)

def run_tests() -> None:
#if __name__ == "__main__":
    logging.basicConfig(filename = "test.log", level = logging.INFO)

    test = lambda x,y,z: testutils.test_request(module_logger, x, y, z, url = "interviewFinish")

    # Test interviewFinishHandler
    # 1. None datatype
    # Expected output: 406 - Fail
    #test_interviewFinish_request(
    test(None, 400, "None value.")#, "None values.")

    # . Non JSON argument
    # Expected output: 406 - Fail
    #test_interviewFinish_request(
    test(1000003, 400, "non-JSON value.")

    # FIX: Test cases where copied directly from the InterviewStartHandler test,
    # and haven't been updated.

    # . JSON argument, empty
    # Expected output: 406 - Fail
    #test_interviewFinish_request({}, 406, "Empty JSON.")

    # . JSON argument, key is in wrong datatype
    # Expected output: 406 - Fail
    #test_interviewFinish_request({1000003: "11006941"}, 406, "JSON with wrong key datatype")

    # .JSON argument, key is string but wrong
    # Expected output: 406 - Fail
    #test_interviewFinish_request({"lore ipsum": "11006941"}, 406, "JSON with wrong key")

    # 2. JSON argument, "uvuid" value is in wrong datatype
    # Expected output: 406 - Fail
    #test_interviewFinish_request({"uvuid": 35}, 406, "JSON with wrong value datatypes.")

    # 3. Valid datatype: Non-numeric string
    # Expected output: 406 - Fail
    #test_interviewFinish_request(
    test(
        {
            "fkuser": "lore ipsum",
            "cancode": "True",
            "enjoyment":"5",
            "social":"5"
        },
        400, "JSON with non-numeric value.")

    # 4. Valid datatype: numeric string
    # Expected output: 200 - OK
    # FIX: Returning error. Is the "cancode" value wrong?
    #if make_interviewFinish_request(
    if testutils.get_status_code("interviewFinish",
        {
            "fkuser": "11006941",
            "cancode": "True",
            "enjoyment": "5",
            "social": "5"
        },) == 200: 
        module_logger.info("succesfully manages valid input")
    else:
        module_logger.error("fails to manage valid input.")

if __name__ == "__main__":
    run_tests()
