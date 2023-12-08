import collections
import fileinput
import pprint

import math

def main():
    sequence_string = ""
    mapping = {}  # code -> {'L': , 'R'}

    for line in fileinput.input():
        if sequence_string == "":
            sequence_string = line.strip()
            continue
        if not line.strip():
            continue
        start, coords = line.strip().split(" = ")
        left, right = coords.replace("(", "").replace(")", "").split(", ")
        mapping[start] = {"L": left, "R": right}

    start_nodes = [key for key in mapping if key[-1] == "A"]
    step_count_list = []
    for start_node in start_nodes:
        print(f"Start Node: {start_node}")
        curr_location = start_node
        step_count = 0
        while True:
            next_move = sequence_string[(step_count % len(sequence_string))]
            next_location = mapping[curr_location][next_move]
            curr_location = next_location
            step_count += 1
            # Hack: We tested all paths end at the start of the cycle, so no need to do module, just step count.
            if curr_location[-1] == "Z":
                step_count_list.append(step_count)
                break

    product = math.lcm(*step_count_list)
    print(product)

if __name__=="__main__":
    main()
