s = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""

data = s.split("\n\n")

from copy import deepcopy

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

class Range:
    def __init__(self, start: int, end: int = None, steps: int = None):
        self.start = start
        if steps:
            self.end = start + steps - 1
        else:
            self.end = end
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
    if r1.start in r2 and r1.start > r2.start:
        output.append(Range(r2.start, r1.start))
    if r1.end in r2 and r1.end < r2.end:
        output.append(Range(r1.end, r2.end))
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
            for seed in seeds:
                if seed.start is None:
                    continue
                source_range = Range(line[1], line[1]+line[2]-1)
                intersection = range_intersection(source_range, seed)
                if intersection:
                    intersection[0] = translate_range(intersection[0], line)
                    new_seeds.extend(intersection)
                    seed.start = None
        new_seeds.extend([seed for seed in seeds if seed.start is not None])
        seeds = deepcopy(new_seeds)
    return seeds

def part2():
    source, destination = parse_data(data)
    sources = ranges_from_seeds(source)
    print(min(get_intersections(sources, destination)).start)

part2()