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

def calculate_rock_vals(data):
    result = [[] for _ in range(len(data[0]))] #gathering results for each column separately
    height = len(data)
    values = [height for _ in range(height)] #calculating valid rock values
    for i, row in enumerate(data):
        for j, char in enumerate(row):
            if char == '#':
                values[j] = height - i - 1
            elif char == 'O':
                result[j].append(values[j])
                values[j] -= 1
    return result

def solve1(data):
    result = calculate_rock_vals(data)
    ic(sum(map(sum, result)))

def parse_data(data):
    #make use of numpy's rotating function
    return np.array([list(row) for row in data])

def roll_rocks(data):
    N = data
    W = np.rot90(data, -1)
    S = np.rot90(data, -2)
    E = np.rot90(data, -3)
    for rolled in (N, W, S, E):
        shift_rocks(rolled)

def shift_rocks(data):
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

def get_values(data):
    #get the values of the rocks
    result = []
    height = len(data)
    for i, row in enumerate(data):
        count = 0
        for char in row:
            if char == 'O':
                count += 1 
        result.append((height - i) * count)
    return result

def solve2(data):
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