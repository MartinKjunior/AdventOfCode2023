#personal setup
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)

maze = []
with open('input.txt') as f:
    for line in f:
        maze.append(line[:-1])

for i, row in enumerate(maze):
    if 'S' in row:
        start = (row.index('S'), i)

for start_dir in 'RULD':
    dir = start_dir
    x, y = start
    flag = True
    solved = False
    nodes = {start: 0}
    path = [start]
    n = 0
    while flag:
        n += 1
        match dir:
            case 'R':
                if x + 1 < len(maze[y]):
                    x += 1
                else:
                    flag = False
            case 'U':
                if y > 0:
                    y -= 1
                else:
                    flag = False
            case 'L':
                if x > 0:
                    x -= 1
                else:
                    flag = False
            case 'D':
                if y + 1 < len(maze):
                    y += 1
                else:
                    flag = False
        if not flag:
            break
        nodes[(x, y)] = n
        path.append((x, y))
        match maze[y][x]:
            case 'L':
                match dir:
                    case 'L':
                        dir = 'U'
                    case 'D':
                        dir = 'R'
            case 'J':
                match dir:
                    case 'R':
                        dir = 'U'
                    case 'D':
                        dir = 'L'
            case '7':
                match dir:
                    case 'R':
                        dir = 'D'
                    case 'U':
                        dir = 'L'
            case 'F':
                match dir:
                    case 'L':
                        dir = 'D'
                    case 'U':
                        dir = 'R'
            case '.':
                flag = False
            case 'S':
                flag = False
                solved = True
    if solved:
        break
print(nodes[start]>>1)
path = path[:-1]

sum = 0
for i in range(len(path)):
    n_1 = path[i]
    n_2 = path[(i+1)%len(path)]
    x_1, y_1 = n_1
    x_2, y_2 = n_2
    sum += x_1 * y_2 - y_1 * x_2

area = abs(sum/2)

print(area-len(path)/2+1)
print(path)