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
stadard_headers = {"Content-Type": "application/json"}

logger = logging.getLogger(__name__)

# TODO: Change parameter from string to dictionary/json
def test_interviewStart(data: str) -> int:
    response = requests.post(
        backend + "interviewStart",
        json = {"uvuid": data},
        headers = standard_headers
    )
    return response.status_code


# TODO: Change parameters from multiple strings to single dictionary/json 
def test_interviewFinish(fkuser: str, cancode: str, enjoyment: str, social: str) -> int:
    post = requests.post(
        backend + "interviewFinish",
        json = {
            "fkuser": fkuser,
            "cancode": cancode,
            "enjoyment": enjoyment,
            "social": social
        },
        headers = standard_headers
    )
    return post.status_code

if __name__ == "__main__":
    logging.basicConfig(filename = test.log, level = logging.INFO)

    # Test interviewStartHandler
    # 1. Insufficient datatype
    # Expected output: 406 - Fail
    if test_interviewStart(None) == 406:
        logger.info("InterviewStartHandler successfully fails None values.")
    # 2. Wrong datatype
    # Expected output: 406 - Fail
    if test_interviewStart(35) == 406:
        logger.info("InterviewStartHandler successfully fails no string values.")
    else:
        error = True
        logger.warning("InterviewStartHandler does not fail non string values.")

    # 3. Valid datatype: Non-numeric string
    # Expected output: 406 - Fail
    if test_interviewStart("lore ipsum") == 406:
        loger.info("InterviewStartHandler successfully fails non-numeric string values.")
    else:
        logger.warning("InterviewStartHandler does not fail non-numeric string values.")
        error = True

    # 4. Valid datatype: numeric string
    # Expected output: 200 - OK
    if test_interviewStart("11006941") == 200:
        logger.info("InterviewStartHandler andler succesfully manages ")
    else:
        logger.error("InterviewStartHandler fails to manage valid input.")

    # Test interviewFinishHandler
    # 1. Insufficient Data
    # Expected output: 406 - Fail
    if test_interviewFinish(None, None, None, None) == 406:

