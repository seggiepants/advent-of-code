import re

# Advent of Code 2021 - Day 19
# ----------------------------

matchHeader = re.compile('-+ scanner (?P<num>\d+).-+')
matchPoint = re.compile('(?P<x>-?\d+),(?P<y>-?\d+),(?P<z>-?\d+)')

matricies = [
    [[1, 0, 0],
     [0, 1, 0],
     [0, 0, 1]],
    [[0, 0, 1],
     [0, 1, 0],
     [-1, 0, 0]],
    [[-1, 0, 0],
     [0, 1, 0],
     [0, 0, -1]],
    [[0, 0, -1],
     [0, 1, 0],
     [1, 0, 0]],

    [[0, -1, 0],
     [1, 0, 0],
     [0, 0, 1]],
    [[0, 0, 1],
     [1, 0, 0],
     [0, 1, 0]],
    [[0, 1, 0],
     [1, 0, 0],
     [0, 0, -1]],
    [[0, 0, -1],
     [1, 0, 0],
     [0, -1, 0]],

    [[0, 1, 0],
     [-1, 0, 0],
     [0, 0, 1]],
    [[0, 0, 1],
     [-1, 0, 0],
     [0, -1, 0]],
    [[0, -1, 0],
     [-1, 0, 0],
     [0, 0, -1]],
    [[0, 0, -1],
     [-1, 0, 0],
     [0, 1, 0]],

    [[1, 0, 0],
     [0, 0, -1],
     [0, 1, 0]],
    [[0, 1, 0],
     [0, 0, -1],
     [-1, 0, 0]],
    [[-1, 0, 0],
     [0, 0, -1],
     [0, -1, 0]],
    [[0, -1, 0],
     [0, 0, -1],
     [1, 0, 0]],
    
    [[1, 0, 0],
     [0, -1, 0],
     [0, 0, -1]],
    [[0, 0, -1],
     [0, -1, 0],
     [-1, 0, 0]],
    [[-1, 0, 0],
     [0, -1, 0],
     [0, 0, 1]],
    [[0, 0, 1],
     [0, -1, 0],
     [1, 0, 0]],
    
    [[1, 0, 0],
     [0, 0, 1],
     [0, -1, 0]],
    [[0, -1, 0],
     [0, 0, 1],
     [-1, 0, 0]],
    [[-1, 0, 0],
     [0, 0, 1],
     [0, 1, 0]],
    [[0, 1, 0],
     [0, 0, 1],
     [1, 0, 0]]
    ]

def matmul(mat, point):
    # point to 1x3 matrix
    Y = [[n] for n in point]
    result = [[0], [0], [0]]
    for i in range(len(mat)):
       # iterating columns of Y matrix
       for j in range(len(Y[0])):
           # iterating rows of Y matrix
           for k in range(len(Y)):
               result[i][j] += mat[i][k] * Y[k][j]
    return (result[0][0], result[1][0], result[2][0])


def load_data(filename):
    data_file = open(filename, 'rt')
    lines = data_file.readlines()
    data_file.close()
    lines = [line.strip() for line in lines]

    return lines
"""
def rotate_point(x, y, z, rot):
    if rot == 0:
        return (x, y, z)
    elif rot == 1:
        return (-y, x, z)
    elif rot == 2:
        return (-x, -y, z)
    elif rot == 3:
        return (y, -x, z)
    
    elif rot == 4:
        return (x, y, z)    
    elif rot == 5:
        return (x, -z, y)
    elif rot == 6:
        return (x, -y, -z)
    elif rot == 7:
        return (x, z, -y)
    
    elif rot == 8:
        return (x, y, z)
    elif rot == 9:
        return (-z, y, x)
    elif rot == 10:
        return (-x, y, -z)
    elif rot == 11:
        return (z, y, -x)
    
    elif rot == 12:
        return (x, y, -z)
    elif rot == 13:
        return (-y, x, -z)
    elif rot == 14:
        return (-x, -y, -z)
    elif rot == 15:
        return (y, -x, -z)
    
    elif rot == 16:
        return (-x, y, z)
    elif rot == 17:
        return (-x, -z, y)
    elif rot == 18:
        return (-x, -y, -z)
    elif rot == 19:
        return (-x, z, -y)
    
    elif rot == 20:
        return (x, -y, z)
    elif rot == 21:
        return (-z, -y, x)
    elif rot == 22:
        return (-x, -y, -z)
    elif rot == 23:
        return (z, -y, -x)
"""
def rotate_point(x, y, z, rot):
    return matmul(matricies[rot], (x, y, z))

# lines = load_data('sample_data.txt')
lines = load_data('data.txt')

# convert lines into a dictonary of scanners and beacon positions.
scanners = {}
scanner_pos = {}
scanner_key = ''

for line in lines:
    m = matchHeader.match(line)
    if m:
        scanner_key = int(m['num'])
    else:
        m = matchPoint.match(line)
        if m:
            x = int(m['x'])
            y = int(m['y'])
            z = int(m['z'])
            point = (x, y, z)
            if scanner_key != '':
                if scanner_key in scanners:
                    scanners[scanner_key].append(point)
                else:
                    scanners[scanner_key] = [point]



beacons = set()
# first scanner is canonical
for x, y, z in scanners[0]:
    beacons.add((x, y, z))
skip = []

#print(f"result: {matmul([[1, 0, 0],[0, 0, 1],[0, -1, 0]], (1, 2, 3))}")

while len(skip) < len(scanners.keys()):
    for i, key in enumerate(scanners.keys()):
        if key in skip:
            continue
        #if i == 0:
        #    continue
        print(f"{i}: Check Scanner: {key}")
        for a in beacons:
            for b in scanners[key]:
                found = False
                for rot in range(24):
                    c = rotate_point(b[0], b[1], b[2], rot)
                    dx = a[0] - c[0]
                    dy = a[1] - c[1]
                    dz = a[2] - c[2]
                    count_matches = 0
                    for x, y, z in scanners[key]:
                        c = rotate_point(x, y, z, rot)
                        if (c[0] + dx, c[1] + dy, c[2] + dz) in beacons:
                            count_matches += 1
                    #matches = []
                    if count_matches >= 12:
                        print(f"Offset ({dx},{dy},{dz}) has {count_matches} matches for rotation: {rot}")
                        found = True
                        scanner_pos[key] = (dx, dy, dz)
                        for x, y, z in scanners[key]:
                            c = rotate_point(x, y, z, rot)
                            #matches.append((c[0] + dx, c[1] + dy, c[2] + dz))
                            beacons.add((c[0] + dx, c[1] + dy, c[2] + dz))
                        skip.append(key)
                        #print(matches)
                        break
                #print(f"Beacons: {len(beacons)}")
                if found:
                    break
            if found:
                break

print(f"Part 1: Beacons Count: {len(beacons)}")
#for i, beacon in enumerate(beacons):
#    print(f"{i + 1}: {beacon}")
max_dist = 0
for p1 in scanner_pos.keys():
    for p2 in scanner_pos.keys():
        if p1 != p2:
            dist = abs(scanner_pos[p2][0] - scanner_pos[p1][0]) + abs(scanner_pos[p2][1] - scanner_pos[p1][1]) + abs(scanner_pos[p2][2] - scanner_pos[p1][2])
            max_dist = max(dist, max_dist)

print(f"Part 2: Maximum Manhatten Distance: {max_dist}")


                    
                
