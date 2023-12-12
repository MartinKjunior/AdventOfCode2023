s = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""

data = s.split('\n')

def parse_data(data: "list[str]") -> "list[tuple[str, tuple[int]]]":
    new_data = []
    for line in data:
        springs, damaged = line.split(' ')
        damaged = tuple([int(x) for x in damaged.split(',')])
        new_data.append((springs, damaged))
    return new_data

parsed = parse_data(data)

print(parsed)

