from kivy.app import App 
from kivy.config import Config
Config.set('graphics', 'width', '630')
Config.set('graphics', 'height', '700')
from kivy.lang import Builder
Builder.load_file("KV_classes/table_of_stones.kv")

from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle, Rotate
from kivy.graphics.context_instructions import PopMatrix, PushMatrix

from GAME.functions import Stone, read_stones, colors

#   on_touch_down - rewrite
# Arguments:
#   1. colors = dictionary ("number": RGBAcolor)
#   2. matrix of some polinomia
class GameStone(Widget):
    def __init__(self, colors:dict, base_stone:Stone, **kwargs):
        super().__init__(**kwargs)

        self.size_hint = (None,None)
        
        self.matrix = base_stone.matrix
        self.color = colors[str(base_stone.color)]
        self.max_x = base_stone.max_x
        self.max_y = base_stone.max_y
        self.rotation = 0

        self.squares = list()  # rectangles in canvas which creates image of stone
        self.create()

        # It is triggered when you resize game window
        self.bind(pos=self.update, size= self.update)  
    # adds rectangles to the canvas 
    def create (self):
        with self.canvas.before:
            Color(rgba = self.color)
            for i in range(self.max_x * self.max_y):
                x,y = i // (self.max_y), i % self.max_y
                if self.matrix[x][y] > 0:
                    a = Rectangle(pos= self.pos, size=self.size)
                    self.squares.append(a)
                else:
                    self.squares.append(None)
    # change rotation
    def rotate (self):
        self.angle += 90
        self.rotation = (self.rotation +1)%4
    # it tedermins positions and size of rectangles in canvas
    def update (self, *args):
        a = max(self.max_x, self.max_y)
        sitelen = int((self.width - 8)/a)
        if self.max_x == self.max_y:
            ofset_x = 4 
            ofset_y = 4 
        elif self.max_y > self.max_x:
            ofset_y = 4
            ofset_x = 4 + (self.max_y - self.max_x)/2*sitelen
        else:
            ofset_x = 4
            ofset_y = 4 + (self.max_x - self.max_y)/2*sitelen
        for i,j in enumerate(self.squares):
            x,y = i // (self.max_y), i % self.max_y
            if self.matrix[x][y] > 0:
                j.pos = (self.pos[0] + ofset_y + 1 + y*sitelen, self.pos[1] + ofset_x +1 + (self.max_x -x-1)*sitelen)
                j.size = (sitelen-2,sitelen-2)

# Arguments:
#   1. stones = list of Stones
#   2. colors = dictionary of colors
class Table_of_Stones (FloatLayout):
    def __init__(self, stones:list, colors:dict,**kwargs):
        super().__init__(**kwargs)
        self.size_hint = (.95,.35)
        self.pos_hint = {"center_x": .5, "center_y": .20}
        
        self.colors = colors
        self.stones = self.create(stones)
        self.bind(pos=self.update, size= self.update)  

    def create (self,field):
        stones = list()
        for i,j in enumerate(field):
            a = GameStone(self.colors, j)
            self.add_widget(a)
            stones.append([a,i%8,i//8])
        return stones

    def update(self, *args):
        size = (self.width )/8
        offset_x = (self.height - 3*size)/4
        for i in self.stones:
            i[0].size = (size,size)
            i[0].pos = (2 + self.pos[0] + i[1]*size, self.pos[1] + (3-i[2])*offset_x + (3-i[2]-1)* size)


if __name__ == "__main__":
    class TestApp (App):
        def build(self):
            policka = read_stones("C:\\Users\\richa\\OneDrive\\Dokumenty\\Python\\škola\\lekce_9SEM\\stones.txt")
            return Table_of_Stones(policka,colors)
            #return Policko((.3,.3),[.5,.5],colors,policka[0])
    TestApp().run()