#personal setup
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)
#solution
with open('galaxies.txt') as f:
    data = f.read().splitlines()
    
from itertools import combinations

class Telescope:
    def __init__(self, data):
        self.data = data
        self.dshape = (len(data), len(data[0]))
        self.galaxy = []
        self.expand_space()
        self.gshape = (len(self.galaxy), len(self.galaxy[0]))
        self.coords = []
        
    def expand_space(self):
        new_data = []
        for row in self.data:
            new_data.append(row)
            if '#' not in row:
                new_data.append(row)
        self.galaxy = [list(row) for row in new_data]
        height = len(self.galaxy)
        width = len(self.galaxy[0])
        for col in range(width-1, -1, -1):
            new_col = ''
            for row in range(height):
                new_col += self.galaxy[row][col]
            if '#' not in new_col:
                for i, val in enumerate(new_col):
                    self.galaxy[i].insert(col, val)
    
    def find_galaxies(self):
        for row in range(self.gshape[0]):
            for col in range(self.gshape[1]):
                if self.galaxy[row][col] == '#':
                    self.coords.append((row, col))
    
    def find_smallest_distance(self):
        distances = []
        for pair in combinations(self.coords, 2):
            distances.append(self.get_distance(pair[0], pair[1]))
        print(f'Part 1 solution: {sum(distances)}')
        
    def get_distance(self, coord1, coord2):
        #without diagonals we just find difference between x and y coordinates
        return abs(coord1[0]-coord2[0]) + abs(coord1[1]-coord2[1])
    
    def solve(self):
        self.find_galaxies()
        self.find_smallest_distance()

T = Telescope(data)
T.solve()