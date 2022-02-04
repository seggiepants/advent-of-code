import sys
import math
from queue import PriorityQueue

# Advent of Code 2021 - Day 15
# ----------------------------

def load_data(filename):
    data_file = open(filename, 'rt')
    lines = data_file.readlines()
    data_file.close()
    lines = [line.strip() for line in lines]

    return lines

def estimate(cell_x, cell_y, target_x, target_y):
    dx = target_x - cell_x
    dy = target_y - cell_y
    return math.sqrt(dx*dx + dy*dy)

def rollover(grid, i, j):
    width = len(grid[0])
    height = len(grid)
    x = i % width
    y = j % height
    x_step = (i - x) / width
    y_step = (j - y) / height
    value = grid[y][x] + x_step + y_step
    return int(((value - 1) % 9) + 1)

def enlarge(grid, multiplier):
    width = len(grid[0])
    height = len(grid)
    return [[rollover(grid, i, j) for i in range(width * multiplier)] for j in range(height * multiplier)]

def search(grid, x, y, target_x, target_y):
    new_grid = [[{'distance': sys.maxsize, 'previous': None, 'cost': col, 'visited': False} for col in row] for row in grid]
    new_grid[y][x]['distance'] = 0    
    queue = PriorityQueue()
    queue.put((estimate(x, y, target_x, target_y), (x, y)))
    while not queue.empty():
        cell = queue.get()[1]
        if new_grid[cell[1]][cell[0]]['visited']:
            continue
        
        new_grid[cell[1]][cell[0]]['visited'] = True
        
        neighbors = get_neighbors(grid, cell[0], cell[1])
        neighbors = [neighbor for neighbor in neighbors if new_grid[neighbor[1]][neighbor[0]]['visited'] == False]
        for neighbor in neighbors:
            
            tempDistance = new_grid[cell[1]][cell[0]]['distance'] + grid[neighbor[1]][neighbor[0]]
            queue.put((tempDistance, neighbor))
            currentDistance = new_grid[neighbor[1]][neighbor[0]]['distance']
            if tempDistance < currentDistance:
                new_grid[neighbor[1]][neighbor[0]]['distance'] = tempDistance
                new_grid[neighbor[1]][neighbor[0]]['previous'] = cell
    cost = 0
    current = (target_x, target_y)
    path = []
    while new_grid[current[1]][current[0]]['previous'] != None:
        path = [current] + path
        cost += grid[current[1]][current[0]]        
        current = new_grid[current[1]][current[0]]['previous']
    path = [(x, y)] + path
    return (cost, path)

def print_grid(grid):
    for row in grid:
        temp_row = [str(i) for i in row]
        print(''.join(temp_row))

# stolen and modified from day 11 to allow only 4 directions.
def get_neighbors(grid, col, row):
    neighbors = []

    directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]
    for direction in directions:
        j = row + direction[1]
        i = col + direction[0]
        if j >= 0 and i >= 0 and j < len(grid) and i < len(grid[row]):
            if j != row or i != col:
                neighbors.append((i, j))
    return neighbors

lines = load_data('data.txt')
# lines = load_data('sample_data.txt')
grid = [[int(cell) for cell in row] for row in lines]

x, y = 0, 0
target_x, target_y = len(lines[0]) - 1, len(lines) - 1

ret = search(grid, x, y, target_x, target_y)
print(f"Part 1: {ret[0]}")
#path = ret[1]
#print_me = [['*' if (i, j) in path else str(grid[j][i]) for i in range(len(grid[0]))] for j in range(len(grid))]
#print_grid(print_me)

rollover = enlarge(grid, 5)
x, y = 0, 0
target_x, target_y = len(rollover[0]) - 1, len(rollover) - 1
ret = search(rollover, x, y, target_x, target_y)
print(f"Part 2: {ret[0]}")

#path = ret[1]
#print_me = [['*' if (i, j) in path else str(rollover[j][i]) for i in range(len(rollover[0]))] for j in range(len(rollover))]
#print_grid(print_me)
