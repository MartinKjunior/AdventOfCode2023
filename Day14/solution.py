#personal setup
import os
from icecream import ic

dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)
#solution
with open('rocks.txt') as f:
    data = f.read().splitlines()

import numpy as np
from hashlib import sha256

def calculate_rock_vals(data: list[str]) -> list[list[int]]:
    result = [[] for _ in range(len(data[0]))] #gathering results for each column separately
    height = len(data)
    values = [height for _ in range(height)] #calculating valid rock values
    for i, row in enumerate(data):
        for j, char in enumerate(row):
            if char == '#':
                #the boundary defined the new maximum possible value
                values[j] = height - i - 1
            elif char == 'O':
                #assign the value to the rock
                #the next rock will have a value of 1 less since it's under the previous rock
                result[j].append(values[j])
                values[j] -= 1
    return result

def solve1(data: list[str]) -> None:
    result = calculate_rock_vals(data)
    #sums the values for each column and then sums the columns
    ic(sum(map(sum, result)))

def parse_data(data: list[str]) -> np.ndarray:
    #make use of numpy's rotating function to make part 2 easier
    return np.array([list(row) for row in data])

def roll_rocks(data: np.ndarray) -> None:
    #rotate the array such that moving the rocks up will move them in the 
    # north, west, south, east direction on the original array
    N = data
    W = np.rot90(data, -1) #returns a view
    S = np.rot90(data, -2)
    E = np.rot90(data, -3)
    for rolled in (N, W, S, E):
        shift_rocks(rolled)

def shift_rocks(data: np.ndarray) -> None:
    #shifts rocks up until they hit a boundary
    coords = np.argwhere(data == 'O')
    for coord in coords:
        #remove the rock from its original position
        #if for loop breaks immediately, rock is placed in its original position
        data[*coord] = '.'
        for _ in range(coord[0]):
            coord[0] -= 1
            if data[*coord] != '.':
                #step back to a valid position
                coord[0] += 1
                break
        data[*coord] = 'O'

def get_values(data: np.ndarray) -> list[int]:
    #get the values of the rocks
    #the rocks are already shifted in the correct location so just count their values
    result = []
    height = len(data)
    for i, row in enumerate(data):
        count = 0
        for char in row:
            if char == 'O':
                count += 1 
        result.append((height - i) * count)
    return result

def solve2(data: list[str]) -> None:
    data = parse_data(data)
    hashes = {}
    while True:
        #use hashes as a representation of the arrays
        h = sha256(data).hexdigest()
        if h in hashes:
            #found loop
            break
        hashes[h] = len(hashes)
        roll_rocks(data)
    start = hashes[h]
    length = len(hashes) - start #length of the loop
    for _ in range((10**9 - start) % length):
        roll_rocks(data)
    result = get_values(data)
    ic(sum(result))

solve1(data)
solve2(data)