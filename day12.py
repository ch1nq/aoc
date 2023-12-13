import tqdm
from aocd import get_data

INPUT = get_data(day=12)

# INPUT = """???.### 1,1,3
# .??..??...?##. 1,1,3
# ?#?#?#?#?#?#?#? 1,3,1,6
# ????.#...#... 4,1,1
# ????.######..#####. 1,6,5
# ?###???????? 3,2,1"""

# INPUT = "?###???????? 3,2,1"


def matches(candidate: str, pattern: str) -> bool:
    return all(c == p or p == "?" for c, p in zip(candidate, pattern))


def hash_key(groups, pattern) -> str:
    return pattern + " " + ",".join(str(x) for x in groups)


cache = {}


def num_matches(groups: list[int], pattern: str):
    if len(groups) == 0:
        return 1
    elif (num := cache.get(hash_key(groups, pattern), None)) is not None:
        return num
    else:
        num = 0
        for i in range(len(pattern)):
            candidate = "." * i + "#" * groups[0]
            candidate += "." * (len(candidate) < len(pattern))
            if matches(candidate, pattern) and len(candidate) <= len(pattern):
                num += num_matches(groups[1:], pattern[len(candidate) :])
        cache[hash_key(groups, pattern)] = num
        return num


def process_line(line: str, copies: int = 1) -> int:
    pattern, groups_str = line.split()
    groups = [int(x) for x in groups_str.split(",")] * copies
    pattern = "?".join([pattern] * copies)
    n = num_matches(groups, pattern)
    return n


ans = sum(process_line(line, 5) for line in tqdm.tqdm(INPUT.splitlines()))
print(ans)
