from copy import deepcopy

#simulate motion of moons
#moons accelerate based on gravity
#otherwise we just track pos and vel

#gravity application:
    #for each pair of moons, apply +-1 to velocity per coordinate to bring them closer

#then we find potential energy * kinetic energy
#potential energy: sum |x_i|
#kinetic energy: sum |v_i|

#reads in list of lines from input string
#outputs list of 3 element lists for each moon
def read_coords(coord_str_list):
    coords = []
    for line in coord_str_list:
        coord = []
        substrs = line.split(',')
        coord.append(int(substrs[0].split('=')[1]))
        coord.append(int(substrs[1].split('=')[1]))
        coord.append(int(substrs[2].split('=')[1][:-2]))
        coords.append(coord)
    return coords

def find_system_energy_Nsteps(system_coords,N_steps=1000):
    pass

puzzle_coords = []
with open('adventfiles/puzzle12.txt') as f:
    puzzle_coords = f.readlines()

puzzle_coords = read_coords(puzzle_coords)

def simulate_N_steps(coords,N=1000):
    vels = [] #velocities
    for i in range(len(coords)):
        vels.append([0,0,0])
    pos = deepcopy(coords) #so we don't modify the input
    for n in range(N): #do steps
        for i in range(len(coords)-1):
            for j in range(i+1,len(coords)):
                loc_i = pos[i]
                loc_j = pos[j]
                vel_i = vels[i]
                vel_j = vels[j]
                for k in range(3):
                    if loc_i[k] < loc_j[k]:
                        vel_i[k] += 1
                        vel_j[k] -= 1
                    elif loc_i[k] > loc_j[k]:
                        vel_i[k] -= 1
                        vel_j[k] += 1
        #now apply velocity
        for i in range(len(coords)):
            loc_i = pos[i]
            vel_i = vels[i]
            for k in range(3):
                loc_i[k] += vel_i[k]
    #after all steps, find energy
    tot_E = 0
    for i in range(len(coords)):
        loc_i = pos[i]
        vel_i = vels[i]
        pot_i = 0
        kin_i = 0
        for k in range(3):
            pot_i += abs(loc_i[k])
            kin_i += abs(vel_i[k])
        tot_E += pot_i*kin_i
    return tot_E

print(f"Puzzle 12-1 Solution: {simulate_N_steps(puzzle_coords)}")

#now find the first time a loop occurs
#we'll need something more efficient than doing one step at a time, as this
#could take maaany simulations

#one important thing is that each coord is totally independent
#so doing memoization of what happens on each coord could save some time
#also we could find the start and period of stable oscillations for each coord
#then find where these 3 oscillations intersect (LCM)

#we'll need these
#euclidean algorithm
    #if g is largest factor of a,b and a>b;
    #then g is also largest factor of (a-b),b
    #so we keep replacing larger number with diff until they are equal
    #then that's the factor
def fast_gcd(a,b):
    new_a = a
    new_b = b
    while new_a != new_b:
        if new_a > new_b:
            new_a = new_a - new_b
        else:
            new_b = new_b - new_a
    return new_a
    

def fast_lcm(a,b):
    if a <= 0 or b <= 0:
        raise ValueError("a,b must be positive!")
    return a*b//(fast_gcd(a,b))

#ok yeah im p confident about that
def find_1d_loop_period(X,cap=999999):
    V = [0]*len(X)
    s = 0
    start_state = X.copy()
    start_V = V.copy()
    while s < cap:
        for i in range(len(X)):
            x1 = X[i]
            v1 = V[i]
            for j in range(i+1,len(X)):
                x2 = X[j]
                v2 = V[j]
                if x1 > x2:
                    V[i] -= 1
                    V[j] += 1
                elif x1 < x2:
                    V[i] += 1
                    V[j] -= 1
            X[i] += V[i]
        s += 1
        #print(X)
        if (X == start_state) and (V==start_V):
            return s
    return -1

#find osc period for each coord seperately, then find LCM of all 3
def find_osc_period(coords):
    lcm = None
    for k in range(3):
        coords_k = [a[k] for a in coords]
        if lcm == None:
            lcm = find_1d_loop_period(coords_k)
        else:
            lcm = fast_lcm(lcm,find_1d_loop_period(coords_k))
    return lcm

print(f"Puzzle 12-2 Solution: {find_osc_period(puzzle_coords)}")
    