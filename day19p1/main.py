import dataclasses
import enum
import fileinput
import pprint
from typing import Dict, Optional, Callable

def less_than(a: int, b: int) -> bool:
    return a < b

def greater_than(a: int, b: int) -> bool:
    return a > b

@dataclasses.dataclass
class Part:
    vals: Dict[str, int]

class DestinationType(enum.Enum):
    ACCEPT = "accept"
    REJECT = "reject"
    WORKFLOW = "workflow"
    NEXT_RULE = "next_rule"

@dataclasses.dataclass
class Destination:
    destination_type: DestinationType
    workflow_key: Optional[str] = None


NEXT_RULE = Destination(destination_type=DestinationType.NEXT_RULE, workflow_key=None)


@dataclasses.dataclass
class Rule:
    conditional_key: Optional[str]
    conditional_comp: Optional[int]
    conditional_operator: Optional[Callable[[int, int], bool]]
    destination: Destination

    def evaluate(self, part: Part) -> Destination:
        if self.conditional_key:
            if self.conditional_operator(part.vals[self.conditional_key], self.conditional_comp):
                return self.destination
            else:
                return NEXT_RULE
        return self.destination

def main():
    workflows = {} # workflow_key -> [rules]
    parts = []
    finished_workflows = False

    for line in fileinput.input():
        if line.strip() == "":
            finished_workflows = True
            continue
        if not finished_workflows:
            workflow_key, rule_strings = line.strip().strip("}").split("{")
            rules = []
            for rule_string in rule_strings.split(","):
                conditional_key = None
                conditional_comp = None
                conditional_operator = None
                if ":" in rule_string:
                    conditional_string, destination_string = rule_string.split(":")
                    conditional_key = conditional_string[0]
                    if conditional_string[1] == "<":
                        conditional_operator = less_than
                    elif conditional_string[1] == ">":
                        conditional_operator = greater_than
                    else:
                        raise AssertionError()
                    conditional_comp = int(conditional_string[2:])
                else:
                    destination_string = rule_string

                if destination_string == "A":
                    destination = Destination(destination_type=DestinationType.ACCEPT)
                elif destination_string == "R":
                    destination = Destination(destination_type=DestinationType.REJECT)
                else:
                    destination = Destination(destination_type=DestinationType.WORKFLOW, workflow_key=destination_string)

                rules.append(Rule(
                    conditional_comp=conditional_comp,
                    conditional_key=conditional_key,
                    conditional_operator=conditional_operator,
                    destination=destination
                ))
            workflows[workflow_key] = rules
        else:
            part_vals_dict = {}
            for p in line.strip().strip("{}").split(","):
                k, v = p.split("=")
                part_vals_dict[k] = int(v)
            parts.append(Part(vals=part_vals_dict))

    accepted_ratings_sum = 0

    for p in parts:
        curr_destination = Destination(destination_type=DestinationType.WORKFLOW, workflow_key="in")
        while curr_destination.destination_type not in {DestinationType.ACCEPT, DestinationType.REJECT}:
            assert curr_destination.destination_type is DestinationType.WORKFLOW
            for rule in workflows[curr_destination.workflow_key]:
                curr_destination = rule.evaluate(p)
                if curr_destination.destination_type is not DestinationType.NEXT_RULE:
                    break
        if curr_destination.destination_type is DestinationType.ACCEPT:
            accepted_ratings_sum += sum(p.vals.values())
            continue
        assert curr_destination.destination_type is DestinationType.REJECT

    print(accepted_ratings_sum)


if __name__ == "__main__":
    main()
