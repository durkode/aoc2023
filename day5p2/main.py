import collections
import fileinput
from typing import List, Tuple
import pprint

# range(start -> end) - range(start -> end)
#                     \-range(start -> end)
# Build up the tree traversing forwards. Then take the leafs, pick the lowest end of the tree and translate backwards

table = collections.defaultdict(list)  # depth -> [(destination start, source start, range)]


def translate_source(seed_start, seed_nums, depth, start_table_pos) -> List[Tuple[int, int]]:  # -> List[(start, nums)]
    if depth >= len(table):
        return [(seed_start, seed_nums)]

    if start_table_pos < len(table[depth]):
        # print(f"   depth {depth}")
        for row_pos in range(start_table_pos, len(table[depth])):
            # print(f"        trans row {row_pos}: {seed_start} {seed_nums} -> {table[depth][row_pos]}")
            dest_start, source_start, trans_length = table[depth][row_pos]
            # case 1: no overlap in translation, continue
            if seed_start >= source_start + trans_length or seed_start + seed_nums <= source_start:
                # print("            skipping ...")
                continue
            # case 2: there is something that needs translating
            lower_side = []
            matched_range = []
            upper_side = []
            # lower side
            if seed_start < source_start:
                lower_side = translate_source(seed_start, source_start - seed_start, depth, row_pos+1)
            # matching range
            match_start = max(seed_start, source_start)
            match_end = min(source_start + trans_length - 1, seed_start + seed_nums - 1)
            match_length = match_end - match_start + 1
            matched_range = translate_source(dest_start + match_start - source_start, match_length, depth + 1, 0)

            # upper side
            if seed_start + seed_nums > source_start + trans_length:
                upper_side = translate_source(source_start + trans_length, (seed_start + seed_nums) - (source_start +
                                                                                                       trans_length),
                                              depth, row_pos+1)
            combined = lower_side + matched_range + upper_side
            # print(f"({seed_start}, {seed_nums}, {depth}, {row_pos}) -> {combined}")
            # print(f"row: {table[depth][row_pos]}")
            return combined

    return translate_source(seed_start, seed_nums, depth+1, 0)


def main():
    seeds = []
    depth = -1
    for line in fileinput.input():
        if not seeds:
            seed_ranges = [int(x) for x in line.split(": ")[1].split()]
            for x in range(0, len(seed_ranges), 2):
                seeds.append((seed_ranges[x], seed_ranges[x+1]))
            continue
        if not line.strip():
            continue
        if ":" in line:
            depth += 1
            continue
        dest_start, source_start, range_length = [int(x) for x in line.split()]
        table[depth].append((dest_start, source_start, range_length))

    lowest_seed = None

    # print(f"seed count: {len(seeds)}")
    for s in seeds:
        # pprint.pprint(s)
        seed_start, seed_nums = s
        translated_ranges = translate_source(seed_start, seed_nums, 0, 0)
        # pprint.pprint(translated_ranges)
        min_location = min(x for x, y in translated_ranges)
        if lowest_seed is None:
            lowest_seed = min_location
        else:
            lowest_seed = min(min_location, lowest_seed)


    # pprint.pprint(table)
    # pprint.pprint(seeds)
    print(lowest_seed)


if __name__ == '__main__':
    main()
