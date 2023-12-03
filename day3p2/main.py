import fileinput
import collections


def ispart(row_index, start, end, grid):
    for row_pointer in range(max(0, row_index-1), min(len(grid), row_index+2)):
        for col_pointer in range(max(0, start-1), min(len(grid[0]), end+2)):
            e = grid[row_pointer][col_pointer]
            if e.isdigit() or e == ".":
                continue
            return True
    return False

def adjacent_numbers(x, y, pos_numbers, grid):
    potential_adjacents = list(pos_numbers[x-1].items()) + list(pos_numbers[x].items()) + list(pos_numbers[x+1].items())
    nums = []
    for coord, val in potential_adjacents:
        start, end = coord
        if start > y+1 or end < y-1:
            continue
        nums.append(val)
    return nums

if __name__ == '__main__':
    grid = []
    gear_ratio_sum = 0
    for line in fileinput.input():
        grid.append(line.strip())
    pos_numbers = collections.defaultdict(dict) # row -> (y1, y2) tuple
    for x in range(len(grid)):
        min_y = 0
        for y in range(len(grid[x])):
            if y < min_y:
                continue
            curr_num = ""
            offset = 0
            while grid[x][y+offset].isdigit():
                curr_num = curr_num + grid[x][y+offset]
                offset += 1
                if y + offset == len(grid[x]):
                    break
            if offset > 0:
                min_y = y + offset
                pos_numbers[x][(y, y+offset-1)] = int(curr_num)

    import pprint
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            if grid[x][y] != '*':
                continue
            nums = adjacent_numbers(x, y, pos_numbers, grid)
            if len(nums) == 2:
                gear_ratio_sum += nums[0] * nums[1]

    print(gear_ratio_sum)