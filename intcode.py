#intcode - originally from day2
#code ref:
    #1 (a) (b) (c): write val(a) + val(b) -> c
    #2 (a) (b) (c): write val(a) * val(b) -> c
    #3 (a): ask input, write -> a
    #4 (a): output a
    #99: halt!
    #after each command, move forward 4 positions!

#val_ops = {1,2,99}

#parameter counts for each operator
#key = operator, val = param count

#problem 5 needs support for i/o
#so adding a terminal
#if no terminal exists, i/o will be handled via python's input/print
#for automatic i/o, here's a terminal class:
class Terminal:
    def __init__(self,input_list):
        self.input_stack = input_list.copy()
        self.input_stack.reverse() #so we can pop inputs off
        self.output = []
    
    def next_input(self):
        return self.input_stack.pop()
    
    def write_output(self,out):
        self.output.append(out)

class PythonTerminal(Terminal):
    def __init__(self):
        pass #override, but doesn't actually need to do anything
    
    def next_input(self): #override
        return int(input("Next input:"))
    
    def write_output(self,out): #override
        print(out)

default_terminal = PythonTerminal()

class Interpreter:
    #map operators onto functions to call
    #functions move the pointer when done
    #just need to be passed interpreter and param_flags
    #operator_map = {}
    
    def __init__(self, code, terminal = default_terminal):
        self.code = code
        self.pointer = 0 #tracks where you are
        self.operator_map = {1: self._add,
                             2: self._mult,
                             3: self._input,
                             4: self._output,
                             5: self._jump_if_true,
                             6: self._jump_if_false,
                             7: self._less_than,
                             8: self._equals}
        self.terminal = terminal
    
    #perform next operator, recurse until op = 99
    def step(self):
        cur_val = self.code[self.pointer]
        op = cur_val % 100
        #check if halt
        if op == 99:
            return
        pflags = cur_val//100
        #do operator
        self.operator_map[op](pflags)
        #next step
        self.step()
    
    #1
    def _add(self,param_flags):
        add_val = 0
        for i in range(2): #add two vals
            target_i = self.pointer + 1 + i
            param_flag = (param_flags // (10**i)) % 10
            if param_flag == 0: #positional
                add_val += self.code[self.code[target_i]]
            elif param_flag == 1: #immediate
                add_val += self.code[target_i]
        #now set val and update pointer
        self.code[self.code[self.pointer+3]] = add_val
        self.pointer += 4
    
    #2
    def _mult(self,param_flags):
        mult_val = 1
        for i in range(2): #add two vals
            target_i = self.pointer + 1 + i
            param_flag = (param_flags // (10**i)) % 10
            if param_flag == 0: #positional
                mult_val *= self.code[self.code[target_i]]
            elif param_flag == 1: #immediate
                mult_val *= self.code[target_i]
        #now set val and update pointer
        self.code[self.code[self.pointer+3]] = mult_val
        self.pointer += 4
    
    #3
    def _input(self,param_flags):
        target_i = self.code[self.pointer+1]
        self.code[target_i] = self.terminal.next_input()
        self.pointer += 2
    
    #4
    def _output(self,param_flags):
        val = None
        if (param_flags % 10) == 1: #immediate
            val = self.code[self.pointer+1]
        else: #position
            val = self.code[self.code[self.pointer+1]]
        self.terminal.write_output(val)
        self.pointer += 2
    
    #5
    def _jump_if_true(self,param_flags):
        #check param flag for jump condition
        jumpcon = False
        if (param_flags % 10) == 1: #immediate
            jumpcon = (self.code[self.pointer+1] != 0)
        else: #position
            jumpcon = (self.code[self.code[self.pointer+1]] != 0)
        if jumpcon: #jump pointer
            #check flag
            if ((param_flags // 10) % 10) == 1: #immediate
                self.pointer = (self.code[self.pointer+2])
            else: #position
                self.pointer = (self.code[self.code[self.pointer+2]])
        else: #go to next operator
            self.pointer += 3
    
    #6
    def _jump_if_false(self,param_flags):
        #check param flag for jump condition
        jumpcon = False
        if (param_flags % 10) == 1: #immediate
            jumpcon = (self.code[self.pointer+1] == 0)
        else: #position
            jumpcon = (self.code[self.code[self.pointer+1]] == 0)
        if jumpcon: #jump pointer
            #check flag
            if ((param_flags // 10) % 10) == 1: #immediate
                self.pointer = (self.code[self.pointer+2])
            else: #position
                self.pointer = (self.code[self.code[self.pointer+2]])
        else: #go to next operator
            self.pointer += 3
    
    #7
    def _less_than(self,param_flags):
        val1 = None
        if (param_flags % 10) == 1: #immediate
            val1 = self.code[self.pointer+1]
        else:
            val1 = self.code[self.code[self.pointer+1]]
        val2 = None
        if ((param_flags // 10) % 10) == 1: #immediate
            val2 = self.code[self.pointer+2]
        else:
            val2 = self.code[self.code[self.pointer+2]]
        #mode is ignored for last parameter as its a write instruction
        target = self.code[self.pointer+3]
        writeval = int(val1 < val2)
        self.code[target] = writeval
        self.pointer += 4
    
    #8
    def _equals(self,param_flags):
        val1 = None
        if (param_flags % 10) == 1: #immediate
            val1 = self.code[self.pointer+1]
        else:
            val1 = self.code[self.code[self.pointer+1]]
        val2 = None
        if ((param_flags // 10) % 10) == 1: #immediate
            val2 = self.code[self.pointer+2]
        else:
            val2 = self.code[self.code[self.pointer+2]]
        #mode is ignored for last parameter as its a write instruction
        target = self.code[self.pointer+3]
        writeval = int(val1 == val2)
        self.code[target] = writeval
        self.pointer += 4

#quickly make and use an interpreter w/ given terminal
def interpret(code, terminal = default_terminal):
    interpreter = Interpreter(code, terminal)
    interpreter.step()