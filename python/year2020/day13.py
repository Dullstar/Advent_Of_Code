import time
import os


class Bus:
    def __init__(self, bus_id: int, next_departure: int, offset: int = -1):
        self.id = bus_id
        self.next_departure = next_departure
        self.offset = offset


def parse_input(filename: str):
    with open(filename, "r") as file:
        contents = [line.strip() for line in file]
        busses = [i for i in contents[1].split(",")]
    # timestamp, bus IDs
    return int(contents[0]), busses


def find_earliest_departure_time(timestamp: int, _bus_ids: list):

    busses = []
    bus_ids = [int(bus_id) for bus_id in _bus_ids if bus_id != "x"]
    for bus_id in bus_ids:
        # If statement accounts for an edge case where this formula won't produce the correct answer
        # There's probably something that works even if it's 0, but I don't know what it is and this seems to work
        # for everything else, so this seems like the best solution.
        if timestamp % bus_id == 0:
            next_departure = timestamp
        else:
            next_departure = timestamp + bus_id - (timestamp % bus_id)
        # print(f"Bus {bus_id}: next departure: {next_departure}")
        busses.append(Bus(bus_id, next_departure))
    busses.sort(key=lambda bus: bus.next_departure)
    print(f"Part 1: The earliest departure is bus {busses[0].id} at time {busses[0].next_departure}")
    print(f"    bus_id * delta_time = {busses[0].id * (busses[0].next_departure - timestamp)}")


def id_problem(bus_ids: list):
    busses = []
    for i in range(len(bus_ids)):
        if bus_ids[i] != "x":
            busses.append(Bus(int(bus_ids[i]), -1, i))

    start_val = 1  # 1 avoids having to handle 0 % anything = 0; we don't learn anything helpful from it
    increment = 1
    for bus in busses:
        start_val, increment = narrow_down_candidates(bus, start_val, increment)

    print("Part 2: The busses align in the requested manner at", start_val)


# I'm certain there's a better name for this, but I can't think of one right now.
def narrow_down_candidates(bus: Bus, start_val: int, increment: int):
    while (start_val + bus.offset) % bus.id != 0:
        start_val += increment
    return start_val, increment * bus.id


def main(input_filename: str):
    if not os.path.exists(input_filename):
        raise FileNotFoundError(f"Couldn't find input file: {input_filename}")

    timestamp, bus_ids = parse_input(input_filename)
    find_earliest_departure_time(timestamp, bus_ids)
    id_problem(bus_ids)


if __name__ == "__main__":
    def run_main():
        os.chdir(os.path.split(__file__)[0])
        filename = "../../inputs/2020/day13.txt"
        main(filename)

    run_main()
