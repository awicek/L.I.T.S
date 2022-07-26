from PLAYERS.my_player import Player

def writeBoard(board, stone, color):
    for i in range(len(stone)):
        row, col = stone[i]
        board[row][col] = color

class Game:
    def __init__(self, board, stones, player_stones, p1, p2):
        

        self.board = [[0 for _ in range(len(board))] for __ in range(len(board))]
        self.marks = board
        self.stones = stones
        self.player_stones = player_stones

        # 1 == crosses and starts, -1 == circles go second
        self.p1 = Player("hozna",self.board,self.marks,self.player_stones,1)
        self.p1_score = 0
        self.p2 = Player("pepa",self.board,self.marks,self.player_stones,-1)
        self.p2_score = 0
        
        self.freestones = [True]*len(stones)
        self.round = 0
        self.claculate_score()

    def claculate_score (self):
        circles = 0 
        crosses = 0
        for i in self.marks:
            for j in i:
                if j == 1:
                    circles +=1
                if j == -1:
                    crosses +=1
        self.p1_score = circles
        self.p2_score = crosses

    def check_move (self, x, y, metrix, num, firstmove = False):
        instructions = list()
        if 0 > x-len(metrix)+1 or  y+len(metrix[0])-1 >= len(self.board):
            return False

        for i,j in enumerate(metrix):
            for k,l in enumerate(j):
                if l > 0:
                    instructions.append([i,k])

        color = self.stones[num].color        
        control =  self.control_base(x-len(metrix)+1,y,instructions,color, firstmove)
        if control:
            return True
        return False

    def human_player_move(self,x,y,matrix,num):
        for i,j in enumerate(matrix):
            for k,l in enumerate (j):
                if l>0:
                    self.board[x+i][y+k] = l
                    self.p1.board[x+i][y+k] = l
                    self.p2.board[x+i][y+k] = l
                    if self.marks[x+i][y+k] == 1:
                        self.p1_score -= 1
                    elif self.marks[x+i][y+k] == -1:
                        self.p2_score -=1
        
        self.freestones[num] = False
        self.p1.freeStones[num] = False
        self.p2.freeStones[num] = False
        self.round +=1

    def p1_move(self):
        a = self.p1.move()
        if a:
            stoneIdx, stone = a
            stoneColor = self.player_stones[stoneIdx][0]
            writeBoard(self.p1.board, stone, stoneColor)
            writeBoard(self.p2.board, stone, stoneColor)
            writeBoard(self.board, stone, stoneColor)
            for i,j in stone:
                if self.marks[i][j] == 1:
                    self.p1_score -= 1
                elif self.marks[i][j] == -1:
                    self.p2_score -=1

            self.p1.freeStones[stoneIdx] = False
            self.p2.freeStones[stoneIdx] = False
            self.freestones[stoneIdx] = False
        else:
            return None,None,None,None
        return stone[0][0], stone[0][1], stone, stoneIdx

    def p2_move (self):
        a = self.p2.move()
        if a:
            stoneIdx, stone = a
            stoneColor = self.player_stones[stoneIdx][0]
            writeBoard(self.p1.board, stone, stoneColor)
            writeBoard(self.p2.board, stone, stoneColor)
            writeBoard(self.board, stone, stoneColor)
            for i,j in stone:
                if self.marks[i][j] == 1:
                    self.p1_score -= 1
                elif self.marks[i][j] == -1:
                    self.p2_score -=1

            self.p1.freeStones[stoneIdx] = False
            self.p2.freeStones[stoneIdx] = False
            self.freestones[stoneIdx] = False
        else:
            return None,None,None,None
        return stone[0][0], stone[0][1], stone, stoneIdx

# METHODS FOR CONTROL
    def control_base(self,xx,yy,pos,color, first):
        control = False
        added = list()
        for i,j in pos:
            x,y = i+xx,yy+j
            if self.board[x][y] > 0:
                self.delete(added)
                return False
            else:
                self.board[x][y] = 9
                added.append([x,y])
            if self.control_rect(x,y):
                self.delete(added)
                return False

            if first:
                control = True
            else:
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
