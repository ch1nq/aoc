from aocd import get_data
import math

ans = [
    math.prod(
        [
            len(list(filter(lambda d: d > d_min, [(t - i) * i for i in range(t)])))
            for t, d_min in zip(
                *map(
                    lambda l: map(int, l.split(":")[1].replace(" ", " " * a).split()),
                    get_data(day=6).splitlines(),
                )
            )
        ]
    )
    for a in (1, 0)
]
print(ans)
