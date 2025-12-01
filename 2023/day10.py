from aocd import get_data
from dataclasses import dataclass


@dataclass(frozen=True)
class Pos:
    x: int
    y: int

    def __add__(self, other):
        return Pos(self.x + other.x, self.y + other.y)

    def __mul__(self, a):
        return Pos(self.x * a, self.y * a)


@dataclass
class Cell:
    pos: Pos
    connections: tuple[Pos, Pos]
    in_main_loop: bool = False
    enclosed: bool | None = None

    def __hash__(self) -> int:
        return self.pos.__hash__()


N, E, W, S = Pos(0, -1), Pos(1, 0), Pos(-1, 0), Pos(0, 1)
DIRS = (N, E, W, S)
pipes = {
    "L": (N, E),
    "J": (N, W),
    "|": (N, S),
    "F": (S, E),
    "7": (S, W),
    "-": (E, W),
    ".": None,
    "S": None,
}

# dir_to_outside = {N: W, S: E, W: S, E: N}
# dir_to_inside = {N: E, S: W, W: N, E: S}
dir_to_outside = {N: E, S: W, W: N, E: S}
dir_to_inside = {N: W, S: E, W: S, E: N}

grid = [
    [Cell(Pos(x, y), pipes[c]) for x, c in enumerate(line)]
    for y, line in enumerate(get_data().splitlines())
]
WIDTH, HEIGHT = len(grid[0]), len(grid)


def get_cell(pos: Pos) -> Cell | None:
    if pos.x in range(WIDTH) and pos.y in range(HEIGHT):
        return grid[pos.y][pos.x]
    else:
        return None


for y, line in enumerate(get_data().splitlines()):
    for x, c in enumerate(line):
        if c == "S":
            start = Pos(x, y)
            get_cell(start).connections = tuple(
                dir
                for dir in DIRS
                if (c := get_cell(start + dir)) is not None
                and (dir * -1) in (c.connections or {})
            )
            break


def update_enclosed(pos: Pos, dir: Pos):
    cell_o = get_cell(pos + dir_to_outside[dir])
    cell_i = get_cell(pos + dir_to_inside[dir])
    if cell_o is not None and cell_o.enclosed is None and not cell_o.in_main_loop:
        cell_o.enclosed = False
    if cell_i is not None and cell_i.enclosed is None and not cell_i.in_main_loop:
        cell_i.enclosed = True


distance = 0
pos = start
while True:
    distance += 1
    cell = get_cell(pos)
    cell.in_main_loop = True
    d1, d2 = cell.connections[0], cell.connections[1]
    p1, p2 = pos + d1, pos + d2
    if not (c := get_cell(p1)).in_main_loop:
        pos = p1
    elif not (c := get_cell(p2)).in_main_loop:
        pos = p2
    else:
        break

ans1 = distance // 2
print(ans1)


pos = start
while True:
    cell = get_cell(pos)
    cell.enclosed = False
    d1, d2 = cell.connections[0], cell.connections[1]
    p1, p2 = pos + d1, pos + d2
    if (c := get_cell(p1)).enclosed is None:
        update_enclosed(pos, d1)
        update_enclosed(p1, d1)
        pos = p1
    elif (c := get_cell(p2)).enclosed is None:
        update_enclosed(pos, d2)
        update_enclosed(p2, d2)
        pos = p2
    else:
        break

unchecked = {c for line in grid for c in line if c.enclosed is False}
while unchecked:
    cell = unchecked.pop()
    if cell.enclosed is None:
        cell.enclosed = False
    adjecent = {}
    for dir in DIRS:
        new_pos = cell.pos + dir
        if (c := get_cell(new_pos)) is not None and c.enclosed is None:
            unchecked.add(c)


ans2 = 0
for row in grid:
    for cell in row:
        if cell.enclosed is not False:
            ans2 += 1

print(ans2)
