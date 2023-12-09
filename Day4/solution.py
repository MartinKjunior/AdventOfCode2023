import os

dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)

with open("scratchcards.txt", "r") as f:
    data = f.read().splitlines()

def parse_input(data):
    parsed = []
    for line in data:
        line = line.split(":")
        numbers = line[1].strip().split("|")
        parsed.append(
            [
                set([int(x) for x in numbers[0].strip().split()]),
                set([int(x) for x in numbers[1].strip().split()])
                ]
            )
    return parsed

def get_win(card: list[set]) -> int:
    return len(card[0].intersection(card[1]))

def get_winnings(parsed):
    num_of_wins = [get_win(x) for x in parsed]
    winnings = [2**(x-1) for x in num_of_wins if x > 0]
    return sum(winnings)

def get_winnings2(i, line):
    return 1 + sum(get_winnings2(j, parsed[j]) for j in range(i + 1, i + 1 + get_win(line)))

def part1():
    print(get_winnings(parsed))
    
def part2():
    total = 0
    for i, line in enumerate(parsed):
        total += get_winnings2(i, line)
    print(total)

parsed = parse_input(data)

part1()
part2()