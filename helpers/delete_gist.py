import requests


def delete_gist(gist_id, token):
    delete_url = f"https://api.github.com/gists/{gist_id}"
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Authorization": f"Bearer {token}",
    }

    response = requests.delete(delete_url, headers=headers)

    if response.status_code == 204:
        print(f"Gist {gist_id} deleted successfully via api.")
    else:
        print(f"Failed to delete gist {gist_id}. Status code: {response.status_code}")
