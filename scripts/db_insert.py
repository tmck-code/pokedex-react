#!/usr/bin/env python3

import os, sys
from collections import namedtuple
import sqlite3

CardSet = namedtuple('CardSet', ['code', 'name', 'description'])
Card = namedtuple('Card', ['number_in_set', 'title', 'image_url', 'description', 'card_set_id'])

def truncate_tables(conn):
    print('truncating')
    cur = conn.cursor()
    cur.execute('DELETE FROM cards;')
    cur.execute('DELETE FROM card_sets;')
    conn.commit()

def insert_card_set(conn, card_set: CardSet):
    print('inserting', card_set)
    sql = 'INSERT INTO card_sets(code, name, description) VALUES(?,?,?)'
    cur = conn.cursor()
    cur.execute(sql, card_set)
    conn.commit()
    return cur.lastrowid

def insert_card(conn, card: Card):
    print('inserting', card)
    sql = 'INSERT INTO cards(number_in_set, title, image_url, description, card_set_code) VALUES(?,?,?,?,?)'
    cur = conn.cursor()
    cur.execute(sql, card)
    conn.commit()
    return cur.lastrowid

def insert_cards_from_dir(dirpath, conn):
    code = os.path.split(os.path.abspath(dirpath))[-1]
    print('inserting cards for set', code, 'from', dirpath)
    insert_card_set(conn, CardSet(code, code, ''))

    for rootdir, dirs, files in os.walk(dirpath):
        for i, filename in enumerate(files):
            if not filename.endswith('.png'):
                continue

            base = os.path.splitext(filename)[0]
            number_in_set, name = base.split('_')
            image_url = os.path.join(rootdir, filename)

            card = Card(
                int(number_in_set), name.replace('_', ' '), image_url, '', code
            )
            insert_card(conn, card)

def run(dirpath):
    conn = sqlite3.connect('./db/main.db')
    truncate_tables(conn)
    for rootdir, dirs, files in os.walk(dirpath):
        for dirname in dirs:
            print('inserting cards from', os.path.join(rootdir, dirname))
            insert_cards_from_dir(os.path.join(rootdir, dirname), conn)
    conn.commit()


if __name__ == '__main__':
    run(sys.argv[1])
