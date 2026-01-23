#day 2
#intcode is in seperate file as it will come up again!
import intcode

#preprocess code, then run it thru intcode interpreter
def grav_program(code):
    code_copy = code.copy()#copy so we don't mess up puzzle case for 2-2
    code_copy[1] = 12
    code_copy[2] = 2
    intcode.interpret(code_copy)
    return code_copy[0]

puzzle_case = []
with open("adventfiles/puzzle2.txt") as f:
    for val in f.readline().split(','):
        puzzle_case.append(int(val))

print(f"Puzzle 2-1 solution: {grav_program(puzzle_case)}")

#part 2
#find what inputs produce 19690720
#lets search smaller pairs first
#can safely cap maxval below len(code), as higher lengths
#will try to read outside the code and throw an error
#this should be unnecessary if a solution exists
#but i'll put it in just in case

goalval = 19690720

#return whether we get goal value w/ provided (noun,verb)
def grav_program_goal(code, valpair):
    code_copy = code.copy() #so we don't change the original
    code_copy[1] = valpair[0]
    code_copy[2] = valpair[1]
    try:
        intcode.interpret(code_copy)
    except: #invalid intcode
        return False #solution not found
    return code_copy[0] == goalval

def try_pairs(code):
    maxval = 0
    while maxval < len(code):
        #search all pairs we haven't already checked w/ vals up to maxval
        #if we ignore ones we've already checked, the larger val will always
        #be maxval
        #smaller value can be anything from 0 to that
        #do both orders if the vals aren't equal
        for smaller_val in range(maxval+1):
            pair1 = (smaller_val,maxval)
            if grav_program_goal(code, pair1):
                return 100 * smaller_val + maxval
            elif smaller_val != maxval:
                pair2 = (maxval,smaller_val)
                if grav_program_goal(code, pair2):
                    return 100 * maxval + smaller_val
        #no solution found, try higher vals
        maxval += 1
    return -1 #no solution exists!

print(f"Puzzle 2-2 solution: {try_pairs(puzzle_case)}")