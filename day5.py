#day 5
#input 1, then recieve diagnostic output
import intcode

puzzle_case = []
with open("adventfiles/puzzle5.txt",'r') as f:
    for val in f.readline().split(','):
        puzzle_case.append(int(val))

#run this program, give an input of 1
#should get a bunch of test outputs (0 if code works correctly)
#then a final code

#terminal that inputs 1
diagnostic_term = intcode.Terminal([1])
intcode.interpret(puzzle_case.copy(),diagnostic_term)
final_code = diagnostic_term.output.pop()
#check if all others are zero
for test_val in diagnostic_term.output:
    assert test_val == 0

print(f'Puzzle 5-1 Solution: {final_code}')

#part 2
#input 5, output should only be one number
term2 = intcode.Terminal([5])
intcode.interpret(puzzle_case.copy(),term2)
final_code = term2.output.pop()
#output should now be empty
assert (not term2.output)

print(f'Puzzle 5-2 Solution: {final_code}')