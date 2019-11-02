from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_cors import CORS
import eventlet

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)

users = []

@app.route('/')
def hello_world():
    return render_template('client.html')

@socketio.on('create')
def on_create():
    print("yooooooo")

@socketio.on('newUser')
def on_newUser(json, methods=['GET','Post']):
    users.append(str(json['user_name']))
    print(users)
    socketio.emit('changeContext')

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: '+ str(json))
    socketio.emit('my response', json, callback=messageReceived)

if __name__ == '__main__':
    socketio.run(app, debug=True)