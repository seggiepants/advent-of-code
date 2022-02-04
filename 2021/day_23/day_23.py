import sys
import math
from queue import PriorityQueue

'#############'
'#...........#'
'###B#C#B#D###'
'  #A#D#C#A#  '
'  #########  '

STEP = 1

def get_key(amphipod):
    return amphipod.key()

def gen_key(x, y, char):
    return str(y) + chr(x + ord('A')) + char

def amphipods_to_state(amphipods):
    state = ""
    amphipods.sort(key=get_key)
    for amphipod in amphipods:
        state += amphipod.key()

    return state

def state_to_amphipods(state):
    amphipods = []
    for i in range(0, len(state), 3):
        amphipods.append(amphipod(state[i:i+3]))
    return amphipods

def state_to_moves(state):
    amphipods = state_to_amphipods(state)
    moves = []
    for amphipod in amphipods:
        moves += amphipod.get_moves(amphipods)

    return moves

def edge_key(state_1, state_2):
    if state_1 < state_2:
        return state_1 + '-' + state_2
    else:
        return state_2 + '-' + state_1

class edge:
    def __init__(self, state_1, state_2, cost):
        self.state_1 = state_1
        self.state_2 = state_2
        self.cost = cost

    def key(self):
        return edge_key(self.state_1, self.state_2)

    def contains_state(self, state):
        return state == self.state_1 or state == self.state_2

class amphipod:
    def __init__(self, key):
        global STEP
        self.y = int(key[0])
        self.x = ord(key[1]) - ord('A')
        self.char = key[2]
        if self.char == 'A':
            self.cost = 1
            self.target_col = 3
        elif self.char == 'B':
            self.cost = 10
            self.target_col = 5
        elif self.char == 'C':
            self.cost = 100
            self.target_col = 7
        else: # self.char == 'D'
            self.cost = 1000
            self.target_col = 9        
        self.target_row_min = 2
        
        # Part 1
        if STEP == 1:
            self.target_row_max = 3
        else:        
            # Part 2
            self.target_row_max = 5
            
        self.hall_min_col = 1
        self.hall_max_col = 11
        self.hall_row = 1
        self.skip_cols = [3, 5, 7, 9]

    def __str__(self):
        return f"char={self.char}, x={self.x}, y={self.y}"

    def key(self):
        return gen_key(self.x, self.y, self.char)

    def is_home(self, amphipods):
        if self.x == self.target_col:
            if self.y == self.target_row_min:
                below = self.below(amphipods)
                if below != None and below.char == self.char:
                    return True
            if self.y == self.target_row_max:
                    return True
        return False

    def above(self, amphipods):
        l = [pod for pod in amphipods if pod.x == self.x and pod.y == self.y - 1]
        if len(l) == 0:
            return None
        else:
            return l[0]

    def left(self, amphipods):
        l = [pod for pod in amphipods if pod.x == self.x - 1 and pod.y == self.y]
        if len(l) == 0:
            return None
        else:
            return l[0]

    def right(self, amphipods):
        l = [pod for pod in amphipods if pod.x == self.x + 1 and pod.y == self.y]
        if len(l) == 0:
            return None
        else:
            return l[0]

    def below(self, amphipods):
        l = [pod for pod in amphipods if pod.x == self.x and pod.y == self.y + 1]
        if len(l) == 0:
            return None
        else:
            return l[0]

    def home(self, amphipods):
        l = [pod for pod in amphipods if pod.x == self.target_col and pod.y >= self.target_row_min and pod.y <= self.target_row_max and pod != self]
        if len(l) == 0:
            return None
        else:
            return l

    def get_next_state(self, amphipods, new_x, new_y):
        pods = []
        for pod in amphipods:
            if pod == self:
                pods.append(amphipod(gen_key(new_x, new_y, self.char)))
            else:
                pods.append(pod)
        return amphipods_to_state(pods)
                        

    def get_moves(self, amphipods):
        moves = []
        # possible moves
        # down to bottom

        # am I in my target column
        if self.x == self.target_col:
            #if self.y == self.target_row_max:
            #    # stop if at target max
            #    return []
            
            if self.y >= self.target_row_min and self.y <= self.target_row_max:
                # stop it at target min or greater and same char in every spot below you is correct
                l = [pod for pod in amphipods if pod.x == self.x and pod.y > self.y and pod.y <= self.target_row_max and pod.char == self.char]
                is_packed = (len(l) == self.target_row_max - self.y)
                if is_packed:
                    return []
                
            # Move down if nothing below and not at bottom
            if self.y >= self.target_row_min and self.y < self.target_row_max:
                l = [pod for pod in amphipods if pod.x == self.x and pod.y > self.y and pod.y <= self.target_row_max]
                if len(l) == 0:
                    moves.append({'state': self.get_next_state(amphipods, self.x, self.y + 1), 'cost': self.cost, 'pos': (self.x, self.y + 1), 'note': 'sink'})

        # am I to the left or right of the target column with nothing in the
        # first two spots of the target column and either an empty or same char
        # ampipod at the bottom
        # if so, move down.
        if self.y == self.hall_row and (self.x == self.target_col - 1 or self.x == self.target_col + 1):
            hall_square = [pod for pod in amphipods if pod.x == self.target_col and pod.y == self.hall_row]            
            home_top_square = [pod for pod in amphipods if pod.x == self.target_col and pod.y == self.target_row_min]
            home_bottom_squares = [pod for pod in amphipods if pod.x == self.target_col and pod.y > self.target_row_min and pod.y <= self.target_row_max and pod.char != self.char]            

            if hall_square == [] and home_top_square == [] and len(home_bottom_squares) == 0:
                moves.append({'state': self.get_next_state(amphipods, self.target_col, self.target_row_min), 'cost': self.cost * 2, 'pos': (self.target_col, self.target_row_min), 'note': 'pop_down'})

        # up from the bottom.
        if self.y > self.target_row_min and self.y <= self.target_row_max and self.above(amphipods) == None:
            moves.append({'state': self.get_next_state(amphipods, self.x, self.y - 1), 'cost': self.cost, 'pos': (self.x, self.y - 1), 'note': 'up'})
        
        # Pop left or right.
        if self.x in self.skip_cols and self.y == self.target_row_min:
            above = self.above(amphipods)
            if above == None:                
                left = [pod for pod in amphipods if pod.x == self.x - 1 and pod.y == self.hall_row]
                right = [pod for pod in amphipods if pod.x == self.x + 1 and pod.y == self.hall_row]
                move_cost = self.cost * 2
                if left == []:
                    moves.append({'state': self.get_next_state(amphipods, self.x - 1, self.hall_row), 'cost': move_cost, 'pos': (self.x - 1, self.hall_row), 'note': 'pop_left'})
                if right == []:
                    moves.append({'state': self.get_next_state(amphipods, self.x + 1, self.hall_row), 'cost': move_cost, 'pos': (self.x + 1, self.hall_row), 'note': 'pop_right'})

        # Move left
        if self.x > self.hall_min_col and self.y == self.hall_row:
            move_cost = self.cost
            may_move = self.left(amphipods) == None # may move if empty
            target_x = self.x - 1
            if target_x in self.skip_cols:
                next_pod = [pod for pod in amphipods if pod.x == self.x - 2 and pod.y == self.y]
                may_move = may_move and next_pod == []
                move_cost *= 2
                target_x = self.x - 2

            if may_move:
                moves.append({'state': self.get_next_state(amphipods, target_x, self.y), 'cost': move_cost, 'pos': (target_x, self.y), 'note': 'left'})
                
        # Move right
        if self.x < self.hall_max_col and self.y == self.hall_row:
            move_cost = self.cost
            may_move = self.right(amphipods) == None # may move if empty
            target_x = self.x + 1
            if self.x + 1 in self.skip_cols:
                next_pod = [pod for pod in amphipods if pod.x == self.x + 2 and pod.y == self.y]
                may_move = may_move and next_pod == []
                move_cost *= 2
                target_x = self.x + 2

            if may_move:
                moves.append({'state': self.get_next_state(amphipods, target_x, self.y), 'cost': move_cost, 'pos': (target_x, self.y), 'note': 'right'})
            
        return moves

def search(state, target_state):
    queue = PriorityQueue()
    queue.put((0, (state, None)))
    visited = {}
    while not queue.empty():
        current_cost, (current_state, current_previous) = queue.get()        
        if current_state in visited:
            continue
        #print(current_state)
        
        visited[current_state] = {'cost': current_cost, 'state': current_state, 'previous': current_previous}        

        if current_state == target_state:
            print('found it')
            break

        moves = state_to_moves(current_state)
        #moves = [move for move in moves if move['state'] not in visited]
        for move in moves:
            move_cost = current_cost + move['cost']
            move_state = move['state']
            if move_state in visited:
                if move_cost < visited[move_state]['cost']:
                    visited[move_state]['cost'] = move_cost
                    visited[move_state]['previous'] = current_state
            else:
                queue.put((move_cost, (move_state, current_state)))

    if target_state in visited:
        return visited[target_state]['cost']
    else:
        return f"Not found!\nvisited: {len(visited)}"

def load_data(filename):
    data_file = open(filename, 'rt')
    lines = data_file.readlines()
    data_file.close()
    lines = [line.strip() for line in lines]

    return lines

PART = 2
if PART == 1:
    # Part 1
    amphipods = []
    amphipods.append(amphipod(gen_key(3, 2, 'A')))
    amphipods.append(amphipod(gen_key(3, 3, 'A')))
    amphipods.append(amphipod(gen_key(5, 2, 'B')))
    amphipods.append(amphipod(gen_key(5, 3, 'B')))
    amphipods.append(amphipod(gen_key(7, 2, 'C')))
    amphipods.append(amphipod(gen_key(7, 3, 'C')))
    amphipods.append(amphipod(gen_key(9, 2, 'D')))
    amphipods.append(amphipod(gen_key(9, 3, 'D')))

    target_state = amphipods_to_state(amphipods)
else:
    # Part 2
    amphipods = []
    amphipods.append(amphipod(gen_key(3, 2, 'A')))
    amphipods.append(amphipod(gen_key(3, 3, 'A')))
    amphipods.append(amphipod(gen_key(3, 4, 'A')))
    amphipods.append(amphipod(gen_key(3, 5, 'A')))
    amphipods.append(amphipod(gen_key(5, 2, 'B')))
    amphipods.append(amphipod(gen_key(5, 3, 'B')))
    amphipods.append(amphipod(gen_key(5, 4, 'B')))
    amphipods.append(amphipod(gen_key(5, 5, 'B')))
    amphipods.append(amphipod(gen_key(7, 2, 'C')))
    amphipods.append(amphipod(gen_key(7, 3, 'C')))
    amphipods.append(amphipod(gen_key(7, 4, 'C')))
    amphipods.append(amphipod(gen_key(7, 5, 'C')))
    amphipods.append(amphipod(gen_key(9, 2, 'D')))
    amphipods.append(amphipod(gen_key(9, 3, 'D')))
    amphipods.append(amphipod(gen_key(9, 4, 'D')))
    amphipods.append(amphipod(gen_key(9, 5, 'D')))
    for pod in amphipods:
        print(pod)
    print()
    
    target_state = amphipods_to_state(amphipods)
    print(target_state)

amphipods = []
if PART == 1:
    #lines = load_data('sample_data.txt')
    lines = load_data('data.txt')
else:
    #lines = load_data('sample_data_2.txt')
    lines = load_data('data_2.txt')

for j, row in enumerate(lines):
    for i, char in enumerate(row):
        if char >= 'A' and char <= 'D':
            amphipods.append(amphipod(gen_key(i, j, char)))

for line in lines:
    print(line)
print()
for pod in amphipods:
    print(pod)


state = amphipods_to_state(amphipods)
#moves = state_to_moves(state)
#for move in moves:
#    print(move)
print(search(state, target_state))


