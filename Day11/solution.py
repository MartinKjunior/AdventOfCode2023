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
        #replaces dots in rows and columns without galaxies with pluses
        new_data = []
        for row in self.data:
            if '#' not in row:
                row = row.replace('.', '+')
            #rows of strings with multiple characters are turned into lists of those characters
            new_data.append(list(row))
        self.galaxy = new_data
        height = len(self.galaxy)
        width = len(self.galaxy[0])
        for col in range(width):
            new_col = ''
            for row in range(height):
                new_col += self.galaxy[row][col]
            if '#' not in new_col:
                for i in range(height):
                    self.galaxy[i][col] = '+'
    
    def find_galaxies(self):
        #finds the coordinates of all galaxies
        self.coords = []
        for row in range(self.gshape[0]):
            for col in range(self.gshape[1]):
                if self.galaxy[row][col] == '#':
                    self.coords.append((row, col))
    
    def find_distances(self, part):
        #for each combination of galaxies, finds the shortest distance without moving diagonally
        distances = []
        for pair in combinations(self.coords, 2):
            distances.append(self.move_between_coords(pair[0], pair[1]))
        print(f'Part {part} solution: {sum(distances)}')
        
    def coord_difference(self, coord1, coord2):
        #without diagonals we just find difference between x and y coordinates
        return coord2[0]-coord1[0], coord2[1]-coord1[1]
    
    def solve(self, part):
        #the only difference between part 1 and 2 is the value of '+'
        if part == 1:
            self.step = 2
        else:
            self.step = 10**6
        self.find_galaxies()
        self.find_distances(part)
    
    def move_between_coords(self, coord1, coord2):
        #moves from coord1 to coord2 one step at a time and records the character after each step
        delta = self.coord_difference(coord1, coord2)
        seen = []
        x, y = coord1
        for dx in range(1, delta[0] + 1):
            seen.append(
                self.galaxy[x + dx][y]
            )
        #variable parity keeps track of whether we are moving to the left or right
        # because of the order in which we find galaxies, coord2[0] > coord1[0]
        # so we only need to do this check for moving within the row
        parity = -1 if delta[1] < 0 else 1
        x = x + delta[0]
        for dy in range(1, delta[1] * parity + 1):
            seen.append(
                self.galaxy[x][y + dy * parity]
            )
        return self.count_steps(seen)
    
    def count_steps(self, path):
        #count how many steps are necessary to move from one galaxy to the next
        total = 0
        for symbol in path:
            if symbol == '+':
                total += self.step
            else:
                total += 1
        return total

T = Telescope(data)
T.solve(1)
T.solve(2)

"""
Loading data takes: 0.0026809329999999965s
Part 1 solution: 9648398
Solving part 1 takes: 1.681386363s
Part 2 solution: 618800410814
Solving part 2 takes: 1.67842136s
"""