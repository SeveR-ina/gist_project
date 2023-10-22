class GistCreatePage:
    def __init__(self, page):
        self.page = page
        self.description_input = page.locator("[name='gist[description]']")
        self.code_input = page.locator('pre.CodeMirror-line')
        self.private_gist_button = page.locator('button:has-text("Create secret gist")')
        self.type_of_gist = page.locator('summary[aria-label="Select a type of pull request"]')
        self.create_public_gist = page.locator('.select-menu-item:has-text("Create public gist")')

    def navigate(self):
        self.page.goto("https://gist.github.com/")

    def fill_form(self, description):
        self.description_input.fill(description)
        self.code_input.click()
        self.code_input.focus()
        self.code_input.fill(description)

    def submit_form(self, is_public):
        if is_public:
            self.type_of_gist.click()
            create_public_gist_visible = self.create_public_gist.is_visible()
            if create_public_gist_visible:
                self.create_public_gist.click()
        else:
            self.private_gist_button.click()
