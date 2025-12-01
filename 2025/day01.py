data = open("data/day01.txt").read().strip()
example_data = """
L68
L30
R48
L5
R60
L55
L1
L99
R14
L82
"""


def parse_line(line: str) -> tuple[int, int]:
    sign = -1 if line[0] == "L" else 1
    rot = int(line[1:])
    return sign, rot


def part1(data):
    dial = 50
    password = 0
    for line in data.strip().splitlines():
        sign, rot = parse_line(line)
        dial = (dial + sign * rot) % 100
        password += dial == 0
    print(password)


def part2stupid(data):
    dial = 50
    password = 0
    for line in data.strip().splitlines():
        sign, rot = parse_line(line)
        for _ in range(rot):
            dial = dial + sign
            dial = dial % 100
            password += dial == 0
    print(password)


if __name__ == "__main__":
    part1(data)
    part2stupid(data)
