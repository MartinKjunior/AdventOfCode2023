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

s3 = """.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ..."""

s4 = """...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
..........."""

s5 = """FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L"""

data = s5.split("\n")

from dataclasses import dataclass
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
        self.loop = [tuple(np.flip(self.start) - np.array([1,1]))]
    
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
        for i, row in enumerate(self.maze):
            for j, cell in enumerate(row):
                if cell == "S":
                    return np.array([i, j])
    
    def get_cell(self, pos):
        return self.maze[pos[0]][pos[1]]
    
    def move_animal(self):
        self.A.move()
        self.A.near = self.get_near()
        self.A.pipe = self.get_cell(self.A.pos)
        if self.A.pipe not in "S":
            self.loop.append(tuple(np.flip(self.A.pos) - np.array([1,1])))
    
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
    
    def fill_dirt(self):
        #fill the dirt (.) to the right side of the direction of motion of the animal with O
        #this needs to account for diagonal dirt and curves
        command = self.dir * (self.A.prev - self.A.pos)
        new_commands = []
        if command[0] == 0:
            new_commands.append(-np.flip(command))
        else:
            new_commands.append(np.flip(command))

        for new_command in new_commands:
            pos = self.A.pos + new_command
            if self.get_cell(pos) == ".":
                self.maze[pos[0]][pos[1]] = "O"
    
    def find_filled(self):
        #find all the filled cells in the maze
        filled = []
        for i, row in enumerate(self.maze):
            for j, cell in enumerate(row):
                if cell == "O":
                    filled.append((i, j))
        return filled
    
    def dilatefill(self):
        #dilate the filled cells to fill the maze
        steps = 1
        while steps:
            steps = 0
            filled = self.find_filled()
            for pos in filled:
                steps += self.dilate(pos)
            self.filled = self.find_filled()

    def dilate(self, pos):
        #dilate the cell at pos
        steps = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if self.get_cell(pos + np.array([i, j])) == ".":
                    self.maze[pos[0]+i][pos[1]+j] = "O"
                    steps += 1
        return steps
    
    def count_dirt(self):
        #count the number of dirt cells in the maze
        dirt = 0
        for row in self.maze:
            dirt += row.count(".")
        return dirt

@dataclass
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
for row in M.maze:
    print("".join(row))
print(M.loop)