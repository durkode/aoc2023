import fileinput
import pprint

def transpose(grid):
    return list(map(list, zip(*grid)))


def row_reflection_before(grid):
    indexes = []
    if len(grid) <= 1:
        return indexes
    for r in range(len(grid)-1):
        max_distance = min(r+1, len(grid)-r-1)
        smudges = 0
        for d in range(max_distance):
            # print(f"at r = {r} d = {d}")
            # print(f"r = {r}, max_distance = {max_distance}")
            if grid[r-d] != grid[r+d+1]:
                smudges += sum([0 if a==b else 1 for a, b in zip(grid[r-d], grid[r+d+1])])
        if smudges == 1:
            # print(f"symmetrical at r = {r}, max_distance = {max_distance}")
            indexes.append(r)
    return [i+1 for i in indexes]

def main():

    grids = []
    active_grid = []

    for line in fileinput.input():
        if line.strip() == "":
            grids.append(active_grid)
            active_grid = []
        else:
            active_grid.append(list(line.strip()))
    grids.append(active_grid)

    row_sum = 0
    col_sum = 0
    for x, grid in enumerate(grids):
        print(f"\ngrid {x}")
        pprint.pprint(grid)
        reflection_rows = row_reflection_before(grid)
        print("rows")
        print(reflection_rows)
        transposed = transpose(grid)
        print()
        # pprint.pprint(transposed)
        reflection_cols = row_reflection_before(transposed)
        print("cols")
        print(reflection_cols)
        row_sum += sum(reflection_rows)
        col_sum += sum(reflection_cols)
    print(100*row_sum + col_sum)


if __name__=="__main__":
    main()
