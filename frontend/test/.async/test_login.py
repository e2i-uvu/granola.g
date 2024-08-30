import asyncio
from playwright.async_api import async_playwright, Page#, _generated.BrowserType, Playwright
from playwright.async_api._generated import BrowserType
import time
import pytest
import pytest_asyncio
from testutils import *

async def test_roles(browser: BrowserType, role: str) -> None:
    browser = await browser.launch()
    page = await access_website(browser, role)
#    page = await browser.new_page()
#    await page.goto('localhost:8080')
#    #assert page.title() == ""
#    time.sleep(1)
#    await page.get_by_test_id("stSelectbox").locator("div").filter(has_text="None").nth(2).click()
#    await page.get_by_label("Selected None. Choose your").fill("")
#    await page.get_by_role("option", name=role).click()
#    time.sleep(1)
#    if role in ('developer', 'admin'):
#        await fill_password(page, role)
    await page.screenshot(path=f'screenshots/test_role_{role}.png')
    await browser.close()

async def main() -> None:
    async with async_playwright() as playwright:
        await test_roles(playwright.firefox, "developer")
        # FIX: Admin role is not set up properly. 
        # .streamlit/.secrets.toml includes an "administrator" role while the frontend includes an "admin" selection.
        await test_roles(playwright.firefox, "admin")
        await test_roles(playwright.firefox, "student")
        #await test_roles(playwright.chromium)

if __name__ == "__main__":
    asyncio.run(main())
