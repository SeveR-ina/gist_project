class GistCreatePage:
    def __init__(self, page):
        self.page = page
        # self.pass_input = page.locator("#password")
        self.discription_input = page.locator("[name='gist[description]']")

    def navigate(self):
        self.page.goto("https://gist.github.com/")

    def fill_form(self, description):
        self.discription_input.fill(description)
