#day 3 - wires
#find closest crossing
#lets say wires start at 0,0
#for each crossing, keep track of manhattan distance and if its lower
#update distance

#how do we know if wires cross?
#each wire is made up of lines
#lets assume no lines on the same place for no (just individual crossings)
#to see if two lines (defined w/ origin, dir, length) cross, we can check:
    #are they perpendicular?  if no, they don't
        #AKA, if they have same or opposite dirs (R,L) (U,D)
    #if they are perpindicular, is the origin of 1 inside the varying coord
    #range of the other, if no they don't
        #AKA, if line A has origin (x,y) and line B goes R/L, is x inside B.x
        #can check via range [B.origin.x, B.origin.x + B.length)
    #does A's other coord cross B's other coord
        #AKA, A.origin.y is on the opposite side of B.origin.y as
        #A.origin.y + A.length

#lets do OOP for this
class WireLine:
    _LR = {'L','R'}
    
    def __init__(self,direction,origin,length):
        self.direction = direction
        self.origin = origin
        self.length = length
        self.coord_range = self._get_coord_range() #save time
    
    #return mincoord,maxcoord
    def _get_coord_range(self):
        if self.direction == 'L':
            return (self.origin[0] - self.length, self.origin[0])
        elif self.direction == 'R':
            return (self.origin[0],self.origin[0]+self.length)
        elif self.direction == 'D':
            return (self.origin[1] - self.length, self.origin[1])
        elif self.direction == 'U':
            return (self.origin[1],self.origin[1]+self.length)
    
    def get_end_pos(self):
        if self.direction == 'L':
            return (self.origin[0]-self.length, self.origin[1])
        elif self.direction == 'R':
            return (self.origin[0]+self.length, self.origin[1])
        elif self.direction == 'D':
            return (self.origin[0], self.origin[1]-self.length)
        elif self.direction == 'U':
            return (self.origin[0], self.origin[1]+self.length)
    
    #return None if no crossing
    def find_crossing(self,line):
        if self.direction in WireLine._LR:
            if line.direction in WireLine._LR:
                return None
            #they are perpindicular, this one's x coord varies
            #check if y is in line's range
            line_range = line.coord_range
            if self.origin[1] >= line_range[0] and\
                self.origin[1] <= line_range[1]:
                    #check lines other coord is in your range
                    if line.origin[0] >= self.coord_range[0] and\
                        line.origin[0] <= self.coord_range[1]:
                            #intersection exists
                            return (line.origin[0],self.origin[1])
        else:
            if line.direction not in WireLine._LR:
                return None
            #same checks as before but reversed
            line_range = line.coord_range
            if self.origin[0] >= line_range[0] and\
                self.origin[0] <= line_range[1]:
                    #check lines other coord is in your range
                    if line.origin[1] >= self.coord_range[0] and\
                        line.origin[1] <= self.coord_range[1]:
                            #intersection exists
                            return (self.origin[0],line.origin[1])
        return None

    #generate list of lines from wire, always starts at 0,0
    def lines_from_wire_str(wire):
        currpos = [0,0]
        lines = []
        for lstr in wire:
            line = WireLine(lstr[0],tuple(currpos),int(lstr[1:]))
            currpos = line.get_end_pos()
            lines.append(line)
        return lines
    
    #for part two
    #check if a point is inside, and if so return dist to it
    def dist_to_point(self, point):
        if self.direction in WireLine._LR: #y axis constant
            if point[1] == self.origin[1]: #same y
                dist = point[0] - self.origin[0] #delta x
                if self.direction == 'L':
                    dist = -dist #fix direction
                if dist >= 0 and dist <= self.length:
                    return dist
        else:
            if point[0] == self.origin[0]: #same x
                dist = point[1] - self.origin[1] #delta y
                if self.direction == 'D':
                    dist = -dist #fix direction
                if dist >= 0 and dist <= self.length:
                    return dist
        return None #point not on line
            
    
    #also part two
    #takes list of wires, traces them until it hits given point
    #returns total dist
    def trace_to_point(wire_list, point):
        cumulative_dist = 0
        for line in wire_list:
            dist = line.dist_to_point(point)
            if dist: #found!
                cumulative_dist += dist
                return cumulative_dist
            else:
                cumulative_dist += line.length #add wire length, try next
        return None #point not found!
        

#ok now for the problem
#go through each line on one wire, check it for collisions with each line
#on other wire
#if collision is found, calculate manhattan dist
#and track smallest manhattan dist

#2D list - first index is wire, second is line
puzzle_case = []
with open("adventfiles/puzzle3.txt",'r') as f:
    for line in f.readlines():
        puzzle_case.append(line.split(','))

def get_closest_crossing(two_wires):
    lines1 = WireLine.lines_from_wire_str(puzzle_case[0])
    lines2 = WireLine.lines_from_wire_str(puzzle_case[1])
    mindist = None
    for line1 in lines1:
        for line2 in lines2:
            collpoint = line1.find_crossing(line2)
            if collpoint:
                colldist = abs(collpoint[0]) + abs(collpoint[1])
                if (not mindist) or (colldist < mindist):
                    mindist = colldist
    return mindist

print(f'Puzzle 3-1 Solution: {get_closest_crossing(puzzle_case)}')

#part 2
#lets do this by getting list of collisions first, then tracing the dist
#to them on each wire

def get_shortest_path(two_wires):
    lines1 = WireLine.lines_from_wire_str(puzzle_case[0])
    lines2 = WireLine.lines_from_wire_str(puzzle_case[1])
    minsteps = None
    #populate collisions
    for line1 in lines1:
        for line2 in lines2:
            collpoint = line1.find_crossing(line2)
            if collpoint:
                #trace and add steps
                steps1 = WireLine.trace_to_point(lines1,collpoint)
                steps2 = WireLine.trace_to_point(lines2,collpoint)
                if (not steps1) or (not steps2): #shouldn't happen
                    print(steps1)
                    print(steps2)
                    print(collpoint)
                    raise ValueError("Trace issue: couldn't find collision!")
                fullsteps = steps1 + steps2
                if (not minsteps) or (fullsteps < minsteps):
                    minsteps = fullsteps
    return minsteps

print(f'Puzzle 3-2 Solution: {get_shortest_path(puzzle_case)}')
        
