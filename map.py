# In this file all the tilemaps available will be drawed block by block using the loop and list technique
import pyxel
import values
import main

class Map:
    def __init__(self):
        self.width = main.board.width
        self.height = main.board.height

    def introduction(self):
        pyxel.bltm(0, 0, 1, 0, 0, self.width, self.height)
        pyxel.blt(40, 10, *values.game_title)