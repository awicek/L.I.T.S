from kivy.uix.widget import Widget
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle

from board import Board
Builder.load_file("test_fl.kv")

class RedWidget (Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        
class BoardBox (Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None,None)
    

class TestLayout (FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.movingobject = RedWidget()
        self.add_widget(self.movingobject)
        self.movingobject.size = (30,30)
        self.a = BoardBox()
        self.add_widget(self.a)
        self.a.size = (50,50)
        self.a.pos = (50,50)

        #Clock.schedule_interval(self.move, .1)
    
    def move (self,td):
        a,b = self.movingobject.pos
        print(a,b)
        self.movingobject.pos = a +10, b + 10

    def on_touch_move(self, touch):
        self.movingobject.pos = touch.pos




class TestApp (App):
    def build(self):
        return TestLayout()

if __name__ == "__main__":
    TestApp().run()