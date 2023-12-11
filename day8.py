import aocd
import math


def get_data():
    return aocd.get_data(day=8)


instructions, node_text = get_data().split("\n\n")
nodes = {line[:3]: (line[7:10], line[12:15]) for line in node_text.splitlines()}

i = 0
curr_id = "AAA"
while curr_id != "ZZZ":
    curr_id = nodes[curr_id][int(instructions[i % len(instructions)] == "R")]
    i += 1

print("ans 1: ", i)

# brüt force
# i = 0
# curr_ids = {id for id in nodes.keys() if id[-1] == "A"}
# while any(id[-1] != "Z" for id in curr_ids):
#     instruction = instructions[i % len(instructions)]
#     curr_ids = {nodes[id][int(instruction == "R")] for id in curr_ids}
#     i += 1
#     if i % 100000 == 0:
#         print(instruction, curr_ids, i)

# find where cycles line up
cycles = set()
for id in {id for id in nodes.keys() if id[-1] == "A"}:
    cycle_len = 0
    while id[-1] != "Z":
        id = nodes[id][int(instructions[cycle_len % len(instructions)] == "R")]
        cycle_len += 1
    cycles.add(cycle_len)


print("ans 2: ", math.lcm(*cycles))
