import fileinput
import pprint

def transpose(grid):
    return list(map(list, zip(*grid)))

def calculate_load(grid):
    load = 0
    for x, row in enumerate(grid):
        load += row.count('O') * (len(grid) - x)
    return load


def shift_north(grid):
    shifted_transposed = []
    for x, row in enumerate(transpose(grid)):
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
        shifted_transposed.append(new_row)
    return transpose(shifted_transposed)


def main():
    grid = []
    for line in fileinput.input():
        grid.append(list(line.strip()))
    pprint.pprint(grid)

    grid = shift_north(grid)
    total_load = calculate_load(grid)
    pprint.pprint(grid)

    print(total_load)


if __name__=="__main__":
    main()
