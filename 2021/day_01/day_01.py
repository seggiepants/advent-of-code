f = open("data.txt","r")
lines = f.readlines()
lines = [int(row) for row in lines]

def sum_window(index, sample_count, data):
    count = 0
    stuff = ""
    for n in range(index - sample_count + 1, index + 1):
        stuff = stuff + ", " + str(data[n])
        count += data[n]
    return count
    

# Part 1
count = 0
for i in range(len(lines)):
    if (i > 0):
        if (lines[i] > lines[i - 1]):
            count += 1
print(count)

# Part 2
count = 0
count_previous = 0
sample_count = 3
total = 0
for i in range(sample_count - 1, len(lines)):
    count = sum_window(i, sample_count, lines)
    if (i >= sample_count):
        if (count > count_previous):
            total += 1
    count_previous = count

print(total)

