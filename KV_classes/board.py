from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.config import Config
Builder.load_file("KV_classes/board.kv")
Config.set('graphics', 'width', '630')
Config.set('graphics', 'height', '700')
from kivy.graphics import Color, Rectangle, Line

from GAME.functions import create_board_file

# widget thats represent each box in board (it has to be widget becoase canvas Rectangle dos not have opacity)
class BoardBox (Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None,None)
        self.opacity = .7
        self.backgroud = list()
        with self.canvas:
            Color(rgba=(1,1,1,1))
            a = Rectangle(pos= self.pos, size = self.size)
            self.backgroud.append(a)
    def change_color (self,color):
        with self.canvas:
            Color(rgba=color)
            a = Rectangle(pos= self.pos, size = self.size)
            self.backgroud.append(a)

# arguments:
    # 1. list: metrix of 0,1,-1 (0 == None, 1 == o, -1 == x)
class Board(FloatLayout):
    def __init__(self,metrix:list, **kwargs):
        super().__init__(**kwargs)
        
        x = .65
        self.size_hint = (x,x/10*9 )
        self.pos_hint = {"center_x":.5, "center_y":.7}

        self.metrix = metrix
        self.rows = len(self.metrix)
        self.black_backgroud = None # I dont use yet
        self.squares = list()
        self.crosses = list()
        self.circles = list()
        self.stones = list()
        self.placed = [[False for i in range(self.rows)] for _ in range(self.rows)]
        self.current_position = list()

        self.create()
        self.bind(pos=self.update, size = self.update)

    def create (self):
        for i,j in enumerate(self.metrix):
            row = list()
            for k,l in enumerate(j):
                r = BoardBox()
                self.add_widget(r)
                row.append(r)
            self.squares.append(row)
        with self.canvas.before:
            self.canvas_color = Color(rgba = (1,1,1,1))
            # for i,j in enumerate(self.metrix):
            #     for k,l in enumerate(j):
            #         r = Rectangle(pos = self.pos, size = self.size)
            #         self.squares.append([r,i,k])

            self.canvas_color = Color(rgba = (0,0,0,1))
            for i,j in enumerate(self.metrix):
                for k,l in enumerate(j):
                    if l == -1: # circle O
                        circle = Line()
                        self.circles.append([circle,i,k])
                    elif l == 1: # cross X
                        l1 = Line()
                        l2 = Line()
                        self.crosses.append([l1,l2,i,k])
            
    def update (self, *args):
        offset = 2
        sitelen = ((self.width-4)/self.rows)
        for i in self.circles:
            i[0].circle = (self.pos[0] + offset + i[2]* sitelen + sitelen/2, self.pos[1] + offset + (self.rows - i[1]-1) *sitelen + sitelen/2, sitelen/2-7)
            i[0].width =  1.5

        for i in self.crosses:
            i[0].points = (
            self.pos[0] + offset + i[3]*sitelen+6, 
            self.pos[1] + offset +1 + (self.rows - i[2]-1)*sitelen+6,
            self.pos[0] + offset + (i[3]+1) *sitelen -6,
            self.pos[1] + offset +1 + (self.rows - i[2])*sitelen-6)
            i[0].width = 1.5
            i[1].points =(
            self.pos[0] + offset + i[3]*sitelen+6, 
            self.pos[1] + offset +1 + (self.rows - i[2])*sitelen-6,
            self.pos[0] + offset + (i[3]+1) *sitelen-6,
            self.pos[1] + offset +1 + (self.rows - i[2]-1)*sitelen+6
            )
            i[1].width = 1.5
            

        for i,j in enumerate(self.squares):
            for k,l in enumerate(j):
                l.pos = (self.pos[0] + offset + i*sitelen, self.pos[1] + offset  + (self.rows - k-1)*sitelen)
                l.size = (sitelen-1, sitelen-1)
                for m in l.backgroud:
                    m.size = (sitelen-1, sitelen-1)
                    m.pos = (self.pos[0] + offset + i*sitelen, self.pos[1] + offset  + (self.rows - k-1)*sitelen) 
                
    def change_opacity(self, list):
        list2 = []
        for i in list:
            list2.append(i)
        if list:
            for i in list:
                a,b = i
                if -1 < a < self.rows and -1 < b < self.rows:
                    if i not in self.current_position:
                            self.squares[a][b].opacity = .3
                    else:
                        self.current_position.pop(self.current_position.index(i))
                else:
                    list2.pop(list2.index(i))
        for a,b in self.current_position:
            self.squares[a][b].opacity = .7

        self.current_position = list2
        
    def make_move (self, instructions, color):
        for i,j in instructions:
            self.squares[j][i].change_color(color)


if __name__ == "__main__":
    basic_board = create_board_file("_board.txt")
    class TestApp (App):
        def build(self):
            return Board(basic_board)
    TestApp().run()
