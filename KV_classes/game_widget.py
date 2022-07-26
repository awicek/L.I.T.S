from kivy.app import App 
from kivy.config import Config
from kivy.lang.builder import Instruction


Config.set('graphics', 'width', '700')
Config.set('graphics', 'height', '700')
from kivy.lang import Builder
Builder.load_file("KV_classes\\game_widget.kv")

from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.widget import Widget
from kivy.uix.label import Label

from KV_classes.board import Board
from KV_classes.table_of_stones import Table_of_Stones
from KVHRA.functions import create_random_board, stones, colors
import time

#Argumetns: 
#   1. matrix: matrix of stone
#   2. color: tuple of colors
#   3. len: len of size one rectangle in board in pixels
class MovingStone (Widget):
    def __init__(self,matrix: list, color:tuple, side_len:int,rotation:int, **kwargs):
        super().__init__(**kwargs)
        self.max_y = len(matrix[0]) 
        self.max_x = len(matrix) 
        self.opacity = .7
        self.size_hint = (None, None)
        self.size = (side_len* self.max_y ,side_len* self.max_x)
        self.matrix = matrix
        self.color = color
        self.side_len = side_len
        self.rectangles = list()
        self.rotate(rotation)
        self.create()

    def rotate (self, num):
        for _ in range(num):
            new_matrix = list()
            for i in range(self.max_y):
                row = list()
                for j in range(self.max_x):
                    row.append(self.matrix[j][self.max_y -1 -i ])
                new_matrix.append(row)
            self.max_y, self.max_x = self.max_x , self.max_y
            self.matrix = new_matrix
                     
    def create (self):
        offset = 3
        with self.canvas:
            Color(rgba = self.color)
            for i,j in enumerate(self.matrix):
                for k,l in enumerate(j):
                    if l != 0:
                        a = Rectangle()
                        b = (k*self.side_len + offset, (self.max_x - 1 - i)* self.side_len + offset)
                        a.size = (self.side_len - 2*offset, self.side_len - 2*offset)
                        a.pos = (self.pos[0] + b[0], self.pos[1] + b[1])
                        self.rectangles.append([a,b])
    
    def update_pos (self, pos):
        for i in self.rectangles:
            a,b = i[1]
            x,y = pos
            i[0].pos = (x+a,y+b)

#Arguments:
#   1. board: list()
#   2. stones: list of Stones
#   3. colors: dict of RGBA sets
class GameWidget (FloatLayout):
    def __init__(self,board: list, stones: list, colors: dict , **kwargs):
        super().__init__(**kwargs)

        self.play_board = Board(board)
        self.add_widget(self.play_board)
        self.play_board.update()
        self.table_of_stones = Table_of_Stones(stones, colors)
        self.add_widget(self.table_of_stones)
        self.colors = colors
        
        self.moving_stone = None
        self.moving_matrix = None
        self.moving_num = None
        self.current_place = list()

        self.playing = 1

    def create_moving_stone(self, number, side_len):
        rotation = self.table_of_stones.stones[number][0].rotation
        self.table_of_stones.stones[number][0].opacity = 0

        self.moving_num = number
        self.moving_stone = MovingStone(self.table_of_stones.stones[number][0].matrix,self.table_of_stones.stones[number][0].color, side_len, rotation)
        self.moving_matrix = self.moving_stone.matrix
        self.add_widget(self.moving_stone)

    def move (self, pos):
        self.moving_stone.pos = pos
        self.moving_stone.update_pos(pos)

    def board_movement (self, pos = None):
        if pos == None:
            self.play_board.change_opacity([])
        else:
            x,y = pos
            instruction = list()
            for i,j in enumerate(self.moving_matrix[::-1]):
                for k,l in enumerate(j):
                    if l > 0:
                        instruction.append([x+k,y-i])
            self.play_board.change_opacity(instruction)

    def delete_moving_stone(self):
        self.remove_widget(self.moving_stone)
        self.table_of_stones.stones[self.moving_num][0].opacity = 1
        self.moving_num = None
        self.moving_stone = None
        self.moving_matrix = None
        self.play_board.change_opacity([])

    def make_move(self,x,y):
        instructions = list()
        for i,j in enumerate(self.moving_matrix):
                for k,l in enumerate(j):
                    if l > 0:
                        instructions.append([x+i,y+k])
        self.play_board.make_move(instructions, self.table_of_stones.stones[self.moving_num][0].color)
    
    def remove_stone (self, num):
        self.table_of_stones.remove_widget(self.table_of_stones.stones[num][0])
    
    def update_score (self, sc1, sc2):
        if self.playing == 0:
            self.ids.x_move.text = "playing ..."
            self.ids.o_move.text = ""
        else:
            self.ids.x_move.text = ""
            self.ids.o_move.text = "playing ..."
        self.playing = (self.playing + 1) % 2
        
        self.ids.score_p1.text = str(sc1)
        self.ids.score_p2.text = str(sc2)

if __name__ == "__main__":
    class TestApp(App):
        def build(self):
            board = create_random_board()
            return GameWidget(board,stones,colors)
    TestApp().run()
