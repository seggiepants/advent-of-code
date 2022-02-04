# Advent of Code 2021 - Day 15
# ----------------------------

def load_data(filename):
    data_file = open(filename, 'rt')
    lines = data_file.readlines()
    data_file.close()
    lines = [line.strip() for line in lines]

    return lines

def read_bits(count):
    global bits
    global index
    if (index + count) >= len(bits):
        print("Error: Bit overflow")
        exit()
    # print(f"Binary: {bits[index: index + count]} Decimal: {int(bits[index: index + count], 2)}")
    data = int(bits[index: index + count], 2)
    index += count

    return data
    

def read_packet():
    global bits
    global index
    global version_sum
    
    version = read_bits(3)
    # print(f"version: {version}")
    version_sum += version
    packet_type = read_bits(3)

    value = 0
    if packet_type == 0:
        # sum
        value = read_sum()
    elif packet_type == 1:
        # product
        value = read_product()
    elif packet_type == 2:
        # min
        value = read_min()
    elif packet_type == 3:
        # max
        value = read_max()
    elif packet_type == 4:
        # literal
        value = read_literal()
    elif packet_type == 5:
        # greater than
        value = read_greaterthan()
    elif packet_type == 6:
        # less than
        value = read_lessthan()        
    elif packet_type == 7:
        # equal to
        value = read_equalto()
    else:
        # invalid operator
        print(f"Error: Invalid Operator or type {packet_type}")
        exit()

    return value

def read_literal():
    global bits
    global index

    value = 0
    flag = 1
    while flag != 0:
        flag = read_bits(1)
        nibble = read_bits(4)
        value = (value * 16) + nibble
            
    # print(f"Literal Value: {value}")  
    return value

def read_sum():
    global bits
    global index

    return sum(read_operator())

def read_product():
    global bits
    global index

    operands = read_operator()
    value = 1
    for num in operands:
        value *= num

    return value

def read_min():
    global bits
    global index

    return min(read_operator())

def read_max():
    global bits
    global index

    return max(read_operator())

def read_lessthan():
    global bits
    global index

    operands = read_operator()
    if operands[0] < operands[1]:
        return 1
    else:
        return 0

def read_greaterthan():
    global bits
    global index

    operands = read_operator()
    if operands[0] > operands[1]:
        return 1
    else:
        return 0

def read_equalto():
    global bits
    global index

    operands = read_operator()
    if operands[0] == operands[1]:
        return 1
    else:
        return 0
    
def read_operator():
    global bits
    global index

    op_type = read_bits(1)
    operands = []
    if op_type == 0:
        length_bits = read_bits(15)
        anchor = index
        while index < anchor + length_bits:
            operands.append(read_packet())
        
    else: # op_type == 1
        count_packets = read_bits(11)
        for i in range(count_packets):
            operands.append(read_packet())
    return operands

lines = load_data('data.txt')
# lines = load_data('sample_data.txt')

hex_lookup = {'0': '0000', '1': '0001', '2': '0010', '3': '0011',
              '4': '0100', '5': '0101', '6': '0110', '7': '0111',
              '8': '1000', '9': '1001', 'A': '1010', 'B': '1011',
              'C': '1100', 'D': '1101', 'E': '1110', 'F': '1111' }
data = lines[0]
bits = "".join(hex_lookup[char] for char in data)
index = 0
version_sum = 0
#print(bits)
value = read_packet()
print(f"Part 1: {version_sum}")
print(f"Part 2: {value}")
