import fileinput
import math

def get_sample(samples: str):
    ret = {}
    for s in samples.split(", "):
        digit, colour = s.split(" ")
        ret[colour] = int(digit)
    return ret


if __name__ == '__main__':
    power_sum = 0
    for line in fileinput.input():
        line = line.strip()
        game, samples = line.split(": ")
        game_number = int(game.lstrip("Game "))
        sample_list = [get_sample(x) for x in samples.split("; ")]
        max_of_samples = {
            "red": 0,
            "green": 0,
            "blue": 0
        }

        for s in sample_list:
            for colour, count in s.items():
                max_of_samples[colour] = max(max_of_samples[colour], count)
        power_sum += math.prod(max_of_samples.values())
    print(power_sum)
