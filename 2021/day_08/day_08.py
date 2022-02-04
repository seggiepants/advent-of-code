import itertools

# Advent of Code 2021 - Day 08
# ----------------------------
def load_data(filename):
    data_file = open(filename, 'rt')
    lines = data_file.readlines()
    data_file.close()
    lines = [line.strip() for line in lines]

    return lines

def sort_word(word):
	l = list(word)
	l.sort()
	return ''.join(l)

lines = load_data('data.txt')
# lines = load_data('sample_data.txt')

# parse each line to pattern, and output
lines = [[row.strip().split(' ') for row in line.split('|')] for line in lines]

# Part 1
# =======
uniques = [2, 4, 3, 7] # unique segment highlighted count.
total = 0
for line in lines:
    output = line[1]
    total += sum(1 for pattern in output if len(pattern) in uniques)
print(total)

# Part 2
# ======
"""
use itertools.permutations('abcdefg', 7) to get every possible combination of wirings 5040 of them.
for each string check if each word when mapped makes a valid digit if not  try next permutation"""
patterns = ['' for i in range(10)]
matches = []
output_total = 0
for line in lines:
    matches = []
    for permutation in itertools.permutations('abcdefg', 7):
        patterns[0] = permutation[0] + permutation[1] + permutation[2] + permutation[4] + permutation[5] + permutation[6]
        patterns[1] = permutation[2] + permutation[5]
        patterns[2] = permutation[0] + permutation[2] + permutation[3] + permutation[4] + permutation[6]
        patterns[3] = permutation[0] + permutation[2] + permutation[3] + permutation[5] + permutation[6]
        patterns[4] = permutation[1] + permutation[2] + permutation[3] + permutation[5]
        patterns[5] = permutation[0] + permutation[1] + permutation[3] + permutation[5] + permutation[6]
        patterns[6] = permutation[0] + permutation[1] + permutation[3] + permutation[4] + permutation[5] + permutation[6]
        patterns[7] = permutation[0] + permutation[2] + permutation[5]
        patterns[8] = ''.join(permutation)
        patterns[9] = permutation[0] + permutation[1] + permutation[2] + permutation[3] + permutation[5] + permutation[6]

        patterns = [sort_word(word) for word in patterns]
        match = True
        
        for signal in line[0] + line[1]:
            if sort_word(signal) not in patterns:
                match = False
                break
        if match: 
            solution = 0
            
            for digit in line[1]:
                for i in range(len(patterns)):
                    if sort_word(digit) == patterns[i]:
                        solution = (solution * 10) + i
                        break
            matches.append((permutation, solution))
            break

    if len(matches) == 1:
        output_total += matches[0][1] # 2nd half of tuple is the decoded output
    else:
        print(f"Error: no matches found")

print(output_total)
