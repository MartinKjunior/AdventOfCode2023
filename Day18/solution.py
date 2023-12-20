#personal setup
import os
import shapely
import matplotlib.pyplot as plt
from icecream import ic
from dataclasses import dataclass

dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)
#solution

@dataclass
class Instruction:
    dir: str
    dist: int
    colour: str #hexadecimal colour

    def __post_init__(self):
        self.DIR_DICT: dict[str, str] = {
            '0': 'R',
            '1': 'D',
            '2': 'L',
            '3': 'U'
        }
        self.dist = int(self.dist)
        self.colour = self.colour.strip('()')
    
    @staticmethod
    def hex_to_dist(hex: str) -> int:
        """translates a hexidecimal string into a distance"""
        return int(hex[1:-1], 16)
    
    def translate_colour(self) -> tuple[str, int]:
        """translates the colour from a hexidecimal string into a direction and distance"""
        dist = self.hex_to_dist(self.colour)
        dir = self.DIR_DICT[self.colour[-1]] #last digit encodes direction
        return dir, dist

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
        self.instructions: list[Instruction] = self.parse_data()
        self.lagoon: list[tuple[int, int]] = list()
        self.digger: Digger = Digger()
        self.colours = []
    
    @classmethod
    def from_file(cls, filename):
        with open(filename) as f:
            data = f.read().splitlines()
        return cls(data)
    
    def reset(self) -> None:
        """resets the digger and the lagoon"""
        self.lagoon = list()
        self.digger = Digger()
        self.colours = []
    
    def parse_data(self) -> list[list[str, int, str]]:
        """parses the data into a list of instructions"""
        parsed = []
        for row in self.data:
            row = row.split(' ')
            parsed.append(Instruction(*row))
        return parsed
    
    def dig(self, part: int) -> None:
        """runs through the instructions and digs the lagoon"""
        dig_runner = None
        match int(part):
            case 1:
                dig_runner = self._dig1
            case 2:
                dig_runner = self._dig2
            case _:
                raise ValueError(f'part must be 1 or 2, not {part}')
        for I in self.instructions:
            dig_runner(I)
    
    def _dig1(self, I: Instruction) -> None:
        """helper function for part 1"""
        self.colours.append(I.colour)
        self.lagoon.append(self.digger.move(I.dir, I.dist))
    
    def _dig2(self, I: Instruction) -> None:
        """helper function for part 2"""
        dir, dist = I.translate_colour()
        self.colours.append(I.dist)
        self.lagoon.append(self.digger.move(dir, dist))
    
    @staticmethod
    def calc_area(loop: list[tuple[int, int]]) -> int:
        """
        Uses Pick's theorem to calculate the area of the lagoon.
        Pick's theorem states that A = i + b/2 - 1, where A is the area of the polygon,
        i is the number of lattice points inside the polygon, and b is the number of
        lattice points on the boundary of the polygon.
        In our case, we need i + b = A + b/2 + 1.
        """
        poly = shapely.Polygon(loop)
        return int(poly.area + poly.length / 2 + 1)

    def solve(self, part: int, draw: bool = True) -> None:
        """part should be an integer, 1 or 2"""
        self.reset()
        self.dig(part)
        print(f'Part {part} solution: {self.calc_area(self.lagoon)}')
        if draw:
            self.draw_map(part)
    
    def draw_map(self, part: int) -> None:
        """draws the map"""
        poly = shapely.Polygon(self.lagoon)
        points = list(zip(*poly.exterior.xy))  # list of (x, y) points
        for i in range(len(points) - 1):
            x_values = [points[i][0], points[i+1][0]]
            y_values = [points[i][1], points[i+1][1]]
            plt.plot(
                x_values, 
                y_values, 
                color = self.get_colour(
                    self.colours[i], 
                    self.instructions[i].dir,
                    part
                    )
                )
        plt.show()
    
    @staticmethod
    def get_colour(colour: int, dir: str, part: int) -> str:
        """in part 2 I calculate the colour as the maximum hex value divided by the step size from part 1"""
        if part == 1:
            return colour
        #for a hex like 0xf0f0f, 0x is removed, letters capitalised and f0f0f prepended with 0s 
        # until it is 6 digits long to make a valid hex colour input #0F0F0F
        return f'#{hex((3000000 * ('RDLU'.index(dir) + 1)) + (419 * colour))[2:].upper().zfill(6)}'

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
        self.DIRS: dict[str, tuple[int, int]] = {
            'U': (1, 0),
            'D': (-1, 0),
            'L': (0, -1),
            'R': (0, 1)
        }
    
    def move(self, dir: str, dist: int = 1) -> tuple[int, int]:
        """moves the digger in a direction and distance"""
        self.pos = tuple(
            map(
                sum, 
                zip(
                    self.pos, 
                    #move by distance dist in direction dir
                    tuple(n * dist for n in self.DIRS[dir])
                    )
                )
            )
        return self.pos

S = Site.from_file('dig_plan.txt')
S.solve(1)
S.solve(2)