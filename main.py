import json
import requests
import os

LOGIN=os.environ.get("LOGIN", default="")
PASSWORD=os.environ.get("PASSWORD", default="")
API_KEY=os.environ.get("API_KEY", default="")

if __name__ == "__main__":
    r = requests.post("https://rebrickable.com/api/v3/users/_token/",
                      headers={"Authorization": f"key {API_KEY}"},
                      data={"username": LOGIN, "password": PASSWORD})
    if r.status_code != 200:
        exit(1)

    user_token = r.json()["user_token"]
    r = requests.get(f"https://rebrickable.com/api/v3/users/{user_token}/setlists/",
                     headers={"Authorization": f"key {API_KEY}"})
    if r.status_code != 200:
        exit(1)

    resp = r.json()
    for i in range(resp["count"]):
        list_id = resp["results"][i]["id"]
        r = requests.get(f"https://rebrickable.com/api/v3/users/{user_token}/setlists/{list_id}/sets",
                        headers={"Authorization": f"key {API_KEY}"},
                        params={"page": 1, "page_size": 1000})
        if r.status_code != 200:
            exit(1)

        resp = r.json()
        if resp["next"] != None:
            exit(1)

        sets = resp["results"]
        print(json.dumps(sets, indent=2, ensure_ascii=True))
