import GAME.base as base
import copy
from collections import defaultdict
from PLAYERS.player_data import rotations_names, all_rotations, connections, forbiden_coords, safe_dict

def unwrap (lst):
    if lst == []:
        return []
    if type(lst[0]) is list:
        return unwrap(lst[0]) + unwrap(lst[1:])
    else:
        return [lst[0]] + unwrap(lst[1:]) 

class Move ():
    def __init__ (self, name:str, x:int, y:int, color:int, stone_id:int, coords:list ):
        self.name = name
        self.x = x
        self.y = y
        self.color = color 
        self.stone_id = stone_id
        self.coords = coords
        self.score = None
        self.score_tab = None
        self.free = 1
    
class Stone ():
    # # #    # # # #   # # #   # #   #   #   # # #   # #     # # #     # 
      #                    #     #   # # #     #       #             # # #
      #                                                # #             #

    def __init__(self,informace,id):# DONE TESTED 
        self.color, self.max_x, self.max_y, self.matrix = self.create(informace)
        self.id = id
        self.r0_180 = self.create_rotation1()
        self.r90_270 =  self.create_rotation2()
        self.rotations = list()

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
        newrotations = list()
        for i in rotations:
            if i in self.r0_180:
                ...
            else:
                newrotations.append(i)
        return newrotations

class Player():
    def __init__(self, name, board, marks, stones, player):

        base.BasePlayer.__init__(self, name, board, marks, stones, player)
        self.algorithm = "NaMe Of YoUr MeThOd. WiLl Be UsEd In ToUrNaMeNt MoDe"

        self.rotations_names = rotations_names
        self.all_rotations =  all_rotations
        self.connections = connections
        self.safe_dict = safe_dict
        self.forbiden_coords = forbiden_coords

        self.my_stones = list()
        for i,j in enumerate(self.stones):
            self.my_stones.append(Stone(unwrap(j),i))
        self.add_rotations_to_my_stones()

        self.rotation_possible_place = self.create_stone_places() # where is NOT possible to plcase a specific rotations 
        self.elimination_board = self.create_elimination_board()  # which cells deletes which stones
        self.elimination_stone = [[] for _ in range(len(self.my_stones))]
        self.old_board = [[0 for _ in range(len(self.board[0]))] for __ in range(len(self.board))]
        self.old_freeStones = copy.deepcopy(self.freeStones)
        self.avalible_marks = [[0 for _ in range(len(self.board[0]))] for __ in range(len(self.board))]
        self.all_moves = list()
        self.rate_table = [[0,0,0],[7,0,0]]
        self.first_move = True

        #[x,xs,xsh,o,os,osh]
        if self.player == 1: # x 1
            self.score_tab = self.rate_table[0] + self.rate_table[1]
        else : # o -1
            self.score_tab = self.rate_table[1] + self.rate_table[0]

# MOVE
    def move (self):
        self.find_new_moves()

        # first move logic
        if self.first_move:
            self.first_move = False
            if self.all_moves:
                best_move = self.all_moves[0]
                best_move_score = self.all_moves[0].score
                for i in self.all_moves:
                    if i.score > best_move_score:
                        best_move = i
                        best_move_score = i.score
                return self.create_final_move(best_move)
            c = 0
            for i in self.board:
                for j in i:
                    if j > 0:
                        c+=1
            if c > 0:
                return[]
            else:
                if len(self.board) == 10 and len(self.board[0]) == 10:
                    moves = self.f_possible_area([0,0,9,9])
                    best_move = moves[0]
                    best_move_score = moves[0].score
                    for i in moves:
                        if i.score > best_move_score:
                            best_move = i
                            best_move_score = i.score
                    return self.create_final_move(best_move)
                elif len(self.board) == 15 and len(self.board[0]) == 15:
                    moves = self.f_possible_area(self.best_starting_area())
                    best_move = moves[0]
                    best_move_score = moves[0].score
                    for i in moves:
                        if i.score > best_move_score:
                            best_move = i
                            best_move_score = i.score
                    return self.create_final_move(best_move)
                else:
                    policko = self.my_stones[0]
                    tah = self.predelej_tah([policko.id,policko.r0_180[0],0,0])
                    return tah
        # ohters moves
        if self.all_moves:
            best_move = self.all_moves[0]
            best_move_score = self.all_moves[0].score
            for i in self.all_moves:
                if i.score > best_move_score:
                    best_move = i
                    best_move_score = i.score
            return self.create_final_move(best_move)

        return []

#---------- OLD MOVE METHODS ----------------------
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

    def f_possible_area (self, area):
        x,y,xx,yy = area
        # a = Move("uplně jedno","x","y","color","stone_id", "coords")
        possible_m = list()
        for i,stone in enumerate(self.my_stones):
            if self.freeStones[i] == True:
                for i in range(x,xx-stone.max_x+2):
                    for j in range(y,yy-stone.max_y+2):
                        for r in stone.r0_180:
                            a = Move("f",i,j,stone.color,stone.id,r)
                            self.rate_move(a)
                            possible_m.append(a)
                for i in range(x,xx-stone.max_y+2):
                    for j in range(y,yy-stone.max_x+2):
                        for r in stone.r90_270:
                            a = Move("f",i,j,stone.color,stone.id,r)
                            self.rate_move(a)
                            possible_m.append(a)
        return (possible_m)
        
    def predelej_tah(self,data):
        id,pole,x,y = data
        vysledek = list()
        vysledek.append(id)
        tahy = list()
        for i,j in pole:
            tahy.append([i + x,j+y])
        vysledek.append(tahy)
        return vysledek
#--------------------------------------------------

#---------- METHOSD FOR CONTROL ----- self.control_base(x,y,[coords],color) -> Ttrue/False
    def control_base(self,xx,yy,pos,color):
        control = False
        added = list()
        for i,j in pos:
            x,y = i+xx,yy+j
            if x >= len(self.board) or y >= len(self.board):
                self.delete(added)
                return False
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

#--------- INICIALIZATIONS METHODS ----------------
    # PREMADE 
    def create_all_rotations (self):
        a = list()
        for i in self.my_stones:
            if i.color == 1:
                row = list()
                for k in i.r0_180 + i.r90_270:
                    row.append(k)   
                a.append(row)
        
    def create_rotations_names (self):
        rotations = dict()
        for i,j in enumerate(self.all_rotations):
            for k,l in enumerate(j):
                code = self.code_from_coords(l)
                rotations[code] = (i,k)
          
    def code_from_coords (self,coords,c = False):
        code = ""
        minx, maxx  = 15,0
        miny, maxy  = 15,0
        for x,y in coords:
            if x < minx:
                minx = x
            if x > maxx:
                maxx = x
            if y < miny: 
                miny = y
            if y > maxy:
                maxy = y
        matrix = [[0 for _ in range(maxy-miny+1)] for __ in range(maxx - minx +1)]
        for x,y in coords:
            matrix[x-minx][y-miny] = 1
        for j in matrix:
            for k in j:
                if k == 0:
                    code += "0"
                else:
                    code += "1"    
        if c:
            return str(maxx- minx) + str(maxy-miny) + code ,minx ,miny
        return str(maxx- minx) + str(maxy-miny) + code 

    def create_forbiden_coords (self):
        forbiden_coords = dict()
        for i,j in enumerate(self.all_rotations):
            for k,l in enumerate(j):
                same_color = list()
                diff_color = list()
                square = list()
                maxx,maxy = 0,0
                for x,y in l:
                    if x > maxx:
                        maxx = x
                    if y > maxy:
                        maxy = y
                matrix = [[0 for _ in range(maxy+3)] for __ in range(maxx+3)]
                for x,y in l:
                    matrix[x+1][y+1] = 1
                for m,n in enumerate(matrix):
                    for o,p in enumerate(n):
                        if p == 1:
                            same_color.append([m-1,o-1])
                        else:
                            for a,b in [[0,1],[1,0],[-1,0],[0,-1]]:
                                xx = m + a
                                yy = o + b
                                if 0 <= xx < len(matrix) and 0 <= yy < len(matrix[0]):
                                    if matrix[xx][yy] == 1:
                                        diff_color.append([m-1,o-1])
                                        break
                forbiden_coords[str(i)+str(k)] = [same_color,diff_color]    
        return forbiden_coords
              
    #----------------------------------------------
    def best_starting_area (self):
        values = [[0,0] for _ in range (13)]
        areas = [[0,0,4,4],[0,5,4,9],[0,10,4,14],[5,0,9,4],[5,5,9,9],[5,10,9,14],[10,0,14,4],[10,5,14,9],[10,10,14,14],[2,2,6,6],[2,8,6,12],[8,2,12,6],[8,8,12,12]]
        player = self.player
        if player == 1: 
            oponent = -1
        else:
            oponent = 1
        for i in range (len(self.board)):
            for j in range(len(self.board)):
                if self.marks[i][j] == player:
                    a = i // 5 * 3 + j // 5 
                    values[a][0] += 1
                    if 1 < i < 7 and 1 < j < 7:
                        values[9][0] += 1
                    elif 1 < i < 7 and 7 < j < 13:
                        values[10][0] += 1
                    elif 7 < i < 13 and 1 < j < 7:
                        values[11][0] += 1
                    elif 7 < i < 13 and 7 < j < 13:
                        values[12][0] +=1
                elif self.marks[i][j] == oponent:
                    a = i // 5 * 3 + j // 5 
                    values[a][1] += 1
                    if 1 < i < 7 and 1 < j < 7:
                        values[9][1] += 1
                    elif 1 < i < 7 and 7 < j < 13:
                        values[10][1] += 1
                    elif 7 < i < 13 and 1 < j < 7:
                        values[11][1] += 1
                    elif 7 < i < 13 and 7 < j < 13:
                        values[12][1] +=1
        a = defaultdict()
        a[0] = [0,1,9,3]
        a[1] = [0,1,2,9,10]
        a[2] = [1,10,5,2]
        a[3] = [0,9,11,6,3]
        a[4] = [9,10,11,12,4]
        a[5] = [10,12,2,8,5]
        a[6] = [3,11,7,6]
        a[7] = [6,11,12,8,7]
        a[8] = [7,12,4,8]
        a[9] = [0,1,4,3,9]
        a[10] = [1,2,4,5,10]
        a[11] = [3,4,6,7,11]
        a[12] = [4,5,7,8,12]
        maxdif = 0
        for i in a[0]:
            maxdif  -= values[i][0]
        index = 0
        for i  in range(len(values)):
            sum = 0
            for k in a[i]:
                sum -= values[k][0]
            sum = (sum / len(a[i])) * 5
            if sum > maxdif:
                maxdif = sum
                index = i

        return areas[index]
  
    def print_squares (self,a):
        
        print(a[0][0],a[1][0],a[2][0],sep= "   ")
        print(f"  {a[9][0]}   {a[10][0]}")
        print(a[3][0],a[4][0],a[5][0],sep= "   ")
        print(f"  {a[11][0]}   {a[12][0]}")
        print(a[6][0],a[7][0],a[8][0],sep= "   ")

        print()

        print(a[0][1],a[1][1],a[2][1],sep= "   ")
        print(f"  {a[9][1]}   {a[10][1]}")
        print(a[3][1],a[4][1],a[5][1],sep= "   ")
        print(f"  {a[11][1]}   {a[12][1]}")
        print(a[6][1],a[7][1],a[8][1],sep= "   ")

        print(len(self.my_stones))

    def add_rotations_to_my_stones (self):
        for i in self.my_stones:
            for j in i.r0_180 + i.r90_270:
                code = self.code_from_coords(j)
                a,b = self.rotations_names[code]
                i.rotations.append(str(a)+str(b))

    def create_stone_places (self):
        places = dict()
        for i in self.stones:
            for j in self.my_stones:
                for k in j.rotations:
                    place = [[[0 for _ in range(len(self.board))] for __ in range(len(self.board))] for ___ in range(3)]
                    places[k] = place
        return places

    def create_elimination_board (self):
        matrix = list()
        for i in range(len(self.board)+3):
            row = list()
            for j in range(len(self.board)+3):
                a =[[],[],[]]
                row.append(a)
            matrix.append(row)
        return matrix
#--------------------------------------------------

#------- METHODS FOR NEW STONES ------------------
    def find_recent_moves (self):
        # move == (color,[x,y],[x,y],....)
        moves = list()
        def find_whole_move (x,y):
            color = self.board[x][y]
            stack = [[x,y]]
            move = [color]
            used = list()
            while stack:
                xx,yy = stack.pop()
                if [xx,yy] in used:
                    ...
                else:
                    used.append([xx,yy])
                    if 0 <= xx < len(self.old_board) and 0 <= yy < len(self.board):
                        if self.board[xx][yy] == color:
                            move.append([xx,yy])
                            self.old_board[xx][yy] = color
                            for i,j in [[1,0],[0,1],[0,-1],[-1,0]]:
                                stack.append([xx+i,yy+j])
            return move

        for i,j in enumerate(self.board):
            for k,l in enumerate(j):
                if l == self.old_board[i][k]:
                    ...
                else:
                    a = find_whole_move(i,k)
                    moves.append(a)

        return moves

    def determine_recent_moves (self):
        moves = self.find_recent_moves()
        moves_codes = list()
        for i in moves:
            color = i.pop(0)
            code,x,y =  self.code_from_coords(i,True)
            a,b = self.rotations_names[code]
            moves_codes.append([color,str(a)+str(b),x,y])
        return moves_codes
    
    def update_avalible_marks (self,moves):
        for i in moves:
            rotation = self.all_rotations[int(i[1][0])][int(i[1][1])]
            a = Move(i[1],i[2],i[3],i[0],400,rotation)
            self.rate_move(a,False)
            for x,y in a.coords:
                self.avalible_marks[x+a.x][y+a.y] = 1

    def find_new_moves (self):
        recent_moves = self.determine_recent_moves()
        self.clear_moves(recent_moves)
        self.update_avalible_marks(recent_moves)
        for i in recent_moves: # i = [color, "89", x,y]
            for j in self.my_stones:
                if self.freeStones[j.id] and i[0] != j.color:
                    xx,yy= i[2], i[3]
                    color = j.color
                    id = j.id
                    for k in j.rotations:
                        possible = self.connections[i[1]][k]
                        rotation = self.all_rotations[int(k[0])][int(k[1])]
                        for x,y in possible:
                            x += xx
                            y += yy
                            if 0 <= x < len(self.board) and 0 <= y < len(self.board):
                                if self.rotation_possible_place[k][color-1][x][y] == 0:
                                    if self.control_base(x,y,rotation,color):
                                        a = Move(k,x,y,color,id,rotation)
                                        self.rate_move(a)
                                        self.update_elimination(a)
                                        self.all_moves.append(a)
                                    self.rotation_possible_place[k][color-1][x][y] = 1
#-------------------------------------------------

#------ METHODS FOR MOVES ------------------------
    def update_elimination (self,move):
        color = move.color 
        xx = move.x
        yy = move.y
        self.elimination_stone[move.stone_id].append(move)
        coords = self.forbiden_coords[move.name]
        for x,y in coords[0]:
            for i in self.elimination_board[x+xx][y+yy]:
                i.append(move)
            
        for x,y in coords[1]:
            self.elimination_board[x+xx][y+yy][color-1].append(move)

    def clear_moves (self,moves):
        for i,j in enumerate(self.freeStones):
            if j != self.old_freeStones[i]:
                self.old_freeStones[i] = False
                for k in self.elimination_stone[i]:
                    k.free = 0
        for i in moves:
                color, coords, xx,yy  = i
                coords = self.all_rotations[int(coords[0])][int(coords[1])]
                for x,y in coords:
                    x += xx 
                    y += yy
                    for i in self.elimination_board[x][y][color-1]:
                        i.free = 0
        new_moves = list()
        for i in self.all_moves:
            if i.free == 1:
                if self.control_base(i.x,i.y,i.coords,i.color):
                    new_moves.append(i)
                else:
                    self.rotation_possible_place[i.name][i.color-1][i.x][i.y] = 1
            else:
                self.rotation_possible_place[i.name][i.color-1][i.x][i.y] = 1
        for i in new_moves:
            self.rate_move(i)
        self.all_moves = new_moves

    def save_half_safe (self,x,y,xo,control = True):
        s = ""
        for xx,yy in [[-1,-1],[-1,0],[-1,1],[0,-1],[0,0],[0,1],[1,-1],[1,0],[1,1]]:
            if 0 <= x +xx < len(self.board) and 0 <= y +yy < len(self.board[0]):
                if xx == 0 and yy == 0:
                    s += "3"
                elif self.board[x + xx][y + yy] >= 1:
                    s += "1"
                else:
                    if self.marks[x + xx][y + yy] == xo:
                        s += "2"
                    else:
                        s += "0"
        value = self.safe_dict[s]
        if control:
            if value == 0:
                return 0
            if value == 2:
                if self.avalible_marks[x][y] == 2 or self.avalible_marks[x][y] == 1:
                    return 0
                else:
                    return 2
            if value == 1:
                if self.avalible_marks[x][y] == 2:
                    return 2
                if self.avalible_marks[x][y] == 1:
                    return 0
                return 1
        else:
            if value == 1:
                if self.avalible_marks[x][y] == 0 or self.avalible_marks[x][y] == 2:
                    self.avalible_marks[x][y] == 1
            if value == 2 and self.avalible_marks[x][y] == 0:
                self.avalible_marks[x][y] == 2
                
    def rate_move(self,move,write =True):
        # 1 == x,  -1 == o
        x = 0
        xs = 0
        xsh = 0
        o = 0
        os = 0
        osh = 0
        added = list()
        stack = list()
        control = list()
        for xx,yy in move.coords:
            xx += move.x
            yy += move.y
            if self.marks[xx][yy] == 1:
                x += 1
            elif self.marks[xx][yy] == -1:
                o += 1
            added.append((xx,yy))
            if write:
                self.board[xx][yy] = 8
            control.append(xx*100+yy)

        for xx,yy in move.coords:
            xx += move.x
            yy += move.y
            for a,b  in [[1,0],[1,1],[1,-1],[0,1],[0,-1],[-1,-1],[-1,0],[-1,1]]:
                if 0 <= a+xx < len(self.old_board) and 0 <= b +yy < len(self.old_board):
                    if (a+xx)*100 + b + yy not in control:
                        stack.append((a+xx,b+yy))
                        control.append((a+xx)*100 + yy +b )
    
        for xx,yy in stack:
            a = self.marks[xx][yy]
            if a == 0:
                ...
            else: 
                c = self.save_half_safe(xx,yy,a,write)
                if c != 0:
                    if a == -1:
                        if c == 1:
                            os += 1
                        else:
                            osh += 1
                    else:
                        if c == 1:
                            xs += 1
                        else:
                            xsh += 1
        score = 0
        scoretab = [x,xs,xsh,o,os,osh]
        for i,j in enumerate (scoretab):
            score += j * self.score_tab[i]
        if write:
            self.delete(added)
            move.score = score
            move.score_tab = scoretab
    
    def create_final_move (self,move):        
        final_coords = list()
        for x,y in move.coords:
            final_coords.append([x+move.x,y+move.y])
        return [move.stone_id, final_coords]
    