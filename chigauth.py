import hashlib, logging as l, chigdb as db

global users
users = {}

def init():
    db.init_auth()
    l.warning("Creating admin user!")
    users["admin"] = "Vince123"

def hashpass(password):
    return hashlib.sha256(password.encode()).hexdigest()

def usernamefree(username):
    cursor = db.conn.cursor()
    cursor.execute('''SELECT EXISTS(SELECT 1 FROM auth WHERE username='%s')''' % username)
    if cursor.fetchone()[0] != 0:
        return False
    else:
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
    cursor.execute('''SELECT username, password FROM auth ORDER BY created_at DESC LIMIT 100''')
    rows = cursor.fetchall()
    for row in rows:
        if row[0] == username:
            passworddb = row[1]
            if hashpass(password) == passworddb:
                l.warning("User authenticated!")
                return True
    return False

init()
register("test", "123")
print(usernamefree("test"))
print(authenticate("test", "123"))