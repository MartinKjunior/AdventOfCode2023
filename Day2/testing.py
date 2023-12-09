s = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""

class Game:
    def __init__(self, game, red=12, green=13, blue=14):
        self.id = self.parse_id(game)
        self.rounds = self.parse_rounds(game)
        self.red = red
        self.green = green
        self.blue = blue
        self.possible = True

    def parse_id(self, game):
        return int(game.split(':')[0].replace('Game ', ''))

    def parse_rounds(self, game):
        return [s.strip() for s in game.split(':')[-1].split(';')]
    
    def parse_round(self, round):
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
    
    def check_round(self, r, g, b):
        if r > self.red:
            self.possible = False
        if g > self.green:
            self.possible = False
        if b > self.blue:
            self.possible = False
    
    def play_rounds(self):
        for round in self.rounds:
            r,g,b = self.parse_round(round)
            self.check_round(r, g, b)
    
    def return_result(self):
        if self.possible:
            return self.id
        else:
            return 0

total = 0
for game in s.split('\n'):
    game = Game(game)
    game.play_rounds()
    total += game.return_result()
print(total)