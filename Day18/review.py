"""
As always - comments are from the lens of looking at this as if it 
were production code getting checked in with an eye towards
maintainability.
overall -- super clean
Biggest improvement to your code would be to take advantage of
custom classes with named parameters -- either through namedtuple
or a dataclass or even a custom class
for 'production code':
- always write a __repr__ for your class. a __str__ is also nice
- docstrings/tests/blahblah
"""

import shapely

"""
From the lens of 'production code' -- you could easily make this a class method
@classmethod
def from_file(cls, filename):
    with open(filename) as f:
        data = f.read().splitlines()
    return cls(data)
    
Then your class consumers could just call it as
s = Site.from_file("dig_plan.txt")
"""
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
        """
        I would make a namedtuple or dataclass Instructions. Then you can
        semantically refer to the individual fields instead of having to access
        them as [0][1][2]
        """
        self.instructions: list[str, int, str] = self.parse_data()
        self.lagoon: list[tuple[int, int]] = list()
        
        """
        I think you can just use self.digger: Digger as the type annotation?
        """
        self.digger: 'Digger' = Digger()
        
        """
        Style note: I'd probably make DIR_DICT all upper case, since you're
        using it like a constant
        """
        self.dir_dict: dict[str, str] = {
            '0': 'R',
            '1': 'D',
            '2': 'L',
            '3': 'U'
        }
    
    def reset(self) -> None:
        #resets the digger and the lagoon
        """
        You should make that a proper docstring instead of a # comment!
        Just change the #resets... to '''resets ...''' (but with whatever quote
        format you're using in this code)
        """
        self.lagoon = list()
        self.digger = Digger()
    
    """
    This has a subtle bug - you should be passing in data as an argument, or
    call 'for row in self.data'. This only works right now in your
    code because 'data' exists in the scope since you're calling from
    init. But it wouldn't work if someone just manually called this method
    """
    def parse_data(self) -> list[list[str, int, str]]:
        #parses the data into a list of instructions
        parsed = []
        for row in data:
            row = row.split(' ')
            """
            If this were a dataclass, you could semantically refer
            to the field names and even do the input sanitization
            """
            """
            @dataclass
            class Instruction:
                dir: str
                dist: int
                color: str
                
                def __post_init__(self):
                    self.dist = int(self.dist)
                    self.color = self.color.strip('()')
            """
            parsed.append([row[0], int(row[1]), row[2].strip('()')])
        return parsed
        
    """
    This code is short enough that it's completely fine to leave it as is,
    but if, say, there were ever a part three, I'd probably move the logic
    of how to handle the code into separate 'private' functions and then
    have dig just be responsible for calling the appropriate function. Like:
    
    def dig(self, part: int) -> None:
        dig_runner = None
        match int(part):
            case 1:
                dig = self._dig1
            case 2:
                dig = self._dig2
            case 3:
                dig = self._dig3
            case _:
                raise TypeError(blah blah...)
        for instruction in self.instructions:
            dig_runner(instruction)
    
    def _dig1(self, instruction):
        ...
    def _dig2(self, instruction):
        ...
    def _dig3(self, instruction):
        ...
    """
     
    def dig(self, part: int) -> None:
        #runs through the instructions and digs the lagoon
        """
        sanitize part by casting it to int (make it easier for people to call your code)
        part = int(part)
        """
        for instruction in self.instructions:
            if part == 1:
                dir = instruction[0]
                dist = instruction[1]
                self.lagoon.append(self.digger.move(dir, dist))
            elif part == 2:
                dir, dist = self.translate_colour(instruction[2])
                self.lagoon.append(self.digger.move(dir, dist))
            """
            You wrote this later: #part should be an integer, 1 or 2
            Since you're enforcing this check, I would actually raise
            an error as else:
            else:
                raise ValueError(f"Part should be 1 or 2, got: {part}")
            """
    

    """
    nitpick: pep8?
    """
    @staticmethod
    def calcArea(loop: list[tuple[int, int]]) -> int:
        poly = shapely.Polygon(loop)
        """
        So, whenever I see a magic constants in code,
        the number one thing you can do to make your code more
        maintainable is to:
        1. Give it a name, and
        2. If that wasn't enough, add a comment.
        
        Comments should (almost) never explain _how_ a code works
        Comments should explain _why_ code does what it does.
        
        I haven't even finished p18 yet... why is it dividing by 2 and adding 1?
        
        Named variables would help. 
        """
        return int(poly.area + poly.length / 2 + 1)


    def solve(self, part: int) -> None:
        #part should be an integer, 1 or 2
        self.reset()
        self.dig(part)
        print(f'Part {part} solution: {self.calcArea(self.lagoon)}')

    def translate_colour(self, colour: str) -> tuple[str, int]:
        #translates the colour into a direction and distance
        """
        The next line could be a separate static method or even a module function.
        Makes it testable. Also - could then be part of your
        dataclass constructor so you don't have to do all these'
        extra things
        """
        dist = int(colour[1:-1], 16) #-- super clever
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
        """
        See note above about constants
        """
        self.dirs: dict[str, tuple[int, int]] = {
            'U': (1, 0),
            'D': (-1, 0),
            'L': (0, -1),
            'R': (0, 1)
        }
    
    def move(self, dir: str, dist: int = 1) -> tuple[int, int]:
        #moves the digger in a direction and distance
        
        """
        _if_ this were production code, I don't know that I would
        advocate for a nested tuple(map(sum, zip())).
        
        It's at the limits of what I'd consider acceptable.
        """
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