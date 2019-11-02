from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
import eventlet

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)

@app.route('/')
def hello_world():
    return "yooo"

@socketio.on('create')
def on_create():
    print("yooooooo")

if __name__ == '__main__':
    socketio.run(app, debug=True)