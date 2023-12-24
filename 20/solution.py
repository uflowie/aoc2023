import re
from math import lcm

with open("20/input.txt", "r") as f:
    puzzle_input = [line.strip() for line in f.readlines()]


def make_modules():
    def make_module(full_name: str, destinations: str, name):
        module_type = full_name[0]
        destinations = destinations.split(", ")
        if module_type == "%":
            return FlipFlop(name, destinations)
        elif module_type == "&":
            return Conjunction(name, destinations)
        else:
            return Broadcaster(name, destinations)

    modules = {
        re.sub(r"[%&]", "", module[0]): make_module(
            module[0], module[1], re.sub(r"[%&]", "", module[0])
        )
        for module in [line.split(" -> ") for line in puzzle_input]
    }

    for module in modules.values():
        if isinstance(module, Conjunction):
            module.init_inputs(modules.values())

    return modules


class FlipFlop:
    def __init__(self, name, destinations):
        self.name = name
        self.destinations = destinations
        self.on = False

    def send_pulse(self, sender, pulse):
        if pulse == "low":
            self.on = not self.on
            output = "high" if self.on else "low"
            return [
                (self.name, destination, output) for destination in self.destinations
            ]
        return []


class Conjunction:
    def __init__(self, name, destinations):
        self.name = name
        self.destinations = destinations
        self.inputs = {}

    def send_pulse(self, sender, pulse):
        self.inputs[sender] = pulse
        return [
            (self.name, destination, self.get_output())
            for destination in self.destinations
        ]

    def init_inputs(self, modules):
        for module in modules:
            for destination in module.destinations:
                if destination == self.name:
                    self.inputs[module.name] = "low"

    def get_output(self):
        return "low" if set(self.inputs.values()) == {"high"} else "high"


class Broadcaster:
    def __init__(self, name, destinations):
        self.name = name
        self.destinations = destinations

    def send_pulse(self, sender, pulse):
        return [(self.name, destination, "low") for destination in self.destinations]


class Subsystem:
    def __init__(self, starting_module_name):
        modules = make_modules()
        self.modules = {}
        self.root = modules[starting_module_name]

        remaining = [self.root]

        while len(remaining) > 0:
            module = remaining.pop(0)
            if module.name in self.modules:
                continue

            self.modules[module.name] = module

            if module.destinations == ["lx"]:
                self.exit_module = module
                # lx is the shared output node, therefore it's not part of the independent subsystem
                continue

            for destination in module.destinations:
                if destination in modules:
                    remaining.append(modules[destination])

    def cycle_length(self):
        i = 0
        while True:
            i += 1
            destinations = [("broadcaster", self.root.name, "low")]
            while len(destinations) > 0:
                sender_name, receiver_name, pulse = destinations.pop(0)
                if receiver_name not in self.modules:
                    # shared exit node
                    continue

                receiver = self.modules[receiver_name]
                receiver_destinations = receiver.send_pulse(sender_name, pulse)

                destinations.extend(receiver_destinations)

                if (
                    self.exit_module.get_output() == "high"
                    and receiver == self.exit_module
                ):
                    return i


def part_1():
    modules = make_modules()

    high_pulses = 0
    low_pulses = 0

    for i in range(1000):
        destinations = [("button", "broadcaster", "low")]
        low_pulses += 1
        while len(destinations) > 0:
            sender_name, receiver_name, pulse = destinations.pop(0)
            if receiver_name not in modules:
                # untyped module
                continue

            receiver = modules[receiver_name]
            receiver_destinations = receiver.send_pulse(sender_name, pulse)

            high_pulses += len(
                [pulse for _, _, pulse in receiver_destinations if pulse == "high"]
            )
            low_pulses += len(
                [pulse for _, _, pulse in receiver_destinations if pulse == "low"]
            )

            destinations.extend(receiver_destinations)

    return high_pulses * low_pulses


def part_2():
    return lcm(
        *[
            subsystem.cycle_length()
            for subsystem in [
                Subsystem(root_node) for root_node in make_modules()["broadcaster"].destinations
            ]
        ]
    )


print(part_1())

print(part_2())
