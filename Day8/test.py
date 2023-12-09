s = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""

data = s.splitlines()

def parse(data):
    instructions = data[0]
    network = {}
    for line in data[2:]:
        splt = line.split(" = ")
        node = splt[0]
        children = tuple(splt[1].replace("(", "").replace(")", "").split(", "))
        network[node] = children
    return instructions, network

def run(current, instructions, network, stop):
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

def solve1(data):
    instructions, network = parse(data)
    position = "AAA"
    total = 0
    stop = "ZZZ"
    while position != stop:
        position, steps = run(position, instructions, network, stop)
        total += steps
    print(total)

def run_old(current_set, instructions, network):
    steps = 0
    stop = False
    for instruction in instructions:
        steps += 1
        Z_endings = 0
        new_set = set()
        for current in current_set:
            if instruction == "L":
                current = network[current][0]
            elif instruction == "R":
                current = network[current][1]
            if current[-1] == "Z":
                Z_endings += 1
                new_set.add(current)
        if Z_endings == len(current_set):
            return current, steps, True
    return current, steps, False

def extract_starts(network):
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
        total = 0
        while not position.endswith(stop):
            position, steps = run(position, instructions, network, stop)
            total += steps
        cycles.add(total)
    print(lcm(*cycles))

solve2(data)