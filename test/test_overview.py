from playwright.sync_api import sync_playwright
from playwright.sync_api._generated import BrowserType
import time
from testutils import *
import pytest

def _test_employee(browser: BrowserType, credentials: dict[str,str], option: str) -> bool:
    browser = browser.launch()
    page = access_website(browser, credentials)
    page.get_by_role("link", name="groups Overview").click()
    page.get_by_test_id("stSelectbox").locator("div").filter(has_text="Select an option").nth(2).click()
    page.get_by_text(option).click()
    return True

def test_overview() -> None:
    credentials = {"id": "11006941", "password": "arch"}
    with sync_playwright() as playwright:
        _test_employee(playwright.firefox, credentials, "hire")

#if __name__ == "__main__":
    #test_employees()
