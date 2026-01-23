#intcode - originally from day2
#code ref:
    #1 (a) (b) (c): write val(a) + val(b) -> c
    #2 (a) (b) (c): write val(a) * val(b) -> c
    #99: halt!
    #after each command, move forward 4 positions!

#val_ops = {1,2,99}
next3_ops = {1,2}

#take code as list of ints
#modifies code in place, so returns nothing
#raises errors if code can't be interpreted correctly
def interpret(code):
    curpos = 0
    curval = code[curpos]
    while curval != 99:
        #perform operation based on curval
        #group operators which read next 3 vals
        if curval in next3_ops:
            pos_a = code[curpos+1]
            pos_b = code[curpos+2]
            pos_c = code[curpos+3]
            if curval == 1:
                code[pos_c] = code[pos_a] + code[pos_b] #ADD
            elif curval == 2:
                code[pos_c] = code[pos_a]*code[pos_b] #MULT
        else: #invalid operator!
            raise ValueError(f"intcode: invalid op! {curval} at pos {curpos}")
        #move to next step - jump 4 positions ahead
        curpos += 4
        curval = code[curpos]