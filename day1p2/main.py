import fileinput

digits = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9
}


if __name__ == '__main__':
    numbers = []
    for line in fileinput.input():
        first = [(line.find(digit), val) for digit, val in digits.items()]
        first = [(p, v) for p, v in first if p > -1]
        first.sort(key=lambda x: x[0])
        first_digit = first[0][1]

        last = [(line.rfind(digit), val) for digit, val in digits.items()]
        last = [(p, v) for p, v in last if p > -1]
        last.sort(key=lambda x: x[0], reverse=True)
        last_digit = last[0][1]

        numbers.append(int(str(first_digit) + str(last_digit)))
    print(sum(numbers))

