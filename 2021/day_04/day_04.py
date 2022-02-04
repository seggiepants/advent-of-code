import re
import functools

data_file = open('data.txt', 'rt')
lines = data_file.readlines()
data_file.close()
lines = [line.strip() for line in lines]
sample_data = [line.strip() for line in ["7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1"
, ""
, "22 13 17 11  0"
, " 8  2 23  4 24"
, "21  9 14 16  7"
, " 6 10  3 18  5"
, " 1 12 20 15 19"
, ""
, " 3 15  0  2 22"
, " 9 18 13 17  5"
, "19  8  7 25 23"
, "20 11 10 24  4"
, "14 21 16 12  6"
, ""
, "14 21 17 24  4"
, "10 16 15  9 19"
, "18  8 23 26 20"
, "22 11 13  6  5"
, " 2  0 12  3  7"]]

# Uncomment to use sample_data
# lines = sample_data

def process_data(lines):
    calls = [int(call.strip()) for call in lines[0].split(',')]
    blank = False
    board = []
    boards = []
    digit = re.compile('(\d+)')
    for i, line in enumerate(lines):
        if i == 0:
            continue
        line = line.strip()
        blank = len(line) == 0
        # Add a completed board, ready for next board
        if blank and len(board) > 0:
            boards.append(board)
            board = []

        if not blank:
            row = [int(cell) for cell in digit.findall(line)]
            board.append(row)
    # Add last completed board
    if len(board) > 0:
        boards.append(board)
            
        
    return calls, boards

def is_bingo(board, calls):
    for row in board:
        matches = 0
        for cell in row:
            if cell in calls:
                matches += 1
        if matches == len(row):
            return True

    for col in range(len(board[0])):
        matches = 0
        for row in range(len(board)):
            if board[row][col] in calls:
                matches += 1
        if matches == len(board[0]):
            return True
    return False

def score_board(board, calls):
    unmarked = 0
    for row in board:
        for cell in row:
            if not cell in calls:
                unmarked += cell
    return unmarked * calls[-1]

# Setup
# -----
calls, boards = process_data(lines)

# Part 1
# ------
index = -1
calls_current = []
match_found = False
match_index = -1

while not match_found and index < len(calls):
    index += 1
    calls_current.append(calls[index])
    for i, board in enumerate(boards):
        if is_bingo(board, calls_current):
            match_found = True
            match_index = i
            break

if match_found:
    # print(f"Match on board {match_index}\ncalls: {calls_current}\nboard:\n{boards[match_index]}")
    print(score_board(boards[match_index], calls_current))
else:
    print("No match")

# Part 2
# ------
index = -1
calls_current = []
is_done = False
match_index = -1
has_won = [False for board in boards]

while not is_done and index < len(calls):
    index += 1
    calls_current.append(calls[index])
    for i, board in enumerate(boards):
        if not has_won[i]:
            if is_bingo(board, calls_current):
                has_won[i] = True
                is_done = functools.reduce(lambda a, b: a and b, has_won)
                if is_done:
                    match_index = i
                    break

if is_done:
    # print(f"Match on board {match_index}\ncalls: {calls_current}\nboard:\n{boards[match_index]}")
    print(score_board(boards[match_index], calls_current))
else:
    print("No match")
