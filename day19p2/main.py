import dataclasses
import enum
import fileinput
import math
import pprint
from typing import Dict, Optional, Callable, Tuple, List

@dataclasses.dataclass
class Part:
    vals: Dict[str, int]


class DestinationType(enum.Enum):
    ACCEPT = "accept"
    REJECT = "reject"
    WORKFLOW = "workflow"

@dataclasses.dataclass
class Destination:
    destination_type: DestinationType
    workflow_key: Optional[str] = None
    rule_index: Optional[int] = None


@dataclasses.dataclass
class Rule:
    conditional_key: Optional[str]
    conditional_comp: Optional[int]
    conditional_operator: Optional[str]
    destination: Destination


def get_accepted_combos(workflows: Dict[str, List[Rule]], ranges: Dict[str, Tuple[int, int]], destination: Destination):
    if destination.destination_type is DestinationType.ACCEPT:
        return math.prod(x[1] - x[0] + 1 for x in ranges.values())
    if destination.destination_type is DestinationType.REJECT:
        return 0
    assert destination.destination_type is DestinationType.WORKFLOW
    rule = workflows[destination.workflow_key][destination.rule_index]
    if not rule.conditional_operator:
        return get_accepted_combos(workflows, ranges, rule.destination)
    else:
        success_destination = rule.destination
        failure_destination = Destination(destination_type=DestinationType.WORKFLOW,
                                          workflow_key=destination.workflow_key, rule_index=destination.rule_index+1)
        affected_lower, affected_upper = ranges[rule.conditional_key]
        if not affected_lower <= rule.conditional_comp <= affected_upper:
            # Rule has no affect, continue
            return get_accepted_combos(workflows, ranges, failure_destination)
        success_ranges = ranges.copy()
        failure_ranges = ranges.copy()
        if rule.conditional_operator == "<":
            success_ranges[rule.conditional_key] = affected_lower, rule.conditional_comp - 1
            failure_ranges[rule.conditional_key] = rule.conditional_comp, affected_upper
        elif rule.conditional_operator == ">":
            success_ranges[rule.conditional_key] = rule.conditional_comp + 1, affected_upper
            failure_ranges[rule.conditional_key] = affected_lower, rule.conditional_comp
        else:
            raise AssertionError

        if any(upper < lower for lower, upper in success_ranges.values()):
            success_combos = 0
        else:
            success_combos = get_accepted_combos(workflows, success_ranges, success_destination)

        if any(upper < lower for lower, upper in failure_ranges.values()):
            failure_combos = 0
        else:
            failure_combos = get_accepted_combos(workflows, failure_ranges, failure_destination)

        # print("==================")
        # pprint.pprint(ranges)
        # pprint.pprint(success_ranges)
        # pprint.pprint(failure_ranges)
        # print("<<<<<<<<<<<<<<<<<")

        return success_combos + failure_combos




def main():
    workflows = {} # workflow_key -> [rules]

    for line in fileinput.input():
        if line.strip() == "":
            break
        workflow_key, rule_strings = line.strip().strip("}").split("{")
        rules = []
        for rule_string in rule_strings.split(","):
            conditional_key = None
            conditional_comp = None
            conditional_operator = None
            if ":" in rule_string:
                conditional_string, destination_string = rule_string.split(":")
                conditional_key = conditional_string[0]
                conditional_operator = conditional_string[1]
                conditional_comp = int(conditional_string[2:])
            else:
                destination_string = rule_string

            if destination_string == "A":
                destination = Destination(destination_type=DestinationType.ACCEPT)
            elif destination_string == "R":
                destination = Destination(destination_type=DestinationType.REJECT)
            else:
                destination = Destination(destination_type=DestinationType.WORKFLOW, workflow_key=destination_string,
                                          rule_index=0)

            rules.append(Rule(
                conditional_comp=conditional_comp,
                conditional_key=conditional_key,
                conditional_operator=conditional_operator,
                destination=destination
            ))
        workflows[workflow_key] = rules

    starting_ranges = {
        "x": (1, 4000),  # inclusive ranges
        "m": (1, 4000),
        "a": (1, 4000),
        "s": (1, 4000),
    }
    print(get_accepted_combos(workflows, starting_ranges, Destination(destination_type=DestinationType.WORKFLOW,
                                                                      workflow_key="in", rule_index=0)))


if __name__ == "__main__":
    main()
