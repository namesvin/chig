import logging as l

global users, cid
users = {}

def init():
    l.warning("Creating admin user!")
    users["admin"] = "Vince123"

def register(username, password):
    if username and password:        
        users[username] = password
        return True
    else:
        return False

def authenticate(username, password):
    if username in users and users[username] == password:
        l.warning("User authenticated!")
        return True
    else:
        return False