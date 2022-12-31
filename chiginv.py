import chigdb as db, logging as l, datetime, hashlib, random

def createinvite(username):
    invbase = username + str(random.random()**random.random()) + username
    invite = hashlib.sha256(invbase.encode()).hexdigest()
    expires = datetime.datetime.now() + datetime.timedelta(days=7)
    print(invbase)
    print(invite)
    print(expires)
    cursor = db.conn.cursor()
    cursor.execute('''INSERT INTO invites (created_by, invite, expires) VALUES (?, ?, ?)''', (username, invite, expires))
    db.conn.commit()

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
        if datetime.datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S').time() > datetime.datetime.now() :
            deleteinvite(invite)
            return True
    return False

db.init_invites()
#createinvite("vin")
print(checkinvite("3c965e8d9d59174ae8a7c443bded4sefa4027b706aeff997cc7c4d3657d7dc7c"))
print(checkexpire("3c965e8d9d59174ae8a7c443bded4sefa4027b706aeff997cc7c4d3657d7dc7c"))