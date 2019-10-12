import sqlite3
import argparse
from datetime import datetime, timedelta

from maps.config import *


def init_db(conn):
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS calls (
    id INTEGER PRIMARY KEY,
    datetime DATETIME,
    lat FLOAT,
    lon FLOAT,
    city TEXT,
    call_type TEXT,
    address TEXT,
    UNIQUE(datetime,lat,lon,call_type)
    );''')
    conn.commit()


def drop_db(conn):
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS calls')
    conn.commit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command')
    parser.add_argument('params', metavar='N', type=int, nargs='*', help='')
    args = parser.parse_args()

    conn = sqlite3.connect(DB_PATH)

    if args.command == "refresh":
        drop_db(conn)
        init_db(conn)
    elif args.command == "scrape":
        from maps.scrape import fetch_data
        days = args.params[0]
        fetch_data(days)
