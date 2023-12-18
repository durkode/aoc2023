import collections
import dataclasses
import enum
import fileinput
import queue
from typing import Dict
import decimal
import pprint
import math

class Turn(enum.Enum):
    LEFT = "left"
    RIGHT = "right"

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

    def move(self, x, y, magnitude):
        return {
            Direction.NORTH: (x, y+magnitude),
            Direction.SOUTH: (x, y-magnitude),
            Direction.EAST: (x+magnitude, y),
            Direction.WEST: (x-magnitude, y),
        }[self]

    def turn_direction(self, from_direction):
        return {
            Direction.NORTH: {
                Direction.EAST: Turn.RIGHT,
                Direction.WEST: Turn.LEFT
            },
            Direction.SOUTH: {
                Direction.EAST: Turn.LEFT,
                Direction.WEST: Turn.RIGHT
            },
            Direction.WEST: {
                Direction.NORTH: Turn.RIGHT,
                Direction.SOUTH: Turn.LEFT,
            },
            Direction.EAST: {
                Direction.NORTH: Turn.LEFT,
                Direction.SOUTH: Turn.RIGHT
            }
        }[from_direction][self]


@dataclasses.dataclass
class Instruction:
    direction: Direction
    distance: int
    colour: str

    def encoded_distance(self):
        return int(self.colour[0:5], 16)

    def encoded_direction(self):
        return {
            0: Direction.EAST,
            1: Direction.SOUTH,
            2: Direction.WEST,
            3: Direction.NORTH
        }[int(self.colour[5])]


def shoelace_area(points):
    determinant_sum = decimal.Decimal(0)
    prev_point = points.get()
    while not points.empty():
        curr_point = points.get()
        determinant_sum += prev_point[0] * curr_point[1] - prev_point[1] * curr_point[0]
        prev_point = curr_point
    return int(determinant_sum / 2)


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

    point_list = queue.SimpleQueue()
    point_list.put((0, 0))

    curr_x = 0
    curr_y = 0
    grid[curr_x][curr_y] = True

    # used to calculate outside edge
    distance_travelled = 0
    left_turns = 0
    right_turns = 0
    prev_direction = None
    first_direction = None

    for i in instructions:
        # direction = i.direction
        # distance = i.distance
        direction = i.encoded_direction()
        distance = i.encoded_distance()
        print(f"distance {distance}, direction {direction}")
        curr_x, curr_y = direction.move(curr_x, curr_y, distance)

        if prev_direction:
            if direction.turn_direction(prev_direction) is Turn.LEFT:
                left_turns += 1
            else:
                right_turns += 1
        else:
            first_direction = direction
        distance_travelled += distance - 1

        print(f"put ({(curr_x, curr_y)})")
        point_list.put((curr_x, curr_y))

        prev_direction = direction

    if first_direction.turn_direction(prev_direction) is Turn.LEFT:
        left_turns += 1
    else:
        right_turns += 1

    print(point_list.qsize())
    poly_area = abs(shoelace_area(point_list))
    distance_addition = distance_travelled * 0.5
    turn_addition = max(left_turns, right_turns) * .75 + min(left_turns, right_turns) * .25
    total_area = poly_area + turn_addition + distance_addition
    print(f"left turns = {left_turns}, right turns = {right_turns}")
    print(f"distance addition = {distance_addition}")
    print(f"turn addition = {turn_addition}")
    print(f"poly_area = {poly_area}, turn_addition = {turn_addition}, total = {total_area}")
    print(total_area)


if __name__=="__main__":
    main()
