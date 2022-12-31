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
        #cursor.execute('''CREATE TABLE messages (id INTEGER PRIMARY KEY, sent_by TEXT, message TEXT, created_at DATETIME DEFAULT(STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW')))''')
        cursor.execute('''CREATE TABLE messages (id INTEGER PRIMARY KEY, sent_by TEXT, message TEXT, created_at TIMESTAMP''')
        conn.commit()
        l.warning("Messages table created!")

def drop():
    connect()

    l.warning("Deleting everything from messages!")
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
        l.warning("Auth table created!")

def drop_auth():
    connect()

    l.warning("Deleting everything from auth!")
    cursor.execute(''' DELETE FROM auth ''')
    conn.commit()

def init_invites():
    connect()

    cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='invites' ''')
    if cursor.fetchone()[0]==1: 
        l.warning("Invites table exists!")
    else:
        l.warning("Invites table does not exist, creating now...")
        cursor.execute('''CREATE TABLE invites (created_by TEXT, invite TEXT, created_at DATETIME DEFAULT CURRENT_TIMESTAMP, expires TIMESTAMP)''')
        conn.commit()
        l.warning("Invites table created!")

def drop_invites():
    connect()

    l.warning("Deleting everything from invites!")
    cursor.execute(''' DELETE FROM invites ''')
    conn.commit()