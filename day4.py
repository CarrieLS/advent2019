#day 4
#part 1
#find code in range satisfying:
    #6 digit #
    #two adjacent digits are the same
    #going L->R, digits never decrease (>=)

#check these conditions
#takes number as str!
def is_number_valid_code(number : str):
    if len(number) != 6:
        return False
    adjacent = False
    for i, char in enumerate(number[:-1]):
        char_next = number[i+1]
        if int(char_next) < int(char):
            return False
        adjacent |= (char_next == char) #update adjacency check
    return adjacent

def count_codes(code_range):
    count = 0
    for val in code_range:
        if is_number_valid_code(str(val)):
            count += 1
    return count

code_range = range(165432,707913)

print(f"Puzzle 4-1 Solution: {count_codes(code_range)}")

#part 2
    #same as before, but you specifically need a pair of digits
    #without another adjacent equal digit


def is_number_valid_updated(number : str):
    if len(number) != 6:
        return False
    pair_found = False
    for i, char in enumerate(number[:-1]):
        char_next = number[i+1]
        if int(char_next) < int(char):
            return False
        if char_next == char: #possible pair, check if either surrounding match
            longer = False
            if i > 0: #check behind
                longer |= (number[i-1] == char) #see if same char behind
            if i < len(number) - 2: #check ahead
                longer |= (number[i+2] == char)
            pair_found |= (not longer) #if not longer, pair has been found
    return pair_found

def count_codes_updated(code_range):
    count = 0
    for val in code_range:
        if is_number_valid_updated(str(val)):
            count += 1
    return count

print(f"Puzzle 4-2 Solution: {count_codes_updated(code_range)}")