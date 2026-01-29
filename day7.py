import intcode

#run amp program
#input asks for phase setting from 0 to 4, then output from last amp
    #first amp should be given 0 as the output from last amp
#all phase settings will be used, but unknown order (5! = 120 possible)
#record final value, find phase order that gives highest value
#so just try every possible one, update max val as you go
    

#generate all permutations of sequence with all diff values
#for phases
def permutes(seq, placed = []):
    if len(seq) == 0:
        return [placed]
    all_orders = [] #2d list
    for i, val in enumerate(seq):
        all_orders.extend(permutes(seq[:i] + seq[i+1:], placed + [val]))
    return all_orders
        
def highest_signal(ampcode, phasers = [0,1,2,3,4], ampcount = 5):
    max_signal = -1
    term = intcode.Terminal() #add inputs as needed
    for order in permutes(phasers):
        nextval = 0
        for amp_i in range(ampcount):
            term.input_stack.append(nextval)
            term.input_stack.append(order[amp_i])
            intcode.interpret(ampcode.copy(),term)
            nextval = term.output.pop()
        max_signal = max(max_signal, nextval)
    return max_signal

test1 = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
test2 = [3,23,3,24,1002,24,10,24,1002,23,-1,23,
         101,5,23,23,1,24,23,23,4,23,99,0,0]
test3 = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,
         1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]

assert highest_signal(test1) == 43210
assert highest_signal(test2) == 54321
assert highest_signal(test3) == 65210

puzzle_case = []
with open('adventfiles/puzzle7.txt','r') as f:
    for val in f.read().split(','):
        puzzle_case.append(int(val))

print(f"Puzzle 7-1 Solution: {highest_signal(puzzle_case)}")

#ok now we need to run 5 copies of the ampcode simultaneously
#and directly feed output from 1 to the next
#A's first input is still 0, but its next input comes from E's output
#each one will need its own terminal and interpreter

def highest_feedback(ampcode, phasers = [5,6,7,8,9], ampcount = 5):
    max_signal = -1
    for order in permutes(phasers):
        amp_interps = []
        for i in range(ampcount):
            term = intcode.Terminal([order[i]]) #provide phase
            interp = intcode.Interpreter(ampcode.copy(),term)
            interp.resume() #run until it wants first input
            amp_interps.append(interp)
        curr_amp_i = 0 #start with A
        next_out = 0 #give it initial signal of 0
        while amp_interps[-1].status != 2: #until final amp halts
            curr_interp = amp_interps[curr_amp_i]
            curr_interp.terminal.input_stack.append(next_out) #pass input
            curr_interp.resume() #interpret till it runs out of input again
            next_out = curr_interp.terminal.output.pop() #update output
            curr_amp_i = (curr_amp_i + 1) % ampcount#go to next amp for now
        max_signal = max(max_signal,next_out)
    return max_signal

print(f"Puzzle 7-2 Solution: {highest_feedback(puzzle_case)}")