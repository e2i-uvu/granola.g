#import asyncio
from playwright.sync_api import sync_playwright, Page#, _generated.BrowserType, Playwright
from playwright.sync_api._generated import BrowserType
import time
#import pytest
#import pytest_asyncio
from testutils import *
from openai import OpenAIError
import pytest

#@timeit
def _test_login(browser: BrowserType, credentials: dict[str, str]) -> bool:
    browser = browser.launch()
    page = access_website(browser, credentials)
    #page.screenshot(path=f'screenshots/test_login.png')
    browser.close()
    return True


def test_login() -> None:
    with sync_playwright() as playwright:
        login_result = _test_login(playwright.firefox, {"id" : "11006941", "password": "arch"})
        assert login_result
        if login_result:
            print("Login working")

if __name__ == "__main__":
    pytest.main()
