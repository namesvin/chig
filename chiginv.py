import chigdb as db, logging as l, datetime, hashlib, random

def createinvite(username):
    invbase = username + str(random.random()**random.random()) + username
    invite = hashlib.sha256(invbase.encode()).hexdigest()
    expires = datetime.date.today() + datetime.timedelta(days=7)
    cursor = db.conn.cursor()
    cursor.execute('''INSERT INTO invites (created_by, invite, expires) VALUES (?, ?, ?)''', (username, invite, expires))
    db.conn.commit()
    return invite

def checkinvite(invite):
    cursor = db.conn.cursor()
    cursor.execute('''SELECT invite FROM invites''')
    rows = cursor.fetchall()
    for row in rows:
        if row[0] == invite:
            return True
    return False

def deleteinvite(invite):
    cursor = db.conn.cursor()
    cursor.execute('DELETE FROM invites WHERE invite = ?', (invite,))
    db.conn.commit()
    return True

def checkexpire(invite):
    cursor = db.conn.cursor()
    cursor.execute('''SELECT invite, expires FROM invites''')
    rows = cursor.fetchall()
    for row in rows:
        if datetime.datetime.strptime(row[1], '%Y-%m-%d').date() > datetime.date.today() :
            deleteinvite(invite)
            return True
    return False

def getinvs(username):
    cursor = db.conn.cursor()
    cursor.execute("SELECT invite FROM invites WHERE created_by=?", (username,))
    rows = cursor.fetchall()
    invs = []
    for row in rows:
        invs.append(row[0])
    return invs
