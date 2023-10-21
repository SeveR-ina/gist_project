class CreatedGistPage:
    def __init__(self, page, text):
        self.page = page
        self.textarea = page.locator('textarea:has-text("{{text}}")'.format(text=text))
        self.title = page.locator('div[itemprop="about"]:has-text("{{text}}")'.format(text=text))
