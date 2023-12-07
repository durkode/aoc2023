import fileinput
import functools
import enum
import collections


class HandType(enum.Enum):
    FIVE_OF_A_KIND = 7
    FOUR_OF_A_KIND = 6
    FULL_HOUSE = 5
    THREE_OF_A_KIND = 4
    TWO_PAIR = 3
    ONE_PAIR = 2
    HIGH_CARD = 1


card_rank = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 1,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
}


def hand_type(hand) -> HandType:
    c = collections.Counter()
    c.update(hand)
    counts = dict(c.items()).values()
    if 5 in counts:
        return HandType.FIVE_OF_A_KIND
    if 4 in counts:
        return HandType.FOUR_OF_A_KIND
    if 3 in counts:
        if 2 in counts:
            return HandType.FULL_HOUSE
        return HandType.THREE_OF_A_KIND
    if 2 in counts:
        if len(counts) == 3:
            return HandType.TWO_PAIR
        return HandType.ONE_PAIR
    return HandType.HIGH_CARD


def hand_type_joker(hand) -> HandType:
    joker_index = hand.find('J')
    if joker_index < 0:
        return hand_type(hand)
    max_hand = HandType.HIGH_CARD
    for card in card_rank:
        if card == "J":
            continue
        sub_hand = hand_type_joker(hand.replace("J", card, 1))
        if sub_hand.value > max_hand.value:
            max_hand = sub_hand
    return max_hand


def hand_cmp(a, b):
    hand_type_difference = hand_type_joker(a).value - hand_type_joker(b).value
    if hand_type_difference != 0:
        return hand_type_difference
    else:
        for a_card, b_card in zip(a, b):
            card_difference = card_rank[a_card] - card_rank[b_card]
            if card_difference != 0:
                return card_difference
    return 0


def main():
    hands = {}
    for line in fileinput.input():
        hand, bid = line.strip().split()
        hands[hand] = int(bid)
    ordered_hands = sorted(hands.keys(), key=functools.cmp_to_key(hand_cmp))
    winnings = 0
    for x, h in enumerate(ordered_hands):
        winnings += (x+1) * hands[h]
    print(winnings)


if __name__=="__main__":
    main()
