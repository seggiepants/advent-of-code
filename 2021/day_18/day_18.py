# Advent of Code 2021 - Day 18
# ----------------------------

def load_data(filename):
    data_file = open(filename, 'rt')
    lines = data_file.readlines()
    data_file.close()
    lines = [line.strip() for line in lines]

    return lines

class pair:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        
        return '(' + str(self.left) + ',' + str(self.right) + ')'

def parse(data):
    # pair is [ pair | number , pair | number ]
    # if either sub item is a pair, parse that.
    bracket_count = 0
    digit = ''
    was_digit = False
    left_start = left_end = right_start = right_end = 0
    for index, char in enumerate(data):
        if (not char.isdigit()) and was_digit:
            # finish the digit
            digit_val = int(digit)
            digit = ''
            
        if char == '[':
            bracket_count += 1
            if bracket_count == 1:
                left_start = index + 1
        elif char == ']':
            bracket_count -= 1
            if bracket_count == 0:
                right_end = index - 1                
        elif char == ',':
            if bracket_count == 1:
                left_end = index - 1
                right_start = index + 1
            
    left_side = data[left_start:left_end + 1]
    right_side = data[right_start:right_end + 1]
    if left_side.isdigit():
        left_side = int(left_side)
    else:
        left_side = parse(left_side)
        
    if right_side.isdigit():
        right_side = int(right_side)
    else:
        right_side = parse(right_side)

    return pair(left_side, right_side)

def explode(data, depth = 0):
    #print(f"data: {str(data)}, depth: {depth}")
    if depth >= 4:
        return data.left, data.right, True, True
    else:
        left_sum, right_sum, any_success = 0, 0, False
        if isinstance(data.left, pair):
            left_num, right_num, collapse, success = explode(data.left, depth + 1)
            #print(f"Data: {data} Left: {left_num}, Right: {right_num}, Collapse: {collapse}, Success: {success}")
            if collapse:
                data.left = 0

            if success:
                any_success = True
                if isinstance(data.left, int) and not collapse:
                    data.left += left_num
                    left_num = 0
                if isinstance(data.right, int):
                    data.right += right_num
                    right_num = 0
                else:
                    right_side = data.right
                    while not isinstance(right_side.left, int):
                        right_side = right_side.left
                    right_side.left += right_num
                    right_num = 0

                left_sum += left_num
                right_sum += right_num
                #return left_num, right_num, False, success
            
        if not any_success and isinstance(data.right, pair):
            left_num, right_num, collapse, success = explode(data.right, depth + 1)
            #print(f"Data: {data} Left: {left_num}, Right: {right_num}, Collapse: {collapse}, Success: {success}")
            if collapse:
                data.right = 0
                
            if success:
                any_success = True
                if isinstance(data.left, int):
                    data.left += left_num
                    left_num = 0
                else:
                    left_side = data.left
                    while not isinstance(left_side.right, int):
                        left_side = left_side.right
                    left_side.right += left_num
                    left_num = 0
                    
                if isinstance(data.right, int) and not collapse:
                    data.right += right_num
                    right_num = 0
                left_sum += left_num
                right_sum += right_num
                #return left_num, right_num, False, success
            
    return left_sum, right_sum, False, any_success

def split(data):
    if isinstance(data.left, int):
        value = data.left
        if value >= 10:
            left_num = value // 2
            right_num = value - left_num
            
            data.left = pair(left_num, right_num)
            return True
        
    elif isinstance(data.left, pair):
        if split(data.left):
            return True

    if isinstance(data.right, int):
        value = data.right
        if value >= 10:
            left_num = value // 2
            right_num = value - left_num
            
            data.right = pair(left_num, right_num)
            return True
        
    elif isinstance(data.right, pair):
        if split(data.right):
            return True

    return False

def reduce(data):
    previous = ''
    current = str(data)
    done = False
    while not done:
        #print(f"--> {current}")
        previous = current
        explode(data)
        current = str(data)
        exploded = previous != current
        if not exploded:
            #print (f"Prev {previous} {str(type(previous))} == Cur {current}{str(type(current))}")
            previous = str(data)
            split(data)
            current = str(data)
            was_split = previous != current
            if not was_split:
                #print("Split returned false")
                done = True
    #print(f"[ok] {data}")

def magnitude(data):
    if isinstance(data.left , int):
        left = 3 * data.left
    else:
        left = 3 * magnitude(data.left)

    if isinstance(data.right, int):
        right = 2 * data.right
    else:
        right = 2 * magnitude(data.right)
    return left + right

def add(x, y):
    return pair(x, y)

def explode_test(data):
    x = parse(data)
    print(x)
    explode(x)
    print(x)
    print()

def split_test(data):
    x = parse(data)
    print(x)
    split(x)
    print(x)
    print()

def reduce_test(data):
    x = parse(data)
    print(x)
    reduce(x)
    print(x)
    print()

lines = load_data('data.txt')
# lines = load_data('sample_data.txt')
lines = [line for line in lines if len(line) > 0]

# print(lines[:5])
#explode_test(' [[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]')
#explode_test('[[[[[9,8],1],2],3],4]')
#explode_test('[7,[6,[5,[4,[3,2]]]]]')
#explode_test('[[[[0,7],4],[7,[[8,4],9]]],[1,1]]')
#split_test('[[[[0,7],4],[15,[0,13]]],[1,1]]')
#split_test('[[[[0,7],4],[[7,8],[0,13]]],[1,1]]')
#reduce_test('[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]')
"""
a = parse("[1,1]")
b = parse("[2,2]")
c = parse("[3,3]")
d = parse("[4,4]")
e = parse("[5,5]")
f = parse("[6,6]")
x = add(a, b)
x = add(x, c)
x = add(x, d)
reduce(x)
print(x)
x = add(x, e)
reduce(x)
print(x)
x = add(x, f)
reduce(x)
print(x)
x = parse('[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]')
print(f"Magnitude: {magnitude(x)}")
"""
first = True
total = parse(lines[0])
print(total)
for line in lines:
    if first:
        first = False
    else:
        value = parse(line)
        print(f"+ {value}")
        print("===========")
        total = add(total, value)
        reduce(total)
        print(f"= {total}")
        
print(f"Part 1: {magnitude(total)}")
# 4230 is too low.

largest_magnitude = 0
for j in range(len(lines)):
    for i in range(len(lines)):
        if i != j:
            a = parse(lines[i])
            b = parse(lines[j])
            a = add(a, b)
            reduce(a)
            current_magnitude = magnitude(a)
            largest_magnitude = max(current_magnitude, largest_magnitude)

print(f"Part 2: {largest_magnitude}")
