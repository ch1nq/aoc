from aocd import get_data
import itertools


# expand universe
universe = get_data().splitlines()
empty_rows = {i for i, row in enumerate(universe) if all(c == "." for c in row)}
empty_cols = {
    i for i in range(len(universe[0])) if all(row[i] == "." for row in universe)
}

galaxies = set()
for y, row in enumerate(universe):
    for x, c in enumerate(row):
        if c == "#":
            galaxies.add((x, y))

for expansion_factor in (2, 1000000):
    ans = 0
    for (ax, ay), (bx, by) in itertools.combinations(galaxies, 2):
        extra_x = empty_cols & {x for x in range(min(ax, bx), max(ax, bx))}
        extra_y = empty_rows & {y for y in range(min(ay, by), max(ay, by))}
        ans += (
            abs(ax - bx)
            + abs(ay - by)
            + len(extra_x) * (expansion_factor - 1)
            + len(extra_y) * (expansion_factor - 1)
        )
    print(ans)
