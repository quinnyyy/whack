from flask import Flask, render_template, jsonify, make_response
from flask_socketio import SocketIO
import eventlet
import game

app = Flask(__name__)
socketio = SocketIO(app)

N = 100
board = game.Board(N)
users = []

@app.route('/')
def hello_world():
    return render_template('client.html')

@socketio.on('newUser')
def on_newUser(json, methods=['GET','Post']):
    users.append(str(json['user_name']))
    print(users)
    socketio.emit('newUserBroadcast', users, broadcast=True)
    #socketio.emit('changeContext', broadcast=False)
    socketio.emit('changeContext', make_response(jsonify(board.serialize())), broadcast=False)

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: '+ str(json))
    socketio.emit('my response', json, callback=messageReceived)

if __name__ == '__main__':
    socketio.run(app, debug=True)