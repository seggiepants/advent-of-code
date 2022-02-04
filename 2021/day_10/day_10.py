# Advent of Code 2021 - Day 10
# ----------------------------

ERROR_MSG = "Error!"

def load_data(filename):
    data_file = open(filename, 'rt')
    lines = data_file.readlines()
    data_file.close()
    lines = [line.strip() for line in lines]

    return lines

def get_syntax_points(line, brackets, points):
    stack = [];
    for char in line:
        if char in brackets.keys():
            stack.append(char)
        else:
            match = stack.pop()
            if char != brackets[match]:
                return points[char]
    # if len(stack[] != 0 then incomplete
    return 0

def get_autocomplete(line, brackets):
    stack = [];
    for char in line:
        if char in brackets.keys():
            stack.append(char)
        else:
            match = stack.pop()
            if char != brackets[match]:
                return ERROR_MSG
    ret = ""
    while len(stack) > 0:
        ret += brackets[stack.pop()]    
    return ret

def score_autocomplete(data, points):
    total_score = 0
    for char in data:
        total_score *= 5
        total_score += points[char]
    return total_score

#lines = load_data('sample_data.txt')
lines = load_data('data.txt')

brackets = { '(': ')', '[': ']', '{': '}', '<': '>'}
points = { ')': 3, ']': 57, '}': 1197, '>': 25137 }
autocomplete_points = {')': 1, ']': 2, '}': 3, '>': 4}

# Part 1
# ======

running_sum = 0
for line in lines:
    running_sum += get_syntax_points(line, brackets, points)

print(f'Part 1: {running_sum}')

# Part 2
# ======
scores = []
for line in lines:
    data = get_autocomplete(line, brackets)
    if data != ERROR_MSG:
        scores.append(score_autocomplete(data, autocomplete_points))

scores.sort()
middle = len(scores) // 2 # Integer divide dropping the .5
print(f'Part 2: {scores[middle]}')
