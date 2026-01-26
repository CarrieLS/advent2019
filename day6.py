#count orbits
#we can go through the list and at each point count # of orbits
#it adds by tracking the nested level of each object
#eg, if our list is:
    #COM ) A
    #A ) B
    #A ) C
    #should be 5 total orbits
#we would go through and count:
    #COM ) A: +1 (COM orbits 0, track that A orbits 1)
    #A ) B: +1+1 = +2, as A orbits 1 (track that B orbits 2)
    #A ) C: +1+1 = +2, as A orbits 1
#use a dict to track this
#oh oops this only works if we start at COM and go up
#we need to support both directions
#lets just build a graph and then count backwards
#using memo for backwards count to make it faster

class OrbitBody:
    def __init__(self, previous = None):
        self.previous = previous
        self.orbitcount = None #defined during counting
    
    #recursively count how many orbits, don't need to trace every time
    def count_orbits(self):
        if self.orbitcount != None:
            return self.orbitcount
        elif self.previous == None: #should only be COM
            self.orbitcount = 0
            return 0
        else:
            self.orbitcount = self.previous.count_orbits() + 1
            return self.orbitcount

#split into a seperate func for easier part 2
#take list of orbits, return dictionary of names -> bodies
def build_map(orbit_list):
    bodymap = {} #dict that maps names onto bodies
    for orbit in orbit_list:
        bodies = orbit.split(')')
        #get bodies if they exist, otherwise make new ones
        primary = None
        if bodies[0] in bodymap:
            primary = bodymap[bodies[0]]
        else:
            primary = OrbitBody()
            bodymap[bodies[0]] = primary
        if bodies[1] in bodymap:
            secondary = bodymap[bodies[1]]
            secondary.previous = primary #update chain
        else:
            secondary = OrbitBody(primary)
            bodymap[bodies[1]] = secondary
    return bodymap

def count_orbits(bodymap):
    #bodymap creation has moved to a diff function
    #now we should be able to count total orbits
    #by counting them for each body
    totalcount = 0
    for body in bodymap.values():
        totalcount += body.count_orbits()
    return totalcount

test_case = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L""".split('\n')

test_map = build_map(test_case)

assert count_orbits(test_map) == 42

puzzle_case = []
with open('adventfiles/puzzle6.txt','r') as f:
    for line in f.readlines():
        puzzle_case.append(line.strip())

puzzle_map = build_map(puzzle_case)

print(f'Puzzle 6-1 Solution: {count_orbits(puzzle_map)}')

#part 2
#trace path between YOU and SAN
#can go backwards from each until the same node is found?
#trace YOU all the way backwards, then trace SAN and as soon as you find a node
#in common you have a path
#as you trace, count steps (not the first one), then add those together

def find_path_length(bodymap,start='YOU',target='SAN'):
    startnode = bodymap[start]
    pathdepths = {}
    currdepth = 0
    currnode = startnode
    while currnode.previous != None:
        currnode = currnode.previous
        pathdepths[currnode] = currdepth
        currdepth += 1
    #now trace SAN until you find a match
    targetnode = bodymap[target]
    currnode = targetnode
    currdepth = 0
    while currnode.previous != None:
        currnode = currnode.previous
        if currnode in pathdepths:
            return currdepth + pathdepths[currnode]
        currdepth += 1
    return -1 #no path exists - shouldn't happen

print(f'Puzzle 6-2 Solution: {find_path_length(puzzle_map)}')