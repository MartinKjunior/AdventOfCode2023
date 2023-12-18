from icecream import ic
import shapely

s = """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)"""

data = s.split('\n')

class Site:
    def __init__(self, data):
        self.data: str = data
        self.instructions: list[str, int, str] = self.parse_data()
        self.lagoon: list[tuple[int, int]] = list()
        self.digger: 'Digger' = Digger()
        self.dir_dict = {
            '0': 'R',
            '1': 'D',
            '2': 'L',
            '3': 'U'
        }
    
    def parse_data(self) -> list[str, int, str]:
        parsed = []
        for row in data:
            row = row.split(' ')
            parsed.append([row[0], int(row[1]), row[2].strip('()')])
        return parsed
    
    def show_instructions(self) -> None:
        for i, row in enumerate(self.instructions):
            ic(i, row)
    
    def dig(self, part: int) -> None:
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
        self.dig(part)
        print(f'Part {part} solution: {self.calcArea(self.lagoon)}')

    def translate_colour(self, colour: str) -> tuple[str, int]:
        dist = int(colour[1:-1], 16)
        dir = self.dir_dict[colour[-1]]
        return dir, dist

class Digger:
    def __init__(self, dir: str = 'None', pos: tuple[int, int] = (0, 0)):
        self.pos = pos
        self.dir = dir
        self.dirs = {
            'U': (1, 0),
            'D': (-1, 0),
            'L': (0, -1),
            'R': (0, 1)
        }
    
    def move(self, dir: str, dist: int = 1) -> tuple[int, int]:
        self.pos = tuple(map(sum, zip(self.pos, tuple(n * dist for n in self.dirs[dir]))))
        return self.pos

S = Site(data)
S.solve(2)