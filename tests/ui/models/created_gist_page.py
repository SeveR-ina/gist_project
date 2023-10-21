class CreatedGistPage:
    def __init__(self, page):
        self.page = page
        # self.textarea = page.locator('textarea:has-text("{{text}}")'.format(text=text))
        # self.title = page.locator('div[itemprop="about"]:has-text("{{text}}")'.format(text=text))

    def navigate(self, username, gist_id):
        self.page.goto(f"https://gist.github.com/{username}/{gist_id}")
