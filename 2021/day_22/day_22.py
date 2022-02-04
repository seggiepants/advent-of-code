import re

def load_data(filename):
    data_file = open(filename, 'rt')
    lines = data_file.readlines()
    data_file.close()
    lines = [line.strip() for line in lines]

    return lines

class cube:
    def __init__(self, x1, x2, y1, y2, z1, z2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.z1 = z1
        self.z2 = z2

    def area(self):
        return (self.x2 - self.x1 + 1) * (self.y2 - self.y1 + 1) * (self.z2 - self.z1 + 1)

    def overlap(self, other):
        
        if other.x2 < self.x1:            
            return False
        elif other.x1 > self.x2:
            return False
        elif other.y2 < self.y1:
            return False
        elif other.y1 > self.y2:
            return False
        elif other.z2 < self.z1:
            return False
        elif other.z1 > self.z2:
            return False
        return True
        """
        x = [self.x1, self.x2, other.x1, other.x2]
        x.sort()
        y = [self.y1, self.y2, other.y1, other.y2]
        y.sort()
        z = [self.z1, self.z2, other.z1, other.z2]
        z.sort()
        dx_separate = (self.x2 - self.x1) + (other.x2 - other.x1) + 2
        dy_separate = (self.y2 - self.y1) + (other.y2 - other.y1) + 2
        dz_separate = (self.z2 - self.z1) + (other.z2 - other.z1) + 2
        dx_group = x[3] - x[0] + 1
        dy_group = y[3] - y[0] + 1
        dz_group = z[3] - z[0] + 1
        return (dx_separate + dy_separate + dz_separate) > (dx_group + dy_group + dz_group)
        """

    def equals(self, other):
        return self.x1 ==  other.x1 and self.x2 ==  other.x2 and self.y1 ==  other.y1 and self.y2 ==  other.y2 and self.z1 ==  other.z1 and self.z2 ==  other.z2

    def contains(self, other):
        return self.x1<= other.x1 and self.x2 >= other.x2 and self.y1<= other.y1 and self.y2 >= other.y2 and self.z1<= other.z1 and self.z2 >= other.z2

    def is_contained(self, other):
        return other.contains(self)
    
    def __str__(self):
        return f"{self.x1}..{self.x2}, {self.y1}..{self.y2}, {self.z1}..{self.z2}"

    def split_cube(self, other, cubes):
        # No merge if cubes don't overlap
        if not self.overlap(other):
            return False

        x = [self.x1, self.x2, other.x1, other.x2]
        y = [self.y1, self.y2, other.y1, other.y2]
        z = [self.z1, self.z2, other.z1, other.z2]
        x.sort()
        y.sort()
        z.sort()

        #if x[1] == x[2] or y[1] == y[2] or z[1] == z[2]:
            # No intersection area
        #    return False
        cx1 = cx2 = x[0]
        cy1 = cy2 = y[0]
        cz1 = cz2 = z[0]
        range_x = [(x[0], x[1] - 1), (x[1], x[2]), (x[2] + 1, x[3])]
        range_y = [(y[0], y[1] - 1), (y[1], y[2]), (y[2] + 1, y[3])]
        range_z = [(z[0], z[1] - 1), (z[1], z[2]), (z[2] + 1, z[3])]
        for cz1, cz2 in range_z:
            for cy1, cy2 in range_y:
                for cx1, cx2 in range_x:
                    # all dimensions are non-zero
                    #if cx1 != cx2 and cy1 != cy2 and cz1 != cz2:                        
                    new_cube = cube(cx1, cx2, cy1, cy2, cz1, cz2)
                    #print(new_cube)
                    # must overlap with self, but not overlap other to be saved.
                    if not other.overlap(new_cube) and self.overlap(new_cube):
                        #print(f"Append: {new_cube} self: {self} - {self.overlap(new_cube)} other: {other} - {other.overlap(new_cube)}")
                        cubes.append(new_cube)
                    #else:
                        #print(f"Skip: {new_cube} self: {self} - {self.overlap(new_cube)} other: {other} - {other.overlap(new_cube)}")
        return True
    
"""
    def split_cube(self, x, y, z):
        ret = [None for i in range(8)]
        # 0. top left front,    1. top right front
        # 2. bottom left front, 3. bottom right front
        # 4. top left back,     5. top right back
        # 6. bottom left back,  7. bottom right back
        if self.x1 < x and self.y1 < y and self.z1 < z:
            # 0. top left front
            ret[0] = cube(self.x1, min(self.x2, x), self.y1, min(self.y2, y), self.z1, min(self.z2, z))
        if self.x2 >= x and self.y1 < y and self.z1 < z:
            # 1. top right front
            ret[1] = cube(max(self.x1, x), self.x2, self.y1, min(self.y2, y), self.z1, min(self.z2, z))
        if self.x1 < x and self.y2 >= y and self.z1 < z:
            # 2. bottom left front
            ret[2] = cube(self.x1, min(x, self.x2), max(self.y1, y1), self.y2, self.z1, min(self.z2, z))
        if self.x2 >= x and self.y2 >= y and self.z1 < z:
            # 3. bottom right front
            ret[3] = cube(max(self.x1, x), self.x2, max(self.y1, y1), self.y2, self.z1, min(self.z2, z))


        if self.x1 < x and self.y1 < y and self.z2 >= z:
            # 4. top left back
            ret[4] = cube(self.x1, min(self.x2, x), self.y1, min(self.y2, y), max(self.z1, z), self.z2)
        if self.x2 >= x and self.y1 < y and self.z2 >= z:
            # 5. top right back
            ret[5] = cube(max(self.x1, x), self.x2, self.y1, min(self.y2, y), max(self.z1, z), self.z2)
        if self.x1 < x and self.y2 >= y and self.z2 >= z:
            # 6. bottom left back
            ret[6] = cube(self.x1, min(x, self.x2), max(self.y1, y1), self.y2, max(self.z1, z), self.z2)
        if self.x2 >= x and self.y2 >= y and self.z2 >= z:
            # 7. bottom right back
            ret[7] = cube(max(self.x1, x), self.x2, max(self.y1, y1), self.y2, max(self.z1, z), self.z2)

        return ret
"""
"""
class node:
    def __init__(self, x1, x2, y1, y2, z1, z2):
        self.children = []
        self.cubes = []
        self.area = cube(x1, x2, y1, y2, z1, z2)
        self.center_x = self.area.x1 + ((self.area.x2 - self.area.x1) // 2)
        self.center_y = self.area.y1 + ((self.area.y2 - self.area.y1) // 2)
        self.center_z = self.area.z1 + ((self.area.z2 - self.area.z1) // 2)

    def __str__(self):
        return f"node: cubes: {len(self.cubes)}, children: {len(self.children)} area: {self.area}"

    def add_cube(self, new_cube):
        has_overlap = False
        has_duplicate = False
        may_split = self.area.x1 != self.center_x and self.area.y1 != self.center_y and self.area.z1 != self.center_z and self.area.x2 != self.center_x and self.area.y2 != self.center_y and self.area.z2 != self.center_z
        for cube in self.cubes:
            if cube.equals(new_cube):
                has_duplicate = True
                break
            elif cube.overlap(new_cube):
                print(f"overlap of {cube} with {new_cube}")
                has_overlap = True
                break
        
        if has_overlap and may_split:
            if len(self.children) == 0:
                self.children.append(node(self.area.x1, self.center_x, self.area.y1, self.center_y, self.area.z1, self.center_z))
                self.children.append(node(self.center_x, self.area.x2, self.area.y1, self.center_y, self.area.z1, self.center_z))
                self.children.append(node(self.area.x1, self.center_x, self.center_y, self.area.y2, self.area.z1, self.center_z))
                self.children.append(node(self.center_x, self.area.x2, self.center_y, self.area.y2, self.area.z1, self.center_z))
                self.children.append(node(self.area.x1, self.center_x, self.area.y1, self.center_y, self.center_z, self.area.z2))
                self.children.append(node(self.center_x, self.area.x2, self.area.y1, self.center_y, self.center_z, self.area.z2))
                self.children.append(node(self.area.x1, self.center_x, self.center_y, self.area.y2, self.center_z, self.area.z2))
                self.children.append(node(self.center_x, self.area.x2, self.center_y, self.area.y2, self.center_z, self.area.z2))
                
            # Send all current cubes into child areas splitting as needed
            for current in self.cubes:
                ret = current.split_cube(self.center_x, self.center_y, self.center_z)
                for i in range(len(ret)):
                    if ret[i] != None:
                        self.children[i].add_cube(ret[i])
            self.cubes = [] # then remove child list
            ret = new_cube.split_cube(self.center_x, self.center_y, self.center_z)
            print(ret)
            for i in range(len(ret)):
                if ret[i] != None:
                    print(f"cube: {ret[i]} to {self.children[i].area} with {len(self.cubes)} children")
                    self.children[i].add_cube(ret[i])

        elif not has_duplicate:
            if len(self.children) == 0:
                # not yet split
                self.cubes.append(new_cube)
            else:
                # was split, so split and add to child nodes
                ret = ret = new_cube.split_cube(self.center_x, self.center_y, self.center_z)
                for i in range(len(ret)):
                    if ret[i] != None:
                        self.children[i].add_cube(ret[i])
"""            
                

    
matchLine = re.compile('(?P<state>on|off) x=(?P<x1>-?\d+)\.\.(?P<x2>-?\d+),y=(?P<y1>-?\d+)\.\.(?P<y2>-?\d+),z=(?P<z1>-?\d+)\.\.(?P<z2>-?\d+)')
"""
lines = [
    'on x=10..12,y=10..12,z=10..12'
    , 'on x=11..13,y=11..13,z=11..13'
    , 'off x=9..11,y=9..11,z=9..11'
    , 'on x=10..10,y=10..10,z=10..10'
]
"""
lines = load_data('data.txt')
"""
lines = [
    #'on x=10..12,y=10..12,z=10..12',
    #'on x=11..13,y=11..13,z=11..13',
    #'off x=9..11,y=9..11,z=9..11',
    #'on x=10..10,y=10..10,z=10..10'
    'on x=-20..26,y=-36..17,z=-47..7',
    'on x=-20..33,y=-21..23,z=-26..28',
    'on x=-22..28,y=-29..23,z=-38..16',
    'on x=-46..7,y=-6..46,z=-50..-1',
    'on x=-49..1,y=-3..46,z=-24..28',
    'on x=2..47,y=-22..22,z=-23..27',
    'on x=-27..23,y=-28..26,z=-21..29',
    'on x=-39..5,y=-6..47,z=-3..44',
    'on x=-30..21,y=-8..43,z=-13..34',
    'on x=-22..26,y=-27..20,z=-29..19',
    'off x=-48..-32,y=26..41,z=-47..-37',
    'on x=-12..35,y=6..50,z=-50..-2',
    'off x=-48..-32,y=-32..-16,z=-15..-5',
    'on x=-18..26,y=-33..15,z=-7..46',
    'off x=-40..-22,y=-38..-28,z=23..41',
    'on x=-16..35,y=-41..10,z=-47..6',
    'off x=-32..-23,y=11..30,z=-14..3',
    'on x=-49..-5,y=-3..45,z=-29..18',
    'off x=18..30,y=-20..-8,z=-3..13',
    'on x=-41..9,y=-7..43,z=-33..15',
    #'on x=-54112..-39298,y=-85059..-49293,z=-27449..7877',
    #'on x=967..23432,y=45373..81175,z=27513..53682'
    ]
"""
data = []
for line in lines:
    m = matchLine.match(line)
    if m:
        x1 = int(m['x1'])
        x2 = int(m['x2'])
        y1 = int(m['y1'])
        y2 = int(m['y2'])
        z1 = int(m['z1'])
        z2 = int(m['z2'])
        state = m['state'] == 'on'
        data.append({'x1': x1, 'y1': y1, 'z1': z1, 'x2': x2, 'y2': y2, 'z2': z2, 'state': state})

"""
min_x1 = min(area['x1'] for area in data)
max_x2 = max(area['x2'] for area in data)
min_y1 = min(area['y1'] for area in data)
max_y2 = max(area['y2'] for area in data)
min_z1 = min(area['z1'] for area in data)
max_z2 = max(area['z2'] for area in data)

#print(f"{min_x1}..{max_x2}, {min_y1}..{max_y2}, {min_z1}..{max_z2}")
root = node(min_x1, max_x2, min_y1, max_y2, min_z1, max_z2)
"""
cubes = []

for n, region in enumerate(data):
    new_cube = cube(region['x1'], region['x2'], region['y1'], region['y2'], region['z1'], region['z2'])

    i = 0
    while i < len(cubes):
        if cubes[i].split_cube(new_cube, cubes):
            cubes.pop(i)
        else:
            i += 1        
#        for item in cubes:
#            print(item)


    if region['state']:
        # add if merge instead of intersect.
        cubes.append(new_cube)
    #print(f"{n + 1}. cubes: {len(cubes)} area: {sum(cube.area() for cube in cubes if cube.x1 >= -50 and cube.x2 <= 50 and cube.y1 >= -50 and cube.y2 <= 50 and cube.z1 >= -50 and cube.z2 <= 50)}")
    #for m, item in enumerate(cubes):
    #    print(f"{m + 1}: {item}")


print(sum(cube.area() for cube in cubes if cube.x1 >= -50 and cube.x2 <= 50 and cube.y1 >= -50 and cube.y2 <= 50 and cube.z1 >= -50 and cube.z2 <= 50))
print(sum(cube.area() for cube in cubes))

#for cube in cubes:
#    print(cube)
    

# too low
# 447826337735319
