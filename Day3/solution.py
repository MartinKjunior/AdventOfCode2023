#personal setup
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)
#solution
with open('schematic.txt') as f:
    l = f.read().splitlines()

h = len(l)
w = len(l[0])

def find_number(l, k, m, w):
    #find all indices of a number in a single row
    idxs = []
    while m < w:
        char = l[k][m]
        if char.isdigit():
            idxs.append(m)
            m += 1
        else:
            break
    return idxs

def bound(n):
    #limit the number to be above 0 for slicing
    #list[-1:2] returns [] instead fo the first 2 elements
    #do list[bound(-1):2] instead
    if n < 0:
        return 0
    else:
        return n

def get_square_slice(lst, x1, y1, x2, y2):
    #get a square slice of a 2D list
    return [row[y1:y2+1] for row in lst[x1:x2+1]]

def check_symbol(s):
    #check if a symbol is a counting symbol
    return not s.isalnum() and s != '.'

def count_flag(square):
    #if check_symbol returns True for any char in list, return True
    return any(check_symbol(char) for row in square for char in row)

def part1():
    total = 0
    for i in range(h):
        j = 0
        while j < w:
            char = l[i][j]
            if char.isdigit():
                idxs = find_number(l, i, j, w)
                square = get_square_slice(l, bound(i-1), bound(idxs[0]-1), i+1, idxs[-1]+1)
                if count_flag(square):
                    total += int(l[i][idxs[0]:idxs[-1]+1])
                #skip to the end of the found number
                j = idxs[-1]
            j += 1
    print(total)

def find_star(square):
    #if check_symbol returns True for any char in list, return True
    for i, row in enumerate(square):
        for j, char in enumerate(row):
            if char == '*':
                return (i, j)
    return None

def part2():
    total = 0
    possible_gears = []
    for i in range(h):
        j = 0
        while j < w:
            char = l[i][j]
            if char.isdigit():
                idxs = find_number(l, i, j, w)
                square = get_square_slice(l, bound(i-1), bound(idxs[0]-1), i+1, idxs[-1]+1)
                star_idx = find_star(square)
                if star_idx is not None:
                    star_position = (star_idx[0] + bound(i-1), star_idx[1] + bound(idxs[0]-1))
                    gear_value = int(l[i][idxs[0]:idxs[-1]+1])
                    possible_gears.append((star_position, gear_value))
                #skip to the end of the found number
                j = idxs[-1]
            j += 1
    #find the product of all part numbers that have a star nearby
    count = {}
    for gear in possible_gears:
        if gear[0] in count:
            count[gear[0]] = [count[gear[0]][0] + 1, count[gear[0]][1] * gear[1]]
        else:
            count[gear[0]] = [1, gear[1]]
    for value in count.values():
        if value[0] > 2:
            print(value)
    #find the sum of all gears where 2 part numbers are sharing the same star
    for value in count.values():
        if value[0] == 2:
            total += value[1]
    print(total)

part1()
part2()
