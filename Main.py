import API
import sys
from collections import deque 

class Cell:
    def __init__(self, distance):
        self.visited = False
        self.wall = {
            "N": False,
            "S": False,
            "E": False,
            "W": False,
        }
        self.distance = distance

    def initWall(self, direction, side):
        if direction == (0, 1):
            if side == "front":
                self.wall["N"] = True
                return "N"
            if side == "back":
                self.wall["S"] = True
                return "S"
            if side == "left":
                self.wall["W"] = True
                return "W"
            if side == "right":
                self.wall["E"] = True
                return "E"
        if direction == (1, 0):
            if side == "front":
                self.wall["E"] = True
                return "E"
            if side == "back":
                self.wall["W"] = True
                return "W"
            if side == "left":
                self.wall["N"] = True
                return "N"
            if side == "right":
                self.wall["S"] = True
                return "S"
        if direction == (0, -1):
            if side == "front":
                self.wall["S"] = True
                return "S"
            if side == "back":
                self.wall["N"] = True
                return "N"
            if side == "left":
                self.wall["E"] = True
                return "E"
            if side == "right":
                self.wall["W"] = True
                return "W"
        if direction == (-1, 0):
            if side == "front":
                self.wall["W"] = True
                return "W"
            if side == "back":
                self.wall["E"] = True
                return "E"
            if side == "left":
                self.wall["S"] = True
                return "S"
            if side == "right":
                self.wall["N"] = True
                return "N"


goal = (7, 7)
start = (0, 0)
WIDTH = API.mazeWidth()
HEIGHT = API.mazeHeight()
DIRECTIONS = {
    "N": (0,1),
    "S": (0,-1),
    "W": (-1,0),
    "E": (1,0)
}
maze = []
for column in range(WIDTH):
    mazeColumn = []
    for row in range(HEIGHT):
        mazeColumn.append(Cell(abs(goal[0] - column) + abs(goal[1] - row)))
    maze.append(mazeColumn)


def log(string):
    sys.stderr.write("{}\n".format(string))
    sys.stderr.flush()


def rotateLeft(direction):
    (x, y) = direction
    newx = x * 0 - y * 1
    newy = x + y * 0
    return (newx, newy)


def rotateRight(direction):
    (x, y) = direction
    newx = x * 0 - y * (-1)
    newy = x * (-1) + y * 0
    return (newx, newy)

def initWall(maze,x,y,direction,side):
    realSide = maze[x][y].initWall(direction,side)
    if realSide == "W" and x>0:
        maze[x-1][y].wall["E"] = True
    if realSide == "E" and x<WIDTH:
        maze[x+1][y].wall["W"] = True
    if realSide == "S" and y>0:
        maze[x][y-1].wall["N"] = True
    if realSide == "N" and y<HEIGHT:
        maze[x][y+1].wall["S"] = True
def updateMap(maze):
    for x in range(WIDTH):
        for y in range(HEIGHT):
            API.setText(x, y, maze[x][y].distance)

        
def floodFill(maze,goal):
    q = deque([goal])
    for x in range(WIDTH):
            for y in range(HEIGHT):
                maze[x][y].visited = False
    maze[goal[0]][goal[1]].visited = True
    while q:
        x,y = q.popleft()
        for direction in DIRECTIONS:
            if not maze[x][y].wall[direction]:
                newx = x+DIRECTIONS[direction][0]
                newy = y+DIRECTIONS[direction][1]
                if 0<=newx < WIDTH and 0<=newy<HEIGHT and not maze[newx][newy].visited:
                    maze[newx][newy].distance = maze[x][y].distance+1
                    log("("+str(newx)+str(newy)+"): "+str(maze[newx][newy].distance))
                    maze[newx][newy].visited = True
                    q.append((newx,newy))


def main():
    API.setColor(0, 0, "G")
    API.setText(0, 0, "abc")
    currentx = start[0]
    currenty = start[1]
    currentDirection = (0, 1)
    updateMap(maze)
    while currenty<8:
        if not API.wallFront():
            API.moveForward()
            currentx += currentDirection[0]
            currenty += currentDirection[1]
            API.setColor(currentx, currenty, "G")
        if API.wallRight():
            initWall(maze,currentx,currenty,currentDirection,"right")
        if API.wallLeft():
            initWall(maze,currentx,currenty,currentDirection,"left")
        if API.wallFront():
            initWall(maze,currentx,currenty,currentDirection,"front")
            floodFill(maze,goal)
            log(maze[currentx][currenty].distance)


if __name__ == "__main__":
    main()
