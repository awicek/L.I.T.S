# DODELAT CREATE_RANDOM_BOARD
import random


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

    def __init__(self,informace,id = 0):# DONE TESTED 
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

# BOARD
def create_board_file (name):
    with open(name, "r") as f:
        board = list()
        for i in f:
            line = list(map(int,i.strip().split()))
            board.append(line)
    return board

def create_random_board(size =-1):
    if size == -1:
        board_size = random.choice([15])
    else:
        board_size = size

    if board_size == 15:
        marks_count = random.randint(50,50)
    else:
        marks_count = random.randint(20,29)

    
    board = [[0 for _ in range(board_size)] for __ in range(board_size)]

    x = 0
    xx = True
    o = 0
    oo = True
    while xx or oo:
        if xx:
            a = random.randint(0,board_size-1)
            b = random.randint(0,board_size-1)
            if board[a][b] == 0:
                board[a][b] = -1
                x +=1
        if oo:
            a = random.randint(0,board_size-1)
            b = random.randint(0,board_size-1)
            if board[a][b] == 0:
                board[a][b] = 1
                o +=1
        if x == marks_count:
            xx = False
        if o == marks_count:
            oo = False
    
    return board
    
# STONES
def s_f_p (filename):
    """ load stones from text file. Stones are stored in the same format as in HW08 """
    f = open(filename,"r")
    stones = []
    for line in f:  
        nums = list(map(int, line.strip().split()))
        color = nums[0]
        coords = nums[1:]
        cells = []
        for i in range(0,len(coords)//2):
            cells.append( [ coords[2*i+0], coords[2*i+1] ] )
        stones.append([color, cells])
    f.close()
    return stones

def read_stones (name):
    with open (name, "r") as f:
        stones_data = list()
        for i in f:
            stones_data.append(list(map(int, i.strip().split())))
        stones = list(map(Stone,stones_data,))
    return stones
    
def create_random_stones (amount = -1):
    if amount == -1:
        stones_amount = random.choice([17,18,19,20,21,22,23,24,24,24,24])
    else:
        stones_amount = amount


    possible_stones = [
        " 0 0 0 1 0 2 1 1 2 1",
        " 0 0 0 1 0 2 0 3 ",
        " 0 0 0 1 0 2 1 2",
        " 0 0 0 1 1 1",
        " 0 0 0 1 0 2 1 0 1 2",
        " 0 0 0 1 0 2 1 1",
        " 0 0 0 1 1 1 2 1 2 2",
        " 0 0 0 1 0 2",
        " 0 1 1 1 1 0 1 2 2 1"
    ]    
        # # #    # # # #   # # #   # #   #   #   # # #   # #     # # #     # 
          #                    #     #   # # #     #       #             # # #
          #                                                # #             #

    stones = list()
    control_dict = dict()
    c = 0
    while c < stones_amount:
        stone = random.choice(["1","2","3"])
        stone += random.choice(possible_stones)
        if control_dict.get(stone):
            ...
        else:
            control_dict[stone] = 1
            stones.append(stone)
            c+=1
    
    game_stones = list()
    for i in stones:
        game_stones.append(list(map(int, i.split())))
    game_stones = list(map(Stone, game_stones))
    
    stones_for_players = list()
    for i in stones:  
        nums = list(map(int, i.split()))
        color = nums[0]
        coords = nums[1:]
        cells = []
        for i in range(0,len(coords)//2):
            cells.append( [ coords[2*i+0], coords[2*i+1] ] )
        stones_for_players.append([color, cells])

    return game_stones, stones_for_players


colors = {"1":(1,0,0,.8), "2": (.4,.7,.3,.8), "3":(0,0,1,.8), "4": (0,1,1,.8)}
stones = read_stones("Game\\KVHRA\\_stones.txt")
stones_for_players = s_f_p("Game\\KVHRA\\_stones.txt")