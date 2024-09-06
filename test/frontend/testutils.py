from playwright.sync_api import sync_playwright, Page
from playwright.sync_api._generated import BrowserType
from time import time, sleep
from collections.abc import Callable

def timeit(function: Callable) -> Callable:
    def _timeit(*args, **kwargs):
        start_time = time()
        output = function(args[0],args[1])
        print("Runtime: ", time() - start_time)
        return output
    return _timeit


# HACK: Deprecated
#def fill_password(page: Page, role: str) -> None:
#    if role not in ('developer', 'admin'):
#        raise ValueError
#    else:
#        page.get_by_label('Password', exact=True).click()
#        if role == 'developer':
#            page.get_by_label('Password', exact=True).fill('arch')
#        else:
#            page.get_by_label('Password', exact=True).fill('innovation')
#        page.get_by_label('Password', exact=True).press("Enter")
#        sleep(1)

def access_website(browser: BrowserType, credentials: dict[str,str]) -> Page:
    page = browser.new_page()
    # HACK: This address might not work in the GitHub Actions Workflow.
    # Change if necessary
    address = 'localhost:8080' 
    page.goto(address)
    #sleep(0.5)

    #page.get_by_test_id("stSelectbox").locator("div").filter(has_text="None").nth(2).click()
    inputID = page.get_by_placeholder("Username / UVID", exact = True)
    inputID.click()
    inputID.fill(credentials["id"])
    inputID.press("Enter")

    inputPassword = page.get_by_label("Password", exact = True)
    inputPassword.click()
    inputPassword.fill(credentials["password"])
    inputPassword.press("Enter") 

    return page

def access_page(page: Page, page_title: str) -> None:
    #if page
    #_ = ""
    #if page.heading.name != page_title:
    page.get_by_role("link", name=page_title).click()
    #await page.get_by_role("link", name="groups Employees").click()



