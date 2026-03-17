#go thru our fuel recipe and track all our demands
#then try to produce enough for each demand, keeping track of ore cost and excess
#do this until we have no demands

test_case = """10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL""".split('\n')

test2 = """157 ORE => 5 NZVS
165 ORE => 6 DCFZ
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
179 ORE => 7 PSHF
177 ORE => 5 HKGWZ
7 DCFZ, 7 PSHF => 2 XJWVT
165 ORE => 2 GPVTF
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT""".split('\n')

test3 = """2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
17 NVRVD, 3 JNWZP => 8 VPVL
53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
22 VJHF, 37 MNCFX => 5 FWMGM
139 ORE => 4 NVRVD
144 ORE => 7 JNWZP
5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
145 ORE => 6 MNCFX
1 NVRVD => 8 CXFTF
1 VJHF, 6 MNCFX => 4 RFSQX
176 ORE => 6 VJHF""".split('\n')

test4 = """171 ORE => 8 CNZTR
7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
114 ORE => 4 BHXH
14 VRPVC => 6 BMBT
6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
5 BMBT => 4 WPTQ
189 ORE => 9 KTJDG
1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
12 VRPVC, 27 CNZTR => 2 XDBXC
15 KTJDG, 12 BHXH => 5 XCVML
3 BHXH, 2 VRPVC => 7 MZWV
121 ORE => 7 VRPVC
7 XCVML => 6 RJRHP
5 BHXH, 4 VRPVC => 5 LTCX""".split('\n')

#31 ore -> 1 fuel and 2A
#if we wanted to find how much we could make from 1000 ore, we would start
#by dividing (1000)//31 to get a factor of 32
#this gives us 32 fuel, 64A, and 8 ORE

puzzle_case = []
with open('adventfiles/puzzle14.txt') as f:
    for line in f:
        puzzle_case.append(line.strip())


def process_input(str_recipes):
    recipes = {}
    for line in str_recipes:
        split_line = line.split(' ') #ex [10,ORE,=>,10,A]
        out_material = None
        out_amount = None
        inputs = []
        i = 0
        while i < len(split_line):
            if split_line[i] == '=>':
                out_material = split_line[i+2]
                out_amount = int(split_line[i+1])
                break
            else:
                inputs.append((split_line[i+1].strip(','),int(split_line[i])))
                i+=2
        recipes[out_material] = [out_amount] + inputs
    return recipes

#fuel always produced 1 at a time so we can ignore that
#this is min cost per N fuel
def find_min_cost(recipes,N=1):
    fuel_recipe = recipes['FUEL']
    demands = {}
    excesses = {}
    orecount = 0 #never put ore in demands/excesses, it goes here
    for components in fuel_recipe[1:]:
        if components[0] == 'ORE':
            orecount += N*components[1]
        else:
            demands[components[0]] = N*components[1]
    while len(demands) != 0:
        curr_key = next(iter(demands.keys()))
        demand = demands[curr_key]
        recipe = recipes[curr_key] #to convert to
        recipe_multiplier = (demand+recipe[0]-1)//(recipe[0])
        del demands[curr_key]
        excess_amount = recipe_multiplier*recipe[0]-demand
        if excess_amount != 0:
            excesses[curr_key] = excess_amount
        #now add inputs to demand
        for component in recipe[1:]:
            material = component[0]
            adj_amount = component[1]*recipe_multiplier
            if material == 'ORE':
                orecount += adj_amount
            elif material in excesses:
                excesses[material] -= adj_amount
                if excesses[material] == 0:
                    del excesses[material]
                elif excesses[material] < 0:
                    demands[material] = -excesses[material]
                    del excesses[material]
            else:
                demands[material] = adj_amount + demands.get(material,0)
    return (orecount, excesses)

puzzle_recipes = process_input(puzzle_case)
puzzle_results = find_min_cost(puzzle_recipes)

print(f"Puzzle 14-1 Solution: {puzzle_results[0]}")
            
#now we need to find how much fuel we can get from 10**12 ore
#we can find the approx value by ignoring the integer restriction

def ore_per_material(recipes,material,memo,debug=False):
    if material in memo:
        return memo[material]
    elif material == 'ORE':
        memo['ORE'] = 1
        return 1
    recipe = recipes[material]
    ore_cost = 0
    for component in recipe[1:]:
        ore_cost += component[1]*ore_per_material(recipes,component[0],memo)
    ore_cost /= recipe[0]
    memo[material] = ore_cost
    return ore_cost


#this gets upper limit
#then we can just test if this value is achievable using our find_min_cost func
#and try lower values until we find an achievable amount
def fuel_per_N_ore(recipes,N=10**12):
    max_fuel = int(N//ore_per_material(recipes,'FUEL',{}))
    curr_guess = max_fuel
    curr_oreval = find_min_cost(recipes,curr_guess)[0]
    while curr_oreval > N:
        curr_guess -= 1
        curr_oreval = find_min_cost(recipes,curr_guess)[0]
    return curr_guess

print(f"Puzzle 14-2 Solution: {fuel_per_N_ore(puzzle_recipes)}")