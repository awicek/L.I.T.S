from kivy.app import App
from kivy.properties import NumericProperty

from kivy.lang import Builder
Builder.load_file("relative_layout.kv")
from kivy.config import Config
Config.set('graphics', 'width', '630')
Config.set('graphics', 'height', '700')
from kivy.clock import Clock

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup

from functions import create_random_board, stones, colors, stones_for_players
from game_widget import GameWidget
from game_logic import Game


#Arguments
#   1. board = matrix of x/o
#   2. stones = list of Stones
#   3. colors = which colors have stones
class GameWin(FloatLayout):
    ratio = NumericProperty(10 / 9.)
    def __init__(self,board: list, stones: list, stones_for_players:list, colors: dict, p1, p2, **kw):
        super().__init__(**kw)
        
        self.game_widget = GameWidget(board,stones,colors)
        self.add_widget(self.game_widget)

        self.game = Game(board,stones,stones_for_players,p1,p2)

        self.board_size = len(board)
        self.number_of_stones = len(stones)

        self.time = 0
        self.timer = None
        self.moving_stone_num = -1
        self.move_in_progress = False
        

        # change it to the True ends a game 
        self.end = False

        # Start of game
        # človíček vs PC 
        if p1 == 1 and p2 == 0: # človíček starts a game
            self.mode = -1
            self.firstmove = True
            self.human_player_on_move = True
        # PC vs PC 
        elif p1 == 0 and p2 == 0:
            self.human_player_on_move = False
            self.computer_vs_computer()
        # človíček vs človíček
        elif p1 == 1 and p2 ==1:
            self.firstmove = True
            self.mode = 2
            self.human_player_on_move = True
        # PC vs človíček
        else: 
            self.mode = 1
            self.human_player_on_move = False
            self.computer_player_move()

# RATIO
    def do_layout(self, *args):
        for child in self.children:
            self.apply_ratio(child)
        super(GameWin, self).do_layout()

    def apply_ratio(self, child):
        # ensure the child don't have specification we don't want
        child.size_hint = None, None
        child.pos_hint = {"center_x": .5, "center_y": .5}

        w, h = self.size
        h2 = w * self.ratio
        if h2 > self.height:
            w = h / self.ratio
        else:
            h = h2
        child.size = w, h
    
# MOUSE INPUT HANDLING
    # on which stone did i click --> if it is valid stone start MOVETIMER
    def on_touch_down(self, touch):
        a,b = self.game_widget.table_of_stones.pos
        x,y = touch.pos[0] - a , touch.pos[1] - b

        b = self.game_widget.table_of_stones.size 

        # stone 
        if  0 < x < b[0] and 0 < y < b[1]:
            lenx = b[0]/8
            leny = (b[1] - lenx*3)/4 + lenx
            number = (x)//lenx
            number += (2 - (y)//leny) *8

            number = int(number)
            if number < self.number_of_stones:
                    self.moving_stone_num = number
                    if self.game.freestones[number] == True:
                        self.move_timer()      

        # buttons
        # end_b
        a,b = self.game_widget.ids.end_b.pos
        # skip_b
        c,d = self.game_widget.ids.skip_b.pos
        # end_b
        e,f = self.game_widget.ids.back_b.pos

        x,y = touch.pos[0] - a , touch.pos[1] - b
        size = self.game_widget.ids.end_b.size

        if  0 < x < size[0] and 0 < y < size[1]:
            print("tudopici")
            self.end = True

    
    # how long did i hold valid stone --> less than 1s --> rotate that stone +90*
    #                                 --> more than 1s --> create a moving stone and start move ON_TOUCH_DONS
    def move_timer(self):
        self.time = 0
        def timeup (arg):
            self.time += 1
            if self.time >3 and  self.human_player_on_move:
                self.create_moving_stone()
                self.move_in_progress = True
                self.timer.cancel()
        self.timer = Clock.schedule_interval(timeup, .1)

    # creates a moving stone
    def create_moving_stone(self):
        len = self.game_widget.play_board.size[1]/self.board_size
        self.game_widget.create_moving_stone(self.moving_stone_num, len)

    # moves stone and calculate where is it currently placed
    def on_touch_move(self, touch):
        if self.move_in_progress:
            self.game_widget.move(touch.pos) 

            len = (self.game_widget.play_board.size[1]/self.board_size)/2
            a,b = self.game_widget.play_board.pos
            x,y = touch.pos[0] - a -2 + len , touch.pos[1] - b +len -2
            b = self.game_widget.play_board.size 
            
            if  0 < x < b[0] and 0 < y < b[1]:
                len = self.game_widget.play_board.width/self.game_widget.play_board.rows
                xx = (x)//len
                yy = (self.game_widget.play_board.rows-1-(y)//len) 
                xx = int(xx)
                yy = int(yy)
                self.game_widget.board_movement([xx,yy])
            else:
                self.game_widget.board_movement()

    # stop TIMER and decides what should happened --> less than 1s --> rotate stone +90*
    #                                             --> more that 1s --> calculate where should be stone placet --> valid move --> placed it
    #                                                                                                         --> invalid move --> raise error 
    def on_touch_up(self, touch):
        if self.time < 4 and self.moving_stone_num > -1:
            self.game_widget.table_of_stones.stones[self.moving_stone_num][0].rotate()

            self.time = 0
            self.moving_stone_num = -1
            self.timer.cancel()

        elif self.move_in_progress:
            len = (self.game_widget.play_board.size[1]/self.board_size)/2
            a,b = self.game_widget.play_board.pos
            x,y = touch.pos[0] - a -2 + len , touch.pos[1] - b +len -2
            b = self.game_widget.play_board.size 
            
            if  0 < x < b[0] and 0 < y < b[1]:
                len = self.game_widget.play_board.width/self.game_widget.play_board.rows
                yy = (x)//len
                xx = (self.game_widget.play_board.rows-1-(y)//len) 
                yy = int(yy)
                xx = int(xx)
                self.check_move(xx,yy)

            else:
                print("INVALID MOVE")

            self.game_widget.delete_moving_stone()
            self.time = 0
            self.moving_stone_num = -1
            self.move_in_progress = False
        
        return super().on_touch_up(touch)
    
# MOVE
    # check if this move is valid or raise 
    def check_move(self,x,y):
        control = self.game.check_move(x, y, self.game_widget.moving_matrix, self.moving_stone_num, self.firstmove)
        if control:
            self.make_move(x-len(self.game_widget.moving_matrix)+1,y)
    # make human move
    def make_move(self,x,y,instruction = None, color = None):
        if instruction != None:
            self.game_widget.play_board.make_move(instruction,color)
        else:
            self.game.human_player_move(x,y,self.game_widget.moving_matrix,self.moving_stone_num)
            self.game_widget.make_move(x,y)
            self.game_widget.remove_stone(self.moving_stone_num)
            if self.mode == 2:
                ...
            else:
                self.human_player_on_move = False
                self.computer_player_move()
        self.firstmove = False
        self.update_score()   
    # make computer move and human continue
    def computer_player_move(self):
        if self.mode == 1:
            x,y,instructions,id = self.game.p1_move() 
        elif self.mode == -1:
            x,y,instructions,id = self.game.p2_move() 
        if x != None:
            self.game_widget.remove_stone(id)
            self.make_move(x,y,instructions,self.game_widget.table_of_stones.stones[id][0].color)
            self.human_player_on_move = True
        else:
            self.end_game()
    # computer vs computer mode
    def computer_vs_computer(self):
        while True:
            x,y,instructions,id = self.game.p1_move() 
            if x != None:
                self.game_widget.remove_stone(id)
                self.make_move(x,y,instructions,self.game_widget.table_of_stones.stones[id][0].color)
            else:
                break
            x,y,instructions,id = self.game.p2_move() 
            if x != None:
                self.game_widget.remove_stone(id)
                self.make_move(x,y,instructions,self.game_widget.table_of_stones.stones[id][0].color)
            else:
                break
        self.end_game()

# OTHERS
    def update_score(self):
        self.game_widget.update_score(self.game.p1_score, self.game.p2_score)

    def end_game (self):
        print("konec") 
        #self.add_widget(Popup())



if __name__ == "__main__":
    class TestApp(App):
        def build(self):
            board = create_random_board()
            return GameWin(board,stones,stones_for_players,colors,0,1)
    TestApp().run()