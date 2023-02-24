import argparse
import os
import requests
import sqlite3

LOGIN=os.environ.get("LOGIN", default="")
PASSWORD=os.environ.get("PASSWORD", default="")
API_KEY=os.environ.get("API_KEY", default="")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Store personal rebrickable sets collection into database")
    parser.add_argument('database')
    args = parser.parse_args()

    r = requests.post("https://rebrickable.com/api/v3/users/_token/",
                      headers={"Authorization": f"key {API_KEY}"},
                      data={"username": LOGIN, "password": PASSWORD})
    if r.status_code != 200:
        print(f"Unable to acquire user token, code={r.status_code}")
        exit(1)

    user_token = r.json()["user_token"]
    r = requests.get(f"https://rebrickable.com/api/v3/users/{user_token}/setlists/",
                     headers={"Authorization": f"key {API_KEY}"})
    if r.status_code != 200:
        print(f"Unable to acquire set lists, code={r.status_code}")
        exit(1)

    resp = r.json()

    try:
        with sqlite3.connect(args.database) as con:
            cur = con.cursor()
            cur.execute('''
                create table if not exists set_lists (
                    setlist varchar(16),
                    set_num varchar(16),
                    quantity smallint
                );
            ''')
            cur.execute('''
                delete from set_lists;
            ''')

            for i in range(resp["count"]):
                list_id = resp["results"][i]["id"]
                r2 = requests.get(f"https://rebrickable.com/api/v3/users/{user_token}/setlists/{list_id}/sets",
                                headers={"Authorization": f"key {API_KEY}"},
                                params={"page": 1, "page_size": 1000})
                if r2.status_code != 200:
                    print(f"Unable to acquire sets for list {list_id}, code={r2.status_code}")
                    exit(1)

                resp2 = r2.json()
                if resp2["next"] != None:
                    print(f"Too many sets in {list_id}. No pagination implemented")
                    exit(1)

                for set in resp2["results"]:
                    cur.execute('''
                        insert into set_lists values (?, ?, ?);
                    ''', (set["list_id"], set["set"]["set_num"], set["quantity"]))
                
                con.commit()
    except sqlite3.Error as e:
        print(e)