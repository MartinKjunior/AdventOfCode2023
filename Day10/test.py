s1 = """-L|F7
7S-7|
L|7||
-L-J|
L|-JF"""

s2 = """7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ"""

data = s2.split("\n")

from dataclasses import dataclass
import numpy as np

class Maze:
    def __init__(self, maze):
        self.maze = maze
        self.pad_maze()
        print(self.maze)
        self.start = self.find_start()
        self.A = Animal(self.start)
        self.A.pipe = self.get_cell(self.A.pos)
        self.A.near = self.get_near()
    
    def __str__(self):
        return self.A.__str__()
    
    def pad_maze(self):
        #pad the maze with dots to avoid index errors
        height = len(self.maze)
        width = len(self.maze[0])
        self.maze.insert(0, "."*(width+2))
        self.maze.append("."*(width+2))
        for i, row in enumerate(self.maze):
            self.maze[i] = "." + row + "."

    def find_start(self):
        for i, row in enumerate(self.maze):
            for j, cell in enumerate(row):
                if cell == "S":
                    return np.array([i, j])
    
    def get_cell(self, pos):
        return self.maze[pos[0]][pos[1]]
    
    def move_animal(self):
        pipe = self.get_cell(self.A.pos)
        self.A.move(pipe)
        self.A.near = self.get_near()
        self.A.pipe = self.get_cell(self.A.pos)
    
    def get_near(self):
        #return a slice of maze around the animal
        pos = self.A.pos
        return [row[pos[1]-1:pos[1]+2] for row in self.maze[pos[0]-1:pos[0]+2]]
    
    def solve(self):
        while not self.A.stop:
            self.move_animal()
            print(self.A.stop)
            print(self.A)
        print(self.A.steps//2)

@dataclass
class Animal():
    def __init__(self, start=np.array([0, 0])):
        self.steps = 0
        self.pos = start
        self.last_pos = self.pos
        self.pipe = "S"
        self.near = []
        self.stop = False
    
    def __str__(self):
        return f"Animal(steps={self.steps}, pos={self.pos}, last_pos={self.last_pos}, \nnear={self.near}), pipe={self.pipe})"

    def move(self, pipe):
        self.steps += 1
        #array of two elements defining the next step
        command = self.last_pos - self.pos
        self.last_pos = self.pos
        if pipe in "|-":
            self.pos = self.pos - command
        elif pipe in "L7":
            self.pos = self.pos - np.flip(command)
        elif pipe in "JF":
            self.pos = self.pos + np.flip(command)
        elif pipe == "S" and self.steps == 1:
            self.find_first_pipe()
            self.steps -= 1
            self.move(self.pipe)
        elif pipe == "S":
            self.steps -= 1
            self.stop = True
        else:
            raise ValueError("Invalid pipe")
    
    def find_first_pipe(self):
        #the animal starts on S but we need to find out where it can move by 
        # considering the pipes around it and then send it there
        near = self.near
        if near[0][1] in "|7F":
            self.last_pos = self.pos + np.array([1, 0])
            self.pipe = "|"
        elif near[1][0] in "-LF":
            self.last_pos = self.pos + np.array([0, 1])
            self.pipe = "-"
        elif near[1][2] in "-J7":
            self.last_pos = self.pos + np.array([0, -1])
            self.pipe = "-"
        elif near[2][1] in "|LJ":
            self.last_pos = self.pos + np.array([-1, 0])
            self.pipe = "|"

M = Maze(data)
print(M)
M.solve()