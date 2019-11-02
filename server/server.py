from flask import Flask
from flask_socketio import SocketIO
import eventlet

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def hello_world():
    return "yooo"

@socketio.on('create')
def on_create():
    print("yooooooo")

if __name__ == '__main__':
    socketio.run(app, debug=True)