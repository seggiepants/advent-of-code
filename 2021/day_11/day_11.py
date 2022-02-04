# Advent of Code 2021 - Day 11
# ----------------------------
ENERGY = 'energy'
FLASHED = 'hasFlashed'

def load_data(filename):
    data_file = open(filename, 'rt')
    lines = data_file.readlines()
    data_file.close()
    lines = [line.strip() for line in lines]

    return lines

def flash_cascade(grid, col, row):    
    grid[row][col][ENERGY] += 1
    
    if grid[row][col][ENERGY] > 9 and grid[row][col][FLASHED] == False:
        grid[row][col][FLASHED] = True

        #print(f"cascade at {col},{row}")
        neighbors = get_neighbors(grid, col, row)

        for neighbor in neighbors:
            flash_cascade(grid, neighbor[0], neighbor[1])
    
def get_neighbors(grid, col, row):
    neighbors = []

    for j in range(row - 1, row + 2):
        for i in range(col - 1, col + 2):
            if j >= 0 and i >= 0 and j < len(grid) and i < len(grid[row]):
                if j != row or i != col:
                    neighbors.append((i, j))
    return neighbors

def step(grid):
    # increment energy level by 1. Flash if needed and cascade   
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            flash_cascade(grid, col, row)

    # reset octopi that have flashed to 0.
    flash_count = 0
    for row in grid:
        for col in row:
            if col[FLASHED]:
                col[FLASHED] = False
                col[ENERGY] = 0
                flash_count += 1
    return flash_count

def pretty_print(grid):
    print('\n'.join([','.join([str(cell['energy']) for cell in row]) for row in grid]))

lines = load_data('data.txt')
# lines = load_data('sample_data.txt')


# Part 1
# ======

# parse into dictionaries item['energy'] = energy level, item['hasFlashed'] = has flashed
octopi = [[{'energy': int(cell), 'hasFlashed': False} for cell in list(row)] for row in lines]

NUM_STEPS = 100
# pretty_print(octopi)

flash_count = 0
for i in range(NUM_STEPS):
    flashes = step(octopi)
    # print("")
    # print(f"Step: {i + 1}  Flash Count: {flashes}")
    # pretty_print(octopi)
    flash_count += flashes
print(f"Flash Count:  {flash_count}")

# Part 2
# ======

# reset the data
octopi = [[{'energy': int(cell), 'hasFlashed': False} for cell in list(row)] for row in lines]

step_num = 0
num_cells = sum(sum(1 for cell in row) for row in octopi)
done = False
while not done:
    step_num += 1
    flashes = step(octopi)
    if flashes == num_cells:
        done = True
print(f"Syncronized Flash at Step: {step_num}")
        
