import math
import aocd
import dataclasses
from collections import defaultdict
from enum import IntEnum

INPUT = aocd.get_data(day=20)


ModId = str


class Pulse(IntEnum):
    LOW = 0
    HIGH = 1


@dataclasses.dataclass
class Module:
    id: ModId
    connections_in: set[ModId] = dataclasses.field(default_factory=set)
    connections_out: set[ModId] = dataclasses.field(default_factory=set)

    def on_receive(self, from_id: ModId, pulse: Pulse) -> Pulse | None:
        ...


@dataclasses.dataclass
class FlipFlop(Module):
    is_on: bool = False

    def on_receive(self, from_id: ModId, pulse: Pulse) -> Pulse | None:
        if pulse == Pulse.LOW:
            self.is_on = not self.is_on
            return Pulse.HIGH if self.is_on else Pulse.LOW
        else:
            return None


@dataclasses.dataclass
class Conjunction(Module):
    memory: defaultdict[ModId, Pulse] = dataclasses.field(default_factory=lambda: defaultdict(lambda: Pulse.LOW))

    def on_receive(self, from_id: ModId, pulse: Pulse) -> Pulse | None:
        self.memory[from_id] = pulse

        if all(self.memory[c] == Pulse.HIGH for c in self.connections_in):
            return Pulse.LOW
        else:
            return Pulse.HIGH


class Broadcaster(Module):
    def on_receive(self, from_id: ModId, pulse: Pulse) -> Pulse | None:
        return pulse


def parse_modules(input) -> dict[ModId, Module]:
    letter_to_module = {"b": Broadcaster, "%": FlipFlop, "&": Conjunction}
    modules = {}
    for line in input.splitlines():
        name = line.split(" -> ")[0]
        m = name[0]
        n = "broadcaster" if m == "b" else name[1:]
        modules[n] = letter_to_module[m](id=n)
    for line in input.splitlines():
        name, conns = line.split(" -> ")
        m = name[0]
        n = "broadcaster" if m == "b" else name[1:]
        for c in conns.split(", "):
            modules[n].connections_out.add(c)
            if c in modules:
                modules[c].connections_in.add(n)
    return modules


def part1():
    pulse_history = []
    modules = parse_modules(INPUT)
    for _ in range(1000):
        queue = [("button", "broadcaster", Pulse.LOW)]
        while queue:
            from_id, to_id, pulse = queue.pop(0)
            pulse_history.append(pulse)
            if (mod := modules.get(to_id, None)) is not None:
                next_pulse = mod.on_receive(from_id, pulse)
                if next_pulse is not None:
                    queue += [(to_id, m, next_pulse) for m in mod.connections_out]

    lows = sum(1 for p in pulse_history if p == Pulse.LOW)
    highs = sum(1 for p in pulse_history if p == Pulse.HIGH)
    print("ans 1:", lows * highs)


def delete_nodes(input: str, ids: list[str]) -> str:
    return "\n".join(filter(lambda line: all(i not in line[:3] for i in ids), input.splitlines()))


def get_cycles(modules) -> int:
    button_presses = 0
    while True:
        button_presses += 1
        queue = [("button", "broadcaster", Pulse.LOW)]
        while queue:
            from_id, to_id, pulse = queue.pop(0)
            if to_id == "rx" and pulse == Pulse.LOW:
                print("cycle:", button_presses)
                return button_presses
            if (mod := modules.get(to_id, None)) is not None:
                next_pulse = mod.on_receive(from_id, pulse)
                if next_pulse is not None:
                    queue += [(to_id, m, next_pulse) for m in mod.connections_out]


def part2():
    groups = {"rk", "zf", "qx", "cd"}
    cycles = []
    for group in groups:
        modules = parse_modules(delete_nodes(INPUT, groups.difference({group})))
        cycles.append(get_cycles(modules))
    print("ans 2:", math.lcm(*cycles))


def plot_network():
    import networkx as nx
    import pyvis.network

    modules = parse_modules(INPUT)
    G = nx.DiGraph()

    def get_group(m_id: ModId) -> str:
        match modules.get(m_id, None):
            case Broadcaster():
                return 1
            case Conjunction():
                return 2
            case FlipFlop():
                return 3
            case _:
                return 4

    G.add_nodes_from([(m, {"group": get_group(m)}) for m in modules.keys()])
    for mod_id, module in modules.items():
        G.add_edges_from([(mod_id, c) for c in module.connections_out])

    nt = pyvis.network.Network(directed=True)
    nt.from_nx(G)
    nt.show("day20.html", notebook=False)


plot_network()
part1()
part2()
