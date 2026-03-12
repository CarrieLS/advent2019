#arcade game running on intcode
#intcode will output what tiles to place on the screen
#output will go x,y,tile_id
#we just want to run the full code and see how many block tiles are on screen

#screen will be a dict of {(loc): tile_id}, where loc is (x,y)

#tile ids:
    #0: empty
    #1: wall - indescructible obstacle
    #2: block - destructible obstacle
    #3: horizontal paddle - inderstructible
    #4: ball - moves diagonally and bounces
    

import intcode_rewrite as ic

puzzle_code = []
with open("adventfiles/puzzle13.txt") as f:
    puzzle_code = [int(s) for s in f.read().split(',')]

def count_block_tiles(screen_code):
    console = ic.ICConsole([])
    interp = ic.ICInterpreter(console, screen_code.copy())
    screen = {}
    interp.start() #should just run all the way to the end
    #now we want to go thru outputs in chronological order, 3 at a time
    for i in range(len(console.output_log)//3):
        x = console.output_log[3*i]
        y = console.output_log[3*i+1]
        t = console.output_log[3*i+2]
        screen[(x,y)]=t
    #now just count block tiles
    block_count = 0
    for value in screen.values():
        if value == 2:
            block_count += 1
    return block_count, screen

print(f"Puzzle 13-1 Solution: {count_block_tiles(puzzle_code)[0]}")

screen_dims = (37,22) #dimensions of screen - goes from 0 to 1-these positions
#we'll use a 2D list for screen info this time since we know the dims
#screen[y][x] is each pixel

#takes screen info as {(x,y): t_id} and prints it in terminal with these reps:
    # . - empty
    # # - wall
    # H - block
    # = - paddle
    # o - ball
def print_screen(screen_info):
    outlines = []
    char_map = ['.','#','H','=','o']
    for y in range(screen_dims[1]):
        outchars = []
        for x in range(screen_dims[0]):
            outchars.append(char_map[screen_info[y][x]])
        outlines.append("".join(outchars))
    print("\n".join(outlines))
            
    

#IC Console that gives output as a log, but input via terminal
#output automatically updates screen/score every 3 outputs
class ArcadeConsole(ic.ICConsole):
    def __init__(self,screen_info):
        super().__init__(None)
        self.screen_info = screen_info
        self.score = None
    
    def output(self, val):
        self.output_log.append(val)
        if len(self.output_log) == 3: #update screen
            if self.output_log[0] == -1: #update score instead
                self.score = self.output_log[2]
            else:
                self.screen_info[self.output_log[1]][self.output_log[0]] =\
                    self.output_log[2]
            self.output_log.clear()
    
    def next_input(self):
        print_screen(self.screen_info)
        return int(input("Joystick Input:"))

#console that plays the arcade game using ai below
#tracks the block count using initial count and subtracting 1 whenever a block
#disappears
#for faster calcs, tracks ball position and only ever checks immediate vicinity
#for changes
class AIConsole(ic.ICConsole):
    def __init__(self,screen_info):
        super().__init__(None)
        self.screen_info = screen_info
        self.ball_pos = None
        self.paddle_x = None
        self.block_count = 0
        self.score = 0
        
    #move towards ball
    #if all blocks have been destroyed, stop providing input
    def next_input(self):
        if self.paddle_x < self.ball_pos[0]:
            self.paddle_x += 1
            return 1
        elif self.paddle_x > self.ball_pos[0]:
            self.paddle_x -= 1
            return -1
        else:
            return 0
    
    #update info every 3 outputs
    def output(self,val):
        self.output_log.append(val)
        if len(self.output_log) == 3: #info set recieved
            if self.output_log[0] == -1: #update score
                self.score = val
            else: #change tile
                x = self.output_log[0]
                y = self.output_log[1]
                if val == 4:#is the ball moving? x -> 4
                    self.ball_pos = [x,y]
                elif val == 3: #is the paddle moving?
                    self.paddle_x = x
                elif val == 2: #was a block created?
                    self.block_count += 1
                if self.screen_info[y][x] == 2: #was a block destroyed? 2 -> x
                    self.block_count -= 1
                self.screen_info[y][x] = val
            self.output_log.clear() #dump output after processing
                

#let's play the game in the terminal
#print out the screen every time we need an input
#input with a val to set joystick to that:
    #0=neutral
    #1=right
    #-1=left

#alternatively we could make very simple AI to do it - just follow the ball
#always move in the direction of the ball, should be easy to just track pos
#if we don't want to deal with physics, we can just check the 4 possible locs
#of the ball each frame
    
def play_game_manual(screen_code):
    code = screen_code.copy()
    code[0] = 2 #add quarters
    screen = []
    for y in range(screen_dims[1]):
        screen_line = []
        for x in range(screen_dims[0]):
            screen_line.append(0)
        screen.append(screen_line)
    console = ArcadeConsole(screen)
    interp = ic.ICInterpreter(console, code)
    interp.start()
    return console.score

def play_game_ai(screen_code):
    code = screen_code.copy()
    code[0] = 2 #add quarters
    screen = []
    for y in range(screen_dims[1]):
        screen_line = []
        for x in range(screen_dims[0]):
            screen_line.append(0)
        screen.append(screen_line)
    console = AIConsole(screen)
    interp = ic.ICInterpreter(console, code)
    interp.start()
    return console.score

print(f"Puzzle 13-2 Solution: {play_game_ai(puzzle_code)}")
