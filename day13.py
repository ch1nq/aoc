import numpy as np
from aocd import get_data

INPUT = get_data()

for part in (0, 1):
    ans = 0
    for matrix_str in INPUT.split("\n\n"):
        lines = matrix_str.splitlines()
        W, H = len(lines[0]), len(lines)
        matrix = np.zeros((H, W))
        for i, line in enumerate(lines):
            for j, c in enumerate(line):
                if c == "#":
                    matrix[i, j] = 1

        for m, factor in [(matrix, 1), (matrix.T, 100)]:
            for col in range(1, m.shape[1]):
                w = min(col, m.shape[1] - col)
                l, r = m[:, col - w : col], m[:, col : col + w]
                r = np.fliplr(r)
                if np.sum(np.abs(l - r)) == part:
                    ans += col * factor
    print(ans)
