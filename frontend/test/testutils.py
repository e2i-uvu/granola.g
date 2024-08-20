import asyncio
from playwright.async_api import async_playwright, Page
from playwright.async_api._generated import BrowserType
import time

async def fill_password(page: Page, role: str) -> None:
    if role not in ('developer', 'admin'):
        raise ValueError
    else:
        await page.get_by_label('Password', exact=True).click()
        if role == 'developer':
            await page.get_by_label('Password', exact=True).fill('arch')
        else:
            await page.get_by_label('Password', exact=True).fill('innovation')
        await page.get_by_label('Password', exact=True).press("Enter")
        time.sleep(1)

async def access_website(browser: BrowserType, role: str) -> Page:
    page = await browser.new_page()
    await page.goto('localhost:8080')
    time.sleep(1)

    await page.get_by_test_id("stSelectbox").locator("div").filter(has_text="None").nth(2).click()
    await page.get_by_label("Selected None. Choose your").fill("")
    await page.get_by_role("option", name=role).click()
    time.sleep(1)

    if role in ('developer', 'admin'):
        await fill_password(page, role)

    return page

async def access_page(page: Page, page_title: str) -> None:
    #if page
    #_ = ""
    #if page.heading.name != page_title:
    await page.get_by_role("link", name=page_title).click()
    #await page.get_by_role("link", name="groups Employees").click()


async def _main():
    async with async_playwright() as p:
        browser = await p.firefox.launch()
        page = await access_website(browser, 'developer')
        #await access_page(page, "reduce_capacity Team Building")
        await page.screenshot(path='screenshots/page.png')
        await browser.close()

if __name__ == "__main__":
    asyncio.run(_main())

