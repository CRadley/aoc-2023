from enum import Enum, auto
from typing import List
import math


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
        self.emitted_high_pulses = []

    def recieve_pulse(
        self, pulse: Pulse, connection: str, button_presses: int
    ) -> Pulse | None:
        self.input_states[connection] = pulse
        if all(state == Pulse.HIGH for state in self.input_states.values()):
            return Pulse.LOW
        self.emitted_high_pulses.append(button_presses)
        return Pulse.HIGH

    def add_input_state(self, name: str):
        self.input_states[name] = Pulse.LOW


class Broadcast:
    def __init__(self, connections, name):
        self.name = name
        self.connections: List[str] = connections

    def recieve_pulse(self, pulse: Pulse) -> Pulse | None:
        return pulse


def generate_starting_modules():
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
    return modules


modules = generate_starting_modules()
modules_2 = generate_starting_modules()


def press_button(modules, n, offset=0) -> (int, int):
    low = 0
    high = 0
    for count in range(n):
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
                next_pulse = module.recieve_pulse(pulse, source, count + 1 + offset)
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


def determine_cycle(modules):
    button_press_count = 0
    while True:
        press_button(modules, 1, button_press_count)
        conjunctions = [
            modules[m] for m in modules if isinstance(modules[m], Conjunction)
        ]
        if all(len(c.emitted_high_pulses) for c in conjunctions):
            break
        button_press_count += 1
    return [
        c.emitted_high_pulses[0]
        for c in conjunctions
        if len(c.emitted_high_pulses) == 1
    ]


low, high = press_button(modules, 1000)
print(low * high)

cycle = determine_cycle(modules_2)
print(math.lcm(*cycle))

# Determine cycle of the 4 feeder

# gt ->
# vr ->
#       &jq -> rx
# nl ->
# lr ->
