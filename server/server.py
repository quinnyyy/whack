from flask import Flask, render_template, jsonify, make_response
from flask_socketio import SocketIO
import eventlet
import game
import json
import random

app = Flask(__name__)
socketio = SocketIO(app)

N = 100
board = game.Board(N)
users = []

userLocations = {}

@app.route('/', methods=['GET','POST'])
def hello_world():
    return render_template('client.html')

@socketio.on('newUser')
def on_newUser(payload, methods=['GET','POST']):
    users.append(str(payload['user_name']))
    newX = random.randint(0,N)
    newY = random.randint(0,N)
    newTile = game.Tile(newX, newY, "Player", name=payload['user_name'])
    board.updateGrid(newX, newY, newTile)

    print(users)
    socketio.emit('newUserBroadcast', users, broadcast=True)
    #socketio.emit('changeContext', broadcast=False)

    socketio.emit('changeContext', board.serialize(), broadcast=False)
    print("GETTING HERE TOO")

@socketio.on('buttonPress')
def on_button(payload, methods=['GET','POST']):
    print(payload)

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: '+ str(json))
    socketio.emit('my response', json, callback=messageReceived)

if __name__ == '__main__':
    socketio.run(app, debug=True)