#personal setup
import os
from icecream import ic
from collections import deque, namedtuple

dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)
#solution
with open('test.txt') as f:
    data = f.read().splitlines()

class Garden:
    """Find possible final locations after taking n steps from the start."""
    
    Walker = namedtuple('Walker', ['x', 'y', 'steps'])
    Point = namedtuple('Point', ['x', 'y'])
    
    def __init__(self, data, steps):
        self.data = data
        self.steps = steps
        self.start = self.find_start()
        self.walkers = deque([self.Walker(*self.start, 0)])
        self.visited = set()
        self.DIRS = [
            self.Point(0, 1), 
            self.Point(0, -1), 
            self.Point(1, 0), 
            self.Point(-1, 0)
            ]
    
    def find_start(self) -> tuple[int, int]:
        for i, row in enumerate(self.data):
            for j, col in enumerate(row):
                if col == 'S':
                    return (i, j)
    
    def step(self, walker):
        for direction in self.DIRS:
            new_walker = self.Walker(
                walker.x + direction.x, 
                walker.y + direction.y,
                walker.steps + 1
                )
            if self.data[new_walker.x][new_walker.y] != '#':
                self.walkers.append(new_walker)
                self.visited.discard(self.Point(new_walker.x, new_walker.y))

    def solve(self):
        while self.walkers:
            walker = self.walkers.popleft()
            if walker not in self.visited and walker.steps <= self.steps:
                self.visited.add(walker)
                self.step(walker)
        reachable = sum([x.steps == self.steps for x in self.visited])
        ic(reachable)
    
G = Garden(data, 6)
G.solve()