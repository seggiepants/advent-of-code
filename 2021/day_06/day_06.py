# Advent of Code 2021 - Day 06
# ----------------------------
def load_data(filename):
    data_file = open(filename, 'rt')
    lines = data_file.readlines()
    data_file.close()
    lines = [line.strip() for line in lines]

    return lines

def step(fish):
    next_fish = {}
    if 0 in fish:
        next_fish[8] = fish[0]   
    for key in fish:
        new_key = key - 1 if key > 0 else 6
        if new_key in next_fish:
            next_fish[new_key] += fish[key]
        else:
            next_fish[new_key] = fish[key]
    return next_fish    

def simulate(initial_fish, num_days):
    fish = {}
    # decompose into life span and count.
    for value in initial_fish:
        if value in fish:
            fish[value] += 1
        else:
            fish[value] = 1
    for i in range(num_days):
        fish = step(fish)
    return sum(fish[key] for key in fish)

# setup data
# lines = load_data('sample_data.txt')
lines = load_data('data.txt')
initial_fish = [int(age) for age in ','.join(lines).split(',')]

# Part 1
# ------
num_days = 80
print(f'Fish after {num_days} days: {simulate(initial_fish, num_days)}')

# Part 2
# ------
num_days = 256
print(f'Fish after {num_days} days: {simulate(initial_fish, num_days)}')
