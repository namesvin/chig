import flask, logging as l, chigdb as db, chigauth as auth
from flask_socketio import SocketIO
from flask_cors import CORS

app = flask.Flask(__name__)
socketio = SocketIO(app)
CORS(app, origins=['*'])
session = {}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'POST':
        username = flask.request.form['username']
        password = flask.request.form['password']

        if auth.authenticate(username, password):
            l.warning("User logged in!")
            session['username'] = username
            return flask.redirect('/')
        else:
            return f"Maybe next time, fucko."
    else:
        return flask.render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if flask.request.method == 'POST':
        username = flask.request.form['username']
        password = flask.request.form['password']
        key = flask.request.form['key']

        if key == 'secretive':
            if auth.register(username, password):
                return flask.redirect('/')
        else:
            return 500
    else:
        return flask.render_template('register.html')

@app.route('/logout')
def logout():
    l.warning("Logout!")
    session.pop('username', None)
    return flask.redirect('/')

@app.route("/")
def index():
    if 'username' in session:
        return flask.render_template('index.html', username=session['username'])
    else:
        return flask.render_template('login.html')

@app.route("/send", methods=["POST"])
def send():
    data = flask.request.form.to_dict()
    message = data.get("message-input")
    username = session['username']
    cursor = db.conn.cursor()
    cursor.execute('''INSERT INTO messages (sent_by, message) VALUES (?, ?)''', (username, message))
    #cursor.execute('''INSERT INTO messages (sent_by) VALUES (?)''', (username,))
    l.warning("Received: " + message)
    db.conn.commit()
    socketio.emit('new_message', message)
    return '', 204

@app.route('/messages_old')
def messages_old():
    cursor = db.conn.cursor()
    cursor.execute('''SELECT message FROM messages ORDER BY created_at DESC LIMIT 100''')
    cursor.execute('''SELECT sent_by FROM messages ORDER BY created_at DESC LIMIT 100''')
    messages = cursor.fetchall()
    return flask.jsonify(messages)

@app.route('/messages')
def messages():
    cursor = db.conn.cursor()
    cursor.execute('''SELECT created_at, sent_by, message FROM messages ORDER BY created_at DESC LIMIT 100''')
    rows = cursor.fetchall()
    print(rows)
    messages = {}
    for row in rows:
        created_at = row[0]
        sent_by = row[1]
        message = row[2]
        messages[created_at] = {'sent_by' : sent_by, 'message' : message}
    print(auth.users)
    return flask.jsonify(messages)

@app.route('/cleardb')
def cleardb():
    l.warning("DB clear called.")
    db.drop()
    return "DB Clear", 200

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  return response

@socketio.on('msg_ts')
def handle_message():
  l.warning("Emitting new message!")
  socketio.emit('msg_fs')

def start():
    db.init()
    auth.init()
    if __name__ == '__main__':
        app.debug = True
        socketio.run(app, port=5000)
        #app.run(port=5000)


start()