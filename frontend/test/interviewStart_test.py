import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os

#import pytest
import logging
#import time

load_dotenv()
backend = os.getenv("BACKEND")
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
standard_headers = {"Content-Type": "application/json"}

logger = logging.getLogger("InterviewStartHandler_Test")

# TODO: Change parameter from string to dictionary/json

#def test_interviewStart( data: dict[str,str] #data: str
def make_interviewStart_request(data: dict[str,str]) -> int:
    response = requests.post(
        backend + "interviewStart", #json = {"uvuid": data},
        json = data,
        headers = standard_headers
    )
    return response.status_code

def test_interviewStart_request(data: dict[str,str], expected_status_code: int, case: str):
    if make_interviewStart_request(data) == expected_status_code:
        logger.info("Sucessfully fails " + case)#ok_message)
    else:
        logger.warning("Does not fail " + case)#error_message)

if __name__ == "__main__":
    logging.basicConfig(filename = "test.log", level = logging.INFO)

    # Test interviewStartHandler
    # 1. None datatype
    # Expected output: 406 - Fail
    test_interviewStart_request(None, 406, "None value.")#, "None values.")

    # . Non JSON argument
    # Expected output: 406 - Fail
    test_interviewStart_request(1000003, 406, "non-JSON value.")

    # FIX: The following test cases don't work

    # . JSON argument, empty
    # Expected output: 406 - Fail
    # test_interviewStart_request({}, 406, "Empty JSON.")

    # . JSON argument, key is in wrong datatype
    # Expected output: 406 - Fail
    #test_interviewStart_request({1000003: "11006941"}, 406, "JSON with wrong key datatype")

    # .JSON argument, key is string but wrong
    # Expected output: 406 - Fail
    #test_interviewStart_request({"lore ipsum": "11006941"}, 406, "JSON with wrong key")

    # 2. JSON argument, "uvuid" value is in wrong datatype
    # Expected output: 406 - Fail
    #test_interviewStart_request({"uvuid": 35}, 406, "JSON with wrong value datatypes.")

    # 3. Valid datatype: Non-numeric string
    # Expected output: 406 - Fail
    test_interviewStart_request({"uvuid": "lore ipsum"}, 406, "JSON with non-numeric value.")

    # 4. Valid datatype: numeric string
    # Expected output: 200 - OK
    if make_interviewStart_request({"uvuid": "11006941"}) == 200:
        logger.info("InterviewStartHandler succesfully manages ")
    else:
        logger.error("InterviewStartHandler fails to manage valid input.")

