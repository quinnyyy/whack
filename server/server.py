from flask import Flask, render_template
from flask_socketio import SocketIO
import eventlet

app = Flask(__name__)
socketio = SocketIO(app)

N = 10000
board = []
users = []

@app.route('/', methods=['GET','POST'])
def hello_world():
    return render_template('client.html')

@socketio.on('newUser')
def on_newUser(json, methods=['GET','POST']):
    users.append(str(json['user_name']))
    print(users)
    socketio.emit('newUserBroadcast', users, broadcast=True)
    #socketio.emit('changeContext', broadcast=False)
    socketio.emit('changeContext', broadcast=False)

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: '+ str(json))
    socketio.emit('my response', json, callback=messageReceived)

if __name__ == '__main__':
    for i in range(0,N):
        new = []
        for j in range(0,N):
            new.append(0)
        board.append(new)
    
    socketio.run(app, debug=True)