from flask import Flask, render_template, jsonify, make_response
from flask_socketio import SocketIO
import eventlet
import game
import json
import random
import math
import threading

app = Flask(__name__)
socketio = SocketIO(app)

N = 100
board = game.Board(N)
users = []

userLocations = {}

def test(i, currentX, currentY, direction):
    print("HELLO!!!")
    garbageX = currentX
    garbageY = currentY
    if direction == "Up":
        garbageY = garbageY - 1
    elif direction == "Down":
        garbageY = garbageY + 1
    elif direction == "Right":
        garbageX = garbageX + 1
    elif direction == "Left":
        garbageX = garbageX - 1

    if garbageX >= N or garbageX < 0 or garbageY >= N or garbageY < 0:
        board.Grid[garbageX][garbageY].Name = ""
        return
    elif board.Grid[garbageX][garbageY].Type == "Player":
        oldname = board.Grid[garbageX][garbageY].Name
        userLocations[board.Grid[currentX][currentY].Name][2] += 1
        userLocations[board.Grid[garbageX][garbageY].Name][3] -= 1
        if userLocations[board.Grid[garbageX][garbageY].Name][3] <= 0:
            print("asdfasdfasdfasdf")
            tile = game.Tile(garbageX,garbageY)
            board.updateGrid(garbageX, garbageY, tile)
            obj = board.Grid[garbageX][garbageY].serialize()
            obj['oldX'] = garbageX
            obj['oldY'] = garbageY
            socketio.emit('loser', oldname, broadcast=True)
            socketio.emit('updateBoard', obj, broadcast=True)

        socketio.emit('newUserBroadcast', userLocations)

        print(userLocations)
        #print(board.Grid[currentX][currentY].Name, board.Grid[garbageX][garbageY].Name)
        return
    elif board.Grid[garbageX][garbageY].Type != "Blank":
        board.Grid[garbageX][garbageY].Name = ""
        return
    else:
        board.Grid[currentX][currentY].X = garbageX
        board.Grid[currentX][currentY].Y = garbageY

        board.updateGrid(garbageX, garbageY, board.Grid[currentX][currentY])
        blank = game.Tile(currentX, currentY)
        board.updateGrid(currentX, currentY, blank)

        obj = board.Grid[garbageX][garbageY].serialize()
        obj['oldX'] = currentX
        obj['oldY'] = currentY
        #print("yooo")
        print(currentX, currentY)
        socketio.emit('updateBoard', obj, broadcast=True)

        if i + 1 < 10:
            print("yooo")
            #threading.Timer(.5, lambda: print("hello")).start()
            eventlet.sleep(.05)
            test(i+1, garbageX, garbageY, direction)
            #t = threading.Timer(.5, test, [i+1, garbageX, garbageY, direction])
            #t.start()
            #t.join()
            print("yo#2")
        else:
            board.Grid[garbageX][garbageY].Name = ""
            


@app.route('/', methods=['GET','POST'])
def hello_world():
    return render_template('client.html')

@socketio.on('newUser')
def on_newUser(payload, methods=['GET','POST']):
    users.append(str(payload['user_name']))
    newX = random.randint(0,N)
    newY = random.randint(0,N)
    print(len(board.Grid))
    while board.Grid[newX][newY].Type != "Blank":
        newX = random.randint(0,N)
        newY = random.randint(0,N)

    newTile = game.Tile(newX, newY, "Player", name=payload['user_name'])
    board.updateGrid(newX, newY, newTile)
    userLocations[payload['user_name']] = [newX, newY, 0, 3]

    print(newX, newY)
    print(board.Grid[newX][newY].Type)

    print(users)
    #socketio.emit('changeContext', broadcast=False)

    print(board.Grid[newX][newY].Type)

    socketio.emit('changeContext', board.serialize(), broadcast=False)
    socketio.emit('newUserBroadcast', userLocations, broadcast=True)
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
    elif board.Grid[newX][newY].Type == "Player":
        return
    elif board.Grid[newX][newY].Type == "Trashcan":
        print("asdkjfhaksjdhfkjasdhfjkashfjk")
        #garbageX = newX
        #garbageY = newY
        #count = 0
        board.Grid[newX][newY].Name = payload['name']
        test(0, newX, newY, direction)
        """
        for i in range(0,10):
            currentX2 = garbageX
            currentY2 = garbageY
            if direction == "Up":
                garbageY = garbageY - 1
            elif direction == "Down":
                garbageY = garbageY + 1
            elif direction == "Right":
                garbageX = garbageX + 1
            elif direction == "Left":
                garbageX = garbageX - 1

            if garbageX >= N or garbageX < 0 or garbageY >= N or garbageY < 0:
                return
            elif board.Grid[garbageX][garbageY].Type != "Blank":
                # add player collision check here later
                return
            else:
                board.Grid[currentX2][currentY2].X = garbageX
                board.Grid[currentX2][currentY2].Y = garbageY

                board.updateGrid(garbageX, garbageY, board.Grid[currentX2][currentY2])
                blank = game.Tile(currentX2, currentY2)
                board.updateGrid(currentX2, currentY2, blank)

                obj = board.Grid[garbageX][garbageY].serialize()
                obj['oldX'] = currentX2
                obj['oldY'] = currentY2
                #count += 1
                #print("yooo")
                socketio.emit('updateBoard', obj, broadcast=True)

        """
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
    