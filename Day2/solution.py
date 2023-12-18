#personal setup
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)
#solution
with open('games.txt') as f:
    content = f.readlines()

class Game:
    def __init__(self, game: str, part: int) -> None:
        self.part = part
        self.id = self.parse_id(game)
        self.rounds = self.parse_rounds(game)
        self.set_colors()
        self.possible = True
        self.power = 0

    def parse_id(self, game: str) -> int:
        return int(game.split(':')[0].replace('Game ', ''))

    def parse_rounds(self, game: str) -> list[str]:
        return [s.strip() for s in game.split(':')[-1].split(';')]

    def set_colors(self) -> None:
        if self.part == 1:
            self.red = 12
            self.green = 13
            self.blue = 14
        elif self.part == 2:
            self.red = 0
            self.green = 0
            self.blue = 0
    
    def parse_round(self, round: str) -> tuple[int, int, int]:
        split = [s.strip() for s in round.split(',')]
        r, g, b = 0, 0, 0
        for cubes in split:
            n, color = cubes.split(' ')
            if color == 'red':
                r = int(n)
            elif color == 'green':
                g = int(n)
            elif color == 'blue':
                b = int(n)
        return r, g, b
    
    def check_round(self, r: int, g: int, b: int) -> None:
        if r > self.red or g > self.green or b > self.blue:
            self.possible = False
    
    def find_min(self, r: int, g: int, b: int) -> None:
        #finds minimum number of cubes needed to win, which is the max of the 
        # current number of cubes and the previous max
        if r > self.red:
            self.red = r
        if g > self.green:
            self.green = g
        if b > self.blue:
            self.blue = b
    
    def play_rounds(self) -> None:
        for round in self.rounds:
            r,g,b = self.parse_round(round)
            if self.part == 1:
                self.check_round(r, g, b)
            elif self.part == 2:
                self.find_min(r, g, b)
                self.power = self.red * self.green * self.blue
    
    def return_result(self) -> int:
        if self.part == 1:
            if self.possible:
                return self.id
            else:
                return 0
        elif self.part == 2:
            return self.power

def solve(n: int) -> None:
    if n not in (1, 2):
        raise ValueError('n must be 1 or 2')
    total = 0
    for game in content:
        game = Game(game, n)
        game.play_rounds()
        total += game.return_result()
    print(total)

solve(2)
