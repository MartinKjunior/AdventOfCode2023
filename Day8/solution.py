#personal setup
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)
#solution
with open("maps.txt", "r") as f:
    data = f.read().splitlines()

def parse(data):
    #returns
    #instructions: string
    #network: dict[node] = (left_child, right_child)
    instructions = data[0]
    network = {}
    for line in data[2:]:
        splt = line.split(" = ")
        node = splt[0]
        children = tuple(splt[1].replace("(", "").replace(")", "").split(", "))
        network[node] = children
    return instructions, network

def run(current, instructions, network, stop):
    #solves one run of the instructions
    #stops when we reach final node
    steps = 0
    for instruction in instructions:
        steps += 1
        if instruction == "L":
            current = network[current][0]
        elif instruction == "R":
            current = network[current][1]
        if current.endswith(stop):
            return current, steps
    return current, steps

def keep_running(position, instructions, network, stop):
    #repeats instructions until we get to the end
    total = 0
    while not position.endswith(stop):
        position, steps = run(position, instructions, network, stop)
        total += steps
    return total

def solve1(data):
    instructions, network = parse(data)
    position = "AAA"
    stop = "ZZZ"
    total = keep_running(position, instructions, network, stop)
    print(total)

def extract_starts(network):
    #returns all nodes that end with "A"
    starts = set()
    for node in network:
        if node[-1] == "A":
            starts.add(node)
    return starts

def solve2(data):
    from math import lcm
    instructions, network = parse(data)
    positions = extract_starts(network)
    stop = "Z"
    cycles = set()
    for position in positions:
        total = keep_running(position, instructions, network, stop)
        cycles.add(total)
    print(lcm(*cycles))

solve1(data)
solve2(data)