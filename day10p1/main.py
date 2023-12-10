import fileinput
import math
import pprint
from typing import Set

class Pipe:

    def __init__(self, char, x, y):
        self.up = char in ["|", "J", "L"]
        self.down = char in ["|", "F", "7"]
        self.left = char in ["-", "J", "7"]
        self.right = char in ["-", "F", "L"]
        self.x = x
        self.y = y

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


def find_start(grid, x, y):
    p = Pipe(".", x, y)
    p.left = y > 0 and grid[x][y-1].right
    p.right = y < len(grid[x])-1 and grid[x][y+1].left
    p.up = x > 0 and grid[x-1][y].down
    p.down = x < len(grid) - 1 and grid[x+1][y].up
    return p

def get_connecting_pipes(grid, x, y) -> Set[Pipe]:
    ret = set()
    curr = grid[x][y]
    if curr.left:
        ret.add(grid[x][y-1])
    if curr.right:
        ret.add(grid[x][y+1])
    if curr.up:
        ret.add(grid[x-1][y])
    if curr.down:
        ret.add(grid[x+1][y])
    return ret


def find_loop_length(grid, start_x, start_y):
    # pick a start at random
    visited = set()
    visited.add(grid[start_x][start_y])
    # Pick a next node at random
    next_node = get_connecting_pipes(grid, start_x, start_y).pop()
    while True:
        visited.add(next_node)
        next_nodes = get_connecting_pipes(grid, next_node.x, next_node.y) - visited
        if not next_nodes:
            break
        next_node = next_nodes.pop()
    return math.floor(len(visited)/2)

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
    pprint.pprint(grid)
    pprint.pprint(start)

    grid[start[0]][start[1]] = find_start(grid, start[0], start[1])

    loop_length = find_loop_length(grid, start[0], start[1])
    print(loop_length)



if __name__=="__main__":
    main()
