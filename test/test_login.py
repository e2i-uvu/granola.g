#import asyncio
from playwright.sync_api import sync_playwright, Page#, _generated.BrowserType, Playwright
from playwright.sync_api._generated import BrowserType
import time
from testutils import *
from openai import OpenAIError
import pytest

#@timeit
def _test_login(browser: BrowserType, credentials: dict[str, str]) -> bool:
    try:
        browser = browser.launch()
        page = access_website(browser, credentials)
        #page.screenshot(path=f'screenshots/test_login.png')
        browser.close()
    finally:
        return True


def test_login() -> None:
    with sync_playwright() as playwright:
        # TODO: Change the credentials
        credentials = {"id" : "11006941", "password": "arch"}
        login_result = _test_login(playwright.firefox, credentials)
        assert login_result
        if login_result:
            print("Login working")

if __name__ == "__main__":
    test_login()
    #pytest.main()
