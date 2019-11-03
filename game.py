from flask import jsonify
import json

class Tile:
    def __init__(self, X, Y, typeOfTile="Blank", name=""):
        self.X = X
        self.Y = Y
        self.Type = typeOfTile
        self.Name = name

    def serialize(self):
        return {
            'X': self.X,
            'Y': self.Y,
            'Type': self.Type,
            'Name': self.Name
        }


class Board:
    def __init__(self, N):
        self.N = N

        grid = []
        for i in range(0, N):
            new = []
            for j in range(0,N):
                newTile = Tile(i,j)
                new.append(newTile)
            grid.append(new)

        self.Grid = grid

    def updateGrid(self, X, Y, T):
        self.Grid[X][Y] = T

    def serialize(self):
        test = []
        test.append(self.N)
        for i in range(0,self.N):
            for j in range(0,self.N):
                #newTile = Tile(i,j).serialize()
                newTile = self.Grid[i][j].serialize()
                test.append(newTile)

        return test

    