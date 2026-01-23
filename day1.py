#advent of code 2019
#day 1
#part 1 - find total fuel costs!

def fuel(module):
    return module//3 - 2

puzzle_case = []
with open("adventfiles/puzzle1.txt") as f:
    for line in f.readlines():
        puzzle_case.append(int(line))

sumval = 0
for module in puzzle_case:
    sumval += fuel(module)

print(f"Puzzle 1-1 Solution: {sumval}")

#part 2 - count additional fuel

def recursive_fuel(module, val = 0):
    newfuel = module//3 - 2
    if newfuel <= 0:
        return val #no more fuel needed!
    return recursive_fuel(newfuel, val + newfuel) #add to tot and calc more

sumval2 = 0
for module in puzzle_case:
    sumval2 += recursive_fuel(module)

print(f"Puzzle 1-2 Solution: {sumval2}")