import math
import aocd
import dataclasses

INPUT = aocd.get_data(day=19)
wf_text, part_text = INPUT.split("\n\n")


def parse_cmp(text: str):
    return (lambda a, b: a < b) if text == "<" else (lambda a, b: a > b)


def parse_rule(text: str):
    match text.split(":"):
        case (r, wf):
            attr, cmp, num = r[0], parse_cmp(r[1]), int(r[2:])
            return (lambda x: wf if cmp(x[attr], num) else None), attr, num
        case wf:
            return (lambda _: wf[0]), None, None


workflows = {}
for line in wf_text.splitlines():
    name, rule_text = line.split("{")
    rule_text = rule_text[:-1]
    rules = [parse_rule(text) for text in rule_text.split(",")]
    workflows[name] = rules


def parse_dict(text: str):
    return {t[0]: int(t[2:]) for t in text[1:-1].split(",")}


# part 1
ans = 0
parts = [parse_dict(p) for p in part_text.splitlines()]
for part in parts:
    wf_name = "in"
    while True:
        for rule, _, _ in workflows[wf_name]:
            wf_name = rule(part)
            if wf_name is not None:
                break
        if wf_name == "A":
            ans += sum(part.values())
            break
        elif wf_name == "R":
            break

print(ans)


# part 2
@dataclasses.dataclass
class Range:
    min: int = 1
    max: int = 4000

    def copy(self) -> "Range":
        return Range(self.min, self.max)

    def __repr__(self) -> str:
        return f"({self.min},{self.max})"


def copy_xmas(xmas: dict[str, Range]) -> dict[str, Range]:
    return {k: v.copy() for k, v in xmas.items()}


def get_combinations(wf_name: str, xmas: dict[str, Range]) -> int:
    print(wf_name, "\t", xmas)
    if wf_name == "R":
        return 0
    elif wf_name == "A":
        return math.prod(max(0, r.max - r.min + 1) for r in xmas.values())
    else:
        combinations = 0
        for rule, attr, limit in workflows[wf_name]:
            if attr is None:
                next_wf = rule(None)
                combinations += get_combinations(next_wf, xmas)
            elif (next_wf := rule({attr: 4000})) is not None:
                xmas1 = copy_xmas(xmas)
                xmas1[attr].min = limit + 1
                xmas[attr].max = limit
                combinations += get_combinations(next_wf, xmas1)
            elif (next_wf := rule({attr: 1})) is not None:
                xmas1 = copy_xmas(xmas)
                xmas1[attr].max = limit - 1
                xmas[attr].min = limit
                combinations += get_combinations(next_wf, xmas1)
        return combinations


ans2 = get_combinations("in", {l: Range() for l in "xmas"})
print(ans2)
