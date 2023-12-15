import fileinput
import dataclasses
from typing import Optional

@dataclasses.dataclass
class Lens:
    label: str
    number: Optional[int]


class Operation:
    lens: Lens
    operation: str
    s: str

    def __init__(self, s):
        self.s = s
        if "=" in s:
            self.operation = "="
            label, number = s.split("=")
            self.lens = Lens(label=label, number=int(number))
        elif "-" in s:
            self.operation = "-"
            self.lens = Lens(label=s.split("-")[0], number=None)
        else:
            raise ValueError()


    def get_hash(self):
        return get_hash(self.lens.label, 0)


def get_hash(val: str, curr: int):
    for c in val:
        curr = ((curr + ord(c)) * 17) % 256
    return curr

def main():
    boxes = {} # box number -> [Lens]
    for line in fileinput.input():
        prev_op = None
        for o in [Operation(o) for o in line.strip().split(",")]:
            # if prev_op:
            #     print(f"After {prev_op}")
                # import pprint
                # pprint.pprint(boxes)
            prev_op = o.s

            box = o.get_hash()
            if box not in boxes:
                if o.operation == "=":
                    boxes[box] = [o.lens]
                continue
            lens_found = False
            for lens_slot, lens in enumerate(boxes[box]):
                if lens.label != o.lens.label:
                    continue
                lens_found = True
                if o.operation == "=":
                    boxes[box][lens_slot] = o.lens
                if o.operation == "-":
                    del boxes[box][lens_slot]
                break
            if not lens_found:
                if o.operation == "=":
                    boxes[box].append(o.lens)
    # print()
    # print(boxes)

    focusing_power = 0
    for box, lenses in boxes.items():
        for lens_slot, lens in enumerate(lenses):
            focusing_power += (1 + box) * (1 + lens_slot) * lens.number
    print(focusing_power)



if __name__=="__main__":
    main()