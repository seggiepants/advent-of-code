import re
import functools

# Advent of Code 2021 - Day 05
# ----------------------------
def load_data(filename):
    data_file = open(filename, 'rt')
    lines = data_file.readlines()
    data_file.close()
    lines = [line.strip() for line in lines]

    return lines

def get_line_segments(lines):
    re_line = re.compile('(?P<x1>\d+),(?P<y1>\d+) -> (?P<x2>\d+),(?P<y2>\d+)')
    return [{'x1': int(m[0])
             , 'y1': int(m[1])
             , 'x2': int(m[2])
             , 'y2': int(m[3])} for m in re_line.findall('\n'.join(lines))]

def sign(num):
    if num == 0:
        return 0
    elif num > 0:
        return 1
    else:
        return -1
    
def build_grid(segments):
    grid = {}
    for segment in segments:
        x1 = segment['x1']
        x2 = segment['x2']
        y1 = segment['y1']
        y2 = segment['y2']
        dx = sign(x2 - x1)
        dy = sign(y2 - y1)
        if dx == 0:
            # vertical
            y_1 = min(y1, y2)
            y_2 = max(y1, y2)
            for y in range(y_1, y_2 + 1):
                if not y in grid:
                    grid[y] = {}
                if x1 in grid[y]:
                    grid[y][x1] += 1
                else:
                    grid[y][x1] = 1
                    
        elif dy == 0:
            # horizontal
            x_1 = min(x1, x2)
            x_2 = max(x1, x2)
            if not y1 in grid:
                grid[y1] = {}
                
            for x in range(x_1, x_2 + 1):
                if x in grid[y1]:
                    grid[y1][x] += 1
                else:
                    grid[y1][x] = 1
        else:
            # diagonal
            # WARNING: Assuming 45 degree angle.
            y = y1
            x = x1
            while x != x2 + dx and y != y2 + dy:
                
                if not y in grid:
                    grid[y] = {}
                if x in grid[y]:
                    grid[y][x] += 1
                else:
                    grid[y][x] = 1

                x += dx
                y += dy
    return grid

sample_data = ['0,9 -> 5,9'
               , '8,0 -> 0,8'
               , '9,4 -> 3,4'
               , '2,2 -> 2,1'
               , '7,0 -> 7,4'
               , '6,4 -> 2,0'
               , '0,9 -> 2,9'
               , '3,4 -> 1,4'
               , '0,0 -> 8,8'
               , '5,5 -> 8,2']

# Part 1
# ------
# Data from file
lines = load_data('data.txt')

# Sample data
# lines = sample_data

# get line segments
segments = get_line_segments(lines)
# limit to horizontal or vertical lines.
cartesian_segments = [segment for segment in segments if segment['x1'] == segment['x2'] or segment['y1'] == segment['y2']]
grid = build_grid(cartesian_segments)
overlap = sum(sum(1 for col in grid[row] if grid[row][col] > 1) for row in grid)
print(overlap)

# Part 2
# ------
grid = build_grid(segments)
overlap = sum(sum(1 for col in grid[row] if grid[row][col] > 1) for row in grid)
print(overlap)
