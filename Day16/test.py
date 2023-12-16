from icecream import ic
from time import sleep
import os

s = R""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|...."""

data = s.split('\n')

class Grid:
    def __init__(self, data):
        self.data = data
        self.width = len(data[0])
        self.height = len(data)
        self.particles = []
        self.new_particles = []
        self.seen = set()

    def __str__(self):
        for row in self.data:
            print(row)
        return f'Particles: \n{"\n".join([particle.__str__() for particle in self.particles])}'
    
    def reset(self):
        self.particles = []
        self.new_particles = []
        self.seen = set()
    
    def create_particle(self, pos, dir):
        Particle.create_and_append(self, pos, dir)

    def move_particle(self, particle):
        particle.pos = tuple(map(sum, zip(particle.pos, particle.dir)))
        if self.within_bounds(particle.pos):
            #if particle has been seen before, remove it
            if (particle.pos, particle.dir) in self.seen:
                return
            self.seen.add((particle.pos, particle.dir))
            self.update_particle(particle)
    
    def within_bounds(self, pos):
        #check if particle position is within bounds
        return 0 <= pos[0] < self.height and 0 <= pos[1] < self.width
    
    def update_particle(self, particle):
        #update particle direction based on the mirror it is on
        mirror = self.data[particle.pos[0]][particle.pos[1]]
        particle.mirrors[mirror]()
    
    def run_simulation(self):
        while len(self.particles) > 0:
            self.new_particles = []
            for _ in range(len(self.particles)):
                self.move_particle(self.particles.pop(0))
            self.particles = self.new_particles
        return len(set([pos for pos, dir in self.seen]))

    def solve(self, cmd='one'):
        #part 1 cmd -> 'one'
        #part 2 cmd -> 'all'
        starting_particles = self.particle_setup(cmd)
        total = []
        for particle in starting_particles:
            self.reset()
            self.particles.append(particle)
            total.append(self.run_simulation())
        ic(max(total))
    
    def particle_setup(self, cmd):
        if cmd == 'one':
            return [Particle((0, -1), (0, 1))]
        elif cmd == 'all':
            #create a starting particle for each position on the edge of the grid
            particles = []
            for i in range(self.width - 1):
                particles.append(Particle((0, i), (1, 0)))
                particles.append(Particle((self.height-1, i), (-1, 0)))
            for i in range(self.height - 1):
                particles.append(Particle((i, 0), (0, 1)))
                particles.append(Particle((i, self.width-1), (0, -1)))
            return particles
    
    def debug(self):
        dir_map = {
            (0, 1): '>',
            (0, -1): '<',
            (1, 0): 'v',
            (-1, 0): '^'
        }
        data = [list(row) for row in self.data]
        for pos, dir in self.seen:
            data[pos[0]][pos[1]] = dir_map[dir]
        for row in data:
            print(''.join(row))

class Particle:
    def __init__(self, pos, dir):
        self.pos = pos
        self.dir = dir
        self.mirrors = {
            '/': self.mirror_slash,
            '\\': self.mirror_backslash,
            '|': self.mirror_vertical,
            '-': self.mirror_horizontal,
            '.': self.dot
        }
        self.NORTH = (-1, 0)
        self.SOUTH = (1, 0)
        self.EAST = (0, 1)
        self.WEST = (0, -1)
    
    def __str__(self):
        return f'Particle: [{self.pos}, {self.dir}]'

    @staticmethod
    def flip(tpl: tuple):
        return (tpl[1], tpl[0])
    
    @staticmethod
    def neg(tpl: tuple):
        return (-tpl[0], -tpl[1])
    
    @staticmethod
    def create_and_append(grid, pos, dir):
        particle = Particle(pos, dir)
        grid.new_particles.append(particle)
    
    def dot(self):
        self.create_and_append(g, self.pos, self.dir)

    def mirror_slash(self):
        self.dir = self.neg(self.flip(self.dir))
        self.create_and_append(g, self.pos, self.dir)
    
    def mirror_backslash(self):
        self.dir = self.flip(self.dir)
        self.create_and_append(g, self.pos, self.dir)

    def mirror_vertical(self):
        if self.dir[0] == 0:
            self.create_and_append(g, self.pos, self.NORTH)
            self.create_and_append(g, self.pos, self.SOUTH)
        else:
            self.dot()
    
    def mirror_horizontal(self):
        if self.dir[1] == 0:
            self.create_and_append(g, self.pos, self.WEST)
            self.create_and_append(g, self.pos, self.EAST)
        else:
            self.dot()

g = Grid(data)
g.solve('one') #part 1
g = Grid(data)
g.solve('all') #part 2