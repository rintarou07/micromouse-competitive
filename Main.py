import API
import sys
from collections import deque 
import json
import math
import heapq


WIDTH = API.mazeWidth()
HEIGHT =API.mazeHeight()
GOAL = (8,8)
DIRECTIONS = {
    "right": (1,0),
    "left": (-1,0),
    "front": (0,1),
    "back": (0,-1)
}

distances = []
walls = [] #wall[x][y][0->3] 0: north(phia bac), 1:east(phia dong), 2:south(phia nam), 3:west(phia tay)
visited = []

class Mouse:
    def __init__(self):
        self.currentx = 0
        self.currenty = 0
        self.direction = (0,1)
    
for column in range( WIDTH):
    mazecolumn = []
    wallcolumn = []
    visitedcolumn = []
    for row in range(HEIGHT):
        mazecolumn.append(abs(GOAL[0]-column)+abs(GOAL[1]-row))
        wallcolumn.append([False,False,False,False])
        visitedcolumn.append(False)
    distances.append(mazecolumn)
    walls.append(wallcolumn)
    visited.append(visitedcolumn)

def getOpenNeighbors(x,y,walls):
    neighborList = []
    if y<HEIGHT-1 and not walls[x][y][0] and not walls[x][y+1][2]:
        neighborList.append((x,y+1))
    if x<WIDTH-1 and not walls[x][y][1] and not walls[x+1][y][3]:
        neighborList.append((x+1,y))
    if y>0 and not walls[x][y][2] and not walls[x][y-1][0]:
        neighborList.append((x,y-1))
    if x>0 and not walls[x][y][3] and not walls[x-1][y][1]:
        neighborList.append((x-1,y))
    return neighborList

def fullTurnRight(mouse):
    API.turnRight()
    mouse.direction = (mouse.direction[0]*0 -mouse.direction[1]*(-1),mouse.direction[0]*(-1) + mouse.direction[1]*0)
def fullTurnLeft(mouse):
    API.turnLeft()
    mouse.direction = (mouse.direction[0]*0 -mouse.direction[1]*1,mouse.direction[0]*1 + mouse.direction[1]*0)
def fullMoveForward(mouse):
    API.moveForward()
    mouse.currentx += mouse.direction[0]
    mouse.currenty += mouse.direction[1]
def updateWall(walls,x,y,direction,side):
    if side == "right":
        if direction == (1,0):
            walls[x][y][2] = True
            if y > 0:
                walls[x][y-1][0] = True
        if direction == (-1,0):
            walls[x][y][0] = True
            if y < HEIGHT-1:
                walls[x][y+1][2] = True
        if direction == (0,1):
            walls[x][y][1] = True
            if x<WIDTH-1:
                walls[x+1][y][3] = True
        if direction == (0,-1):
            walls[x][y][3] = True
            if x > 0:
                walls[x-1][y][1] = True
    if side == "left":
        if direction == (1,0):
            walls[x][y][0] = True
            if y < HEIGHT-1:
                walls[x][y+1][2] = True
        if direction == (-1,0):
            walls[x][y][2] = True
            if y > 0:
                walls[x][y-1][0] = True
        if direction == (0,1):
            walls[x][y][3] = True
            if x > 0:
                walls[x-1][y][1] = True
        if direction == (0,-1):
            walls[x][y][1] = True
            if x<WIDTH-1:
                walls[x+1][y][3] = True

    if side == "front":
        if direction == (1,0):
            walls[x][y][1] = True
            if x<WIDTH-1:
                walls[x+1][y][3] = True
        if direction == (-1,0):
            walls[x][y][3] = True
            if x > 0:
                walls[x-1][y][1] = True
        if direction == (0,1):
            walls[x][y][0] = True
            if y < HEIGHT-1:
                walls[x][y+1][2] = True
        if direction == (0,-1):
            walls[x][y][2] = True
            if y > 0:
                walls[x][y-1][0] = True
def getMinDistance(x,y,walls):
    minDistance = 1000
    openNeighbors = getOpenNeighbors(x, y,walls)
    for coordinate in openNeighbors:
        if minDistance>distances[coordinate[0]][coordinate[1]]:
            minDistance = distances[coordinate[0]][coordinate[1]]
    return minDistance
def move(mouse,distances,walls):
    minDistance = getMinDistance(mouse.currentx,mouse.currenty,walls)
    minCoordinate = ()
    openNeighbors = getOpenNeighbors(mouse.currentx, mouse.currenty,walls)
    # if (mouse.currentx, mouse.currenty+1) in openNeighbors and distances[mouse.currentx][mouse.currenty+1] == minDistance:
    #     return (mouse.currentx, mouse.currenty+1)

    for coordinate in openNeighbors:
        if distances[coordinate[0]][coordinate[1]] == minDistance:
            minCoordinate = coordinate
            break
    currentDirection = mouse.direction
    if mouse.currentx + currentDirection[0] == minCoordinate[0] and mouse.currenty +currentDirection[1] == minCoordinate[1]:
        fullMoveForward(mouse)
        return
    currentDirection = (mouse.direction[0]*0 -mouse.direction[1]*(-1),mouse.direction[0]*(-1) + mouse.direction[1]*0)
    if mouse.currentx + currentDirection[0] == minCoordinate[0] and mouse.currenty +currentDirection[1] == minCoordinate[1]:
        fullTurnRight(mouse)
        fullMoveForward(mouse)
        return
    currentDirection = (mouse.direction[0]*0 -mouse.direction[1]*1,mouse.direction[0]*1 + mouse.direction[1]*0)
    if mouse.currentx + currentDirection[0] == minCoordinate[0] and mouse.currenty +currentDirection[1] == minCoordinate[1]:
        fullTurnLeft(mouse)
        fullMoveForward(mouse)
        return
    else:
        fullTurnLeft(mouse)
        fullTurnLeft(mouse)
        fullMoveForward(mouse)
        return
def generateMaze(walls,fileName):
    maze = [[True for _ in range(WIDTH*2+1)] for _ in range(HEIGHT*2+1)]
    for x in range(WIDTH*2+1):
        maze[x][0] = False
    for x in range(WIDTH):
        for y in range(HEIGHT):
            if walls[x][y][0]:
                maze[x*2][y*2+2]=False
                maze[x*2+1][y*2+2]=False
                maze[x*2+2][y*2+2]=False
            if walls[x][y][1]:
                maze[x*2+2][y*2]=False
                maze[x*2+2][y*2+1]=False
                maze[x*2+2][y*2+2]=False
            if walls[x][y][2]:
                maze[x*2][y*2]=False
                maze[x*2+1][y*2]=False
                maze[x*2+2][y*2]=False
            if walls[x][y][3]:
                maze[x*2][y*2]=False
                maze[x*2][y*2+1]=False
                maze[x*2][y*2+2]=False
    jsonFile = json.dumps(maze)
    with open(fileName,"w") as f:
        f.write(jsonFile)


def floodFill(currentx,currenty,distances,walls):
    q = deque()
    q.appendleft((currentx,currenty))
    while q:
        (x,y) = q.popleft()
        if (x,y) == GOAL:
            continue
        minDistance = getMinDistance(x,y,walls)
        if distances[x][y] - 1 != minDistance:
            distances[x][y] = minDistance + 1
            if x>0 and distances[x-1][y] != 0:
                q.appendleft((x-1,y))
            if y > 0 and distances[x][y-1] != 0:
                q.appendleft((x,y-1))
            if y < HEIGHT-1 and distances[x][y+1] != 0:
                q.appendleft((x,y+1))
            if x < WIDTH-1 and distances[x+1][y] != 0:
                q.appendleft((x+1,y))
    return
def NewfloodFill(distances, walls, visited):
    q = deque()
    found_unvisited = False
    for x in range(WIDTH):
        for y in range(HEIGHT):
            if not visited[x][y]:
                distances[x][y] = 0
                q.append((x,y)) 
                found_unvisited = True
            else:
                distances[x][y] = 255 

    if not found_unvisited:
        return False
    while q:
        (x,y) = q.popleft()
        current_dist = distances[x][y]
        
        for (nx, ny) in getOpenNeighbors(x, y, walls):
            if visited[nx][ny] and distances[nx][ny] == 255: 
                distances[nx][ny] = current_dist + 1
                q.append((nx, ny))
                
    return True 
def displayDistances(distances):
    for y in range(HEIGHT):
        for x in range (WIDTH):
            API.setText(x,y,distances[x][y])
def log(string):
    sys.stderr.write("{}\n".format(string))
    sys.stderr.flush()
def isValid(x, y,width,height):
    return (x >= 0) and (x < width) and (y >= 0) and (y < height)
def isAcessible(map,x,y):
    return map[x][y]
def goalReached(x,y,goal):
    return (x,y) == goal    
def getPath(cells,goal):
    path = []
    (x,y) = goal
    while not (cells[x][y][0] == x and cells[x][y][1] == y):
        path.insert(0,(x,y))
        parentx = cells[x][y][0]
        parenty = cells[x][y][1]
        x = parentx
        y = parenty
    path.insert(0, (x,y))
    return path

def hCostCalculated(x,y,goal):
    (xGoal, yGoal) = goal
    dx = abs(xGoal-x)
    dy = abs(yGoal-y)
    return dx+dy - (1.000000000000001-2)*min(dx,dy)
def rotation(direction,angle):
    (x,y) = direction
    newx = round(x*math.cos(math.radians(angle)) - y*math.sin(math.radians(angle)))
    newy = round(x*math.sin(math.radians(angle)) + y*math.cos(math.radians(angle)))
    return (newx,newy)


def aStar(map,goal,start=(1,1)):
    WIDTH = len(map)
    HEIGHT = len(map[0])
    if not isValid(start[0],start[1],WIDTH,HEIGHT) or not isValid(goal[0],goal[1],WIDTH,HEIGHT):
        print("not valid")
        return
    
    if goalReached(start[0],start[1],goal):
        return


    openList = []
    closedList = [[False for _ in range(HEIGHT)] for _ in range(WIDTH)]
    cells = [[[None, None, float('inf'), float('inf'), float('inf')] for _ in range(HEIGHT)] for _ in range(WIDTH)] #cell[0] is parentx, cell[1] is parenty, cell[2] is g value, cell[3] is h value, cell[4] is f value
    x = start[0]
    y = start[1]
    cells[x][y][0] = x
    cells[x][y][1]= y
    cells[x][y][2] = 0
    cells[x][y][3] = hCostCalculated(x,y,goal)
    cells[x][y][4] =  cells[x][y][2]+ cells[x][y][3]

    heapq.heappush(openList,(0,x,y))
    while len(openList)>0:
        p=heapq.heappop(openList)
        x = p[1]
        y = p[2]
        closedList[x][y] = True
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for direction in directions:
            nx = x + direction[0]
            ny = y + direction[1]
            if isValid(nx,ny,WIDTH,HEIGHT) and isAcessible(map,nx,ny) and not closedList[nx][ny]:
                if goalReached(nx,ny,goal):
                    cells[nx][ny][0]=x
                    cells[nx][ny][1]=y
                    return getPath(cells,goal)
                else:
                    g = cells[x][y][2] + 1 + max(0,abs(direction[0]*direction[1]))*0.00000000000001
                    h = hCostCalculated(nx,ny,goal)
                    f = g + h
                    if  cells[nx][ny][4]>f:
                        heapq.heappush(openList,(f,nx,ny))
                        cells[nx][ny][0]=x
                        cells[nx][ny][1]=y
                        cells[nx][ny][2] = g
                        cells[nx][ny][3] = h
                        cells[nx][ny][4] = f
    return None
def moveAlongPath(path):
  current = 0
  direction = (0,1)
  while current < len(path)-1:
    if path[current+1] == (path[current][0]+direction[0],path[current][1]+direction[1]):
        API.moveForwardHalf()
        current+=1
    elif path[current+1] == (path[current][0]+rotation(direction,-90)[0],path[current][1] + rotation(direction,-90)[1]):
        direction=rotation(direction,-90)
        API.turnRight()
        API.moveForwardHalf()
        current+=1
    elif path[current+1] == (path[current][0]+rotation(direction,90)[0],path[current][1] + rotation(direction,90)[1]):
        direction=rotation(direction,90)
        API.turnLeft()
        API.moveForwardHalf()
        current+=1
    elif path[current+1] == (path[current][0]+rotation(direction,-45)[0],path[current][1] + rotation(direction,-45)[1]):
        direction=rotation(direction,-45)
        API.turnRight45()
        API.moveForwardHalf()
        current+=1
    elif path[current+1] == (path[current][0]+rotation(direction,45)[0],path[current][1] + rotation(direction,45)[1]):
        direction=rotation(direction,45)
        API.turnLeft45()
        API.moveForwardHalf()
        current+=1
def firstRun():
    log("lan chay dau tien: bat dau scan")
    mouse = Mouse()
    global visited
    i = 0
    while True:
        visited[mouse.currentx][mouse.currenty] = True
        API.setColor(mouse.currentx,mouse.currenty,"G")
        if API.wallFront():
            updateWall(walls,mouse.currentx,mouse.currenty,mouse.direction,"front")

        if API.wallLeft():
            updateWall(walls,mouse.currentx,mouse.currenty,mouse.direction,"left")

        if API.wallRight():
            updateWall(walls,mouse.currentx,mouse.currenty,mouse.direction,"right")

        keep_exploring = NewfloodFill(distances, walls, visited)
        if not keep_exploring:
            break
        move(mouse,distances,walls)
    generateMaze(walls,"maze.json")
    log("scan hoan tat, ket thuc luot chay")
def secondRun(maze):
    log("lan chay thu 2: chay duong ngan nhat")
    resizedGoal = (GOAL[0]*2+1,GOAL[1]*2+1)
    path = aStar(maze,resizedGoal)
    moveAlongPath(path)
    with open("maze.json",'w') as f:
        log("hoan thanh toi dich")

if __name__ == "__main__":
    with open("maze.json","a+") as f:
        f.seek(1)
        if f.read(1) == "[":
            f.seek(0)
            maze=json.load(f)
        else:
            maze=None
    if maze == None:
        firstRun()
    else:
        secondRun(maze)
    
    
