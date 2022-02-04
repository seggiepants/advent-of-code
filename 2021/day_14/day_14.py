import re

# Advent of Code 2021 - Day 14
# ----------------------------

matchKey = re.compile('(?P<key>\w+) -> (?P<value>\w)')

def load_data(filename):
    data_file = open(filename, 'rt')
    lines = data_file.readlines()
    data_file.close()
    lines = [line.strip() for line in lines]

    return lines

def step(state, pairs):
    new_state= ''
    key = ''
    for i in range(0, len(state) - 1):
        key = state[i:i + 2]
        if len(key) > 1:
            if key in pairs:
                new_state += key[0] + pairs[key]
            else:
                new_state += key[0]
    if len(key) > 1:
        new_state += key[1]

    return new_state

def step2(state, count, isFirst, elements):
    global pairs
    global reuseElements
    if count < 1:
        for char in state:
            if char in elements:
                elements[char] += 1
            else:
                elements[char] = 1
            return
    
    for i in range(0, len(state) - 1):
        key = state[i:i + 2]
        if len(key) > 1:
            if key in pairs:
                new_char = pairs[key]
                key1 = key[0] + new_char
                key2 = new_char + key[1]
                if isFirst:
                    if key1 not in reuseElements:
                        newElements = {}
                        step2(key1, count - 1, False, newElements)
                        reuseElements[key1] = newElements
                    for elemKey in reuseElements[key1].keys():
                            if elemKey in elements:
                                elements[elemKey] += reuseElements[key1][elemKey]
                            else:
                                elements[elemKey] = reuseElements[key1][elemKey]

                    if key2 not in reuseElements:
                        newElements = {}
                        step2(key2, count - 1, False, newElements)
                        reuseElements[key2] = newElements
                    for elemKey in reuseElements[key2].keys():
                            if elemKey in elements:
                                elements[elemKey] += reuseElements[key2][elemKey]
                            else:
                                elements[elemKey] = reuseElements[key2][elemKey]
                else:                
                    step2(key[0] + new_char, count - 1, False, elements)
                    step2(new_char + key[1], count - 1, False, elements)
        if isFirst and i % 1000 == 0:
            print((100 * i)/len(state))
    #if len(key) > 1:
    #    new_state += key[1]

lines = load_data('data.txt')
# lines = load_data('sample_data.txt')
startState = ''
pairs = {}

for line in lines:
    if len(startState) == 0 and len(line) > 0:
        startState = line
    elif len(line) > 0:
        m = matchKey.match(line)
        if m:
            pairs[m['key']] = m['value']

state = startState
# print(f'Start: {state}')
for i in range(10):
    state = step(state, pairs)
    # print(f'{i + 1}: {state}')

elements = {}
for char in state:
    if char in elements:
        elements[char] += 1
    else:
        elements[char] = 1
sortedElements = sorted(elements, key = elements.get, reverse=False)
print(f'Part 1: {elements[sortedElements[-1]] - elements[sortedElements[0]]}')
# print(elements)

# stalls at about 20
for i in range(10):
    state = step(state, pairs)
    print(i + 11)


#state = startState
# print(f'Start: {state}')
#for i in range(40):
#    state = step(state, pairs)
#    print(f'{i + 1}: {len(state)}')

iterations = 20 # last 20.
elements = {}
reuseElements = {}
step2(state, iterations, True, elements)
# print(f'{iterations}: {state} {len(state)}')

if state[-1] in elements:
    elements[state[-1]] += 1
else:
    elements[state[-1]] = 1

#for char in state:
#    if char in elements:
#        elements[char] += 1
#    else:
#        elements[char] = 1
sortedElements = sorted(elements, key = elements.get, reverse=False)
print(f'Part 2: {elements[sortedElements[-1]] - elements[sortedElements[0]]}')
print(elements)
