import intcode_rewrite as ic

puzzle_case = []
with open('adventfiles/puzzle9.txt') as f:
    for val in f.read().split(','):
        puzzle_case.append(int(val))

def test_boost(program):
    t_console = ic.ICConsole([1])
    ic.quick_interp(program,t_console)
    return t_console.output_log[0]

print(f"Puzzle 9-1 Solution: {test_boost(puzzle_case)}")

def sensor_boost(program):
    t_console = ic.ICConsole([2])
    ic.quick_interp(program,t_console)
    return t_console.output_log[0]

print(f"Puzzle 9-1 Solution: {sensor_boost(puzzle_case)}")