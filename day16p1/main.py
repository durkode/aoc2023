import dataclasses
import enum
import fileinput
import functools
import pprint
from typing import Tuple, List

class Direction(enum.Enum):
    LEFT = "left"
    RIGHT = "right"
    UP = "up"
    DOWN = "down"

@dataclasses.dataclass
class Destination:
    direction: Direction
    coords: Tuple[int, int]

    def row(self):
        return self.coords[0]

    def col(self):
        return self.coords[1]

def move(coords, direction):
    row, col = coords
    if direction is direction.LEFT:
        return row, col-1
    if direction is direction.RIGHT:
        return row, col+1
    if direction is direction.UP:
        return row-1, col
    if direction is direction.DOWN:
        return row+1, col
    raise ValueError()

grid = []
visited = set()
past_moves = set()
def filter_invalid(destinations: List[Destination]) -> List[Destination]:
    return [d for d in destinations if 0 <= d.row() < len(grid) and 0 <= d.col() < len(grid[0])]

def beam_destinations(destination: Destination):
    coords = destination.coords
    direction = destination.direction
    print(coords)
    visited.add(coords)
    if (coords, direction) in past_moves:
        return []
    else:
        past_moves.add((coords, direction))
    row, col = coords
    tile = grid[row][col]
    if tile == ".":
        new_coords = move(coords, direction)
        filtered = filter_invalid([Destination(coords=new_coords, direction=direction)])
        return filtered
    if tile == "\\":
        if direction is Direction.RIGHT:
            new_dir = Direction.DOWN
        elif direction is Direction.UP:
            new_dir = Direction.LEFT
        elif direction is Direction.DOWN:
            new_dir = Direction.RIGHT
        elif direction is Direction.LEFT:
            new_dir = Direction.UP
        else:
            raise ValueError()
        return filter_invalid([Destination(coords=move(coords, new_dir), direction=new_dir)])
    if tile == "/":
        if direction is Direction.RIGHT:
            new_dir = Direction.UP
        elif direction is Direction.UP:
            new_dir = Direction.RIGHT
        elif direction is Direction.DOWN:
            new_dir = Direction.LEFT
        elif direction is Direction.LEFT:
            new_dir = Direction.DOWN
        else:
            raise ValueError()
        return filter_invalid([Destination(coords=move(coords, new_dir), direction=new_dir)])

    if tile == "-":
        if direction in {Direction.LEFT, Direction.RIGHT}:
            return filter_invalid([Destination(coords=move(coords, direction), direction=direction)])
        else:
            return filter_invalid([
                Destination(coords=move(coords, Direction.LEFT), direction=Direction.LEFT),
                Destination(coords=move(coords, Direction.RIGHT), direction=Direction.RIGHT),
            ])

    if tile == "|":
        if direction in {Direction.UP, Direction.DOWN}:
            return filter_invalid([Destination(coords=move(coords, direction), direction=direction)])
        else:
            return filter_invalid([
                Destination(coords=move(coords, Direction.UP), direction=Direction.UP),
                Destination(coords=move(coords, Direction.DOWN), direction=Direction.DOWN),
            ])

def visit(start, direction):
    to_visit = [Destination(coords=start, direction=direction)]
    while to_visit:
        d = to_visit.pop()
        print(f"Visiting {d}")
        new_destinations = beam_destinations(d)
        print(f"New locations: {new_destinations}")
        to_visit += new_destinations


def main():

    for line in fileinput.input():
        grid.append(list(line.strip()))

    pprint.pprint(grid)
    visit((0,0), Direction.RIGHT)
    print(len(visited))

if __name__=="__main__":
    main()