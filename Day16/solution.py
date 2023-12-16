#personal setup
import os
from icecream import ic

dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)
#solution
with open('cave.txt') as f:
    data = f.read().splitlines()

class Grid:
    """
    Class for simulating light rays as particles moving through a grid of mirrors.
    Initialise with a list of strings representing the grid, e.g. g = Grid(data).
    Run the solution using g.solve(cmd) where cmd is either 'one' or 'all'.

    Attributes:
    self.data: list[str] -> grid of mirrors
    self.width: int -> width of grid
    self.height: int -> height of grid
    self.particles: list[Particle] -> list of particles currently in the simulation
    self.new_particles: list[Particle] -> list of particles to be added to the simulation
    self.seen: set -> set of tuples (position, direction) of particles that have been seen before
    """
    def __init__(self, data: list[str]) -> None:
        self.data: list[str] = data
        self.width: int = len(data[0])
        self.height: int = len(data)
        self.particles: list['Particle'] = []
        self.new_particles: list['Particle'] = []
        self.seen: set = set()

    def __str__(self) -> str:
        #print grid and particles
        for row in self.data:
            print(''.join(row))
        return f'Particles: \n{"\n".join([particle.__str__() for particle in self.particles])}'
    
    def reset(self) -> None:
        #reset simulation
        self.particles = []
        self.new_particles = []
        self.seen = set()
    
    def create_particle(self, pos: tuple[int, int], dir: tuple[int, int]) -> None:
        Particle.create_and_append(self, pos, dir)

    def move_particle(self, particle: 'Particle') -> None:
        #move the particle, check if it is within bounds, and update its direction
        #update particle position by adding the direction vector to the current position
        particle.pos = tuple(map(sum, zip(particle.pos, particle.dir)))
        if self.within_bounds(particle.pos):
            #if particle has been seen before, do not add it to new_particles, 
            # effectively removing it from the simulation
            if (particle.pos, particle.dir) in self.seen:
                return
            self.seen.add((particle.pos, particle.dir))
            self.update_particle(particle)
    
    def within_bounds(self, pos: tuple[int, int]) -> bool:
        #check if particle position is within bounds
        return 0 <= pos[0] < self.height and 0 <= pos[1] < self.width
    
    def update_particle(self, particle: 'Particle') -> None:
        #update particle direction based on the mirror it is on
        mirror = self.data[particle.pos[0]][particle.pos[1]]
        particle.mirrors[mirror]()
    
    def run_simulation(self) -> int:
        while len(self.particles) > 0:
            self.new_particles = []
            for _ in range(len(self.particles)):
                self.move_particle(self.particles.pop(0))
            self.particles = self.new_particles
        return len(set([pos for pos, _ in self.seen]))

    def solve(self, cmd='one') -> None:
        #part 1 cmd -> 'one'
        #part 2 cmd -> 'all'
        starting_particles = self.particle_setup(cmd)
        total = []
        for particle in starting_particles:
            self.reset()
            self.particles.append(particle)
            total.append(self.run_simulation())
        ic(max(total))
    
    def particle_setup(self, cmd: str) -> list['Particle']:
        if cmd == 'one':
            #create a single particle starting in the top left corner moving right
            return [Particle((0, -1), (0, 1))]
        elif cmd == 'all':
            #create a starting particle for each position on the edge of the grid
            #the particles are created outside of the actual grid because when move_particle is called
            # the particle is moved before the particle position is checked to be inside the grid
            particles = []
            for i in range(self.width - 1):
                particles.append(Particle((-1, i), (1, 0)))
                particles.append(Particle((self.height, i), (-1, 0)))
            for i in range(self.height - 1):
                particles.append(Particle((i, -1), (0, 1)))
                particles.append(Particle((i, self.width), (0, -1)))
            return particles

class Particle:
    """
    Class for handling particle motion. New instances are created upon mirror collision.
    Results of mirror collision are stored in new_particles list of Grid class.
    Post-collision direction is calculated based on the mirror the particle is on.
    Cardinal directions are defined as tuples of index changes.
    New particle is created using Particle.create_and_append(grid, pos, dir)
    Particle direction is updated using Grid.update_particle(particle)

    Attributes:
    self.pos: tuple[int, int] -> particle position
    self.dir: tuple[int, int] -> particle direction
    self.mirrors: dict[str, callable] -> dictionary of mirror types and their corresponding transformation functions
    self.<DIRECTION>: tuple[int, int] -> cardinal directions
    """
    def __init__(self, pos: tuple[int, int], dir: tuple[int, int]):
        self.pos = pos
        self.dir = dir
        self.mirrors:dict[str, callable] = {
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
    
    def __str__(self) -> str:
        return f'Particle: [{self.pos}, {self.dir}]'

    @staticmethod
    def flip(tpl: tuple[int, int]) -> tuple[int, int]:
        #flips vector
        return (tpl[1], tpl[0])
    
    @staticmethod
    def neg(tpl: tuple[int, int]) -> tuple[int, int]:
        #negates vector
        return (-tpl[0], -tpl[1])
    
    @staticmethod
    def create_and_append(grid: Grid, pos: tuple[int, int], dir: tuple[int, int]) -> None:
        grid.new_particles.append(Particle(pos, dir))
    
    def dot(self) -> None:
        #creates a new particle moving in the same direction
        self.create_and_append(g, self.pos, self.dir)

    def mirror_slash(self) -> None:
        #flips direction vector and negates it
        self.dir = self.neg(self.flip(self.dir))
        self.create_and_append(g, self.pos, self.dir)
    
    def mirror_backslash(self) -> None:
        #flips direction vector
        self.dir = self.flip(self.dir)
        self.create_and_append(g, self.pos, self.dir)

    def mirror_vertical(self) -> None:
        #creates two new particles moving north and south if approached from the east or west
        if self.dir[0] == 0:
            self.create_and_append(g, self.pos, self.NORTH)
            self.create_and_append(g, self.pos, self.SOUTH)
        #otherwise, the mirror is treated as empty space
        else:
            self.dot()
    
    def mirror_horizontal(self) -> None:
        #creates two new particles moving east and west if approached from the north or south
        if self.dir[1] == 0:
            self.create_and_append(g, self.pos, self.WEST)
            self.create_and_append(g, self.pos, self.EAST)
        #otherwise, the mirror is treated as empty space
        else:
            self.dot()

g = Grid(data)
g.solve('one') #part 1
g = Grid(data)
g.solve('all') #part 2