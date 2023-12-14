from aocd import get_data
import numpy as np

np.set_printoptions(threshold=99999999)

lines = get_data().splitlines()
W, H = len(lines[0]), len(lines)
matrix = np.zeros((2, H, W), int)
for i, line in enumerate(lines):
    for j, c in enumerate(line):
        if c == "O":
            matrix[0, i, j] = 1
        if c == "#":
            matrix[1, i, j] = 1


def tilt(matrix):
    for col in range(W):
        rocks = matrix[1, :, col]
        boulders = matrix[0, :, col]
        for section in np.split(boulders, np.argwhere(rocks == 1).reshape(-1) + 1):
            section[::-1].sort()


def cycle(matrix):
    for _ in range(4):
        tilt(matrix)
        matrix = np.rot90(matrix, k=-1, axes=(1, 2))


m1 = matrix.copy()
m2 = matrix.copy()


def hash(matrix: np.ndarray):
    return np.array2string(matrix[0])


cache = {}
n_iter = 1_000_000_000
i = 0
while i < n_iter:
    if (j := cache.get(hash(m2), None)) is not None:  # cycle detected
        diff = i - j
        remaining = n_iter - i
        print(f"cycle detected {i=}, {j=}, {remaining=}, {diff=}")
        i += (remaining // diff) * diff  # skip ahead
        print("skipped to", i)
        cache = {}
    else:
        cache[hash(m2)] = i
        cycle(m2)
        i += 1

tilt(m1)
for m in (m1, m2):
    ans = 0
    for i, row in enumerate(matrix[0, ::-1, :]):
        ans += row.sum() * (i + 1)
    print("ans", ans)
