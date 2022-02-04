import re

# Advent of Code 2021 - Day 13
# ----------------------------

fold = re.compile('fold along (?P<axis>x|y)=(?P<coordinate>\d+)')
point = re.compile('(?P<x>\d+), ?(?P<y>\d+)')

def load_data(filename):
    data_file = open(filename, 'rt')
    lines = data_file.readlines()
    data_file.close()
    lines = [line.strip() for line in lines]

    return lines

def print_grid(grid):
    for row in grid:
        print(row)
    print()

def fold_grid(grid, axis, coordinate):
    old_width = len(grid[0])
    old_height = len(grid)

    if axis == 'x':
        new_grid = [['.' for x in range(coordinate)] for y in range(old_height)]
        for y in range(old_height):
            for x in range(old_width):
                if x < coordinate:
                    new_grid[y][x] = '#' if grid[y][x] == '#' or new_grid[y][x] == '#' else '.'
                elif x > coordinate:
                    new_grid[y][coordinate - x] = '#' if grid[y][x] == '#' or new_grid[y][coordinate - x] == '#' else '.'
                else:
                    pass #skip on fold line.
    elif axis == 'y':
        new_grid = [['.' for x in range(old_width)] for y in range(coordinate)]
        for y in range(old_height):
            for x in range(old_width):
                if y < coordinate:
                    new_grid[y][x] = '#' if grid[y][x] == '#' or new_grid[y][x] == '#' else '.'
                elif y > coordinate:
                    new_grid[coordinate - y][x] = '#' if grid[y][x] == '#' or new_grid[coordinate - y][x] == '#' else '.'
                else:
                    pass #skip on fold line.
    else:
        return [[]] # empty grid

    new_grid = [''.join(row) for row in new_grid]
    return new_grid

lines = load_data('data.txt')
# lines = load_data('sample_data.txt')

# convert into points and folds
points = []
folds = []
for line in lines:
    m = point.match(line)
    if m:
        x = int(m['x'])
        y = int(m['y'])
        points.append((x, y))
    else:
        m = fold.match(line)
        if m:
            axis = m['axis']
            coordinate = int(m['coordinate'])
            folds.append((axis, coordinate))

# now make a grid out of it
grid = [''.join(['#' if (x, y) in points else '.' for x in range(max(point[0] for point in points) + 1)]) for y in range(max(point[1] for point in points) + 1)]
# print_grid(grid)

firstFold = True
for fold in folds:
    grid = fold_grid(grid, fold[0], fold[1])
    if firstFold:
        firstFold = False
        dot_count = sum(sum(1 for cell in row if cell == '#') for row in grid)
        print(dot_count)

print_grid(grid)

    
