import fileinput
import math

cards_won_cache = {}
cards = {} # number -> (winning_numbers, your_numbers)


def game_value(winning_numbers, your_numbers):
    matched = 0
    for n in winning_numbers:
        if n in your_numbers:
            matched += 1
    return matched


def cards_won(card_num):
    if card_num in cards_won_cache:
        return cards_won_cache[card_num]
    if card_num not in cards:
        return 0
    y, z = cards[card_num]
    won = game_value(y, z)
    if won > 0:
        for x in range(card_num + 1, card_num + won + 1):
            won += cards_won(x)
    cards_won_cache[card_num] = won
    return won


if __name__ == '__main__':
    card_count = 0
    cards = {} # number -> (winning_numbers, your_numbers)
    for line in fileinput.input():
        card_count += 1
        _, line = line.strip().split(": ")
        winning, yours = line.split(" | ")
        cards[card_count] = (winning.split(), yours.split())

    for card_num in cards:
        card_count += cards_won(card_num)
    print(card_count)
