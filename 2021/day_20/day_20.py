import turtle

# Advent of Code 2021 - Day 19
# ----------------------------

pix_lookup = { '#': '1', '.': '0'}

def load_data(filename):
    data_file = open(filename, 'rt')
    lines = data_file.readlines()
    data_file.close()
    lines = [line.strip() for line in lines]

    return lines

def border(pixels, border_size, char):
    data = []
    for i in range(border_size):
        data.append(char*(len(pixels[0]) + (border_size * 2)))
    for line in pixels:
        data.append(char*border_size + line + char*border_size)
    for i in range(border_size):
        data.append(char*(len(pixels[0]) + (border_size * 2)))
    return data

def step(pixels, key, default_char):
    new = ['.' * len(pixels[0]) for row in pixels]
    for j in range(len(pixels)):
        row = [pixel for pixel in pixels[j]]
        for i in range(len(row)):
            row[i] = key[sample(pixels, i, j, default_char)] #key[0])]
        new[j] = ''.join(row)
    #print_grid(new)
    #print()
    return new

def sample(pixels, i, j, default_char):
    ret = ''
    max_y = len(pixels) - 1
    max_x = len(pixels[0]) - 1
    for y in range(j - 1, j + 2):
        for x in range(i - 1, i + 2):
            if x < 0 or x >= max_x or y < 0 or y > max_y:
                char = default_char
            else:
                char = pixels[y][x]
            ret += pix_lookup[char]
    return int(ret, base=2)

def print_grid(pixels):
    for line in pixels:
        print(line)

def draw_image(data):
    img = [row for row in data if row != '.'*len(row)]
    left_chop = 0
    first = True
    for row in img:
        indent = 0
        while row[indent] == '.':
            indent += 1
        if first:
            left_chop = indent
            first = False
        else:
            left_chop = min(left_chop, indent)
    for i in range(len(img)):
        img[i] = img[i][left_chop:]

    right_chop = 0
    first = True
    for row in img:
        indent = len(row) - 1
        while row[indent] == '.' and indent >= 0:
            indent -= 1
        if first:
            right_chop = indent
            first = False
        else:
            right_chop = max(right_chop, indent)
    for i in range(len(img)):
        img[i] = img[i][:right_chop]

    print_grid(img)

    half_x = len(img[0]) / 2
    half_y = len(img) / 2
    turtle.penup()
    turtle.left(90)
    turtle.forward(half_y)
    turtle.left(90)
    turtle.forward(half_y)
    turtle.right(180)
    turtle.pencolor('black')
    turtle.speed('fastest')
    turtle.tracer(0, 0)
    turtle.hideturtle()
    for row in img:
        for char in row:
            if char == '#':
                turtle.pendown()
            else:
                turtle.penup()
            turtle.forward(1)
        turtle.penup()
        turtle.right(90)
        turtle.forward(1)
        turtle.right(90)
        turtle.forward(len(row))
        turtle.left(180)
        
    turtle.update()            

# lines = load_data('sample_data.txt')
lines = load_data('data.txt')

key = lines[0]
odd_even = []
if key[0] == '#':
    odd_even = ['.', '#']
else:
    odd_even = ['.']
      
data = lines[2:]
#print_grid(data)
print()
ptr = 0
for i in range(2):
    data = border(data, 2, odd_even[ptr]) #key[0])
    data = step(data, key, odd_even[ptr])
    print_grid(data)
    print(f"default_char = {odd_even[ptr]}")
    print()
    ptr = (ptr + 1) % len(odd_even)
print(f"Lit pixel count: {sum(sum(1 for i, char in enumerate(row) if char == '#' and i >= 2 and i < len(row) - 1) for j, row in enumerate(data) if j >= 2 and j < len(data) - 1)}")
# 5606 is too high
# 7145 is too high
# 5186 is too high
# 5135 is too high
# 5140
# 5097 is right

ptr = 0
data = lines[2:]
for i in range(50):
    data = border(data, 2, odd_even[ptr]) #key[0])
    data = step(data, key, odd_even[ptr])
    #print_grid(data)
    #print(f"default_char = {odd_even[ptr]}")
    #print()
    ptr = (ptr + 1) % len(odd_even)
    print(f"{i + 1}_Lit pixel count: {sum(sum(1 for i, char in enumerate(row) if char == '#' and i >= 2 and i < len(row) - 1) for j, row in enumerate(data) if j >= 2 and j < len(data) - 1)}")
draw_image(data)
