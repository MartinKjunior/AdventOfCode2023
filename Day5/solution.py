#personal setup
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)
#solution
from copy import deepcopy

with open("almanac.txt", "r") as f:
    data = f.read().split("\n\n")

def parse_data(data: list) -> (list[int], list[list[list[int]]]): 
    data = [line.split(":")[1] for line in data]
    data = [line.split("\n") for line in data]
    for i, _ in enumerate(data):
        data[i] = [line.strip() for line in data[i] if line]
        data[i] = [line.split(" ") for line in data[i]]
        for j, _ in enumerate(data[i]):
            data[i][j] = [int(line) for line in data[i][j]]
    source = data[0][0]
    destination = data[1:]
    return source, destination

def translate_number(seed: int, line: list[int]):
    return line[0] + (seed - line[1])

def check_number(seed: int, map: list[list[int]]):
    for line in map:
        n = line[1] #source number
        if n <= seed <= n + line[2]:
            return translate_number(seed, line)
    return seed

def translate_seeds(source: list[int], destination: list[list[list[int]]]):
    translated = []
    for seed in source:
        for map in destination:
            seed = check_number(seed, map)
        translated.append(seed)
    return translated
class Range:
    def __init__(self, start: int, end: int = None, steps: int = None):
        self.start = start
        if steps:
            self.end = start + steps - 1
        else:
            self.end = end
        self.seen = False
    def __contains__(self, item: int):
        return self.start <= item <= self.end
    def __repr__(self):
        return f"Range({self.start}, {self.end})"
    def __lt__(self, other):
        return self.start < other.start
    def __gt__(self, other):
        return self.end > other.end

def ranges_from_seeds(source: list[int]):
    sources = []
    for i in range(0,len(source),2):
        sources.append(Range(source[i], steps=source[i+1]))
    return sources

def range_intersection(r1: Range, r2: Range):
    #r1 -> source from map, r2 -> source from seeds
    if not (r2.start <= r1.end and r2.end >= r1.start):
        return []
    output = []
    output.append(Range(max(r1.start, r2.start), min(r1.end, r2.end)))
    if r2.start < r1.start:
        output.append(Range(r2.start, r1.start - 1))
    if r2.end > r1.end:
        output.append(Range(r1.end + 1, r2.end))
    return output

def translate_range(seed: Range, line: list[int]):
    return Range(
        line[0] + (seed.start - line[1]),
        line[0] + (seed.end - line[1]),
        )

def get_intersections(seeds: list[Range], destinations: list[list[list[int]]]):
    for Map in destinations:
        new_seeds = []
        for line in Map:
            source_range = Range(line[1], steps = line[2])
            for seed in seeds:
                if seed.seen:
                    continue
                intersection = range_intersection(source_range, seed)
                if intersection:
                    new_seeds.append(translate_range(intersection[0], line))
                    seeds.extend(intersection[1:])
                    seed.seen = True
        new_seeds.extend([seed for seed in seeds if not seed.seen])
        seeds = new_seeds.copy()
    return seeds

def part1():
    print(min(translate_seeds(*parse_data(data))))

def part2():
    source, destination = parse_data(data)
    sources = ranges_from_seeds(source)
    print(min(get_intersections(sources, destination)).start)

part1()
part2()