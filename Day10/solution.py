#personal setup
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)
#solution
with open('tiles.txt') as f:
    data = f.read().splitlines()

import numpy as np

class Maze:
    def __init__(self, maze):
        self.maze = maze
        self.parse_maze()
        self.pad_maze()
        self.start = self.find_start()
        self.A = Animal(self.start)
        self.A.pipe = self.get_cell(self.A.pos)
        self.A.near = self.get_near()
        self.filled = []
        self.dir = 1
        self.loop = [np.flip(self.start) - np.array([1,1])] #removing the padding
    
    def __str__(self):
        return self.A.__str__()
    
    def size(self):
        #check if the maze is a rectangle otherwise raise error
        for row in self.maze:
            if len(row) != len(self.maze[0]):
                raise ValueError("Maze is not a rectangle")
        return (len(self.maze), len(self.maze[0]))
    
    def parse_maze(self):
        #split the maze into a 2D array
        self.maze = [list(row) for row in self.maze]
    
    def pad_maze(self):
        #pad the maze with dots to avoid index errors
        width = len(self.maze[0])
        self.maze.insert(0, list("X"*(width)))
        self.maze.append(list("X"*(width)))
        for i, row in enumerate(self.maze):
            row.insert(0, "X")
            row.append("X")
            self.maze[i] = row

    def find_start(self):
        #returns the coordinates of the starting position
        for i, row in enumerate(self.maze):
            for j, cell in enumerate(row):
                if cell == "S":
                    return np.array([i, j])
    
    def get_cell(self, pos):
        #returns the pipe at position pos
        return self.maze[pos[0]][pos[1]]
    
    def move_animal(self):
        #moves animal one step and updates its surroundings
        self.A.move()
        self.A.near = self.get_near()
        self.A.pipe = self.get_cell(self.A.pos)
        if self.A.pipe not in "S":
            self.loop.append(np.flip(self.A.pos) - np.array([1,1]))
    
    def get_near(self):
        #return a slice of maze around the animal
        pos = self.A.pos
        return [row[pos[1]-1:pos[1]+2] for row in self.maze[pos[0]-1:pos[0]+2]]
    
    def solve(self):
        while not self.A.stop:
            self.move_animal()
        print(f'Part 1 solution: {self.A.steps//2}')
        print(f'Part 2 solution: {self.calcArea()}')
    
    def calcArea(self):
        #calculates the area of the maze
        # Shoelace formula
        sum = 0
        path = self.loop
        for i in range(len(path)):
            n_1 = path[i]
            n_2 = path[(i+1)%len(path)]
            x_1, y_1 = n_1
            x_2, y_2 = n_2
            sum += x_1 * y_2 - y_1 * x_2

        area = abs(sum/2)

        # Pick's theroem
        return int(area - len(self.loop)//2 + 1)

class Animal():
    def __init__(self, start=np.array([0, 0])):
        self.steps = 0
        self.pos = start #current position
        self.prev = self.pos
        self.pipe = "S"
        self.near = []
        self.stop = False
    
    def __str__(self):
        return f"Animal(steps={self.steps}, pos={self.pos}, prev={self.prev}, \nnear={self.near}), pipe={self.pipe})"

    def move(self):
        self.steps += 1
        pipe = self.pipe
        #array of two elements defining the next step
        command = self.prev - self.pos
        self.prev = self.pos
        if pipe in "|-":
            self.pos = self.pos - command
        elif pipe in "L7":
            self.pos = self.pos - np.flip(command)
        elif pipe in "JF":
            self.pos = self.pos + np.flip(command)
        elif pipe == "S" and self.steps == 1:
            self.find_first_pipe()
            self.steps -= 1
            self.move()
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
            self.prev = self.pos + np.array([1, 0])
            self.pipe = "|"
        elif near[1][0] in "-LF":
            self.prev = self.pos + np.array([0, 1])
            self.pipe = "-"
        elif near[1][2] in "-J7":
            self.prev = self.pos + np.array([0, -1])
            self.pipe = "-"
        elif near[2][1] in "|LJ":
            self.prev = self.pos + np.array([-1, 0])
            self.pipe = "|"

M = Maze(data)
M.solve()