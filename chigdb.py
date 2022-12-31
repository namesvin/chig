import sqlite3, logging as l

def init():
    global conn
    global cursor
    conn = sqlite3.connect('chat.db', check_same_thread=False)
    cursor = conn.cursor()

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
    global aconn
    global acursor
    aconn = sqlite3.connect('auth.db', check_same_thread=False)
    acursor = conn.cursor()

    acursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='auth' ''')
    if acursor.fetchone()[0]==1: 
        l.warning("Table exists!")
    else:
        l.warning("Table does not exist, creating now...")
        acursor.execute('''CREATE TABLE auth (username TEXT, password TEXT, created_at DATETIME DEFAULT CURRENT_TIMESTAMP)''')
        aconn.commit()
        l.warning("Table created!")

def drop():
    l.warning("Deleting everything!")
    acursor.execute(''' DELETE FROM auth ''')
    aconn.commit()
