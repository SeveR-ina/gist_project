class GistUserNamePage:
    def __init__(self, page, gist_id, username):
        self.page = page
        self.link_to_user_gist = page.locator(".css-truncate-target")

    def navigate(self, username):
        self.page.goto("https://gist.github.com/{username}".format(username=username))
