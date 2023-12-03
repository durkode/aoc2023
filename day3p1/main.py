import fileinput
import collections


def ispart(row_index, start, end, grid):
    for row_pointer in range(max(0, row_index - 1), min(len(grid), row_index + 2)):
        for col_pointer in range(max(0, start - 1), min(len(grid[0]), end + 2)):
            e = grid[row_pointer][col_pointer]
            if e.isdigit() or e == ".":
                continue
            return True
    return False


if __name__ == '__main__':
    grid = []
    part_sum = 0
    for line in fileinput.input():
        grid.append(line.strip())
    pos_numbers = collections.defaultdict(dict)  # row -> (y1, y2) tuple
    for x in range(len(grid)):
        min_y = 0
        for y in range(len(grid[x])):
            if y < min_y:
                continue
            curr_num = ""
            offset = 0
            while grid[x][y + offset].isdigit():
                curr_num = curr_num + grid[x][y + offset]
                offset += 1
                if y + offset == len(grid[x]):
                    break
            if offset > 0:
                min_y = y + offset
                pos_numbers[x][(y, y + offset - 1)] = int(curr_num)
    import pprint

    pprint.pprint(grid)
    pprint.pprint(pos_numbers)

    for x, row_nums in pos_numbers.items():
        for coords, num in row_nums.items():
            start, end = coords
            if ispart(x, start, end, grid):
                part_sum += num

    print(part_sum)
