from playwright.sync_api import sync_playwright
from helpers_ui.models.login_page import LoginPage


# async def login(page, email, password):
#     async with sync_playwright():
#         login_page = LoginPage(page)
#         await login_page.navigate()
#         await login_page.login(email, password)
#         return login_page

def login(page, email, password):
    with sync_playwright():
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.login(email, password)
        return login_page
