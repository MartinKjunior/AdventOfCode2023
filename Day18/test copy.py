from icecream import ic
from time import sleep
import os
from colorama import init
init(autoreset=True)

dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)

with open('dig_plan.txt') as f:
    data = f.read().splitlines()

class Site:
    def __init__(self, data):
        self.data: str = data
        self.instructions: list[str, int, str] = self.parse_data()
        self.lagoon: list[tuple[tuple[int, int], str]] = list()
        self.digger: 'Digger' = Digger()
    
    @staticmethod
    def hex_to_rgb(hex):
        return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))

    @staticmethod
    def rgb_to_ansi(r, g, b):
        return f'\033[38;2;{r};{g};{b}m'
    
    def parse_data(self) -> list[str, int, str]:
        parsed = []
        for row in data:
            row = row.split(' ')
            parsed.append([row[0], int(row[1]), row[2].strip('()')])
        return parsed
    
    def draw_map(self) -> None:
        seen_coords = [x[0] for x in self.lagoon]
        #finds the length and width of a map necessary to incorporate points stored in self.lagoon
        #creates a map of dots and replaces dots with # for points in self.lagoon, then prints the map
        width_max = max([x[1] for x in seen_coords]) + 1
        width_min = min([x[1] for x in seen_coords])
        height_max = max([x[0] for x in seen_coords]) + 1
        height_min = min([x[0] for x in seen_coords])
        map = [[('.', '#FFFFFF') for _ in range(width_max - width_min)] for _ in range(height_max - height_min)]
        #translate points so they are always positive values
        for point in seen_coords:
            map[point[0] - height_min][point[1] - width_min] = ('#', self.lagoon[seen_coords.index(point)][1])
        self.print_coloured_map(map)
    
    def print_coloured_map(self, map: list[list[str]]) -> None:
        for row in map:
            row_str = ''
            for char in row:
                if char[0] == '#':
                    hex_color = char[1]
                    r, g, b = self.hex_to_rgb(hex_color[1:])  # remove the '#' at the start
                    ansi_color = self.rgb_to_ansi(r, g, b)
                    row_str += f'{ansi_color}{char[0]}\033[0m'
                else:
                    row_str += char[0]
            print(row_str)
    
    def show_instructions(self) -> None:
        for i, row in enumerate(self.instructions):
            ic(i, row)
    
    def dig(self, draw: bool = True, speed: float = 0.5) -> None:
        for instruction in self.instructions:
            dir = instruction[0]
            dist = instruction[1]
            colour = instruction[2]
            for _ in range(dist):
                self.lagoon.append((self.digger.move(dir), colour))
                if draw:
                    self.draw_map()
                    sleep(speed)
                    if True:
                        os.system('clear')
        else:
            if draw:
                os.system('clear')
                self.draw_map()
    
    def calcArea(self, loop: list[tuple[int, int]]) -> int:
        #calculates the area of the dig site
        # Shoelace formula
        sum = 0
        path = loop
        for i in range(len(path)):
            n_1 = path[i]
            n_2 = path[(i+1)%len(path)]
            x_1, y_1 = n_1
            x_2, y_2 = n_2
            sum += x_1 * y_2 - y_1 * x_2

        area = abs(sum/2)

        # Pick's theroem
        return int(area - len(loop)//2 + 1) + len(loop)

    def solve(self) -> None:
        self.dig(draw = False)
        print(f'Part 1 solution: {self.calcArea([x[0] for x in self.lagoon])}')

class Digger:
    def __init__(self, dir: str = 'None', pos: tuple[int, int] = (0, 0), dist: int = 1):
        self.pos = pos
        self.dir = dir
        self.dist = dist
        self.dirs = {
            'U': (1, 0),
            'D': (-1, 0),
            'L': (0, -1),
            'R': (0, 1)
        }
    
    def move(self, dir: str) -> tuple[int, int]:
        self.pos = tuple(map(sum, zip(self.pos, tuple(n * self.dist for n in self.dirs[dir]))))
        return self.pos

S = Site(data)
S.dig(speed = 0.1) #draws the map
#S.solve() #prints the solution