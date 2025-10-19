import API
import sys
from collections import deque 


    


WIDTH = 16#API.mazeWidth()
HEIGHT =16 #API.mazeHeight()
GOAL = (7,7)
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
    if mouse.currentx == 1 and mouse.currenty == 3:
        log(minCoordinate)
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
def main():
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
            log("--- KHAM PHA HOAN TAT! ---")
            # Khi khám phá xong, bạn có thể break
            # Hoặc chuyển sang chế độ "Speed Run" (chạy về ô 0, rồi chạy đến GOAL)
            break
        move(mouse,distances,walls)
        
        displayDistances(distances)


if __name__ == "__main__":
    main()
