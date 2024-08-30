import asyncio
from playwright.async_api import async_playwright, Page
from playwright.async_api._generated import BrowserType
import time

from testutils import *

# FIX: Need openai key for testing in localhost???

async def test_chatbox(browser: BrowserType, role: str):
    browser = await browser.launch()
    page = await access_website(browser, role)
    await access_page(page, '')

    


async def main():
    async with async_playwright() as playwright:
        await test_chatbox(playwright.firefox, 'developer')

if __name__ == "__main__":
    asyncio.run()
