import fileinput
import io
import pprint
import math

def grid_string(grid):
    buf = io.StringIO()
    for row in grid:
        for c in row:
            buf.write(c)
    return buf.getvalue()

def transpose(grid):
    return list(map(list, zip(*grid)))

def vflip(grid):
    return [list(reversed(row)) for row in grid]

def hflip(grid):
    return transpose(vflip(transpose(grid)))

def calculate_load(grid):
    load = 0
    for x, row in enumerate(grid):
        load += row.count('O') * (len(grid) - x)
    return load

def cycle(grid):
    cycled_north = cycle_north(grid)
    # print("NORTH")
    # pprint.pprint(cycled_north)
    cycled_west = cycle_west(cycled_north)
    # print("WEST")
    # pprint.pprint(cycled_west)
    cycled_south = cycle_south(cycled_west)
    # print("SOUTH")
    # pprint.pprint(cycled_south)
    cycled_east = cycle_east(cycled_south)
    return cycled_east

def cycle_north(grid):
    return transpose(shift_west(transpose(grid)))

def cycle_west(grid):
    return shift_west(grid)

def cycle_south(grid):
    return hflip(cycle_north(hflip(grid)))

def cycle_east(grid):
    return vflip(shift_west(vflip(grid)))

def shift_west(grid):
    new_grid = []
    for x, row in enumerate(grid):
        new_row = []
        circle_count = 0
        blank_count = 0
        for c in row:
            if c == ".":
                blank_count += 1
            elif c == "O":
                circle_count += 1
            elif c == "#":
                while circle_count > 0:
                    new_row.append('O')
                    circle_count -= 1
                while blank_count > 0:
                    new_row.append('.')
                    blank_count -= 1
                new_row.append("#")
            else:
                raise ValueError("Invalid tile")
        while circle_count > 0:
            new_row.append('O')
            circle_count -= 1
        while blank_count > 0:
            new_row.append('.')
            blank_count -= 1
        new_grid.append(new_row)
    return new_grid


def main():
    grid = []
    for line in fileinput.input():
        grid.append(list(line.strip()))
    pprint.pprint(grid)

    cache = {} # grid_string -> cycle_number
    cycles = 0
    cycled = grid
    max_cycles = 1000000000
    while cycles < max_cycles:
        cycled = cycle(cycled)
        cycled_string = grid_string(cycled)
        cycles += 1
        if cycled_string not in cache:
            cache[cycled_string] = cycles
        else:
            cycle_diff = cycles - cache[cycled_string]
            cycles = max_cycles - (max_cycles - cycles) % cycle_diff
        print(f"cycled {cycles}")
        # pprint.pprint(cycled)

    total_load = calculate_load(cycled)
    print(total_load)


if __name__=="__main__":
    main()
