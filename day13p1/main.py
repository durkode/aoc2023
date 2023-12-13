import fileinput
import pprint


def row_reflection_indexes(grid):
    indexes = []
    if len(grid) <= 1:
        return indexes
    for r in range(len(grid)-1):
        max_distance = max(1, min(r, len(grid)-r))
        symmetrical = True
        for d in range(max_distance):
            print(f"at r = {r} d = {d}")
            if grid[r-d+1] != grid[r+d]:
                symmetrical = False
        if symmetrical:
            print(f"symmetrical at r = {r}, max_distance = {max_distance}")
            indexes.append(r)
    return indexes

def main():

    grids = []
    active_grid = []

    for line in fileinput.input():
        if line.strip() == "":
            grids.append(active_grid)
            active_grid = []
        else:
            active_grid.append(line.strip().split())
    grids.append(active_grid)

    for x, grid in enumerate(grids):
        print(f"\ngrid {x}")
        pprint.pprint(grid)
        reflection_rows = row_reflection_indexes(grid)
        print()
        print(reflection_rows)


if __name__=="__main__":
    main()
