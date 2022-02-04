import re
import functools

# Advent of Code 2021 - Day 21
# ----------------------------

NUM_SPACES = 10
POINTS_MAX = 1000
POINTS_MAX_DIRAC = 21
ROLL_COUNT = 3
playerMatch = re.compile('Player (?P<num>\d+) starting position: (?P<position>\d+)')
counter = 0
p1_wins = {}
p2_wins = {}

def load_data(filename):
    data_file = open(filename, 'rt')
    lines = data_file.readlines()
    data_file.close()
    lines = [line.strip() for line in lines]

    return lines

def roll_deterministic():
    global counter
    counter = (counter % 100) + 1
    return counter

def play_game(game, roll, max_points):
    global NUM_SPACES
    global ROLL_COUNT
    is_won = False
    player_keys = list(game['players'].keys())
    player_keys.sort()
    while not is_won:
        game['round'] += 1
        for key in player_keys:
            player = game['players'][key]
            spaces = sum(roll() for i in range(ROLL_COUNT))
            player['position'] = ((player['position'] - 1 + spaces) % NUM_SPACES) + 1
            player['points'] += player['position']
            game['rolls'] += ROLL_COUNT
            is_won = sum(1 for key in game['players'] if game['players'][key]['points'] >= max_points) > 0
            if is_won:
                break
    return game

def play_game2(game, max_points):
    player_1 = game['players'][1]
    player_2 = game['players'][2]
    print(max_points)
    return play_game2_helper(player_1['position'], player_1['points'], player_2['position'], player_2['points'], 1, max_points)

def path_multiplier(path):
    ret = 1
    for char in path:
        if char in '48':
            ret *= 3
        elif char in '57':
            ret *= 6
        elif char == '6':
            ret *= 7
        # 3, 9 = *= 1
    return ret

@functools.lru_cache(maxsize=None)
def play_game2_helper(p1_pos, p1_points, p2_pos, p2_points, turn, max_points):
    global NUM_SPACES    
    global ROLL_COUNT
    
    p1_wins = 0
    p2_wins = 0

    for i in range(3, 10):
        w1 = w2 = 0
        if i == 3 or i == 9:
            multiplier = 1
        elif i == 4 or i == 8:
            multiplier = 3
        elif i == 5 or i == 7:
            multiplier = 6
        else: # i == 6
            multiplier = 7
            
        if turn == 1:
            pos = ((p1_pos - 1 + i) % NUM_SPACES) + 1
            points = p1_points + pos
            if points >= max_points:
                #print("p1 add")
                p1_wins += multiplier
            else:
                w1, w2 = play_game2_helper(pos, points, p2_pos, p2_points, 2, max_points)
        else:
            pos = ((p2_pos - 1 + i) % NUM_SPACES) + 1
            points = p2_points + pos
            if points >= max_points:
                #print("p2 add")
                p2_wins += multiplier
            else:
                w1, w2 = play_game2_helper(p1_pos, p1_points, pos, points, 1, max_points)

        p1_wins += w1 * multiplier
        p2_wins += w2 * multiplier

    return (p1_wins, p2_wins)

# lines = load_data('sample_data.txt')
lines = load_data('data.txt')

players = {}
for line in lines:
    m = playerMatch.match(line)
    if m:
        players[int(m['num'])] = {'position': int(m['position']), 'points': 0}
        
game = { 'round': 0, 'rolls': 0, 'players': players}
play_game(game, roll_deterministic, POINTS_MAX)
losers = [game['players'][key] for key in game['players'] if game['players'][key]['points'] < POINTS_MAX]
print(f"Part 1: Score = {losers[0]['points'] * game['rolls']}")

players = {}
for line in lines:
    m = playerMatch.match(line)
    if m:
        players[int(m['num'])] = {'position': int(m['position']), 'points': 0}
        
game = { 'round': 0, 'rolls': 0, 'players': players}
p1_wins = {}
p2_wins = {}
p1, p2 = play_game2(game, POINTS_MAX_DIRAC)
#p1 = sum(p1_wins[key] * path_multiplier(key) for key in p1_wins.keys())
#p2 = sum(p2_wins[key] * path_multiplier(key) for key in p2_wins.keys())
print(f"Part 2: Most Wins = {max(p1, p2)}")
