from enum import Enum, auto
from typing import List


class ModuleType(Enum):
    BUTTON = auto()
    BROADCAST = auto()
    FLIP_FLOP = auto()
    CONJUNCTION = auto()


class Pulse(Enum):
    LOW = "LOW"
    HIGH = "HIGH"


class FlipFlopState(Enum):
    ON = auto()
    OFF = auto()


class FlipFlop:
    def __init__(self, connections, name):
        self.name = name
        self.state: FlipFlopState = FlipFlopState.OFF
        self.connections: List[str] = connections

    def recieve_pulse(self, pulse: Pulse) -> Pulse | None:
        if pulse == Pulse.HIGH:
            return None

        if self.state == FlipFlopState.ON:
            self.state = FlipFlopState.OFF
            return Pulse.LOW
        self.state = FlipFlopState.ON
        return Pulse.HIGH


class Conjunction:
    def __init__(self, connections, name):
        self.name = name
        self.connections: List[str] = connections
        self.input_states = {}

    def recieve_pulse(self, pulse: Pulse, connection: str) -> Pulse | None:
        self.input_states[connection] = pulse
        if all(state == Pulse.HIGH for state in self.input_states.values()):
            return Pulse.LOW
        return Pulse.HIGH

    def add_input_state(self, name: str):
        self.input_states[name] = Pulse.LOW


class Broadcast:
    def __init__(self, connections, name):
        self.name = name
        self.connections: List[str] = connections

    def recieve_pulse(self, pulse: Pulse) -> Pulse | None:
        return pulse


with open("inputs/d20") as file:
    data = file.read().splitlines()


modules = {"output": "OUTPUT", "rx": "RX"}

for line in data:
    module, connections = line.split(" -> ")
    if module.startswith("%"):
        modules[module[1:]] = FlipFlop(connections.split(", "), module[1:])
    elif module.startswith("&"):
        modules[module[1:]] = Conjunction(connections.split(", "), module[1:])
    else:
        modules[module] = Broadcast(connections.split(", "), module)

for module in list(modules.values()):
    if isinstance(module, str):
        continue
    for c in module.connections:
        _m = modules[c]
        if isinstance(_m, Conjunction):
            _m.add_input_state(module.name)


def press_button(modules, n) -> (int, int):
    low = 0
    high = 0
    for _ in range(n):
        queue = [(Pulse.LOW, modules["broadcaster"], "button")]
        while len(queue):
            current = queue.pop(0)
            pulse, module, source = current
            if pulse == Pulse.LOW:
                low += 1
            else:
                high += 1
            if isinstance(module, str):
                continue
            if isinstance(module, FlipFlop):
                next_pulse = module.recieve_pulse(pulse)
                if next_pulse:
                    for i, c in enumerate(module.connections):
                        if isinstance(modules[source], Conjunction):
                            queue.insert(
                                len(module.connections) + i,
                                (next_pulse, modules[c], module.name),
                            )
                        else:
                            queue.append((next_pulse, modules[c], module.name))
            elif isinstance(module, Conjunction):
                next_pulse = module.recieve_pulse(pulse, source)
                if next_pulse:
                    for i, c in enumerate(module.connections):
                        queue.insert(
                            len(modules[source].connections) + i,
                            (next_pulse, modules[c], module.name),
                        )
            elif isinstance(module, Broadcast):
                next_pulse = module.recieve_pulse(pulse)
                if next_pulse:
                    for c in module.connections:
                        queue.append((next_pulse, modules[c], module.name))

    return low, high


low, high = press_button(modules, 1000)
print(f"Low: {low}, High: {high}, Product: {low * high}")
