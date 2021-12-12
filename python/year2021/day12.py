import time
import os


class Node:
    def __init__(self, label: str):
        self.label = label
        self.repeatable = label.isupper()
        self.connections = set()

    def __str__(self):
        return f"Node {self.label}: Connections: {self.connections}" \
               + f"    Repeatable: {self.repeatable}"


class Cave:
    def __init__(self, filename: str):
        self.nodes = dict()
        with open(filename, "r") as file:
            for line in file:
                line = line.strip().split("-")
                if line[0] not in self.nodes:
                    self.nodes[line[0]] = Node(line[0])
                if line[1] not in self.nodes:
                    self.nodes[line[1]] = Node(line[1])
                self._make_connection(self.nodes[line[0]], self.nodes[line[1]])

    @staticmethod
    def _make_connection(node1: Node, node2: Node):
        node1.connections.add(node2.label)
        node2.connections.add(node1.label)

    def count_paths(self, extra_repeats: int = 0):
        def count_branches(node: Node, current_path: list[str] = None, repeats_used: int = 0):
            if current_path is None:
                current_path = []
            total = 0
            current_path.append(node.label)
            for node_label in node.connections:
                neighbor = self.nodes[node_label]
                if node_label == "end":
                    total += 1
                elif (not neighbor.repeatable) and (neighbor.label in current_path):
                    if repeats_used < extra_repeats and neighbor.label != "start":
                        total += count_branches(self.nodes[node_label], current_path, repeats_used + 1)
                    else:
                        total += 0
                else:
                    total += count_branches(self.nodes[node_label], current_path, repeats_used)
            current_path.pop()
            return total
        return count_branches(self.nodes["start"])


def main(input_filename: str):
    start_time = time.time()
    cave = Cave(input_filename)
    part1_start = time.time()
    print(f"Part 1: {cave.count_paths()} possible routes")
    part2_start = time.time()
    print(f"Part 2: {cave.count_paths(1)} possible routes")
    end_time = time.time()

    print("Elapsed Time:")
    print(f"    Parsing: {(part1_start - start_time) * 1000:.2f} ms")
    print(f"    Part 1: {(part2_start - part1_start) * 1000:.2f} ms")
    print(f"    Part 2: {(end_time - part2_start) * 1000:.2f} ms")
    print(f"    Total: {(end_time - start_time) * 1000:.2f} ms")


if __name__ == "__main__":
    os.chdir(os.path.split(__file__)[0])
    main("../../inputs/2021/day12.txt")
