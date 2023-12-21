#personal setup
import os
from icecream import ic
from collections import deque, namedtuple
from collections.abc import Iterable
from scipy import interpolate

dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)
#solution
with open('garden.txt') as f:
    data = f.read().splitlines()

class Garden:
    """Find possible final locations after taking n steps from the start."""
    
    Walker = namedtuple('Walker', ['x', 'y', 'steps'])
    Point = namedtuple('Point', ['x', 'y'])
    
    def __init__(self, data: list[str]):
        self.data = data
        self.size = (len(data), len(data[0]))
        self.steps = 0
        self.start = self.find_start()
        self.walkers = deque([self.Walker(*self.start, 0)])
        self.visited = set()
        self.DIRS = [
            self.Point(0, 1), 
            self.Point(0, -1), 
            self.Point(1, 0), 
            self.Point(-1, 0)
            ]
    
    def reset(self) -> None:
        self.walkers = deque([self.Walker(*self.start, 0)])
        self.visited = set()
    
    def find_start(self) -> tuple[int, int]:
        for i, row in enumerate(self.data):
            for j, col in enumerate(row):
                if col == 'S':
                    return (i, j)
    
    def step(self, walker: Walker) -> None:
        """Take a step in each cardinal direction. Ensure new location is not blocked."""
        for direction in self.DIRS:
            new_walker = self.Walker(
                walker.x + direction.x, 
                walker.y + direction.y,
                walker.steps + 1
                )
            if self.data[new_walker.x % self.size[0]][new_walker.y % self.size[1]] != '#':
                self.walkers.append(new_walker)

    def solve1(self, steps: int) -> int:
        """Find the number of locations that can be reached in exactly n steps."""
        self.reset()
        self.steps = steps
        while self.walkers:
            walker = self.walkers.popleft()
            if walker not in self.visited and walker.steps <= self.steps:
                self.visited.add(walker)
                self.step(walker)
        reachable = sum([x.steps == self.steps for x in self.visited])
        print(f'Part 1: {reachable=}')
        return reachable
    
    def solve2(self) -> None:
        results = []
        inputs = [65, 196, 327]
        goal = 26501365
        for steps in inputs:
            results.append(self.solve1(steps))
        bary = self._interp_bary(inputs, results, goal)
        lagrange = self._interp_lag(inputs, results, goal)
        splrep = self._interp_splrep(inputs, results, goal)
        print(f'Part 2: {bary=},\n\t{lagrange=},\n\t{splrep=}')
    
    @staticmethod
    def _interp_bary(x: Iterable, y: Iterable, x0: int) -> int:
        #barycentric interpolation did not work
        return int(interpolate.barycentric_interpolate(x, y, x0).round())
    
    @staticmethod
    def _interp_lag(x: Iterable, y: Iterable, x0: int) -> int:
        return int(interpolate.lagrange(x, y)(x0))
    
    @staticmethod
    def _interp_splrep(x: Iterable, y: Iterable, x0: int) -> int:
        result = interpolate.splrep(x, y, k = 2)
        return int(interpolate.splev(x0, result).round())
    
G = Garden(data)
G.solve1(64) #part 1
G.solve2() #part 2