import fileinput

def get_sample(samples: str):
    ret = {}
    for s in samples.split(", "):
        digit, colour = s.split(" ")
        ret[colour] = int(digit)
    return ret


if __name__ == '__main__':
    possible_id_sum = 0
    max_allowed = {
        'red': 12,
        'green': 13,
        'blue': 14
    }
    for line in fileinput.input():
        line = line.strip()
        game, samples = line.split(": ")
        game_number = int(game.lstrip("Game "))
        sample_list = [get_sample(x) for x in samples.split("; ")]
        max_exceeded = False
        for s in sample_list:
            for colour, count in s.items():
                if count > max_allowed[colour]:
                    max_exceeded = True
                    break
            if max_exceeded:
                break
        if max_exceeded:
            continue
        possible_id_sum += game_number
    print(possible_id_sum)

