import flask, datetime, logging as l, chigdb as db, chigauth as auth, chiginv as inv
from flask_socketio import SocketIO
from flask_cors import CORS
from flask_session import Session

app = flask.Flask(__name__)
app.secret_key = b'nyomod fasz'
app.config['SESSION_TYPE'] = 'filesystem'
socketio = SocketIO(app)
CORS(app, origins=['*'])
Session(app)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'POST':
        username = flask.request.form['username']
        password = flask.request.form['password']

        if auth.authenticate(username, password):
            l.warning("User logged in!")
            flask.session['username'] = username
            return flask.redirect('/')
        else:
            return f"Maybe next time, fucko."
    else:
        return flask.render_template('login.html')

@app.route('/logout')
def logout():
    l.warning("Logout!")
    flask.session.pop('username', None)
    return flask.redirect('/')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if flask.request.method == 'POST':
        username = flask.request.form['username']
        password = flask.request.form['password']
        invite = flask.request.form['invite']

        if inv.checkinvite(invite):
            if auth.register(username, password):
                return flask.redirect('/')
        else:
            return 500
    else:
        return flask.render_template('register.html')

@app.route("/invites")
def invites():
    if 'username' in flask.session:
        return flask.render_template('invites.html', username=flask.session['username'])
    else:
        return flask.redirect('/')

@app.route("/invq")
def invq():
    return flask.jsonify(inv.getinvs(flask.session['username']))

@app.route("/reqinv")
def reqinv():
    return inv.createinvite(flask.session['username'])

@app.route("/")
def index():
    if 'username' in flask.session:
        return flask.render_template('index.html', username=flask.session['username'])
    else:
        return flask.render_template('login.html')

@app.route("/send", methods=["POST"])
def send():
    data = flask.request.form.to_dict()
    message = data.get("message-input")
    if message == '':
        return '', 204
    username = flask.session['username']
    cursor = db.conn.cursor()
    cursor.execute('''INSERT INTO messages (sent_by, message, created_at) VALUES (?, ?, ?)''', (username, message, datetime.datetime.now()))
    #cursor.execute('''INSERT INTO messages (sent_by) VALUES (?)''', (username,))
    l.warning("Received: " + message)
    db.conn.commit()
    socketio.emit('new_message', message)
    return '', 204

@app.route('/messages')
def messages():
    cursor = db.conn.cursor()
    cursor.execute('''SELECT created_at, sent_by, message FROM messages ORDER BY created_at DESC LIMIT 100''')
    rows = cursor.fetchall()
    messages = {}
    for row in rows:
        created_at = row[0]
        sent_by = row[1]
        message = row[2]
        messages[created_at] = {'sent_by' : sent_by, 'message' : message}
    return flask.jsonify(messages)

@app.route('/cleardb')
def cleardb():
    l.warning("DB clear called.")
    db.drop()
    db.drop_auth()
    return "DBs Cleared", 200

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  return response

def start():
    db.init()
    db.init_auth()
    db.init_invites()
    if __name__ == '__main__':
        app.debug = True
        socketio.run(app, port=5000, host="0.0.0.0")

start()