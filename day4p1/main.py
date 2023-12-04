import fileinput
import math

def game_value(winning_numbers, your_numbers):
    matched = 0
    for n in winning_numbers:
        if n in your_numbers:
            matched += 1
    if matched == 0:
        return 0
    value = int(math.pow(2, matched-1))
    print(value)
    return value


if __name__ == '__main__':
    match_sum = 0
    for line in fileinput.input():
        _, line = line.strip().split(": ")
        winning, yours = line.split(" | ")
        match_sum += game_value(winning.split(), yours.split())
    print(match_sum)
