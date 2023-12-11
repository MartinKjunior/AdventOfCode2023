s = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""

data = s.splitlines()

from itertools import combinations

class Telescope:
    def __init__(self, data, part=1):
        self.data = data
        self.dshape = (len(data), len(data[0]))
        self.galaxy = []
        self.expand_space()
        self.gshape = (len(self.galaxy), len(self.galaxy[0]))
        self.coords = []
        if part == 1:
            self.step = 2
        else:
            self.step = 10**6
        
    def expand_space(self):
        new_data = []
        for row in self.data:
            if '#' not in row:
                new_row = row.replace('.', '+')
                new_data.append(new_row)
            else:
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
                    self.galaxy[i].insert(col, '+')
    
    def find_galaxies(self):
        for row in range(self.gshape[0]):
            for col in range(self.gshape[1]):
                if self.galaxy[row][col] == '#':
                    self.coords.append((row, col))
    
    def find_smallest_distance(self):
        distances = []
        for pair in combinations(self.coords, 2):
            distances.append(self.move_between_coords(pair[0], pair[1]))
        print(f'Part 1 solution: {sum(distances)}')
        
    def coord_difference(self, coord1, coord2):
        #without diagonals we just find difference between x and y coordinates
        return coord2[0]-coord1[0], coord2[1]-coord1[1]
    
    def solve(self):
        self.find_galaxies()
        self.find_smallest_distance()
    
    def move_between_coords(self, coord1, coord2):
        x1, x2 = sorted([coord1[0], coord2[0]])
        y1, y2 = sorted([coord1[1], coord2[1]])
        path = []
        col = []
        for row in range(x1+1, x2):
            col.append(self.galaxy[row][y1])
        path.extend(col)
        path.extend(self.galaxy[x2][y1:y2+1])
        return self.count_steps(path)
    
    def count_steps(self, path):
        total = 0
        for symbol in path:
            if symbol == '+':
                total += self.step
            else:
                total += 1
        return total

T = Telescope(data)
for row in T.galaxy:
    print(''.join(row))
T.solve()