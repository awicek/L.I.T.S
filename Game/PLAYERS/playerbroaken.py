import sys
import random
import copy
import base
import random

from draw import Drawer

class Policko ():
    def __init__(self,informace,id):
        self.barva, self.max_x, self.max_y, self.matice = self.vytvor_tvar(informace)
        self.id = id

    def vypis (self):
        for i in self.matice:
            for j in i:
                print (j, end=" ")
            print ()
             
    def vytvor_tvar (self, pole):
        barva = pole[0]
        pole2 = list()
        for i in range(len(pole[1:])//2):
            pole2.append([pole[i*2+1], pole[i*2+2]])

        pole2.sort()
        x_min = pole2[0][0]
        x_max = pole2[-1][0]

        pole2.sort(key = lambda x: x[1])

        y_min = pole2[0][1]
        y_max = pole2[-1][1]

        x = x_max - x_min +1
        y = y_max - y_min +1
        matice = [[0 for _ in range(y)] for __ in range(x)]
        
        for i in pole2:
            matice[i[0]-x_min][i[1]-y_min] = barva
        return barva ,len(matice),len(matice[0]),matice


class Player(base.BasePlayer):
    # self.marsk = tam kde jsou značky
    # self.board = to kde jsou položený šutry
    # self.stones = to kde jsou položený šutry
    # self.freeStones = které šutry můžu používat
    def __init__(self, name, board, marks, stones, player):
        def rozbal (pole):
            if pole == []:
                return []
            if type(pole[0]) is list:
                return rozbal(pole[0]) + rozbal(pole[1:])
            else:
                return [pole[0]] + rozbal(pole[1:])

        

        base.BasePlayer.__init__(self, name, board, marks, stones, player)  #do not change this line!!
        self.algorithm = "name of your method. Will be used in tournament mode"

        self.my_stones = list()
        for i,j in enumerate(self.stones):
            self.my_stones.append(Policko(rozbal(j),i))

    def move(self):
        if False in self.freeStones:
            possiblemoves = self.find_possible()
            if possiblemoves:
                return self.stone_to_move(random.choice(possiblemoves))
            return []
        else:
            return self.stone_to_move([4,0,self.my_stones[0],1])
    
    def test (self, stone, i,j):
        
        listt = list()
        a = self.kontrola_policko1(stone, i,j)
        if a:
            listt.append(["jedna",self.stone_to_move([i,j,stone,1])])

        a = self.kontrola_policko2(stone, i,j)
        if a:
            listt.append(["dva",self.stone_to_move([i,j,stone,2])])

        a = self.kontrola_policko3(stone, i,j)
        if a:
            listt.append(["tri",self.stone_to_move([i,j,stone,3])])

        a = self.kontrola_policko4(stone, i,j)
        if a:
            listt.append(["ctyri",self.stone_to_move([i,j,stone,4])])
        return listt

    def find_possible (self):
        solution = list()
        for i,stone in enumerate(self.my_stones):
            if self.freeStones[i] == True:
                for i,j in (enumerate(self.board[: 1- stone.max_x]) if stone.max_x > 1 else  enumerate(self.board)):
                    for k,l in (enumerate(j[: 1-stone.max_y ]) if stone.max_y > 1 else enumerate(j)):
                        #nulová rotace
                        a = self.kontrola_policko1(stone, i,k)   
                        if a != False:
                            solution.append([i,k,stone,1])
                        # rotace o 180
                        a = self.kontrola_policko2(stone, i,k)   
                        if a != False:
                            solution.append([i,k,stone,2])
                # rotace o 90 pravo a o 90 levo

                for i,j in (enumerate(self.board[: 1- stone.max_y]) if stone.max_y > 1 else  enumerate(self.board)):
                    for k,l in (enumerate(j[: 1-stone.max_x ]) if stone.max_x > 1 else enumerate(j)):
                        # rotace o 90 pravo
                        a = self.kontrola_policko3(stone, i,k)   
                        if a != False:
                            solution.append([i,k,stone,3])
                        # rotace o 90 levo
                        a = self.kontrola_policko4(stone, i,k)   
                        if a != False:
                            solution.append([i,k,stone,4])
        return solution

    def kontrola_policko1 (self,policko,x,y):
        kontrola = False
        vlozenepolicka = list()

        for i in range(x, x + policko.max_x):
            for j in range(y,y+ policko.max_y):
                if self.board[i][j] != 0:
                    if policko.matice[i-x][j-y] != 0:
                        self.vymaz(vlozenepolicka)
                        return False
                    else:
                        ...
                elif policko.matice[i-x][j-y] != 0:
                    self.board[i][j] == -1
                    vlozenepolicka.append([i,j])

                    a = self.kontrola_barva(i,j,policko.barva)
                    if a == 0:
                        self.vymaz(vlozenepolicka)
                        return False
                    elif a == 1:
                        kontrola = True
                    
                    b = self.kontrola_cterec(i,j)
                    if b == False:
                        self.vymaz(vlozenepolicka)
                        return False
        if kontrola == True:
            self.vymaz(vlozenepolicka)
            return True
        self.vymaz(vlozenepolicka)
        return False

    def kontrola_policko2 (self,policko,x,y):
        kontrola = False
        vlozenepolicka = list()

        for i in range(x, x + policko.max_x):
            for j in range(y,y+ policko.max_y):
                if self.board[i][j] != 0:
                    if policko.matice[policko.max_x - i + x-1][policko.max_y - j + y-1] != 0:
                        self.vymaz(vlozenepolicka)
                        return False
                    else:
                        ...
                elif policko.matice[policko.max_x - i + x-1][policko.max_y - j + y-1] != 0:
                    self.board[i][j] == -1
                    vlozenepolicka.append([i,j])

                    a = self.kontrola_barva(i,j,policko.barva)
                    if a == 0:
                        self.vymaz(vlozenepolicka)
                        return False
                    elif a == 1:
                        kontrola = True
                    
                    b = self.kontrola_cterec(i,j)
                    if b == False:
                        self.vymaz(vlozenepolicka)
                        return False
        if kontrola == True:
            self.vymaz(vlozenepolicka)
            return True
        self.vymaz(vlozenepolicka)
        return False

    def kontrola_policko4 (self,policko,x,y):
        kontrola = False
        vlozenepolicka = list()

        for i in range(x, x + policko.max_y):
            for j in range(y,y+ policko.max_x):
                if self.board[i][j] != 0:
                    if policko.matice[policko.max_x - j + y-1][i-x] != 0:
                        self.vymaz(vlozenepolicka)
                        return False
                    else:
                        ...
                if policko.matice[policko.max_x - j + y-1][i-x] != 0:
                    self.board[i][j] == -1
                    vlozenepolicka.append([i,j])

                    a = self.kontrola_barva(i,j,policko.barva)
                    if a == 0:
                        self.vymaz(vlozenepolicka)
                        return False
                    elif a == 1:
                        kontrola = True
                    
                    b = self.kontrola_cterec(i,j)
                    if b == False:
                        self.vymaz(vlozenepolicka)
                        return False
        if kontrola == True:
            self.vymaz(vlozenepolicka)
            return True
        self.vymaz(vlozenepolicka)
        return False

    def kontrola_policko3 (self,policko,x,y):
        kontrola = False
        vlozenepolicka = list()

        for i in range(x, x + policko.max_y):
            for j in range(y,y+ policko.max_x):
                if self.board[i][j] != 0:
                    if policko.matice[j-y][policko.max_y -1 -i + x]!= 0:
                        self.vymaz(vlozenepolicka)
                        return False
                    else:
                        ...
                if policko.matice[j-y][policko.max_y -1 -i + x]!= 0:
                    self.board[i][j] == -1
                    vlozenepolicka.append([i,j])

                    a = self.kontrola_barva(i,j,policko.barva)
                    if a == 0:
                        self.vymaz(vlozenepolicka)
                        return False
                    elif a == 1:
                        kontrola = True
                    
                    b = self.kontrola_cterec(i,j)
                    if b == False:
                        self.vymaz(vlozenepolicka)
                        return False
        if kontrola == True:
            self.vymaz(vlozenepolicka)
            return True
        self.vymaz(vlozenepolicka)
        return False

    def kontrola_cterec (self,x,y):
        for i in range(-1,1):
            for j in (-1,1):
                c = 0
                for a,b in [[0,0],[0,1],[1,0],[1,1]]:
                    if -1 < x+i+a < len(self.board) and -1 < y+j+b < len(self.board[0]):
                        if self.board[x+i+a][y+j+b] == 0:
                            break
                        else:
                            c +=1
                if c == 4:
                    return False
        return True

    def kontrola_barva(self,x,y,barva):
        kontola = False
        for i,j in [[1,0],[-1,0],[0,-1],[0,1]]:
            if -1 < x+i < len(self.board) and -1 < y+j < len(self.board[0]):
                if self.board[x+i][y+j] == 0:
                    ...
                elif self.board[x+i][y+j] == barva:
                    return  0
                elif self.board[x+i][y+j] == -1:
                    ...
                else:
                    kontola = True
        if kontola:
            return 1
        return -1

    def stone_to_move(self,data):
        x,y,stone,rotace = data
        
        move = list()
        move.append(stone.id)
        place = list()

        if rotace == 1:
            for i in range(x, x + stone.max_x):
                for j in range(y,y+ stone.max_y):
                    if stone.matice[i-x][j-y] != 0:
                        place.append([i,j])
        elif rotace == 2:
            for i in range(x, x + stone.max_x):
                for j in range(y,y+ stone.max_y):
                    if stone.matice[stone.max_x - i + x-1][stone.max_y - j + y-1] != 0:
                        place.append([i,j])
                
        elif rotace == 4:
            for i in range(x, x + stone.max_y):
                for j in range(y,y+ stone.max_x):
                    if stone.matice[stone.max_x - j + y-1][i-x] != 0:
                        place.append([i,j])
        elif rotace == 3:
            for i in range(x, x + stone.max_y):
                for j in range(y,y+ stone.max_x):
                    if stone.matice[j-y][stone.max_y -1 -i + x]!= 0:
                        place.append([i,j])
                        
        move.append(place)
        return move

    def vymaz(self,pole):
        for i,j in pole:
            self.board[i][j] == 0

    def vypis(self):
        for i in self.board:
            print(i)


stones = base.loadStones("C:\\Users\\richa\\OneDrive\\Dokumenty\\Python\\škola\\lekce_9SEM\\stones.txt")
board, marks = base.makeBoard10()
p1 = Player("pepa", board, marks, stones, 1)
p2 = Player("franta", board, marks, stones, -1)
m = p1.move()  #first player, we assume that a corrent output is returned

if len(m) == 0:
    p1play = False
else:
    stoneIdx, stone = m
    stoneColor = stones[stoneIdx][0]
    base.writeBoard(p1.board, stone, stoneColor) #write stone to player1's board
    base.writeBoard(p2.board, stone, stoneColor) #write stone to player2's board
    p1.freeStones[ stoneIdx ] = False #tell player1 which stone is used
    p2.freeStones[ stoneIdx ] = False #tell player2 which stone is used

p2.vypis()
p2.my_stones[1].vypis()
a = (p2.test(p2.my_stones[1],6,0))
print(a)
base.writeBoard(p1.board, a[0][1][1], p2.my_stones[1].barva) #write stone to player1's board
base.writeBoard(p2.board, a[0][1][1], p2.my_stones[1].barva) #write stone to player2's board
p2.vypis()


if __name__ == "__fmain__":

    #load stones from file
    stones = base.loadStones("C:\\Users\\richa\\OneDrive\\Dokumenty\\Python\\škola\\lekce_9SEM\\stones.txt")

    #prepare board and marks
    board, marks = base.makeBoard10()

    #create both players    
    p1 = Player("pepa", board, marks, stones, 1)
    p1.vypis()
    p2 = Player("franta", board, marks, stones, -1)

    #not necessary, only if you want to draw board to png files
    d = Drawer()
    d.draw(p1.board, p1.marks, "init.png")

    moveidx = 0
    while True:
        p1play = True
        p2play = True

        m = p1.move()  #first player, we assume that a corrent output is returned

        #the following if/else is simplified. On Brute, we will check if return value
        #from move() is valid ...
        
        if len(m) == 0:
            p1play = False
        else:
            stoneIdx, stone = m
            stoneColor = stones[stoneIdx][0]
            base.writeBoard(p1.board, stone, stoneColor) #write stone to player1's board
            base.writeBoard(p2.board, stone, stoneColor) #write stone to player2's board
            p1.freeStones[ stoneIdx ] = False #tell player1 which stone is used
            p2.freeStones[ stoneIdx ] = False #tell player2 which stone is used
                    
        d.draw(p2.board, p2.marks, "move-{:02d}a.png".format(moveidx)) #draw to png

        #now we call player2 and update boards/freeStones of both players
        m = p2.move()  
        if len(m) == 0:
            p2play = False
        else:
            stoneIdx, stone = m
            stoneColor = stones[stoneIdx][0]
            base.writeBoard(p1.board, stone, stoneColor)
            base.writeBoard(p2.board, stone, stoneColor)
            p1.freeStones[ stoneIdx ] = False
            p2.freeStones[ stoneIdx ] = False
        
        d.draw(p1.board, p1.marks, "move-{:02d}b.png".format(moveidx))
        

        #if both players return [] from move, the game ends
        if p1play == False and p2play == False:
            print("end of game")
            break
    
        moveidx+=1
        print(" -- end of move ", moveidx, " score is ", p1.score(p1.player), p1.score(-p1.player) )