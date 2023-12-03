import fileinput


if __name__ == '__main__':
    numbers = []
    for line in fileinput.input():
        x = [d for d in line if d.isdigit()]
        numbers.append(int(x[0] + x[-1]))
    print(sum(numbers))

