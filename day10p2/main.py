import fileinput
import math
import pprint
from typing import List, Set, Tuple


class Pipe:

    def __init__(self, char, row, col):
        self.up = char in ["|", "J", "L"]
        self.down = char in ["|", "F", "7"]
        self.left = char in ["-", "J", "7"]
        self.right = char in ["-", "F", "L"]
        self.row = row
        self.col = col

    def __str__(self):
        if self.up and self.down:
            return "|"
        if self.up and self.left:
            return "J"
        if self.up and self.right:
            return "L"
        if self.left and self.right:
            return "-"
        if self.down and self.left:
            return "7"
        if self.down and self.right:
            return "F"
        return "."

    def __repr__(self):
        return self.__str__()


def find_start(grid, row, col):
    p = Pipe(".", row, col)
    p.left = col > 0 and grid[row][col-1].right
    p.right = col < len(grid[row])-1 and grid[row][col+1].left
    p.up = row > 0 and grid[row-1][col].down
    p.down = row < len(grid) - 1 and grid[row+1][col].up
    return p


def get_connecting_pipes(grid, row, col) -> Set[Pipe]:
    ret = set()
    curr = grid[row][col]
    if curr.left:
        ret.add(grid[row][col-1])
    if curr.right:
        ret.add(grid[row][col+1])
    if curr.up:
        ret.add(grid[row-1][col])
    if curr.down:
        ret.add(grid[row+1][col])
    return ret


def pipe_tiles(grid, start_row, start_col):
    # pick a start at random
    visited = set()
    visited.add(grid[start_row][start_col])
    # Pick a next node at random
    next_node = get_connecting_pipes(grid, start_row, start_col).pop()
    while True:
        visited.add(next_node)
        next_nodes = get_connecting_pipes(grid, next_node.row, next_node.col) - visited
        if not next_nodes:
            break
        next_node = next_nodes.pop()
    return visited


def adjacent_tiles(grid, row, col):
    ret = set()
    if row > 0:
        ret.add(grid[row-1][col])
    if col > 0:
        ret.add(grid[row][col-1])
    if row < len(grid) - 1:
        ret.add(grid[row+1][col])
    if col < len(grid[row]) - 1:
        ret.add(grid[row][col+1])
    return ret


def fill_out(grid, pipes, starting_set) -> Set[Pipe]:
    curr_set = starting_set.copy()
    filled = set()
    while True:
        length = len(filled)
        filled = filled | curr_set
        next_set = set()
        for p in curr_set:
            adjacent = adjacent_tiles(grid, p.row, p.col)
            next_set = next_set | adjacent
        next_set = next_set - filled - pipes
        curr_set = next_set

        if len(filled) == length:
            break
        print(len(filled))
    return filled


def expand_grid(grid, pipes) -> Tuple[List[List[Pipe]], Set[Pipe]]:
    new_grid = []
    new_pipes = set()
    for row in range(0, 2*len(grid) - 1):
        r = []
        for col in range(0, 2*len(grid[0]) - 1):
            r.append(Pipe(".", row, col))
        new_grid.append(r)

    for p in pipes:
        new_p = Pipe(p.__str__(), p.row * 2, p.col * 2)
        new_pipes.add(new_p)
        new_grid[new_p.row][new_p.col] = new_p
        if new_p.up and new_grid[new_p.row-1][new_p.col].__str__() == ".":
            filler = Pipe("|", new_p.row-1, new_p.col)
            new_grid[filler.row][filler.col] = filler
            new_pipes.add(filler)
        if new_p.down and new_grid[new_p.row+1][new_p.col].__str__() == ".":
            filler = Pipe("|", new_p.row+1, new_p.col)
            new_grid[filler.row][filler.col] = filler
            new_pipes.add(filler)
        if new_p.left and new_grid[new_p.row][new_p.col - 1].__str__() == ".":
            filler = Pipe("-", new_p.row, new_p.col - 1)
            new_grid[filler.row][filler.col] = filler
            new_pipes.add(filler)
        if new_p.right and new_grid[new_p.row][new_p.col + 1].__str__() == ".":
            filler = Pipe("-", new_p.row, new_p.col + 1)
            new_grid[filler.row][filler.col] = filler
            new_pipes.add(filler)

    return new_grid, new_pipes


def main():
    grid = []
    start = None
    for line in fileinput.input():
        curr = []
        for c in line.strip():
            if c == "S":
                start = (len(grid), len(curr))
            curr.append(Pipe(c, len(grid), len(curr)))
        grid.append(curr)

    grid[start[0]][start[1]] = find_start(grid, start[0], start[1])

    pipes = pipe_tiles(grid, start[0], start[1])

    # Now, expand the world so every odd coord is an existing pipe, every even is interfill
    grid, pipes = expand_grid(grid, pipes)

    print(f"Grid is {len(grid)} x {len(grid[0])} = {len(grid) * len(grid[0])}")

    all_tiles = set()
    for row in grid:
        for p in row:
            all_tiles.add(p)

    # pprint.pprint(grid)

    edge_tiles = set()
    for row in grid:
        edge_tiles.add(row[0])
        edge_tiles.add(row[-1])
    for col in grid[0] + grid[-1]:
        edge_tiles.add(col)
    edge_tiles = edge_tiles - pipes

    print("Flooding")

    flooded = fill_out(grid, pipes, edge_tiles)

    print("Flooded")

    enclosed = all_tiles - pipes - flooded

    enclosed_evens = [e for e in enclosed if e.row % 2 == 0 and e.col % 2 == 0]
    print(f"Enclosed: {len(enclosed_evens)}")


if __name__=="__main__":
    main()
