from playwright.sync_api import sync_playwright

from helpers_ui.login import login
from helpers_ui.models.gist_create_page import GistCreatePage


def open_create_gist_page(page, email, password, token):
    with sync_playwright():
        login_page = login(page, email, password, token)
        gist_create_page = GistCreatePage(login_page)
        gist_create_page.navigate()
        return gist_create_page
