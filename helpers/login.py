from playwright.sync_api import sync_playwright
from helpers.models.login_page import LoginPage


def login(page, email, password, token):
    with sync_playwright():
        login_page = LoginPage(page)
        login_page.navigate_to_login_page(token)
        login_page.login(email, password)
        return login_page
