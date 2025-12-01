import math

# import aocd

# data = aocd.get_data(year=2025, day=1)

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

example_data_2 = """
R34
R23
L15
L36
R50
R24
R19
R21
R16
L27
R12
R39
R20
L15
L39
L22
R1000
R39
R13
L6
R0
R0
R0
R100
L19
L24
L23
L17
L4
R31
R35
R50
L9
L24
R12
L20
R4
R29
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


# def part2(data):
#     dial = 50
#     password = 0
#     for line in data.strip().splitlines():
#         was = dial
#         s = -1 if line[0] == "L" else 1
#         rot = int(line[1:])
#         change = s * rot
#         dial = dial + change

#         during_rot = abs(math.floor((dial) / 100))
#         edge_case = (dial % 100) == 0 and s < 0
#         after_rot = (dial % 100) == 0
#         password += during_rot + int(edge_case)

#         if after_rot:
#             print(
#                 f"{was=}\t{change=}\t{dial=}\t{int(dial % 100==0)=}\t{during_rot=}\t{edge_case=}"
#             )

#         dial = dial % 100

#     print(password)


if __name__ == "__main__":
    part1(data)
    part2stupid(data)
