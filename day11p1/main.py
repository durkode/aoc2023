import fileinput
import dataclasses


@dataclasses.dataclass
class Coord:
    row: int
    col: int

    def __hash__(self):
        return hash((self.row, self.col))


def main():
    grid = []
    galaxies = set() # set of (row, col) coords

    for line in fileinput.input():
        row = list(line.strip())
        grid.append(row)
        row_idx = len(grid) - 1
        for col_idx, char in enumerate(grid[row_idx]):
            print(f"HERE {col_idx} {char}")
            if char == "#":
                print("THERE")
                galaxies.add(Coord(row=row_idx, col=col_idx))

    galaxy_cols = {g.col for g in galaxies}
    galaxy_rows = {g.row for g in galaxies}

    distance_sum = 0
    import pprint
    pprint.pprint(grid)
    pprint.pprint(galaxies)

    processed = set()
    for p1 in galaxies:
        processed.add(p1)
        for p2 in galaxies.difference(processed):
            print(f"Processing {p1} {p2}")
            distance = 0
            for x in range(min(p1.row, p2.row), max(p1.row, p2.row)):
                distance += 1 if x in galaxy_rows else 2
            for y in range(min(p1.col, p2.col), max(p1.col, p2.col)):
                distance += 1 if y in galaxy_cols else 2
            distance_sum += distance
    print(distance_sum)



if __name__=="__main__":
    main()
