import functools

# Advent of Code 2021 - Day 09
# ----------------------------
def load_data(filename):
    data_file = open(filename, 'rt')
    lines = data_file.readlines()
    data_file.close()
    lines = [line.strip() for line in lines]

    return lines

def isLowPoint(grid, i, j):
    cell = grid[j][i]
    ret = True
    if j > 0:
        ret = ret and grid[j - 1][i] > cell
    if i > 0:
        ret = ret and grid[j][i - 1] > cell
    if j < len(grid) - 1:
        ret = ret and grid[j + 1][i] > cell
    if i < len(grid[j]) - 1:
        ret = ret and grid[j][i + 1] > cell
    return ret

def getBasinSize(grid, i, j):
    return getBasinSize_Helper(grid, i, j, set())

def getBasinSize_Helper(grid , i, j, visited):
    # base case
    if grid[j][i] == 9 or (i, j) in visited:
        return len(visited)

    visited.add((i, j))
    # recursive call neighbors if exist.
    if j > 0:
        getBasinSize_Helper(grid, i, j - 1, visited)
    if i > 0:
        getBasinSize_Helper(grid, i - 1, j, visited)
    if j < len(grid) - 1:
        getBasinSize_Helper(grid, i, j + 1, visited)
    if i < len(grid[j]) - 1:
        getBasinSize_Helper(grid, i + 1, j, visited)

    return len(visited)
    
lines = load_data('data.txt')
# lines = load_data('sample_data.txt')

grid = [[int(cell) for cell in list(row)] for row in lines]

riskLevel = 0

for j in range(len(grid)):
    for i in range(len(grid[j])):
        if isLowPoint(grid, i, j):
            riskLevel += 1 + grid[j][i]

print(f'Part 1: {riskLevel}')

basin_sizes = []                   
for j in range(len(grid)):
    for i in range(len(grid[j])):
        if isLowPoint(grid, i, j):
            basin_sizes.append(getBasinSize(grid, i, j))

basin_sizes.sort(reverse=True)
print(f'Part 2: {functools.reduce(lambda a, b: a * b, basin_sizes[:3])}')
                               
