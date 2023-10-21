class LoginPage:
    def __init__(self, page):
        self.page = page
        self.login_input = page.locator("#login_field")
        self.pass_input = page.locator("#password")

    def navigate(self, token):
        self.page.goto("https://github.com/login")
        self.page.set_extra_http_headers({"Authorization": f"Bearer {token}"})

    def login(self, email, password):
        self.login_input.fill(email)
        self.pass_input.fill(password)
        self.pass_input.press("Enter")
