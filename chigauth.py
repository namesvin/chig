import hashlib, logging as l, chigdb as db

def hashpass(password):
    return hashlib.sha256(password.encode()).hexdigest()

def usernamefree(username):
    cursor = db.conn.cursor()
    cursor.execute('''SELECT EXISTS(SELECT 1 FROM auth WHERE username='%s')''' % username)
    if cursor.fetchone()[0] != 0:
        l.warning("Username " + username + " already taken!")
        return False
    else:
        l.warning("Username " + username + " free!")
        return True

def register(username, password):
    if usernamefree(username):
        if username and password:
            l.warning("Registering user " + username)
            cursor = db.conn.cursor()
            cursor.execute('''INSERT INTO auth (username, password) VALUES (?, ?)''', (username, hashpass(password)))
            db.conn.commit()
            return True
        else:
            l.warning("Missing something!")
            return False
    else:
        l.warning("User " + username + " already exists!")
        return False

def authenticate(username, password):
    cursor = db.conn.cursor()
    cursor.execute('''SELECT username, password FROM auth''')
    rows = cursor.fetchall()
    for row in rows:
        if row[0] == username:
            passworddb = row[1]
            if hashpass(password) == passworddb:
                l.warning("User " + username + " authenticated!")
                return True
    l.warning("User " + username + " failed to authenticate!")
    return False

def deleteuser(username):
    cursor = db.conn.cursor()
    l.warning("Deleting user " + username)
    cursor.execute('DELETE FROM auth WHERE username = ?', (username,))
    return True
