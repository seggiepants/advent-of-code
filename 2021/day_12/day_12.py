# Advent of Code 2021 - Day 12
# ----------------------------

def load_data(filename):
    data_file = open(filename, 'rt')
    lines = data_file.readlines()
    data_file.close()
    lines = [line.strip() for line in lines]

    return lines

def populate_caves(segments):
    caves = {}

    for segment in segments:
        names = segment.split('-')
        for name in names:
            destinations = names.copy()
            destinations.remove(name)
            if name in caves:
                caves[name] += destinations
            else:
                caves[name] = destinations
    return caves

def find_paths(caves, current_path, end_node, visited):
    current = current_path[-1] # last place is the current.
    any_children = False
    path_count = 0
    for destination in caves[current]:
        if destination.isupper() or destination not in visited:
            any_children = True
            if destination == end_node:
                # print(current_path + [destination])
                path_count += 1
            else:
                path_count += find_paths(caves, current_path + [destination], end_node, visited + [destination])
    return path_count
                
def find_paths2(caves, current_path, end_node, visited, exclusions):
    current = current_path[-1] # last place is the current.
    any_children = False
    path_count = 0

    revisit = []
    may_revisit = True
    for node in current_path:
        if node.islower():
            if node in revisit:
                may_revisit = False
                break
            else:
                revisit.append(node)
               
    for destination in caves[current]:
        if destination.isupper() or destination not in visited or (may_revisit and destination not in exclusions):
            any_children = True
            if destination == end_node:
                # print(current_path + [destination])
                path_count += 1
            else:
                path_count += find_paths2(caves, current_path + [destination], end_node, visited + [destination], exclusions)
    return path_count            

lines = load_data('data.txt')
# lines = load_data('sample_data.txt')

# Part 1
# ======
caves = populate_caves(lines)
path_count = find_paths(caves, ['start'], 'end', ['start'])
print(f'Number of paths found: {path_count}')

# Part 2
# ======
path_count = find_paths2(caves, ['start'], 'end', ['start'], ['start', 'end'])
print(f'Number of paths found: {path_count}')
