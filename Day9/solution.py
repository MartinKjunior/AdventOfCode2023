import os

dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)

with open("oasis.txt", "r") as f:
    data = f.read().splitlines()

def parse_data(data):
    return [list(map(int, line.split(' ')))[::-1] for line in data]

def calculate_next_line(line):
    #subtract neighbouring numbers to find the next line
    new_line = []
    for i in range(len(line)-1):
        new_line.append(line[i] - line[i+1])
    return new_line

def find_prediction(line):
    #we can find the forward prediction by finding the sum of the
    # right-most diagonal of the resulting pyramid
    line_total = 0 #part 1
    backward_values = [] #part 2
    while not all([n == 0 for n in line]):
        backward_values.append(line[-1]) #part 2
        line_total += line[0] #part 1
        line = calculate_next_line(line) #part 1
    return line_total, backward_values[::-1]

def solve(data, part):
    data = parse_data(data)
    total_forward = []
    total_backward = []
    #find results
    for line in data:
        line_total, backward_values = find_prediction(line)
        total_forward.append(line_total)
        total_backward.append(calculate_backward(backward_values))
    #get results and show
    result1 = sum(total_forward)
    result2 = sum(total_backward)
    if part == 1:
        print(result1)
    elif part == 2:
        print(result2)
    elif part == 'both':
        print(f'Part 1: {result1}')
        print(f'Part 2: {result2}')
    elif part == 'debug':
        pass

def calculate_backward(backward_values):
    #all we need to figure out the backward value is the
    # left-most diagonal of the resulting pyramid
    # luckily the number of steps isn't too high
    current_value = 0
    for i in range(len(backward_values)):
        backward_values[i] = backward_values[i] - current_value
        current_value = backward_values[i]
    return backward_values[-1]

solve(data, 'both')