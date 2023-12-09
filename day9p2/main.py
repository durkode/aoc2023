import fileinput
from typing import List

def next_val(input: List[int]) -> int:
    if all(x == 0 for x in input):
        return 0

    diff_list = [input[x] - input[x-1] for x in range(1, len(input))]
    next_diff_list = next_val(diff_list)
    return input[-1] + next_diff_list

def prev_val(input: List[int]) -> int:
    if all(x == 0 for x in input):
        return 0

    diff_list = [input[x] - input[x-1] for x in range(1, len(input))]
    prev_diff_list = prev_val(diff_list)
    return input[0] - prev_diff_list

def main():
    inputs = []
    for line in fileinput.input():
        inputs.append([int(x) for x in line.strip().split()])
    print(sum(prev_val(i) for i in inputs))

if __name__=="__main__":
    main()