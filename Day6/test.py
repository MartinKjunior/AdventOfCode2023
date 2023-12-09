s = """Time:      7  15   30
Distance:  9  40  200"""

data = s.split("\n")

import numpy as np

def parse_data(data):
    data = [line.split(":")[1] for line in data]
    data = [line.split() for line in data]
    for i, _ in enumerate(data):
        data[i] = [int(line) for line in data[i]]
    return data

def distance(t_max, t_charge):
    return t_charge * (t_max - t_charge)

def max_t_charge(t_max, d_record):
    return (t_max + np.sqrt(t_max**2 - 4*d_record)) / 2, (t_max - np.sqrt(t_max**2 - 4*d_record)) / 2

def calculate_possibilities(t_max, d_record):
    limits = max_t_charge(t_max, d_record)
    t_charge = int(limits[1]+1), int(np.ceil(limits[0]-1))
    return t_charge[1] - t_charge[0] + 1

def part1(parsed):
    total = 1
    for t_max, d_record in zip(*parsed):
        total *= calculate_possibilities(t_max, d_record)
    print(total)

def alter_data(parsed):
    parsed = [int("".join(map(str, line))) for line in parsed]
    return parsed

def part2(parsed):
    t_max, d_record = alter_data(parsed)
    print(calculate_possibilities(t_max, d_record))

parsed = parse_data(data)
part1(parsed)
part2(parsed)