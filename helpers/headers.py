def get_headers_for_auth_user(token):
    return {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def get_headers():
    return {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }


def get_bad_headers():
    return {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2024-11-28"
    }
