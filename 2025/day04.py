import numpy as np

example = """
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
""".strip()


def part1(data: str):
    lines = data.splitlines()

    rolls = []
    for line in lines:
        row = []
        for c in line:
            row.append(int(c == "@"))
        rolls.append(row)
    rolls = np.array(rolls)
    print(rolls)

    viz = np.zeros_like(rolls)
    for i, row in enumerate(rolls):
        i_min = max(i - 1, 0)
        i_max = min(i + 1, len(rolls)) + 1
        for j, _ in enumerate(row):
            j_min = max(j - 1, 0)
            j_max = min(j + 1, len(row)) + 1
            print(rolls[i_min:i_max, j_min:j_max])
            if rolls[i, j]:
                # +1 for the cell in the middle
                viz[i, j] = rolls[i_min:i_max, j_min:j_max].sum() < 4 + 1

    print(viz)
    print(np.sum(viz))


def part2(data: str):
    lines = data.splitlines()

    rolls = []
    for line in lines:
        row = []
        for c in line:
            row.append(int(c == "@"))
        rolls.append(row)
    rolls = np.array(rolls)
    print(rolls)

    total = 0
    while True:
        to_remove = np.zeros_like(rolls)
        for i, row in enumerate(rolls):
            i_min = max(i - 1, 0)
            i_max = min(i + 1, len(rolls)) + 1
            for j, _ in enumerate(row):
                j_min = max(j - 1, 0)
                j_max = min(j + 1, len(row)) + 1
                if rolls[i, j]:
                    # +1 for the cell in the middle
                    to_remove[i, j] = rolls[i_min:i_max, j_min:j_max].sum() < 4 + 1
        removed = np.sum(to_remove)
        if not removed:
            break
        total += removed
        rolls -= to_remove

    print(total)


if __name__ == "__main__":
    data = open("data/day04.txt").read().strip()
    part1(data)
    part2(data)
