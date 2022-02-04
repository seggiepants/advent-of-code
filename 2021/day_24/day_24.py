import re

# Advent of Code 2021 - Day 24
# ----------------------------

match_inp = re.compile('(?P<cmd>inp) (?P<op1>w|x|y|z)')
match_op = re.compile('(?P<cmd>add|mul|div|mod|eql) (?P<op1>w|x|y|z) (?P<op2>w|x|y|z|-?\d+)')
match_number = re.compile('^-?\d+$')

class alu:
    def __init__(self, instructions):
        self.regs = {}
        self.reset(instructions)

    def reset(self, instructions):
        self.regs['w'] = 0
        self.regs['x'] = 0
        self.regs['y'] = 0
        self.regs['z'] = 0
        self.pc = 0
        
        self.instructions = instructions

        self.input_ptr = 0
        self.input = []

    def get_w(self):
        return self.regs['w']

    def get_x(self):
        return self.regs['x']

    def get_y(self):
        return self.regs['y']

    def get_z(self):
        return self.regs['z']

    def set_input(self, data):
        self.input_ptr = 0
        self.input = data

    def get_input(self):
        data = 0
        if self.input_ptr < len(self.input):
            data = self.input[self.input_ptr]
            self.input_ptr += 1
        #print(f"DATA: {data} ptr = {self.input_ptr} input = {self.input}")
        return data

    def step(self):
        global match_inp
        global match_number
        global match_op
        
        if self.pc >= len(self.instructions):
            return
        line = self.instructions[self.pc]
        self.pc += 1

        m = match_inp.match(line)
        cmd = ''
        op1 = 'w'
        op2 = 0
        if m:
            cmd = m['cmd']
            op1 = m['op1']
            op2 = 0
        else:
            m = match_op.match(line)
            if m:
                cmd = m['cmd']
                op1 = m['op1']
                op2 = m['op2']                
                n = match_number.match(op2)
                if n:
                    op2 = int(op2)
        if cmd != '':
            if cmd == 'inp':
                data = self.get_input()                
                self.regs[op1] = data
                #print(f"{cmd} {op1} <- {data}) ", end="")
            else:
                num1 = self.regs[op1]
                if type(op2) == int:
                    num2 = op2
                else:
                    num2 = self.regs[op2]

                #print(f"{cmd} {op1} ({num1}), {op2} ({num2}) ", end="")

                if cmd == 'add':
                    self.regs[op1] = num1 + num2
                elif cmd == 'mul':
                    self.regs[op1] = num1 * num2
                elif cmd == 'div':
                    self.regs[op1] = num1 // num2
                elif cmd == 'mod':
                    self.regs[op1] = num1 % num2
                elif cmd == 'eql':
                    if num1 == num2:
                        self.regs[op1] = 1
                    else:
                        self.regs[op1] = 0
            #print(f"\tregs w={self.regs['w']}, x={self.regs['x']}, y={self.regs['y']}, z={self.regs['z']}")
    def run(self):
        while self.pc < len(self.instructions):
            self.step()
                
                    

def load_data(filename):
    data_file = open(filename, 'rt')
    lines = data_file.readlines()
    data_file.close()
    lines = [line.strip() for line in lines]

    return lines

def print_instructions(instructions):
    for instruction in instructions:
        print(instruction)


# lines = load_data('sample_data.txt')
lines = load_data('data.txt')

# print_instructions(lines)
# debug test
"""
new_alu = alu(lines)
new_alu.reset(lines)
new_alu.set_input([3, 9])
new_alu.run()
if new_alu.get_z() == 1:
    print('success')
else:
    print('failure')

new_alu.reset(lines)
new_alu.set_input([3, 4])
new_alu.run()
if new_alu.get_z() == 0:
    print('success')
else:
    print('failure')
"""

new_alu = alu(lines)
fail_count = 0
#for i in range(99919699999928, 11111111111111, -1):
#for i in range(999196929597199, 11111111111111, -1):
"""
for i in range(99919692949999, 99111111111111, -1):
    if '0' not in str(i):
        new_alu.reset(lines)
        new_alu.set_input([int(digit) for digit in str(i)])
        new_alu.run()
        if new_alu.get_z() == 0:
            print(f"Part 1: {i}")
            #break;
        else:
            fail_count += 1
            if fail_count >= 10000:
                fail_count = 0
                print(".", end="")
            #print(f"Fail z = {new_alu.get_z()}")
        #break
#elif i % 100000 == 0:
#    print('.', end='')
"""
# answer was: 99919692496939
# stopped on 11914228487873
for i in range(11914228487873, 21111111111111, 1):
    if '0' not in str(i):
        new_alu.reset(lines)
        new_alu.set_input([int(digit) for digit in str(i)])
        new_alu.run()
        if new_alu.get_z() == 0:
            print(f"Part 1: {i}")
            break;
        else:
            fail_count += 1
            if fail_count >= 10000:
                fail_count = 0
                print(".", end="")
            #print(f"Fail z = {new_alu.get_z()}")
        #break

        
    

