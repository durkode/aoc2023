import fileinput
import math
import functools
import sys

# Ideas: starting groups must match, total count must not be over

def find_middle_index(length):
    middle = float(length)/2
    if middle % 2 != 0:
        return int(middle - .5)
    else:
        # Return the left most if 2 available
        return int(middle)


@functools.lru_cache
def possible_arrangements_v2(record, damage_counts):
    # print("HERE")
    # print(damage_counts)
    if not record and not damage_counts:
        return 1
    if not damage_counts and "#" in record:
        return 0
    if len(record) < sum(damage_counts) + len(damage_counts) - 1:
        return 0

    possible = 0
    undamaged_indexes = [i for i, c in enumerate(record) if c == "."]
    # Case 1: divide and conquer on split
    if undamaged_indexes:
        middle_index = find_middle_index(len(undamaged_indexes))
        left = record[:undamaged_indexes[middle_index]]
        right = record[undamaged_indexes[middle_index]+1:]
        # print(f"RECORD: {record} L: {left} R: {right} DAMAGE: {damage_counts}")
        for x in range(len(damage_counts) + 1):
            left_possible = possible_arrangements_v2(left, damage_counts[:x])
            if left_possible > 0:
                right_possible = possible_arrangements_v2(right, damage_counts[x:])
                # print(f"left({left}, {damage_counts[:x]}) = {left_possible}, right({right}, {damage_counts[x:]}) ="
                #       f" {right_possible}")

                possible += left_possible * right_possible
        return possible

    wildcard_indexes = [i for i, c in enumerate(record) if c == "?"]
    # Case 2: Only ? and #
    if wildcard_indexes:
        middle_index = find_middle_index(len(wildcard_indexes))
        left = record[:wildcard_indexes[middle_index]]
        right = record[wildcard_indexes[middle_index]+1:]
        for p in {'.', '#'}:
            substitute = left + p + right
            possible += possible_arrangements_v2(substitute, damage_counts)
        return possible

    # Case 3: Only # left
    val = 1 if len(damage_counts) == 1 and len(record) == damage_counts[0] else 0
    # print(f"Fall through {record} val {val} with {damage_counts}")
    return val


def main():
    possible_combination_sum = 0
    num = 0
    for line in fileinput.input():
        num += 1
        record, sums = line.strip().split()
        # sum_list = [int(x) for x in sums.split(",")]
        sum_list = tuple(int(x) for x in sums.split(",")) * 5
        record = record + "?" + record + "?" + record + "?" + record + "?" + record
        print(f"{num} :: {record, sum_list}")

        possible = possible_arrangements_v2(record, sum_list)
        possible_combination_sum += possible
        print(possible)
        print(possible_combination_sum)
    print(possible_combination_sum)


if __name__=="__main__":
    main()
