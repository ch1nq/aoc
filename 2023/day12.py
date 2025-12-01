import tqdm
from aocd import get_data

INPUT = get_data(day=12)


def matches(candidate: str, pattern: str) -> bool:
    return all(c == p or p == "?" for c, p in zip(candidate, pattern))


def hash_key(groups, pattern) -> str:
    return pattern + " " + ",".join(str(x) for x in groups)


cache = {}


def num_matches(*groups: int, pattern: str):
    if len(groups) == 0:
        return 1 if all(map(lambda x: x == "." or x == "?", pattern)) else 0
    elif (num := cache.get(hash_key(groups, pattern), None)) is not None:
        return num
    else:
        num = 0
        for i in range(len(pattern)):
            candidate = "." * i + "#" * groups[0]
            candidate += "." * int(len(candidate) < len(pattern))
            if matches(candidate, pattern) and len(candidate) <= len(pattern):
                num += num_matches(*groups[1:], pattern=pattern[len(candidate) :])
        cache[hash_key(groups, pattern)] = num
        return num


def process_line(line: str, copies: int = 1) -> int:
    pattern, groups_str = line.split()
    groups = [int(x) for x in groups_str.split(",")] * copies
    pattern = "?".join([pattern] * copies)
    return num_matches(*groups, pattern=pattern)


ans = sum(process_line(line, 5) for line in tqdm.tqdm(INPUT.splitlines()))
print(ans)
