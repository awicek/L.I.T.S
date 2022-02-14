from kivy.app import App 
from kivy.config import Config

Config.set('graphics', 'width', '700')
Config.set('graphics', 'height', '700')
from kivy.lang import Builder
Builder.load_file("__main.kv")

from kivy.uix.label import Label 
from kivy.uix.scrollview import ScrollView
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.gridlayout import GridLayout

from functools import partial
import json

from kivy.uix.screenmanager import ScreenManager, Screen
from functions import create_random_stones, stones, colors,  stones_for_players, create_random_board
from relative_layout import GameWin

from kivy.clock import Clock


class MyLabel (Label):
    def on_size(self,*args):
        self.text_size = self.size

class MyGridLayout (GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.widgets = list()
# this saves settings to the file
class MyScroll (ScrollView):
    def __init__(self,options,informations,**kwargs):
        super().__init__(**kwargs)
        self.grid = MyGridLayout()
        self.add_widget(self.grid)
        self.options = options
        self.informations = informations 
        self.create()
        self.current_selection = None

    def create (self):
        for i,j in enumerate(self.options):
            a = ToggleButton(text = j)
            a.on_press = partial(self.change_info, i)
            self.grid.widgets.append(a)

        for i in self.grid.widgets:
            self.grid.add_widget(i)

    def change_info (self,num):
        if self.grid.widgets[num].state == "down":
            for i,j in enumerate(self.grid.widgets):
                if i == num:
                    ...
                else:
                    j.state = "normal"
            self.current_selection = self.informations[num]
        else:
            self.current_selection = None

# screen that loads game from json file
class GameScreen (Screen):
    def create_game (self):
        with open ("game_settings.json", "r") as f:
            data = json.load(f)
        p1 = data["player1"]
        p2 = data["player2"]

        board_size = data["board_size"]

        stones_num = data["stones"]
        sourse = data["sourse"]

        board = create_random_board(board_size)

        if sourse == 1:
            stones1 = stones
            stones2 = stones_for_players
        else:
            stones1,stones2 = create_random_stones(stones_num)

        
        self.game = GameWin(board,stones1,stones2,colors,p1,p2)
        self.add_widget(self.game)
    
    def end_game(self):
        self.remove_widget(self.game)
        self.game = None
# mainmenu screen
class MainMenuScreen (Screen):
    ...
# screen with settings
class SettingsScreen (Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.p1 = MyScroll(
        ["PC","človíček"], 
        [0, 1],
        pos_hint= {"center_x":0.3, "center_y":.85},
        size_hint= (.15,.1)
        )
        self.add_widget(self.p1)

        self.p2 = MyScroll(
        ["človíček","PC",], 
        [1, 0],
        pos_hint= {"center_x":0.8, "center_y":.85},
        size_hint= (.15,.1)
        )
        self.add_widget(self.p2)

        self.board_size = MyScroll(
        ["10x10","15x15","Random"], 
        [10,15,-1],
        pos_hint= {"center_x":0.3, "center_y":.6},
        size_hint= (.15,.1)
        )
        self.add_widget(self.board_size)

        self.amount = MyScroll(
        ["10","12","14","16","18","20","22","24","Random"], 
        [10,12,14,16,18,20,22,24,-1],
        pos_hint= {"center_x":0.3, "center_y":.3},
        size_hint= (.15,.1)
        )
        self.add_widget(self.amount)

        self.sourse = MyScroll(
        ["File","Random"], 
        [1,-1],
        pos_hint= {"center_x":0.8, "center_y":.3},
        size_hint= (.15,.1)
        )
        self.add_widget(self.sourse)
        
    def safe_settings (self):
        # 1 == človíček, 0 == PC
        p1 = self.p1.current_selection
        p2 = self.p2.current_selection
        
        # number == (size, amount, amount), -1 == random
        board_size = self.board_size.current_selection
        stones = self.amount.current_selection

        # file == 1, random ==0
        sourse = self.sourse.current_selection
        data_list = ["player1", "player2", "board_size", "stones", "sourse"]
        with open ("game_settings.json", "r") as f:
            data = json.load(f)
        
        for i,j in enumerate([p1,p2,board_size,stones,sourse]):
            if j != None:
                data[data_list[i]] = j

        with open ("game_settings.json", "w") as f:
            json.dump(data, f, indent=4)
        
# Main App
class MainWindow (ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
        self.ids.mainmenu.ids.settings_b.on_release = self.to_settings
        self.ids.settings.ids.mainmenu_b.on_release = self.to_main_menu_l   
        self.ids.mainmenu.ids.game_b.on_release = self.to_game

        def end_game_check (dt):
            if self.current == "Game":
                if self.ids.game.game.end == True:
                    self.ids.game.end_game()
                    self.to_main_menu_r()

        Clock.schedule_interval(end_game_check,.5)

    def to_settings (self):
        self.transition.direction = 'right'
        self.current = "Settings"
    
    def to_main_menu_r (self):
        self.transition.direction = 'right'
        self.current = "MainMenu"
    
    def to_main_menu_l (self):
        self.transition.direction = 'left'
        self.current = "MainMenu"
        self.ids.settings.safe_settings()
    
    def to_game (self):
        self.transition.direction = 'left'
        self.ids.game.create_game()
        self.current = "Game"
        

if __name__ == "__main__":
    class TestApp (App):
        def build(self):
            return MainWindow()
    TestApp().run()


 

    