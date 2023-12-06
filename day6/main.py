import fileinput
import math


winning_combo_cache = {}


def winning_combos(time, record, speed) -> int:
    if (time, record, speed) in winning_combo_cache:
        return winning_combo_cache[(time, record, speed)]
    if time <= 0:
        winning_combo_cache[(time, record, speed)] = 0
        return 0
    winning = 1 if speed * time > record else 0
    combos = winning + winning_combos(time-1, record, speed+1)
    winning_combo_cache[(time, record, speed)] = combos
    return combos


def winning_combos_iterative(time, record, speed) -> int:
    winning_combos = 0
    while time > 0:
        winning_combos += 1 if speed * time > record else 0
        time -= 1
        speed += 1
    return winning_combos

def main():
    races = []
    with fileinput.input() as f:
        times = f.readline().strip().lstrip("Time:").split()
        records = f.readline().strip().lstrip("Distance: ").split()
        races = list(zip(times, records))
    print(races)

    winning_nums = [winning_combos_iterative(int(time), int(record), 0) for time, record in races]
    print(math.prod(winning_nums))


if __name__ == "__main__":
    main()
