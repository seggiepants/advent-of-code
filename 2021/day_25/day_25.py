# Advent of Code 2021 - Day 25
# ----------------------------


def load_data(filename):
    data_file = open(filename, 'rt')
    lines = data_file.readlines()
    data_file.close()
    lines = [list(line.strip()) for line in lines]

    return lines

def str_grid(grid):
    return '\n'.join(''.join(row) for row in grid)

def print_grid(grid):
    print(str_grid(grid))
    print()

def step(grid):
    next_grid = [[cell for cell in row] for row in grid]
    
    # first pass east-ward moving
    for j, row in enumerate(grid):
        for i, cell in enumerate(row):
            next_i = i + 1
            if next_i >= len(row):
                next_i = 0
            if cell == '>' and grid[j][next_i] == '.':
                next_grid[j][next_i] = '>'
                next_grid[j][i] = '.'

    # second pass southward-moving
    counter = 0
    for j, row in enumerate(next_grid):
        next_j = j + 1
        if next_j >= len(next_grid):
            next_j = 0
        for i, cell in enumerate(row):
            if grid[j][i] == 'v':
                if next_grid[next_j][i] == '.' and (grid[next_j][i] == '.' or grid[next_j][i] == '>'):
                    next_grid[next_j][i] = 'v'
                    next_grid[j][i] = '.' #str(counter)
                    counter = (counter + 1) % 10

    return next_grid


# lines = load_data('sample_data.txt')
lines = load_data('data.txt')

grid = [[cell for cell in row] for row in lines]
current = str_grid(grid)
previous = ''
i = 0
while current != previous:
    i += 1    
    previous = current
    grid = step(grid)
    current = str_grid(grid)

print(f"Part 1: Stopped moving at {i} steps.")

