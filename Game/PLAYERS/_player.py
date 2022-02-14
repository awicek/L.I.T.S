import sys
import random
import copy
import _base as base

from draw import Drawer

class Player(base.BasePlayer):
    class policko ():
        def __init__(self,informace):
            self.barva, self.max_x, self.max_y, self.matice = self.vytvor_tvar(informace)
            
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
    
    def __init__(self, name, board, marks, stones, player):

        base.BasePlayer.__init__(self, name, board, marks, stones, player)  #do not change this line!!
        self.algorithm =  "name of your method. Will be used in tournament mode"
        self.stones = list()
        

    def move(self):
       # return [ stoneIdx, [ stonePosition] ]
       # return [] - když chci skipnout tah
        return []

    


import time
import sys
# CLASA POLICek
class policko ():
    def __init__(self,informace):
        self.barva, self.max_x, self.max_y, self.matice = self.vytvor_tvar(informace)
        
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

# NACTENI VSTUPU

# REKURZE  NA HLDÁNÍ (MATICE POLICKA)

def kontrola_policko1 (matice,kostka, x,y):
    vysledek = list()
    for i in matice:
        radek = list()
        for j in i:
            radek.append(j)
        vysledek.append(radek)

    for i in range(x, x + kostka.max_x):
        for j in range(y,y+ kostka.max_y):
            if vysledek[i][j] != 0:
                if kostka.matice[i-x][j-y] != 0:
                    return False
                else:
                    ...
            else: 
                vysledek[i][j] =  kostka.matice[i-x][j-y]
    return vysledek
                
def kontrola_policko2 (matice,kostka, x,y):
    vysledek = list()
    for i in matice:
        radek = list()
        for j in i:
            radek.append(j)
        vysledek.append(radek)

    for i in range(x, x + kostka.max_x):
        for j in range(y,y+ kostka.max_y):
            if vysledek[i][j] != 0:
                if kostka.matice[kostka.max_x - i + x-1][kostka.max_y - j + y-1] != 0:
                    return False
                else:
                    ...
            else: 
                vysledek[i][j] =  kostka.matice[kostka.max_x - i + x-1][kostka.max_y - j + y-1]
    return vysledek

def kontrola_policko3 (matice,kostka, x,y):
    vysledek = list()
    for i in matice:
        radek = list()
        for j in i:
            radek.append(j)
        vysledek.append(radek)

    for i in range(x, x + kostka.max_y):
        for j in range(y,y+ kostka.max_x):
            if vysledek[i][j] != 0:
                if kostka.matice[kostka.max_x - j + y-1][i-x] != 0:
                    return False
                else:
                    ...
            else: 
                vysledek[i][j] =  kostka.matice[kostka.max_x - j + y-1][i-x]
    return vysledek

def kontrola_policko4 (matice,kostka, x,y):
    vysledek = list()
    for i in matice:
        radek = list()
        for j in i:
            radek.append(j)
        vysledek.append(radek)

    for i in range(x, x + kostka.max_y):
        for j in range(y,y+ kostka.max_x):
            if vysledek[i][j] != 0:
                if kostka.matice[j-y][kostka.max_y -1 -i + x]!= 0:
                    return False
                else:
                    ...
            else: 
                vysledek[i][j] =  kostka.matice[j-y][kostka.max_y -1 -i + x]
    return vysledek


def vyres(policka, matice,):
    if not policka:
        print(matice)
        sys.exit()
    for i,j in (enumerate(matice[: 1- policka[0].max_x]) if policka[0].max_x > 1 else  enumerate(matice)):
        for k,l in (enumerate(j[: 1-policka[0].max_y ]) if policka[0].max_y > 1 else enumerate(j)):
            #nulová rotace
            a = kontrola_policko1(matice, policka[0], i,k)   # kontrola jestli se do matice dá vepsat
            if a != False:
                vyres(policka[1:],a)
            # rotace o 180
            a = kontrola_policko2(matice, policka[0], i,k)   # kontrola jestli se do matice dá vepsat
            if a != False:
                vyres(policka[1:],a)
    # rotace o 90 pravo a o 90 levo
    for i,j in (enumerate(matice[: 1- policka[0].max_y]) if policka[0].max_y > 1 else  enumerate(matice)):
        for k,l in (enumerate(j[: 1-policka[0].max_x ]) if policka[0].max_x > 1 else enumerate(j)):
            # rotace o 90 pravo
            a = kontrola_policko3(matice, policka[0], i,k)   # kontrola jestli se do matice dá vepsat
            if a != False:
                vyres(policka[1:],a)
            # rotace o 90 levo
            a = kontrola_policko4(matice, policka[0], i,k)   # kontrola jestli se do matice dá vepsat
            if a != False:
                vyres(policka[1:],a)






