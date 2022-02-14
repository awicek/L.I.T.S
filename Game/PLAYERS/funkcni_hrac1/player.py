import random   
import base

#11 řádek v control_base


class Stone ():
    # must have for game:
    # self.color
    # self.max_x
    # self.max_y
    # self.matrix
    # self.id

    # others
    # self.r0_180
    # self.r90_270

    def __init__(self,informace,id):# DONE TESTED 
        self.color, self.max_x, self.max_y, self.matrix = self.create(informace)
        self.id = id
        self.r0_180 = self.create_rotation1()
        self.r90_270 =  self.create_rotation2()

    def create (self, input):        # DONE TESTED 
        color = input[0]
        input2 = list()
        for i in range(len(input[1:])//2):
            input2.append([input[i*2+1], input[i*2+2]])

        input2.sort()
        x_min = input2[0][0]
        x_max = input2[-1][0]

        input2.sort(key = lambda x: x[1])

        y_min = input2[0][1]
        y_max = input2[-1][1]

        x = x_max - x_min +1
        y = y_max - y_min +1
        matice = [[0 for _ in range(y)] for __ in range(x)]
        
        for i in input2:
            matice[i[0]-x_min][i[1]-y_min] = color
        return color ,len(matice),len(matice[0]),matice
    
    def create_rotation1 (self):    # DONE TESTED 
        rotations = list()
        r1 = list()
        for i,j in enumerate(self.matrix):
            for k,l in enumerate(j):
                if l > 0:
                    r1.append([i,k])
        r2 = list()
        for i in range(self.max_x):
            for j in range(self.max_y):
                if self.matrix[self.max_x - i -1][self.max_y - j -1] > 0:
                    r2.append([i,j])
        if r1 == r2:
            rotations.append(r1)
        else:    
            rotations.append(r1)
            rotations.append(r2)
        return rotations

    def create_rotation2 (self):    # DONE TESTED 
        rotations = list()
        r2 = list()
        r1 = list()
        for i in range(self.max_y):
            for j in range(self.max_x):
                if self.matrix[j][self.max_y -1 -i ] > 0:
                    r1.append([i,j])
        for i in range(self.max_y):
            for j in range(self.max_x):
                if self.matrix[self.max_x - j -1][i] > 0:
                    r2.append([i,j])
        if r1 == r2:
            rotations.append(r1)
        else:    
            rotations.append(r1)
            rotations.append(r2)
        return rotations

    def print_f (self):             # DONE TESTED 
        for i in self.matrix:
            print(i)
        print()
    
    def print_r (self):             # DONE TESTED 
        print("---rotations---")
        for r in self.r0_180:
            for i in range(self.max_x):
                for j in range(self.max_y):
                    if [i,j] in r:
                        print(self.color, end=" ")
                    else:
                        print(0,end=" ")
                print()
            print("-----")
        for r in self.r90_270:
            for i in range(self.max_y):
                for j in range(self.max_x):
                    if [i,j] in r:
                        print(self.color, end=" ")
                    else:
                        print(0,end=" ")
                print()
            print("-----")                          

class Player(base.BasePlayer):

    # self.marks
    # self.board
    # self.stones
    # self.freeStones

    # self.my_stones
    
    def __init__(self, name, board, marks, stones, player): # OK
        def rozbal (pole):
            if pole == []:
                return []
            if type(pole[0]) is list:
                return rozbal(pole[0]) + rozbal(pole[1:])
            else:
                return [pole[0]] + rozbal(pole[1:])
        base.BasePlayer.__init__(self, name, board, marks, stones, player)
        self.algorithm = "NaMe Of YoUr MeThOd. WiLl Be UsEd In ToUrNaMeNt MoDe"
        self.my_stones = list()
        for i,j in enumerate(self.stones):
            self.my_stones.append(Stone(rozbal(j),i))

    def move(self):
        konntrola = True
        for i in self.board:
            for j in i:
                if j >0:
                    konntrola = False
                    break

        if konntrola:
            policko = self.my_stones[0]
            tah = self.predelej_tah([policko.id,policko.r0_180[0],0,0])
            return tah
        else: 
            tahy = self.f_possible() # stone.id,r,i,k
            if tahy:
                tah = random.choice(tahy)
                tah = self.predelej_tah(tah)
                return tah
            return []
        
    #--- METHODS FOR TESTING ---------------
    def testmove(self,x,y,stone):
        for i,j in enumerate(stone.r0_180 + stone.r90_270):
            print(j)
            a = self.control_base(x,y,j,stone.color)
            print(a,i)
    #-------------------------------------------------


    def f_possible (self):
        possible_m = list()
        for i,stone in enumerate(self.my_stones):
            if self.freeStones[i] == True:
                #ROTACE 0 A 180
                for i,j in (enumerate(self.board[: 1- stone.max_x]) if stone.max_x > 1 else  enumerate(self.board)):
                    for k,l in (enumerate(j[: 1-stone.max_y ]) if stone.max_y > 1 else enumerate(j)):
                        for r in stone.r0_180:
                            if self.control_base(i,k,r,stone.color):
                                possible_m.append([stone.id,r,i,k])
                #ROTACE 90 A 270
                for i,j in (enumerate(self.board[: 1- stone.max_y]) if stone.max_y > 1 else  enumerate(self.board)):
                    for k,l in (enumerate(j[: 1-stone.max_x ]) if stone.max_x > 1 else enumerate(j)):
                        for r in stone.r90_270:
                            if self.control_base(i,k,r,stone.color):
                                possible_m.append([stone.id,r,i,k])
        return possible_m
    #------------FUNCTIONS FOR F_POSSIBLE-------------
    def control_base(self,xx,yy,pos,color):
        control = False
        added = list()
        for i,j in pos:
            x,y = i+xx,yy+j
            # kontrola jesti se pole vejde, případne vepsání 9
            if self.board[x][y] > 0:
                self.delete(added)
                return False
            else:
                self.board[x][y] = 9
                added.append([x,y])

            # kontrola jesti se neporuší pravidlo o čtevrcích
            if self.control_rect(x,y):
                self.delete(added)
                return False

            # kontrola jestli se neporuší pravidlo barev
            c2 = self.control_color(color,x,y)
            if c2 == 0:
                self.delete(added)
                return False
            elif c2 == 1:
                control = True
        if control:
            self.delete(added)
            return True
        self.delete(added)
        return False
    # TRUE = square found
    # FALSE = test pass 
    def control_rect(self,x,y):
        for i in range(-1,1):
            for j in range(-1,1):
                c = 0
                for a,b in [[0,0],[0,1],[1,0],[1,1]]:
                    
                    if -1 < x+i+a < len(self.board) and -1 < y+j+b < len(self.board[0]):
                        if self.board[x+i+a][y+j+b] == 0:
                            break
                        else:
                            c +=1
                    else: 
                        break
                if c == 4:
                    return True
        return False
    # 0 = touch with same color
    # 1 = touch with different color
    # 2 = no touch at all
    def control_color (self, color, x,y):
        kontola = False
        for i,j in [[1,0],[-1,0],[0,-1],[0,1]]:
            if -1 < x+i < len(self.board) and -1 < y+j < len(self.board[0]):
                if self.board[x+i][y+j] == 0:
                    ...
                elif self.board[x+i][y+j] == color:
                    return  0
                elif self.board[x+i][y+j] == 9:
                    ...
                else:
                    kontola = True
        if kontola:
            return 1
        return -1
    # it delletes added "nines" (10th line in control_base)
    def delete (self, field):#HOTOVO 
        for x,y in field:
            self.board[x][y] = 0

    #-------------------------------------------------
    def predelej_tah(self,data):
        id,pole,x,y = data
        vysledek = list()
        vysledek.append(id)
        tahy = list()
        for i,j in pole:
            tahy.append([i + x,j+y])
        vysledek.append(tahy)
        return vysledek




