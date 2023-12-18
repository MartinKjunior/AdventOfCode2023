#personal setup
import os
import shapely

dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)
#solution
with open('dig_plan.txt') as f:
    data = f.read().splitlines()

class Site:
    """
    Class to keep track of the dig site.

    Attributes:
        data: the data from the input file
        instructions: the instructions for the digger
        lagoon: the coordinates of the lagoon vertices
        digger: the active digger
        dir_dict: a dictionary to translate ending of the hex colour into directions
    
    Methods:
        parse_data: parses the data into a list of instructions
        dig: runs through the instructions and digs the lagoon
        calcArea: calculates the area of the lagoon
        *solve: solves the problem -> main function
        translate_colour: translates the hex colour into a direction and distance
    """
    def __init__(self, data):
        self.data: str = data
        self.instructions: list[str, int, str] = self.parse_data()
        self.lagoon: list[tuple[int, int]] = list()
        self.digger: 'Digger' = Digger()
        self.dir_dict: dict[str, str] = {
            '0': 'R',
            '1': 'D',
            '2': 'L',
            '3': 'U'
        }
    
    def reset(self) -> None:
        #resets the digger and the lagoon
        self.lagoon = list()
        self.digger = Digger()
    
    def parse_data(self) -> list[list[str, int, str]]:
        #parses the data into a list of instructions
        parsed = []
        for row in data:
            row = row.split(' ')
            parsed.append([row[0], int(row[1]), row[2].strip('()')])
        return parsed
    
    def dig(self, part: int) -> None:
        #runs through the instructions and digs the lagoon
        for instruction in self.instructions:
            if part == 1:
                dir = instruction[0]
                dist = instruction[1]
                self.lagoon.append(self.digger.move(dir, dist))
            elif part == 2:
                dir, dist = self.translate_colour(instruction[2])
                self.lagoon.append(self.digger.move(dir, dist))
    
    @staticmethod
    def calcArea(loop: list[tuple[int, int]]) -> int:
        poly = shapely.Polygon(loop)
        return int(poly.area + poly.length / 2 + 1)

    def solve(self, part: int) -> None:
        #part should be an integer, 1 or 2
        self.reset()
        self.dig(part)
        print(f'Part {part} solution: {self.calcArea(self.lagoon)}')

    def translate_colour(self, colour: str) -> tuple[str, int]:
        #translates the colour into a direction and distance
        dist = int(colour[1:-1], 16)
        dir = self.dir_dict[colour[-1]]
        return dir, dist

class Digger:
    """
    Class to keep track of the digger.

    Attributes:
        dir: the current direction
        pos: the current position
        dirs: a dictionary to translate directions into coordinates

    Methods:
        move: moves the digger in a direction by some distance
    """
    def __init__(self, dir: str = 'None', pos: tuple[int, int] = (0, 0)):
        self.pos: tuple[int, int] = pos
        self.dir: tuple[int, int] = dir
        self.dirs: dict[str, tuple[int, int]] = {
            'U': (1, 0),
            'D': (-1, 0),
            'L': (0, -1),
            'R': (0, 1)
        }
    
    def move(self, dir: str, dist: int = 1) -> tuple[int, int]:
        #moves the digger in a direction and distance
        self.pos = tuple(
            map(
                sum, 
                zip(
                    self.pos, 
                    #move by distance dist in direction dir
                    tuple(n * dist for n in self.dirs[dir])
                    )
                )
            )
        return self.pos

S = Site(data)
S.solve(1)
S.solve(2)