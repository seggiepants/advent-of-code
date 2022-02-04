import re

# Advent of Code 2021 - Day 17
# ----------------------------

def load_data(filename):
    data_file = open(filename, 'rt')
    lines = data_file.readlines()
    data_file.close()
    lines = [line.strip() for line in lines]

    return lines

def trace(x1, y1, x2, y2, dx, dy):
    x, y = 0, 0
    hit = False
    done = False
    if x1 > x2:
        # swap
        x1, x2 = x2, x1
        
    if  y1 < y2:
        # swap
        y1, y2 = y2, y1
    
    while not done:        
        if x >= x1 and x <= x2 and y <= y1 and y >= y2:
            hit = True
            done = True
        elif y < y2 and dy < 0:
            hit = False
            done = True
            
        yield (x, y, hit)

        if not done:
            x += dx
            y += dy

            if dx > 0:
                dx -= 1
            elif dx < 0:
                dx += 1

            dy -= 1
    

lines = load_data('data.txt')
# lines = load_data('sample_data.txt')
matchCoordinates = re.compile('target area: x=(?P<x1>-?\d+)..(?P<x2>-?\d+), y=(?P<y1>-?\d+)..(?P<y2>-?\d+)')
if len(lines) < 1:
    print("Error no data!")
    exit()

m = matchCoordinates.match(lines[0])
if not m:
    print("Data does not match expected format.")
    exit()

x1 = int(m['x1'])
x2 = int(m['x2'])
y1 = int(m['y1'])
y2 = int(m['y2'])
max_y = 0
hit_i = -500
hit_j = -500
hit_hit = False
candidates = []
for j in range(-500, 501):
    for i in range(501):
        run_max_y = 0
        for x, y, hit in trace(x1, y1, x2, y2, i, j):
            run_max_y = max(y, run_max_y)
        if hit:
            candidates.append((i, j))
            if run_max_y > max_y:
                max_y = run_max_y
                hit_i = i
                hit_j = j
                hit_hit = hit
print(f"Part 1: (see max[y]) i: {hit_i}, j: {hit_j}, x: {x}, y: {y}, hit: {hit_hit}, max(y): {max_y}")
print(f"Part 2: {len(candidates)}")
# 897 is too low

            
    
