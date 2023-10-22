import requests


def get_gist(gist_id, token):
    gist_url = f"https://api.github.com/gists/{gist_id}"
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Authorization": f"Bearer {token}",
    }

    response = requests.get(gist_url, headers=headers)

    if response.status_code == 200:
        gist_data = response.json()
        print(f"Gist {gist_id} retrieved successfully.")
        return gist_data
    else:
        print(f"Failed to retrieve gist {gist_id}. Status code: {response.status_code}")
        return None
