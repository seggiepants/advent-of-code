data_file = open('data.txt', 'rt')
lines = data_file.readlines()
data_file.close()
lines = [line.strip() for line in lines]

sample = [
    '00100', '11110', '10110', '10111', '10101', '01111', '00111',
    '11100', '10000', '11001', '00010', '01010'
    ]
# uncomment to use sample values
# lines = sample

# Filter down list of values until only one entry remains.
# Parameters:
# minimize: are get getting the gamma (maximizer) or epsilon (mimizer) result
# values: list of binary numbers stored a strings
# returns: decimal version of only remaining value
def filter_input(minimize, values):
    index = 0
    key = ''
    key_len = max(len(value) for value in values)
    while len(values) > 1 and index < key_len:
        zero_count = len(list(filter(lambda x: x[index] == '0', values)))
        one_count = len(list(filter(lambda x: x[index] == '1', values)))
        if zero_count == one_count:
            char = '0' if minimize else '1'
        elif zero_count > one_count:
            char = '1' if minimize else '0'
        else: # one_count > zero_count
            char = '0' if minimize else '1'
        key = key + char 
        values = list(filter(lambda x: x[index] == key[index], values))
        index += 1
    return int(values[0], 2)

# Part 1
# ------
max_len = max(len(line) for line in lines)
gamma = ""
epsilon = ""
for i in range(max_len):
    count_zero = 0
    count_one = 0
    for line in lines:
        char = line[i]
        if char == '0':
            count_zero += 1
        elif char == '1':
            count_one += 1
    gamma += '0' if count_zero > count_one else '1'
    epsilon += '1' if count_zero > count_one else '0'

print(f"Part 1:  {int(gamma, 2) * int(epsilon, 2)}")

# Part 2
# ------
gamma = filter_input(False, lines)
epsilon = filter_input(True, lines)
print(f"Part 2: {gamma * epsilon}")
