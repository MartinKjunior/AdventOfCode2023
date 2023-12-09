s = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""

data = s.split("\n")

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

def get_winnings2(cards):
    total = 0
    for card in cards:
        win = get_win(card)
        get_winnings2(card)
    else:
        total += win

def part1():
    parsed = parse_input(data)
    print(get_winnings(parsed))
    
def part2():
    parsed = parse_input(data)
    print(get_winnings2(parsed))

part1()