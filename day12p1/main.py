import fileinput
import sys

def is_valid_arrangement(record, damage_counts):
    groupings = [x for x in record.split(".") if x]
    if len(groupings) != len(damage_counts):
        return False
    for group, length in zip(groupings, damage_counts):
        if len(group) != length:
            return False
    return True

def possible_arrangements(record, damage_counts):
    if "?" not in record:
        return 1 if is_valid_arrangement(record, damage_counts) else 0

    possible = 0
    for p in {".", "#"}:
        possible += possible_arrangements(record.replace("?", p, 1), damage_counts)
    return possible


def main():
    possible_combination_sum = 0
    for line in fileinput.input():
        print(f"Solving {line}")
        record, sums = line.strip().split()
        sum_list = [int(x) for x in sums.split(",")]
        possible_combination_sum += possible_arrangements(record, sum_list)
    print(possible_combination_sum)


if __name__=="__main__":
    main()
