class Board:
    def __init__(self, height, length,robots,goal,path=[]):
        self.goal = goal # two int list that tells us where the goal is                #0-0x234
        self.height = height                                                           #1-012x4
        self.length = length                                                           #2-01G34
        self.robots = robots # a dict of robots on the board with numbered ids         #3-01x34
        grid = []                                                                      #4-x123X   ^x >y
        self.grid = grid
        self.path=path
        for h in range(height):
            temp = []
            for l in range(length):
                temp.append("x")
            grid.append(temp)
        for robot in robots:
            x = robots[robot][0]
            y = robots[robot][1]
            self.grid[x][y] = robot
        x=goal[0]
        y=goal[1]
        grid[x][y]="G"

    def changePos(self,num,x,y):
        self.grid=[]
        self.robots[num] = [x,y]
        self.path.append([num,x,y])
        for h in range(self.height):
            temp = []
            for l in range(self.length):
                temp.append("x")
            self.grid.append(temp)
        for robot in self.robots:
            x = self.robots[robot][0]
            y = self.robots[robot][1]
            self.grid[x][y] = robot
        x=self.goal[0]
        y=self.goal[1]
        self.grid[x][y]="G"


    def Move(self,num,d):
        loc = self.robots[num]
        x = loc[0]
        y = loc[1]
        if d == "R":
            ls = self.grid[x]
            for pos in range(y,len(ls)+1,1):
                for robot in self.robots:
                    if self.robots[robot][0] == x and self.robots[robot][1] == pos and robot != num:
                        return [x,pos-1]
            return "Invalid Move"
        elif d == "L":
            ls = self.grid[x]
            for pos in range(y,-1,-1):
                for robot in self.robots:
                    if self.robots[robot][0] == x and self.robots[robot][1] == pos and robot != num:
                        return [x,pos+1]
            return "Invalid Move"
        elif d == "U":
            for pos in range(x,-1,-1):
                for robot in self.robots:
                    if self.robots[robot][0] == pos and self.robots[robot][1] == y and robot != num:
                        return[pos+1,y]
            return "Invalid Move"
        elif d == "D":
            for pos in range(x,self.height+1,1):
                for robot in self.robots:
                    if self.robots[robot][0] == pos and self.robots[robot][1] == y and robot != num:
                        return[pos-1,y]
            return "Invalid Move"
        else:
            return "Invalid Move"

    def ToString(self):
        for row in self.grid:
            for column in row:
                print(column,end="\t")
            print()

    def won(self):
        x = self.robots["X"][0]
        y = self.robots["X"][1]
        if x == self.goal[0] and y == self.goal[1]:
            return True
        else:
            return False




class Intel:
    def __init__(self,board):
        self.board = board
        self.open = [board] #this needs to store a list of grids not just the object
        self.close = [] #this needs to ^^

    def findMoves(self):
        tempOpen = []
        b = self.calcCost()#loop through boards in open
        if type(b) == str:
            return b
        for robot in b.robots: # go through all the robots
            if type(b.Move(robot,"R")) == list: #if the move is valid
                tempB = Board(b.height,b.length,b.robots.copy(),b.goal.copy(),b.path.copy())#create temp board the same as the board
                pos = tempB.Move(robot,"R") #move the robot and record the new position
                if pos != tempB.robots[robot]:
                    tempB.changePos(robot,pos[0],pos[1])
                    if tempB.won():
                        tempB.ToString()
                        print(tempB.path)
                        return 1
                    self.open.append(tempB)
            if type(b.Move(robot,"L")) == list:
                tempB = Board(b.height,b.length,b.robots.copy(),b.goal.copy(),b.path.copy())
                pos = tempB.Move(robot,"L")
                if pos != tempB.robots[robot]:
                    tempB.changePos(robot,pos[0],pos[1])
                    if tempB.won():
                        tempB.ToString()
                        print(tempB.path)
                        return 1
                    self.open.append(tempB)
            if type(b.Move(robot,"D")) == list:
                tempB = Board(b.height,b.length,b.robots.copy(),b.goal.copy(),b.path.copy())
                pos = tempB.Move(robot,"D")
                if pos != tempB.robots[robot]:
                    tempB.changePos(robot,pos[0],pos[1])
                    if tempB.won():
                        tempB.ToString()
                        print(tempB.path)
                        return 1
                    self.open.append(tempB)
            if type(b.Move(robot,"U")) == list:
                tempB = Board(b.height,b.length,b.robots.copy(),b.goal.copy(),b.path.copy())
                pos = tempB.Move(robot,"U")
                if pos != tempB.robots[robot]:
                    tempB.changePos(robot,pos[0],pos[1])
                    if tempB.won():
                        tempB.ToString()
                        print(tempB.path)
                        return 1
                    self.open.append(tempB)

        (self.close.append(b)) #once the current board has been looped through and no win condition is found and
                               #all other potential moves made and stored it is placed in the closed list
        (self.open.remove(b))
        return 0 #return that the solution was not found

    def calcCost(self):
        hold = 10000
        temp = 0
        mvs = ["R","L","U","D"]
        if self.open == []:
            return "Not Solvable"
        for b in self.open:
            future = (len(b.robots)*4)+1
            past = len(b.path)
            for robot in b.robots:
                for i in mvs:
                    pos = (b.Move(robot,i))
                    if type(pos) == list:
                        if pos == b.goal:
                            return b
                        future-=1
            score = past+future
            if score < hold:
                hold = score
                temp = b
        return b

    def cleanHouse(self):
        hold = []
        for b in self.open:
            # tempB = Board(b.height,b.length,b.robots.copy(),b.goal.copy(),b.path.copy())
            if (b.grid in [i.grid for i in self.close]) == False and (b.grid in [i.grid for i in hold]) == False:
                hold.append(b)
        self.open = hold.copy()

def readFile(fl):
    robots = {}
    lines = [line.split() for line in open("./Lockout Samples/"+fl)]
    for i in lines[1:]:
        robots[i[0]] = [int(i[1]),int(i[2])]
    length = 5
    height = 5
    goal = [2,2]
    B = Board(height,length,robots,goal)
    return B
print("ensure that all files for testing are in the same directory as program")
fl = input("choose a file: ")
B = readFile("lockout"+fl+".txt")
#B.ToString()
AI = Intel(B)
flag = 0
while flag == 0:
    flag = AI.findMoves()
    AI.cleanHouse()
    # input("next: ")
    if type(flag) == str:
        for i in AI.close:
            print(i.path)
        print("puzzle not Solvable")
    if flag == 1:
        print("Won game")


            #find a valid move that can be made
            #create a new board and make that Move
            #check to see if that board is already stored
                #if not store that board in the open list
        #if no moves can be made on that board store it in the closed
