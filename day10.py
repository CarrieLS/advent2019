#for each asteroid, we can track the angles to other asteroids
#an asteroid can only track as many asteroids as it has angles
#for angles, lets track tan(theta) [Dy/Dx], with None for vertical angles
#we can use python fractions for this to avoid floating point errors

#we can go thru the asteroids in order and for each one only check asteroids
#with higher index, this should be O(N^2) where N is # of asteroids

#first lets make a list of asteroid locations, this is O(XY) which is
#generally <O(N^2) assuming high asteroid density
from fractions import Fraction
import numpy as np

def map_to_locations(asteroid_map):
    locs = []
    for y in range(len(asteroid_map)):
        for x in range(len(asteroid_map[0])):
            if asteroid_map[y][x] == '#':
                locs.append((x,y))
    return locs

def find_best_location(asteroid_map):
    locs = map_to_locations(asteroid_map)
    best_loc = None
    best_count = 0
    pa_dict = {}
    na_dict = {}
    for i,loc in enumerate(locs[:len(locs)-1]):
        p_angles = set() #angles where Dx > 0, or if Dx == 0 then Dy > 0
        n_angles = set() #angles where Dx < 0, or if Dx == 0 then Dy < 0
        if i in pa_dict:
            p_angles = pa_dict[i]
        else:
            pa_dict[i] = p_angles
        if i in na_dict:
            n_angles = na_dict[i]
        else:
            na_dict[i] = n_angles
        for j,loc2 in enumerate(locs[i+1:],start=i+1):
            Dy = loc2[1] - loc[1]
            Dx = loc2[0] - loc[0]
            new_angle = None
            angle_dir = (Dx > 0) #true for p_angle
            if Dx != 0:
                new_angle = Fraction(Dy,Dx)
                angle_dir = (Dy > 0) #true for p_angle
            if angle_dir:
                p_angles.add(new_angle)
                if j in na_dict:
                    na_dict[j].add(new_angle)
                else:
                    na_dict[j] = {new_angle}
            else:
                n_angles.add(new_angle)
                if j in pa_dict:
                    pa_dict[j].add(new_angle)
                else:
                    pa_dict[j] = {new_angle}
        count = len(p_angles) + len(n_angles)
        if count >= best_count:
            best_count = count
            best_loc = loc
    return best_loc,best_count

test_case = """.#..#
.....
#####
....#
...##""".split()

test_2 = """......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####""".split()

puzzle_case = []
with open('adventfiles/puzzle10.txt') as f:
    puzzle_case = f.read().split()

puzzle_loc,puzzle_count = find_best_location(puzzle_case)

print(f"Puzzle 10-1 solution: {puzzle_count}")

#first we will find angle relative to vertical
#and distance (r*2 since we only need order) for each
#then we will sweep through and remove one per angle
#lets use actual angle this time with arctan for simplicity

#this func gives the angle of a 2d coord (Dx,Dy) relative to up
#angle is given in radians
def angle_relative_up(Dx,Dy):
    #verticals
    if Dx == 0:
        if Dy > 0:
            return 0
        return np.pi
    return np.arctan2(-Dx,-Dy)+np.pi

#make a dict of angles : [(distance,coord_score)]
#use bisect insort to keep list sorted by distance
def find_Nth_vaporized(asteroid_map,location,N=200):
    locs = map_to_locations(asteroid_map)
    locs.remove(location) #ignore the asteroid we are on
    angles = {}
    for loc in locs:
        Dx = loc[0] - location[0]
        Dy = location[1] - loc[1]
        dist = Dx**2 + Dy**2
        coord_score = loc[0]*100+loc[1]
        angle = angle_relative_up(Dx,Dy)
        if angle in angles:
            angles[angle].append((dist,coord_score))
        else:
            angles[angle] = [(dist,coord_score)]
    sorted_asteroid_groups = []
    for angle in sorted(angles.keys()):
        sorted_asteroid_groups.append(sorted(angles[angle],reverse=True))
    count = 0 #count what asteroid we are on
    i = 0
    loop_check = False #tracks if we found any asteroids in our full loop,
    #to avoid looping forever with no more asteroids
    while count < N:
        if i >= len(sorted_asteroid_groups):
            if loop_check:
                i = 0
                loop_check = False
            else:
                return None
        next_asteroid_group = sorted_asteroid_groups[i]
        if len(next_asteroid_group) == 0:
            i += 1
            continue
        else:
            asteroid = next_asteroid_group.pop()
            count += 1
            i += 1
            if count == N:
                return asteroid[1]
            
vapor_test = """.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##""".split()

vapor_loc = (11,13)

print(f"Puzzle 10-2 Solution: {find_Nth_vaporized(puzzle_case,puzzle_loc)}")