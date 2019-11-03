from flask import Flask, render_template, jsonify, make_response
from flask_socketio import SocketIO
import eventlet
import game
import json
import random
import math

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
    userLocations[payload['user_name']] = [newX, newY]

    print(newX, newY)
    print(board.Grid[newX][newY].Type)

    print(users)
    socketio.emit('newUserBroadcast', users, broadcast=True)
    #socketio.emit('changeContext', broadcast=False)

    print(board.Grid[newX][newY].Type)

    socketio.emit('changeContext', board.serialize(), broadcast=False)
    print("GETTING HERE TOO")

@socketio.on('buttonPress')
def on_button(payload, methods=['GET','POST']):
    currentX = userLocations[payload['name']][0]
    currentY = userLocations[payload['name']][1]
    newX = currentX
    newY = currentY

    direction = payload['button']
    if direction == "Up":
        newY = currentY - 1
    elif direction == "Down":
        newY = currentY + 1
    elif direction == "Right":
        newX = currentX + 1
    elif direction == "Left":
        newX = currentX - 1

    if newX >= N or newX < 0 or newY >= N or newY < 0:
        return

    board.Grid[currentX][currentY].X = newX
    board.Grid[currentX][currentY].Y = newY

    userLocations[payload['name']][0] = newX
    userLocations[payload['name']][1] = newY

    board.updateGrid(newX, newY, board.Grid[currentX][currentY])
    blank = game.Tile(currentX, currentY)
    board.updateGrid(currentX, currentY, blank)

    obj = board.Grid[newX][newY].serialize()
    obj['oldX'] = currentX
    obj['oldY'] = currentY

    socketio.emit('updateBoard', obj, broadcast=True)


def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: '+ str(json))
    socketio.emit('my response', json, callback=messageReceived)

if __name__ == '__main__':
    #python not js lmao
    for ii in range(0,N):
        for jj in range(0,N):
            if random.randint(0,N*N) % (50) == 0 and board.Grid[ii][jj].Type == "Blank":
                print("name jeff")
                board.Grid[ii][jj].Type = "Trashcan"

    socketio.run(app, debug=True,port = 5000, host = '0.0.0.0')
    