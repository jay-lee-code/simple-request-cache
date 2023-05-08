import requests
import time
import json
import argparse
import sqlite3
from flask import Flask, abort

app = Flask(__name__)

con = sqlite3.connect("cache.db", check_same_thread=False)
cur = con.cursor()

port = 5123
# described in seconds:
max_elapsed = 60 * 60 * 24 * 30
debug = True
baseurl = ""


def create_table():
    cur.execute(
        "CREATE TABLE IF NOT EXISTS web_requests (url TEXT PRIMARY KEY, data TEXT, timestamp INTEGER);"
    )


def get_cache(url):
    res = cur.execute('SELECT * FROM web_requests WHERE "url" = ?;', (url,))
    data = res.fetchone()

    if data is None or (time.time() - data[2] > max_elapsed):
        return None

    return data[1:]


def replace_cache(url, data, timestamp):
    cur.execute(
        "REPLACE INTO web_requests(url, data, timestamp) VALUES(?, ?, ?);",
        (url, data, timestamp)
    )
    con.commit()
    pass


# catch all routes, source: https://stackoverflow.com/a/45777812
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    path = baseurl + path
    # ignore extremely short strings like favicon
    if len(path) < 12:
        return ''

    print(path)

    cached_req = get_cache(path)
    if cached_req:
        if debug:
            print("Using cached request data.")
        return json.loads(cached_req[0])
    elif debug:
        print("No valid cached data found, making request.")

    r = requests.get(path)

    if r.status_code > 299:
        abort(r.status_code)

    replace_cache(path, json.dumps(r.json()), int(time.time()))

    return r.json()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Start simple request cache service.'
    )
    parser.add_argument(
        "--port", help="port to use",
        type=int,
        required=False
    )
    parser.add_argument(
        "--maxelapsed",
        help="max time (integer seconds) before invalidating cache",
        type=int,
        required=False
    )
    parser.add_argument(
        "--baseurl",
        help="base url prefix for all requests",
        required=False
    )
    parser.add_argument(
        "--nodebug",
        action="store_true",
        help="disables hot reloading and debug messages",
        required=False
    )

    args = parser.parse_args()

    if args.port:
        port = args.port

    if args.maxelapsed:
        max_elapsed = args.maxelapsed

    if args.baseurl:
        baseurl += args.baseurl

    debug = not args.nodebug

    create_table()
    app.run(port=port, debug=debug)
