#day 2
#intcode is in seperate file as it will come up again!
import intcode

#preprocess code, then run it thru intcode interpreter
def grav_program(code):
    code[1] = 12
    code[2] = 2
    intcode.interpret(code)
    return code[0]

puzzle_case = []
with open("adventfiles/puzzle2.txt") as f:
    for val in f.readline().split(','):
        puzzle_case.append(int(val))

print(f"Puzzle 2-1 solution: {grav_program(puzzle_case)}")