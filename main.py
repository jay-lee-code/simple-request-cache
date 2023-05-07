import requests
import time
import argparse
import sqlite3
from flask import Flask, abort

app = Flask(__name__)

con = sqlite3.connect("cache.db")
cur = con.cursor()

port = 5123
# described in seconds:
max_elapsed = 60 * 60 * 24 * 30


def create_table():
    cur.execute(
        "CREATE TABLE IF NOT EXISTS web_requests (url TEXT PRIMARY KEY, data BLOB, timestamp INTEGER);"
    )


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
        action="store_false",
        help="disables hot reloading and debug messages",
        required=False
    )

    args = parser.parse_args()

    if args.port:
        port = args.port

    if args.maxelapsed:
        max_elapsed = args.maxelapsed

    create_table()
    app.run(port=port, debug=args.nodebug)
