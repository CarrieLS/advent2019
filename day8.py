

#find layer with fewest 0s
#on that layer, return N(1) * N(2)
#each layer will be w*h digits, so just count 0s in those
def zero_layer(image_ints, width = 25, height = 6):
    layer_size = width*height
    layer_count = len(image_ints) // layer_size
    min_zero_counts = None #update to layer w/ least zeros
    for l_i in range(layer_count):
        layer_ints = image_ints[l_i*layer_size:(l_i+1)*layer_size]
        counts = [0,0,0] #counts of 0,1,2
        for val in layer_ints:
            if val >= 0 and val <= 2:
                counts[val] += 1
        if min_zero_counts == None or counts[0] < min_zero_counts[0]:
            min_zero_counts = counts
    if min_zero_counts == None:
        return -1
    return min_zero_counts[1]*min_zero_counts[2]

puzzle_case = []
with open('adventfiles/puzzle8.txt','r') as f:
    for char in f.read().strip():
        puzzle_case.append(int(char))

print(f"Puzzle 8-1 Solution: {zero_layer(puzzle_case)}")

#now we need to render the image
#2s are transparent, so we only care about the first 0/1 in each slot
#lets save those as a final image, then render it using block characters
#colored black or white

#black and white squares
outstrings = ['\33[30m\u2588','\33[0m\u2588','\33[31m\u2588']

def show_image(image_ints, width = 25, height = 6):
    layer_size = width*height
    final_image = []
    for y_i in range(height):
        image_row = []
        for x_i in range(width):
            image_row.append(2)
        final_image.append(image_row)
    layer_count = len(image_ints) // layer_size
    for l_i in range(layer_count):
        layer_ints = image_ints[l_i*layer_size:(l_i+1)*layer_size]
        for d_i, digit in enumerate(layer_ints):
            x_i = d_i % width
            y_i = d_i // width
            if final_image[y_i][x_i] == 2:
                final_image[y_i][x_i] = digit
    #now print final image
    printlines = []
    for y_i in range(height):
        linechars = []
        for x_i in range(width):
            linechars.append(outstrings[final_image[y_i][x_i]])
        linestr = "".join(linechars)
        printlines.append(linestr)
    printstr = "\n".join(printlines)
    print(printstr)

print("Puzzle 8-2 Solution:\n")
show_image(puzzle_case)
        