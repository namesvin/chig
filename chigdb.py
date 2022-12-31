import sqlite3, logging as l

def connect():
    global conn
    global cursor
    conn = sqlite3.connect('chig.db', check_same_thread=False)
    cursor = conn.cursor()

def init():
    connect()

    cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='messages' ''')
    if cursor.fetchone()[0]==1: 
        l.warning("Table exists!")
    else:
        l.warning("Table does not exist, creating now...")
        cursor.execute('''CREATE TABLE messages (id INTEGER PRIMARY KEY, sent_by TEXT, message TEXT, created_at DATETIME DEFAULT CURRENT_TIMESTAMP)''')
        conn.commit()
        l.warning("Table created!")

def drop():
    l.warning("Deleting everything!")
    cursor.execute(''' DELETE FROM messages ''')
    conn.commit()

def init_auth():
    connect()

    cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='auth' ''')
    if cursor.fetchone()[0]==1: 
        l.warning("Auth table exists!")
    else:
        l.warning("Auth table does not exist, creating now...")
        cursor.execute('''CREATE TABLE auth (username TEXT, password TEXT, created_at DATETIME DEFAULT CURRENT_TIMESTAMP)''')
        conn.commit()
        l.warning("Table created!")

def drop_auth():
    l.warning("Deleting everything!")
    cursor.execute(''' DELETE FROM auth ''')
    conn.commit()
