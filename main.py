import requests
import time
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

def create_table():
    cur.execute(
        "CREATE TABLE IF NOT EXISTS web_requests (url TEXT PRIMARY KEY, data BLOB, timestamp INTEGER);"
    )


def get_cache(url):
    res = cur.execute("SELECT ? FROM web_requests;", (url,))
    data = res.fetchone()

    # add timestamp check
    if data is None:
        return None

    # todo fix to return data
    return res.fetchone()


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
    if path == 'favicon.ico':
        return ''
    
    print(path)

    cached_req = get_cache(path)
    if cached_req:
        if debug:
            print("Using cached request data.")

    print(cached_req)

    replace_cache(path, "test", 0)

    return(str(path))

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
    
    debug = not args.nodebug

    create_table()
    app.run(port=port, debug=debug)
