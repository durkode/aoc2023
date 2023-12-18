import collections
import dataclasses
import enum
import fileinput
import queue
from typing import Dict
import pprint


class Direction(enum.Enum):
    NORTH = "north"
    SOUTH = "south"
    EAST = "east"
    WEST = "west"

    @staticmethod
    def from_udlr(s):
        return {
            "U": Direction.NORTH,
            "D": Direction.SOUTH,
            "L": Direction.WEST,
            "R": Direction.EAST
        }[s]

    def move(self, x, y):
        return {
            Direction.NORTH: (x, y+1),
            Direction.SOUTH: (x, y-1),
            Direction.EAST: (x-1, y),
            Direction.WEST: (x+1, y),
        }[self]


@dataclasses.dataclass
class Instruction:
    direction: Direction
    distance: int
    colour: str


def surrounding_squares(x, y):
    return [
        Direction.NORTH.move(x, y),
        Direction.SOUTH.move(x, y),
        Direction.EAST.move(x, y),
        Direction.WEST.move(x, y)
    ]


def flood_fill(grid, min_x, min_y, max_x, max_y):

    fill_grid: Dict[int, Dict[int, bool]] = collections.defaultdict(dict)
    # copy to new grid
    for x, row in grid.items():
        for y, val in row.items():
            fill_grid[x][y] = val

    old_size = sum(len(o) for o in grid.values())

    def in_bounds(x, y):
        return min_x <= x <= max_x and min_y <= y <= max_y

    q = queue.SimpleQueue()

    for x in range(min_x, max_x+1):
        q.put((x, min_y))
        q.put((x, max_y))
    for y in range(min_y, max_y+1):
        q.put((min_x, y))
        q.put((max_x, y))

    print(f"x: {min_x} to {max_x}")
    print(f"y: {min_y} to {max_y}")

    while not q.empty():
        x, y = q.get()
        if y in fill_grid[x]:
            continue
        if x < min_x or x > max_x or y < min_y or y > max_y:
            print(f"VIOLATION: {(x, y)}")
        fill_grid[x][y] = True
        for new_x, new_y in [(a, b) for a, b in surrounding_squares(x, y) if in_bounds(a, b)]:
            q.put((new_x, new_y))

    new_size = sum(len(o) for o in fill_grid.values())
    total_area = (max_x-min_x+1) * (max_y - min_y+1)

    print(f"x: {min_x} to {max_x}")
    print(f"y: {min_y} to {max_y}")
    for y in range(max_y, min_y-1, -1):
        for x in range(max_x, min_x-1, -1):
            if y in fill_grid[x]:
                print("#", end="")
            else:
                print(".", end="")
        print("\n", end="")

    print(f"x: {min_x} to {max_x}")
    print(f"y: {min_y} to {max_y}")
    print(f"New size {new_size}, old_size {old_size}, total area = {total_area}")

    return total_area - new_size + old_size




def main():
    instructions = []

    for input in fileinput.input():
        d, l, c = input.strip().split(" ")
        instructions.append(Instruction(
            direction=Direction.from_udlr(d),
            distance=int(l),
            colour=c.strip("(#)")
        ))

    grid: Dict[int, Dict[int, bool]] = collections.defaultdict(dict)

    curr_x = 0
    curr_y = 0
    min_x = curr_x
    min_y = curr_y
    max_x = curr_x
    max_y = curr_y
    grid[curr_x][curr_y] = True
    for i in instructions:
        to_travel = i.distance
        while to_travel > 0:
            to_travel -= 1
            curr_x, curr_y = i.direction.move(curr_x, curr_y)
            grid[curr_x][curr_y] = True
            min_x = min(min_x, curr_x)
            min_y = min(min_y, curr_y)
            max_x = max(max_x, curr_x)
            max_y = max(max_y, curr_y)

    print(sum(len(o) for o in grid.values()))

    area = flood_fill(grid, min_x, min_y, max_x, max_y)

    print(area)


if __name__=="__main__":
    main()
