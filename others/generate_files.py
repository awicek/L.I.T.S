# Used for generate PLAYERS.player_data
import copy

def save_half_safe2 (self,xx,yy, control = False):
       field = list()
       for x,y in [[-1,1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]:
           if self.board[xx+x,yy+y] == 0:
               field = "a"

control = dict()
possible = list()
def generate9 (current):
    global possible
    global control
    if  len(current) == 9:
        if control.get(str(current)):
            ...
        else: 
            possible.append(current)
            control[str(current)] = 1
        return
    if len(current) == 4:
        generate9(current + [3])
    else:
        for i in [0,1,2]:
            generate9(current + [i])

def generate4 (current):
    global possible
    global control
    c = 0
    for i in current:
        if i == 3:
            c += 1
    if c > 1:
        return
    if c == 1 and len(current) == 4:
        if control.get(str(current)):
            ...
        else: 
            possible.append(current)
            control[str(current)] = 1
        return
    if len(current) < 4:
        for i in [0,1,2,3]:
            generate4(current + [i])

def generate6 (current):
    global possible
    global control
    c = 0
    for i in current:
        if i == 3:
            c += 1
    if c > 1:
        return
    if c == 1 and len(current) == 6:
        if control.get(str(current)):
            ...
        else: 
            possible.append(current)
            control[str(current)] = 1
        return
    if len(current) < 6:
        if len(current) in [4,2,1,3]:
            for i in [0,1,2,3]:
                generate6(current + [i])
        else: 
            for i in [0,1,2]:
                generate6(current + [i])


def rate4 (field):
    matrix = [[0,0],[0,0]]
    result = list()
    coords =list()
    for i in range(2):
        for j in range(2):
            coords.append([i,j])
            matrix[i][j] = field[i*2+j]
    while coords:
        x,y = coords.pop(0)
        stack = [[x,y]]
        c = 0
        while stack:
            x,y = stack.pop()
            if 0 <= x <2 and 0<= y < 2:
                if matrix[x][y] == 1:
                    c += 1
                    for xx,yy in [[0,1],[1,0],[0,-1],[-1,0]]:
                        stack.append([x + xx, y + yy])
                matrix[x][y] = 3
        if c >= 1:
            result.append(c)
    if result:
        if max(result) >= 2 or len(result) ==2:
            return 1
        return 2
    return 0

def rate6 (field):
    result = list()
    coords =list()
    if field[2] == 3 or field[3] == 3:
        mode = 1
        matrix = [[0,0],[0,0],[0,0]]  
        for i in range(3):
            for j in range(2):
                coords.append([i,j])
                matrix[i][j] = field[i*2+j]
        matrix2 = copy.deepcopy(matrix)
        while coords:
            x,y = coords.pop(0)
            stack = [[x,y]]
            c = 0
            while stack:
                x,y = stack.pop()
                if 0 <= x <3 and 0<= y < 2:
                    if matrix[x][y] == 1:
                        c += 1
                        for xx,yy in [[0,1],[1,0],[0,-1],[-1,0]]:
                            stack.append([x + xx, y + yy])
                    matrix[x][y] = 3
            if c >= 1:
                result.append(c)
    else:
        mode =2
        matrix = [[0,0,0],[0,0,0]]  
        for i in range(2):
            for j in range(3):
                coords.append([i,j])
                matrix[i][j] = field[i*3+j]
        matrix2 = copy.deepcopy(matrix)
        while coords:
            x,y = coords.pop(0)
            stack = [[x,y]]
            c = 0
            while stack:
                x,y = stack.pop()
                if 0 <= x <2 and 0<= y < 3:
                    if matrix[x][y] == 1:
                        c += 1
                        for xx,yy in [[0,1],[1,0],[0,-1],[-1,0]]:
                            stack.append([x + xx, y + yy])
                    matrix[x][y] = 3
            if c >= 1:
                result.append(c)
    if result:
        if max(result) > 3 or len(result) ==3:
            return 1
        if len (result) == 2:
            return 1
        if len(result) ==1:
            if result[0] == 2:
                if mode == 1:
                    if matrix2[0][0] == 1 and matrix2[0][1] == 1:
                        if matrix2[1][0] == 2 or matrix2[1][1] == 2:
                            return 2
                    elif matrix2[2][0] == 1 and matrix2[2][1] == 1:
                        if matrix2[1][0] == 2 or matrix2[1][1] == 2:
                            return 2
                    
                if mode == 2:
                    if matrix2[0][0] == 1 and matrix2[1][0] == 1:
                        if matrix2[0][1] == 2 or matrix2[1][1] == 2:
                            return 2
                    elif matrix2[0][2] == 1 and matrix2[1][2] == 1:
                        if matrix2[0][1] == 2 or matrix2[1][1] == 2:
                            return 2
    return 0

def rate9 (field):
    matrix = [[0 for _ in range(3)] for __ in range(3)]
    result = list()
    coords =list()
    for i in range(3):
        for j in range(3):
            coords.append([i,j])
            matrix[i][j] = field[i*3+j]
    matrix2 = copy.deepcopy(matrix)
    while coords:
        x,y = coords.pop(0)
        stack = [[x,y]]
        c = 0
        while stack:
            x,y = stack.pop()
            if 0 <= x <3 and 0<= y < 3:
                if matrix[x][y] == 1:
                    c += 1
                    for xx,yy in [[0,1],[1,0],[0,-1],[-1,0]]:
                        stack.append([x + xx, y + yy])
                matrix[x][y] = 3
        if c >= 1:
            result.append(c)
    if result:
        if max(result) >= 4:
            return 1
        if len(result) == 4:
            if matrix2[0][0] != 1:
                return 1
            else:
                return 0
        if max(result) == 3:
            if min(result) == 2:
                return 1
            if len(result) == 2 and min(result) == 3:
                return 1
            if matrix2[0][0] == 1 and matrix2[0][1] == 1 and matrix2[1][0] == 1:
                return 1
            if matrix2[1][0] == 1 and matrix2[2][0] == 1 and matrix2[2][1] == 1:
                return 1
            if matrix2[2][1] == 1 and matrix2[2][2] == 1 and matrix2[1][2] == 1:
                return 1
            if matrix2[1][2] == 1 and matrix2[0][2] == 1 and matrix2[0][1] == 1:
                return 1
        if len(result) == 3:
            c = 0
            for i in result:
                if i == 2:
                    c +=1
            if c > 0:
                return 1
        if max(result) == 2 or max(result) ==3:
            if matrix2[0][1] == 2 and matrix2[0][0] == 1 and matrix2[1][0] == 1:
                return 2
            elif matrix2[0][1] == 2 and matrix2[0][2] == 1 and matrix2[1][2] == 1:
                return 2
            elif matrix2[1][0] == 2 and matrix2[0][0] == 1 and matrix2[0][1] == 1:
                return 2
            elif matrix2[1][0] == 2 and matrix2[2][0] == 1 and matrix2[2][1] == 1:
                return 2
            elif matrix2[2][1] == 2 and matrix2[1][0] == 1 and matrix2[2][0] == 1:
                return 2
            elif matrix2[2][1] == 2 and matrix2[1][2] == 1 and matrix2[2][2] == 1:
                return 2
            elif matrix2[1][2] == 2 and matrix2[0][1] == 1 and matrix2[0][2] == 1:
                return 2
            elif matrix2[1][2] == 2 and matrix2[2][1] == 1 and matrix2[2][2] == 1:
                return 2
    return 0

generate4([])
generate6([])
generate9([])

resulting_dict = dict()

for i in possible:
    # 0 any safe, 1 safe, 2 halfsafe
    s = ""
    if len(i) == 4:
        for j in i:
            s += str(j)
        resulting_dict[s] = rate4(i)
    if len(i) == 6:
        for j in i:
            s += str(j)
        resulting_dict[s] = rate6(i)
    if len(i) == 9:
        for j in i:
            s += str(j)
        resulting_dict[s] = rate9(i)

print(resulting_dict)


