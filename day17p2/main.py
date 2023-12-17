import collections
import dataclasses
import enum
import fileinput
import functools
import pprint
import queue
from typing import Tuple

grid = []

MAX_MOVES_IN_LINE = 3

ULTRA_MIN_MOVES = 4
ULTRA_MAX_MOVES = 10

class Direction(enum.Enum):
    NORTH = "north"
    SOUTH = "south"
    EAST = "east"
    WEST = "west"

    def reverse(self):
        return {
            Direction.NORTH: Direction.SOUTH,
            Direction.EAST: Direction.WEST,
            Direction.WEST: Direction.EAST,
            Direction.SOUTH: Direction.NORTH
        }[self]

    def get_from(self, from_coords, magnitude):
        r, c = from_coords
        return {
            Direction.NORTH: (r-magnitude, c),
            Direction.SOUTH: (r+magnitude, c),
            Direction.WEST: (r, c-magnitude),
            Direction.EAST: (r, c+magnitude)
        }[self]

@dataclasses.dataclass
class Move:
    prev_direction: Direction
    coords: Tuple[int, int]
    prev_direction_moves: int

class MoveCache:

    def __init__(self):
        self.cache = {} # coord -> prev_direction -> prev_move -> cost

    def add(self, coord, prev_direction, prev_direction_moves, cost):
        coord_cache = self.cache.get(coord)
        if not coord_cache:
            self.cache[coord] = {prev_direction: {prev_direction_moves: cost}}
            return
        direction_cache = coord_cache.get(prev_direction)
        if not direction_cache:
            coord_cache[prev_direction] = {prev_direction_moves: cost}
            return
        if prev_direction_moves not in direction_cache:
            direction_cache[prev_direction_moves] = cost
        else:
            direction_cache[prev_direction_moves] = min(cost, direction_cache[prev_direction_moves])

    def get(self, coord, prev_direction):
        try:
            return self.cache[coord][prev_direction].copy()
        except KeyError:
            return None

def get_next_coords(grid, curr_coords, previous_direction, previous_direction_moves):
    banned_directions = [previous_direction.reverse()] if previous_direction_moves < MAX_MOVES_IN_LINE else [previous_direction.reverse(), previous_direction]

    base_list = [
        d.get_from(curr_coords) for d in Direction if d not in banned_directions
    ]
    return [
        (r, c) for r, c in base_list if 0 <= r < len(grid) and 0 <= c < len(grid[0])
    ]

def in_grid(grid, l):
    return [
        (r, c) for r, c in l if 0 <= r < len(grid) and 0 <= c < len(grid[0])
    ]

def get_next_coords_ultra(grid, curr_coords, previous_direction: Direction, previous_direction_moves):

    # Special case: first move
    if previous_direction_moves == 0:
        return in_grid(grid, [d.get_from(curr_coords, ULTRA_MIN_MOVES) for d in Direction])

    banned_directions = [previous_direction.reverse()]
    if previous_direction_moves >= ULTRA_MAX_MOVES:
        banned_directions.append(previous_direction)

    base_list = [
        d.get_from(curr_coords, 1 if d is previous_direction else ULTRA_MIN_MOVES) for d in Direction if d not in banned_directions
    ]
    return in_grid(grid, base_list)


def get_direction(from_coords, to_coords):
    from_row, from_col = from_coords
    to_row, to_col = to_coords
    if to_row < from_row and to_col == from_col:
        return Direction.NORTH
    if to_row > from_row and to_col == from_col:
        return Direction.SOUTH
    if to_row == from_row and to_col < from_col:
        return Direction.WEST
    if to_row == from_row and to_col > from_col:
        return Direction.EAST

    print(f"from {from_coords} to {to_coords}")
    raise ValueError()

def get_coords(from_coords, to_coords):
    # Get all coords in interval, not including from_coords
    from_row, from_col = from_coords
    to_row, to_col = to_coords
    ret = []
    if to_row < from_row and to_col == from_col:
        while to_row < from_row:
            from_row -= 1
            ret.append((from_row, from_col))
        return ret
    if to_row > from_row and to_col == from_col:
        while to_row > from_row:
            from_row += 1
            ret.append((from_row, from_col))
        return ret
    if to_row == from_row and to_col < from_col:
        while to_col < from_col:
            from_col -= 1
            ret.append((from_row, from_col))
        return ret
    if to_row == from_row and to_col > from_col:
        while to_col > from_col:
            from_col += 1
            ret.append((from_row, from_col))
        return ret

    raise ValueError()

def get_cost(grid):
    move_cache = MoveCache()
    node_count = 1
    target = (len(grid)-1, len(grid[0])-1)
    # target = (5, 5)
    q = queue.PriorityQueue()
    q.put((0, node_count, Move(coords=(0, 0), prev_direction=Direction.SOUTH, prev_direction_moves=0), []))
    while not q.empty():
        cost, _, move, prior_moves = q.get()
        print(f"Coords: {move.coords}, cost {cost}, prev_direction: {move.prev_direction}, prev_moves: {move.prev_direction_moves}")
        if move.coords == target:
            return cost, prior_moves
        next_coords = get_next_coords_ultra(grid, move.coords, move.prev_direction, move.prev_direction_moves)
        print(f"iterating coords {next_coords}")
        for next_stop in next_coords:
            node_count += 1
            print(f"Next {next_stop}")
            interval_coords = get_coords(move.coords, next_stop)
            next_direction = get_direction(move.coords, next_stop)
            change_in_direction = next_direction is not move.prev_direction
            next_direction_moves =  len(interval_coords) if change_in_direction else move.prev_direction_moves + len(interval_coords)
            if (0, 5) == next_stop:
                print(f"(0, 5): next_direction_moves == {next_direction_moves}, change_in_direction == {change_in_direction}")
                print(f"PREV_DIRECTION {move.prev_direction}, next_direction  {next_direction}")
            new_cost = cost + sum(grid[r][c] for r, c in interval_coords)

            cached_vals = move_cache.get(next_stop, next_direction)
            if cached_vals:
                # cached_vals dict of move_count -> cost
                cached_cost = cached_vals.get(next_direction_moves)
                if cached_cost is not None:
                    if cached_cost <= new_cost:
                        continue # Already queued up to explore

            new_move = Move(
                    coords=next_stop,
                    prev_direction=next_direction,
                    prev_direction_moves=next_direction_moves
                )
            entry = new_cost, node_count, new_move, prior_moves.copy() + [(new_move, new_cost)]
            q.put(entry)
            move_cache.add(next_stop, next_direction, next_direction_moves, new_cost)
        print("Done interating")

    raise AssertionError()




def main():
    for line in fileinput.input():
        grid.append([int(x) for x in list(line.strip())])


    pprint.pprint(grid)

    cost, prior_moves = get_cost(grid)
    for m in prior_moves:
        move, running_cost = m
        print(f"coords = {move.coords}, cost = {running_cost}")
    print(cost)



if __name__=="__main__":
    main()