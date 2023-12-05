import collections
import fileinput
import pprint

if __name__ == '__main__':
    seeds = []
    table = collections.defaultdict(list) # depth -> [(destination start, source start, range)]
    depth = -1
    for line in fileinput.input():
        if not seeds:
            seeds = [int(x) for x in line.split(": ")[1].split()]
            continue
        if not line.strip():
            continue
        if ":" in line:
            depth += 1
            continue
        dest_start, source_start, range_length = [int(x) for x in line.split()]
        table[depth].append((dest_start, source_start, range_length))

    lowest_seed = None

    for s in seeds:
        # print(f"starting with {s}")
        for d in range(len(table)):
            for trans in table[d]:
                dest_start, source_start, range_length = trans
                if s >= source_start and s < source_start + range_length:
                    s = (s - source_start) + dest_start
                    # print(f"source start {source_start}, dest start {dest_start}, range {range_length}")
                    # print(f" --> {s}")
                    break
        # print(f"Ending with {s}")
        if lowest_seed is None:
            lowest_seed = s
        else:
            lowest_seed = min(s, lowest_seed)

    print(lowest_seed)
