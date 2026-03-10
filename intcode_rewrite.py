class ICConsole:
    def __init__(self,input_stack):
        self.input_stack = input_stack
        self.output_log = []
    
    def next_input(self):
        if len(self.input_stack) == 0:
            return None
        return self.input_stack.pop()
    
    def output(self,val):
        self.output_log.append(val)

class PyConsole(ICConsole):
    def __init__(self):
        super().__init__(None)
    
    def next_input(self):
        return int(input("Next Input:"))
    
    def output(self,val):
        print(val)

class ICInterpreter:
    def __init__(self,console,program):
        self.console = console
        self.pointer = 0 #where we currently are in the code
        self.status = 1 #1 for paused, 0 for running
        #code uses a dict now for flexible memory usage
        self.program = dict(enumerate(program))
        self.rel_base = 0
    
    #run operators in a loop until halted
    #you should call start instead to start this, as run doesn't update status
    def _run(self):
        while self.status == 0:
            opcode = self.program[self.pointer]
            nextOp = ICOperator(self, opcode)
            pointOffset = nextOp.execute()
            self.pointer += pointOffset
    
    #run a single step, printing info about it
    def debug_step(self):
        self.status = 0
        if self.pointer < 0 or self.pointer > len(self.program):
            raise ValueError(f"Pointer has reached \
                             invalid index: {self.pointer}")
        opcode = self.program[self.pointer]
        print(f"Pointer: {self.pointer}")
        print(f"Opcode: {opcode}")
        print(f"Relative base: {self.rel_base}")
        nextOp = ICOperator(self, opcode)
        pointOffset = nextOp.execute()
        self.pointer += pointOffset
        if self.status == 1:
            print("HALTED")
        
    
    def start(self):
        self.status = 0
        self._run()
    
    def getNextParams(self,param_modes):
        params = []
        p_offset = 1
        for i,mode in enumerate(param_modes):
            val = self.program[self.pointer+p_offset]
            params.append(ICParameter(self, mode, val))
            p_offset += 1
        return params
        
    
    def getValAt(self,index):
        if index >= 0:
            return self.program.get(index,0)
        else:
            raise ValueError(f"Attempted to read value \
                             at invalid index: {index}")
    
    def setValAt(self,index,val):
        if index >= 0:
            self.program[index] = val
        else:
            raise ValueError(f"Attempted to set value \
                             at invalid index: {index}")
            

class ICOperator:
    def add(interpreter,params):
        addVal = params[0].readParam() + params[1].readParam()
        interpreter.setValAt(params[2].readAsTarget(),addVal)
        return 4
    
    def multiply(interpreter,params):
        multVal = params[0].readParam()*params[1].readParam()
        interpreter.setValAt(params[2].readAsTarget(),multVal)
        return 4
    
    def input_set(interpreter,params):
        val = interpreter.console.next_input()
        if val == None:
            interpreter.status = 1
            return 0
        else:
            interpreter.setValAt(params[0].readAsTarget(),val)
            return 2
        
    def jump_if_true(interpreter,params):
        if params[0].readParam() != 0:
            interpreter.pointer = params[1].readParam()
            return 0
        return 3
    
    def jump_if_false(interpreter,params):
        if params[0].readParam() == 0:
            interpreter.pointer = params[1].readParam()
            return 0
        return 3
      
    def less_than(interpreter,params):
        store_val = 0
        if params[0].readParam() < params[1].readParam():
            store_val = 1
        interpreter.setValAt(params[2].readAsTarget(),store_val)
        return 4
      
    def equals(interpreter,params):
        store_val = 0
        if params[0].readParam() == params[1].readParam():
            store_val = 1
        interpreter.setValAt(params[2].readAsTarget(),store_val)
        return 4
            
    
    def output_val(interpreter,params):
        val = params[0].readParam()
        interpreter.console.output(val)
        return 2
    
    def adjust_relative(interpreter,params):
        val = params[0].readParam()
        interpreter.rel_base += val
        return 2
    
    def halt(interpreter,params):
        interpreter.status = 1
        return 0
        
        
    opfuncs = {1:add,2:multiply,3:input_set,4:output_val,5:jump_if_true,
               6:jump_if_false,7:less_than,8:equals,9:adjust_relative,
               99:halt}
    param_counts = {1:3,2:3,3:1,4:1,5:2,6:2,7:3,8:3,9:1,99:0}
    
    def __init__(self,interpreter,raw_opcode):
        self.interp = interpreter
        corr_opcode = raw_opcode % 100
        self.opfunc = ICOperator.opfuncs[corr_opcode]
        param_count = ICOperator.param_counts[corr_opcode]
        param_modes = [] #will be in order we read params in (left to right)
        for i in range(param_count):
            param_modes.append(raw_opcode//(10**(i+2)) % 10)
        self.params = self.interp.getNextParams(param_modes)
    
    #runs operator, returns how much to advance pointer by
    def execute(self):
        return self.opfunc(self.interp,self.params)
        

class ICParameter:
    def __init__(self,interpreter,mode,val):
        self.mode = mode #0 for position, 1 for immediate, 2 for relative
        self.val = val
        self.interp = interpreter
    
    #for reading a parameter the normal way (sometimes operators override this)
    def readParam(self):
        if self.mode == 0:
            return self.interp.getValAt(self.val)
        elif self.mode == 1:
            return self.val
        elif self.mode == 2:
            return self.interp.getValAt(self.val+self.interp.rel_base)
        else:
            raise ValueError("Invalid mode!")
    
    #for reading a param as a target index
    def readAsTarget(self):
        if self.mode == 0:
            return self.val
        elif self.mode == 2:
            return self.val + self.interp.rel_base
        else:
            raise ValueError("Invalid mode!")

p_console = PyConsole()

def quick_interp(program,console=p_console):
    interp = ICInterpreter(console, program)
    interp.start()