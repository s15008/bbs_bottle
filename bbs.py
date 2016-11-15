# -*- coding: utf-8 -*-

from bottle import run, route, template, request
import sqlite3
import time

DB_NAME = './db/bbs.db'
TABLE_NAME = 'responses'
DEFAULT_NAME = '名無しの便座くん'

@route('/')
def bbs():
    return template('./template/bbs.tpl', reses=get_reses())

@route('/', method='post')
def submit_res():
    message = request.forms.getunicode('message')
    name = request.forms.getunicode('name') or DEFAULT_NAME
    created_date = time.time()

    # 本文が空だとDBに書き込まない
    if not message: return template('./template/bbs.tpl', reses=get_reses())

    conn = sqlite3.connect(DB_NAME)
    try:
        query = 'INSERT INTO {}(message, name, created_date) VALUES(?, ?, ?)'.format(TABLE_NAME)
        conn.execute(query, (message, name, created_date))
        conn.commit()
    finally:
        conn.close()

    return template('./template/bbs.tpl', reses=get_reses())

def get_reses():
    reses = []

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = dict_factory
    c = conn.cursor()
    try:
        c.execute('SELECT * FROM {}'.format(TABLE_NAME))
        reses = c.fetchall()
    finally:
        conn.close()

    for res in reses:
        res['created_date'] = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(res['created_date']))

    return reses

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

run(debug=True)
