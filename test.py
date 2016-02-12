f = open("counter.txt","r")

sum = 0
for line in f:
    line = line[16:-1]
    sum += int(line)

print sum