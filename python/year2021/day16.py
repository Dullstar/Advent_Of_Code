import time
import os


class PacketType:
    ADD = 0
    MULT = 1
    MIN = 2
    MAX = 3
    VALUE = 4
    GREATER = 5
    LESS = 6
    EQUAL = 7


class Packet:
    def __init__(self, version: int, _type: int):
        self.version = version
        self.type = _type

    def __str__(self):
        return f"Version: {self.version}; Type: {self.type}"

    def to_string(self, depth):
        return self.__str__()

    def version_sum(self):
        return self.version

    def evaluate(self):
        return 0  # Intended to be overridden, but defined here to prevent warnings from Pycharm's type checking system.


class ValuePacket(Packet):
    def __init__(self, version: int, _type: int, value: int):
        super().__init__(version, _type)
        self.value = value

    def __str__(self):
        return f"{super().__str__()} (ValuePacket); Value: {self.value}"

    def evaluate(self):
        return self.value


class OperatorPacket(Packet):
    def __init__(self, version: int, _type: int, subpackets: list[Packet]):
        super().__init__(version, _type)
        self.subpackets = subpackets

    def __str__(self):
        return self.to_string(0)

    def to_string(self, depth: int):
        output = f"{super().__str__()} (OperatorPacket)"
        for packet in self.subpackets:
            output += f"\n{' ' * 4 * (depth + 1)}{packet.to_string(depth + 1)}"
        return output

    def version_sum(self):
        return sum([p.version_sum() for p in self.subpackets]) + self.version

    def evaluate(self):
        if self.type == PacketType.ADD:
            return sum(self.evaluate_subpackets())
        elif self.type == PacketType.MULT:
            total = 1
            for i in self.evaluate_subpackets():
                total *= i
            return total
        elif self.type == PacketType.MIN:
            return min(self.evaluate_subpackets())
        elif self.type == PacketType.MAX:
            return max(self.evaluate_subpackets())
        elif self.type == PacketType.GREATER:
            return int(self.subpackets[0].evaluate() > self.subpackets[1].evaluate())
        elif self.type == PacketType.LESS:
            return int(self.subpackets[0].evaluate() < self.subpackets[1].evaluate())
        elif self.type == PacketType.EQUAL:
            return int(self.subpackets[0].evaluate() == self.subpackets[1].evaluate())

    def evaluate_subpackets(self):
        return [p.evaluate() for p in self.subpackets]


def parse_input(filename: str):
    with open(filename, "r") as file:
        contents = file.read().strip()
    binary = ""
    for char in contents:
        # This FEELS inelegant, but it's easier than the bit twiddling we'd be dealing with otherwise.
        binary += f"{bin(int(char, 16))[2:]:>4}"
    # print(binary)
    return binary.replace(" ", "0")


def parse_packet(binary: str, i: int = 0):
    try:
        while i < len(binary):
            # Start a packet
            version = int(binary[i:i+3], 2)
            i += 3
            packet_type = int(binary[i:i+3], 2)
            i += 3
            if packet_type == PacketType.VALUE:
                value = ""
                while True:
                    signal_bit = binary[i]
                    i += 1
                    value += binary[i:i+4]
                    i += 4
                    if signal_bit == "0":  # the last chunk
                        break
                return ValuePacket(version, packet_type, int(value, 2)), i
            else:
                length_type_id = binary[i]
                i += 1
                subpackets = []
                if length_type_id == "0":  # Keep reading packets until exhausting the available length
                    length_in_bits = int(binary[i:i+15], 2)
                    i += 15
                    stop = length_in_bits + i
                    while i < stop:
                        subpacket, i = parse_packet(binary, i)
                        subpackets.append(subpacket)
                elif length_type_id == "1":
                    number_packets = int(binary[i:i+11], 2)
                    i += 11
                    for j in range(number_packets):
                        subpacket, i = parse_packet(binary, i)
                        subpackets.append(subpacket)
                return OperatorPacket(version, packet_type, subpackets), i
    except IndexError:
        # Shouldn't happen.
        print("Ran out of bits. Stopping.")


def main(input_filename: str):
    start_time = time.time()
    binary = parse_input(input_filename)
    part1_start = time.time()
    packet = parse_packet(binary)[0]
    print(f"Part 1: Sum of versions: {packet.version_sum()}")
    part2_start = time.time()
    print(f"Part 2: Evaluation result: {packet.evaluate()}")
    end_time = time.time()

    print("Elapsed Time:")
    print(f"    Parsing: {(part1_start - start_time) * 1000:.2f} ms")
    print(f"    Part 1: {(part2_start - part1_start) * 1000:.2f} ms")
    print(f"    Part 2: {(end_time - part2_start) * 1000:.2f} ms")
    print(f"    Total: {(end_time - start_time) * 1000:.2f} ms")


if __name__ == "__main__":
    os.chdir(os.path.split(__file__)[0])
    main("../../inputs/2021/day16.txt")
