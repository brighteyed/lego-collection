import requests


API_BASE = "https://rebrickable.com/api/v3"


def _auth_header(api_key):
    return {"Authorization": f"key {api_key}"}


def get_user_token(api_key, username, password):
    resp = requests.post(
        f"{API_BASE}/users/_token/",
        headers=_auth_header(api_key),
        data={"username": username, "password": password},
        timeout=30,
    )
    if resp.status_code != 200:
        raise RuntimeError(
            f"Authentication failed (HTTP {resp.status_code}). "
            f"Check your Rebrickable credentials."
        )
    return resp.json()["user_token"]


def get_set_lists(user_token, api_key):
    results = []
    url = f"{API_BASE}/users/{user_token}/setlists/"
    while url:
        resp = requests.get(
            url, headers=_auth_header(api_key), params={"page_size": 100}, timeout=30
        )
        if resp.status_code != 200:
            raise RuntimeError(
                f"Failed to fetch set lists (HTTP {resp.status_code})"
            )
        data = resp.json()
        results.extend(data["results"])
        url = data.get("next")
    return results


def get_list_sets(user_token, list_id, api_key):
    results = []
    url = f"{API_BASE}/users/{user_token}/setlists/{list_id}/sets/"
    while url:
        resp = requests.get(
            url,
            headers=_auth_header(api_key),
            params={"page_size": 500},
            timeout=30,
        )
        if resp.status_code != 200:
            raise RuntimeError(
                f"Failed to fetch sets for list {list_id} (HTTP {resp.status_code})"
            )
        data = resp.json()
        results.extend(data["results"])
        url = data.get("next")
    return results