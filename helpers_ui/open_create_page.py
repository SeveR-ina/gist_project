from playwright.sync_api import sync_playwright

from helpers_ui.login import login
from helpers_ui.models.gist_create_page import GistCreatePage


# async def open_create_gist_page(page, email, password):
#     async with sync_playwright():
#         login_page = await login(page, email, password)
#         gist_create_page = GistCreatePage(login_page)
#         await gist_create_page.navigate()
#         return gist_create_page

def open_create_gist_page(page, email, password):
    with sync_playwright():
        login_page = login(page, email, password)
        gist_create_page = GistCreatePage(login_page)
        gist_create_page.navigate()
        return gist_create_page

