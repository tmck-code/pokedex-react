#!/usr/bin/env python3

from collections import defaultdict
import os, sys
from collections import namedtuple
from laser_prynter import pp, pbar
import sqlite3


CardSet = namedtuple("CardSet", ["code", "name", "description"])
Card = namedtuple(
    "Card", ["number_in_set", "title", "image_url", "description", "card_set_id"]
)

def init_tables(conn):
    try:
        cur = conn.cursor()
        cur.execute(
            """CREATE TABLE IF NOT EXISTS card_sets (
                code TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT
            );"""
        )
        cur.execute(
            """CREATE TABLE IF NOT EXISTS cards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                number_in_set INTEGER NOT NULL,
                title TEXT NOT NULL,
                image_url TEXT NOT NULL,
                description TEXT,
                card_set_code TEXT NOT NULL,
                FOREIGN KEY (card_set_code) REFERENCES card_sets (code)
            );"""
        )
    except sqlite3.OperationalError as e:
        print("error initializing tables", e)
    finally:
        conn.commit()

def truncate_tables(conn):
    print("truncating")
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM cards;")
        cur.execute("DELETE FROM card_sets;")
    except sqlite3.OperationalError as e:
        print("error truncating tables", e)
    finally:
        conn.commit()

def insert_card_set(conn, card_set: CardSet):
    pp.ppd(
        {"msg": "inserting card set", "card_set": card_set},
        indent=None,
        style="material",
    )
    sql = "INSERT INTO card_sets(code, name, description) VALUES(?,?,?)"
    cur = conn.cursor()
    cur.execute(sql, card_set)
    conn.commit()
    return cur.lastrowid


def insert_card(conn, card: Card):
    pp.ppd(
        {"msg": "inserting card", "card": card},
        indent=None,
        style="material",
    )
    sql = "INSERT INTO cards(number_in_set, title, image_url, description, card_set_code) VALUES(?,?,?,?,?)"
    cur = conn.cursor()
    cur.execute(sql, card)
    conn.commit()
    return cur.lastrowid


def insert_cards_from_dir(dirpath, conn):
    todo = []
    seen_codes = set()
    for rootdir, _, files in os.walk(dirpath):
        for _, filename in enumerate(files):
            code = os.path.basename(rootdir)
            if code not in seen_codes:
                insert_card_set(conn, CardSet(code, code, ""))
                seen_codes.add(code)
            todo.append((code, rootdir, filename))

    with pbar.PBar(total=len(todo)) as bar:
        for code, rootdir, filename in todo:
            if not filename.endswith(".png"):
                bar.update(1)
                continue

            number_in_set, name = filename.split("_", 1)
            image_url = os.path.join(rootdir, filename)

            if not number_in_set.isdigit():
                pp.ppd(
                    {"msg": "skipping card with invalid number", "filename": filename},
                    indent=None,
                    style="fruity",
                )
                bar.update(1)
                continue

            insert_card(
                conn,
                Card(
                    number_in_set=int(number_in_set),
                    title=os.path.basename(name).replace("_", " "),
                    image_url=image_url,
                    description="",
                    card_set_id=code,
                ),
            )
            bar.update(1)


def run(dirpath):
    conn = sqlite3.connect("./db/main.db")
    init_tables(conn)
    truncate_tables(conn)
    pp.ppd({"info": "inserting cards from", "dirpath": dirpath}, indent=None)
    insert_cards_from_dir(dirpath, conn)
    conn.commit()


if __name__ == "__main__":
    run(sys.argv[1])
