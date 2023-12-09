s = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""

data = s.split('\n')

def parse_data(data):
    return [list(map(int, line.split(' ')))[::-1] for line in data]

def calculate_next_line(line):
    new_line = []
    for i in range(len(line)-1):
        new_line.append(line[i] - line[i+1])
    return new_line

def find_prediction(line):
    line_total = 0
    backward_values = []
    while not all([n == 0 for n in line]):
        line_total += line[0]
        backward_values.append(line[-1])
        line = calculate_next_line(line)
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
    current_value = 0
    for i in range(len(backward_values)):
        backward_values[i] = backward_values[i] - current_value
        current_value = backward_values[i]
    return backward_values[-1]

solve(data, 'both')