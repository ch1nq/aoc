import math
from collections import defaultdict
from aocd import get_data

points = 0
card_instances = defaultdict(lambda: 0)
for line in get_data().splitlines():
    (card, content) = line.split(":", maxsplit=1)
    # part1
    (win_nums, my_nums) = content.split("|", maxsplit=1)
    win_nums = {int(w) for w in win_nums.split()}
    my_nums = {int(n) for n in my_nums.split()}
    matches = win_nums & my_nums
    points += math.floor(2 ** (len(matches) - 1))

    # part 2
    (_, card_id) = card.split(maxsplit=1)
    card_id = int(card_id)
    card_instances[card_id] += 1
    next_card_id = card_id + 1
    for id in range(next_card_id, next_card_id + len(matches)):
        card_instances[id] += card_instances[card_id]

print("ans 1:", points)
print("ans 2:", sum(card_instances.values()))
