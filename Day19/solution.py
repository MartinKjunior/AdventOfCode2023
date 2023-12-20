#personal setup
import os
from icecream import ic
from dataclasses import dataclass
import operator
from collections import namedtuple

dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)
#solution
with open('workflows.txt') as f:
    data = f.read()

@dataclass
class Part:
    x: int
    m: int
    a: int
    s: int

    def __repr__(self) -> str:
        return f'Part(x={self.x}, m={self.m}, a={self.a}, s={self.s})'

    def __str__(self) -> str:
        return f'Part(x={self.x}, m={self.m}, a={self.a}, s={self.s})'

    def __getitem__(self, key):
        return getattr(self, key)
    
    def yield_attrs(self) -> tuple[str, int]:
        for attr in self.__dict__.keys():
            yield attr, getattr(self, attr)
    
    def get_values(self) -> tuple[int]:
        return tuple(val for _, val in self.yield_attrs())

class System:

    Expression = namedtuple(
            'Expression', 
            'key op value nxt', 
            defaults=(None, None, None, None),
        )

    def __init__(self, data: str):
        self.workflows: dict[str, list[self.Expression]] = {}
        self.parts: list[Part] = []
        self.parse_data(data)
        self.comparators: dict[str, function] = {
            '>': operator.gt,
            '<': operator.lt,
        }
        self.accepted: list[Part] = []
        self.rejected: list[Part] = []
    
    def __repr__(self) -> str:
        return f'System({self.workflows}, {self.parts})'

    def parse_data(self, data: str) -> None:
        """Parses the data into workflows and parts"""
        workflows, parts = data.split('\n\n')
        for part in parts.splitlines():
            self.parts.append(Part(**self.parse_part(part)))
        for workflow in workflows.splitlines():
            self.parse_workflow(workflow)

    def parse_workflow(self, workflow: str) -> None:
        """Parses a workflow string into a dictionary of workflow names and lists of Expressions"""
        name = workflow[:workflow.index('{')]
        expression = workflow[workflow.index('{') + 1:-1]
        self.workflows[name] = self.parse_expression(expression)
    
    def parse_expression(self, expression: str) -> list[Expression|str]:
        """Parses an expression string into a list of Expressions"""
        output = []
        for exp in expression.split(','):
            if ':' in exp:
                #example input: "a<2006:qkq"
                name = exp[0]
                op = exp[1]
                value, nxt = exp[2:].split(':')
                output.append(
                    self.Expression(name, op, int(value), nxt)
                    )
            else:
                output.append(exp)
        return output

    @staticmethod
    def parse_part(part: str) -> dict[str, int]:
        """Parses a part into a dictionary to feed into Part class"""
        d = {}
        for expression in part[1:-1].split(','):
            attr, value = expression.split('=')
            d[attr] = int(value)
        return d

    def run(self) -> None:
        """Runs the system"""
        for part in self.parts:
            self.run_part(part)

    def run_part(self, part: Part) -> str:
        """Runs a part through the system stopping at A or R"""
        curr = 'in'
        while curr not in ('A', 'R'):
            expressions = self.workflows[curr]
            for E in expressions:
                if isinstance(E, str):
                    curr = E
                    break
                else:
                    if self.comparators[E.op](part[E.key], E.value):
                        curr = E.nxt
                        break
        if curr == 'A':
            self.accepted.append(part)
        else:
            self.rejected.append(part)
    
    def solve(self) -> None:
        """Solves the assignment"""
        self.run()
        ic(sum(sum(part.get_values()) for part in self.accepted))

S = System(data)
S.solve()