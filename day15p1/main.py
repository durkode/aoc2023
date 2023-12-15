import fileinput

def get_hash(val: str, curr: int):
    for c in val:
        curr = ((curr + ord(c)) * 17) % 256
    return curr

def main():
    inputs = []
    for line in fileinput.input():
        inputs += line.strip().split(",")

    print(inputs)
    print(sum(get_hash(i, 0) for i in inputs))


if __name__=="__main__":
    main()