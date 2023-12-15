#personal setup
import os
from icecream import ic

dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)
#solution
with open('initialization_sequence.txt') as f:
    data = f.read().split(',')

def HASH(curr: int, s: str) -> int:
    return (curr + ord(s)) * 17 % 256

def apply_hash(s: str) -> int:
    curr = 0
    for c in s:
        curr = HASH(curr, c)
    return curr

def solve1(data: list[str]) -> None:
    total = 0
    for step in data:
        total += apply_hash(step)
    ic(total)

def add(boxes: dict[int, dict[str, int]], step: str) -> None:
    boxes[apply_hash(step[:-2])][step[:-2]] = int(step[-1])

def delete(boxes: dict[int, dict[str, int]], step: str) -> None:
    boxes[apply_hash(step[:-1])].pop(step[:-1], None)

def focusing_power(boxes: dict[int, dict[str, int]]) -> int:
    total = 0
    for i, box in enumerate(boxes.values(), 1):
        for j, f in enumerate(box.values(), 1):
            total += i * j * f
    return total

def solve2(data: list[str]) -> None:
    boxes: dict[int, dict[str, int]] = {i : {} for i in range(256)}
    for step in data:
        if step[-2] == '=':
            add(boxes, step)
        elif step.endswith('-'):
            delete(boxes, step)
    ic(focusing_power(boxes))

solve1(data)
solve2(data)