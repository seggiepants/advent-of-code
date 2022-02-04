# Advent of Code 2021 - Day 07
# ----------------------------
def load_data(filename):
    data_file = open(filename, 'rt')
    lines = data_file.readlines()
    data_file.close()
    lines = [line.strip() for line in lines]

    return lines

def calc_cost(crabs, position):
    return sum(abs(position - crab) for crab in crabs)

def calc_increasing_cost(crabs, position):
    return sum(distance_cost(abs(position - crab)) for crab in crabs)

def distance_cost(distance):
    return int((distance * (distance + 1)) / 2.0)

# Sample Data
# lines = load_data('sample_data.txt')

# Puzzle Data
lines = load_data('data.txt')
lines = [int(num) for num in ','.join(lines).split(',')]

start = min(lines)
stop = max(lines)

# Part 1
# ======
has_cost = False
min_cost = 0
min_target = 0
for target in range(start, stop + 1):
    cost = calc_cost(lines, target)
    if not has_cost or cost < min_cost:
        min_target = target
        min_cost = cost
        has_cost = True

print(f"Target {min_target} for a cost of {min_cost}")

# Part 2
# ======
has_cost = False
min_cost = 0
min_target = 0
for target in range(start, stop + 1):
    cost = calc_increasing_cost(lines, target)
    if not has_cost or cost < min_cost:
        min_target = target
        min_cost = cost
        has_cost = True

print(f"Target {min_target} for a cost of {min_cost}")
