import requests


def create_gist(data, token):
    create_url = "https://api.github.com/gists"
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Authorization": f"Bearer {token}",
    }

    response = requests.post(create_url, headers=headers, json=data)

    if response.status_code == 201:
        gist_id = response.json().get('id')
        print(f"Gist {gist_id} created successfully via api.")
        return gist_id
    else:
        print(f"Failed to create a gist. Status code: {response.status_code}")
        return None
