import sqlite3
import os

db_file = 'data.db'

def create_table():
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS checked_comments
                 (issue_key TEXT PRIMARY KEY, last_checked TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS checked_statuses
                 (issue_key TEXT PRIMARY KEY, last_status TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS checked_tasks
                     (issue_key TEXT PRIMARY KEY, last_status TEXT)''')
    conn.commit()
    conn.close()

#Методы для записи комментариев
def load_checked_comments():
    if not os.path.exists(db_file):
        create_table()
    try:
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        c.execute('SELECT * FROM checked_comments')
        rows = c.fetchall()
        checked_comments = {row[0]: row[1] for row in rows}
        conn.close()
    except sqlite3.Error:
        checked_comments = {}
    return checked_comments

def save_checked_comments(checked_comments):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute('DELETE FROM checked_comments')
    for issue_key, last_checked_time in checked_comments.items():
        c.execute('INSERT INTO checked_comments VALUES (?, ?)', (issue_key, last_checked_time))
    conn.commit()
    conn.close()

#Методы для записи статусов
def load_checked_statuses():
    if not os.path.exists(db_file):
        create_table()
    try:
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        c.execute('SELECT * FROM checked_statuses')
        rows = c.fetchall()
        checked_statuses = {row[0]: row[1] for row in rows}
        conn.close()
    except sqlite3.Error:
        checked_statuses = {}
    return checked_statuses

def save_checked_statuses(checked_statuses):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute('DELETE FROM checked_statuses')
    for issue_key, last_status in checked_statuses.items():
        c.execute('INSERT INTO checked_statuses VALUES (?, ?)', (issue_key, last_status))
    conn.commit()
    conn.close()

def update_checked_statuses(issue_key, new_status):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute('INSERT OR REPLACE INTO checked_statuses VALUES (?, ?)', (issue_key, new_status))
    conn.commit()
    conn.close()

def load_checked_assigned_tasks():
    if not os.path.exists(db_file):
        create_table()
    try:
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        c.execute('SELECT * FROM checked_tasks')
        rows = c.fetchall()
        checked_assigned_tasks = {row[0]: row[1] for row in rows}
        conn.close()
    except sqlite3.Error:
        checked_assigned_tasks = {}
    return checked_assigned_tasks

def save_checked_assigned_tasks(checked_assigned_tasks):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute('DELETE FROM checked_tasks')
    for issue_key, last_checked_time in checked_assigned_tasks.items():
        c.execute('INSERT INTO checked_tasks VALUES (?, ?)', (issue_key, last_checked_time))
    conn.commit()
    conn.close()

def update_checked_assigned_tasks(issue_key, new_last_checked_time):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute('INSERT OR REPLACE INTO checked_assigned_tasks VALUES (?, ?)', (issue_key, new_last_checked_time))
    conn.commit()
    conn.close()