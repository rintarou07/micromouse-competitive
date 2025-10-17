import API
import sys

class Cell:
    def __init__(self,distance):
        self.visited = False
        self.wall = {
        "N" : False,
        "S" : False,
        "E" : False,
        "W" : False,
      }
        self.distance = 0
goal = (7,7)
start = (0,0)
WIDTH = API.mazeWidth()
HEIGHT = API.mazeHeight()
maze = []
for column in range(WIDTH):
    mazeColumn = []
    for row in range(HEIGHT):
        print(abs(goal[0]-column)+abs(goal[1]-row))
        mazeColumn.append(Cell(abs(goal[0]-column)+abs(goal[1]-row)))
    maze.append(mazeColumn)
def log(string):
    sys.stderr.write("{}\n".format(string))
    sys.stderr.flush()
def rotateLeft(direction):
        (x,y) = direction
        newx = x*0 - y*1
        newy = x + y*0
        return (newx,newy)
def rotateRight(direction):
        (x,y) = direction
        newx = x*0 - y*(-1)
        newy = x*(-1) + y*0
        return (newx,newy)

def main():
    API.setColor(0, 0, "G")
    API.setText(0, 0, "abc")
    x=start[0]
    y=start[0]
    direction = (0,1)
    log(rotateRight(direction))
    API.moveForwardHalf()
    API.turnRight45()
    API.moveForwardHalf()
    API.turnRight45()
    API.moveForwardHalf()
    
    # while True:
    #     if not API.wallLeft():
    #         API.turnLeft()
    #     while API.wallFront():
    #         API.turnRight()
    #     API.moveForward()

if __name__ == "__main__":
    main()