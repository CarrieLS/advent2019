import intcode_rewrite as ic

#robot interfaces with intcode
    #when it asks for input, provide 0 if over a black panel, 1 for white panel
    #then it outputs two vals:
        #first val is color to paint the panel 0/1
        #second val is direction to turn, 0 is left and 1 is right
#the robot starts facing up and always moves forward 1 after turning

puzzle_code = []
with open('adventfiles/puzzle11.txt') as f:
    puzzle_code = [int(x) for x in f.read().split(',')]

def count_painted_locs():
    robot_loc = (0,0)
    dirs = [(0,1),(1,0),(0,-1),(-1,0)] #directions robot can move
    robot_dir_i = 0 #0 for up, +1 to turn right and -1 to turn left
    painted_locs = set() #tracks what locs have been painted ever
    white_locs = set() #tracks which locs are currently white
    console = ic.ICConsole([])
    interp = ic.ICInterpreter(console, puzzle_code)
    while interp.status != 2: #until program halts
        interp.start() #run until next stop
        if len(console.output_log) >= 2: #act on outputs
            turn_dir = console.output_log.pop()
            color = console.output_log.pop()
            painted_locs.add(robot_loc)
            if color == 1:
                white_locs.add(robot_loc)
            elif robot_loc in white_locs:
                white_locs.remove(robot_loc)
            if turn_dir == 1:
                robot_dir_i = (robot_dir_i + 1) % 4
            else:
                robot_dir_i = (robot_dir_i - 1) % 4
            #now move the bot
            robot_loc = (robot_loc[0] + dirs[robot_dir_i][0],
                         robot_loc[1] + dirs[robot_dir_i][1])
        if interp.status == 1: #needs input:
            if robot_loc in white_locs:
                console.input_stack.append(1)
            else:
                console.input_stack.append(0)
    return len(painted_locs)

print(f"Puzzle 11-1 Solution: {count_painted_locs()}")

def paint_ID():
    robot_loc = (0,0)
    dirs = [(0,1),(1,0),(0,-1),(-1,0)] #directions robot can move
    robot_dir_i = 0 #0 for up, +1 to turn right and -1 to turn left
    painted_locs = set() #tracks what locs have been painted ever
    white_locs = {(0,0)} #tracks which locs are currently white
    console = ic.ICConsole([])
    interp = ic.ICInterpreter(console, puzzle_code)
    while interp.status != 2: #until program halts
        interp.start() #run until next stop
        if len(console.output_log) >= 2: #act on outputs
            turn_dir = console.output_log.pop()
            color = console.output_log.pop()
            painted_locs.add(robot_loc)
            if color == 1:
                white_locs.add(robot_loc)
            elif robot_loc in white_locs:
                white_locs.remove(robot_loc)
            if turn_dir == 1:
                robot_dir_i = (robot_dir_i + 1) % 4
            else:
                robot_dir_i = (robot_dir_i - 1) % 4
            #now move the bot
            robot_loc = (robot_loc[0] + dirs[robot_dir_i][0],
                         robot_loc[1] + dirs[robot_dir_i][1])
        if interp.status == 1: #needs input:
            if robot_loc in white_locs:
                console.input_stack.append(1)
            else:
                console.input_stack.append(0)
    #now let's make a print out of white_locs
    xlambda = lambda a: a[0]
    ylambda = lambda a: a[1]
    x_bounds = (min(white_locs,key=xlambda)[0],max(white_locs,key=xlambda)[0])
    y_bounds = (min(white_locs,key=ylambda)[1],max(white_locs,key=ylambda)[1])
    outlines = []
    for y in reversed(range(y_bounds[0],y_bounds[1]+1)):
        outline_chars = []
        for x in range(x_bounds[0],x_bounds[1]+1):
            if (x,y) in white_locs:
                outline_chars.append("#")
            else:
                outline_chars.append(".")
        outlines.append("".join(outline_chars))
    print('\n'.join(outlines))

print("Puzzle 11-2 Solution:")
paint_ID()
    