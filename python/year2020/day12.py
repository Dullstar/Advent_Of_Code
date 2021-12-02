import time
import os


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def to_string(self):
        return f"({self.x}, {self.y})"


def parse_input(filename):
    # I believe we'll be best off leaving these as strings today until we need them.
    lines = []
    with open (filename, "r") as file:
        for line in file:
            if len(line) > 0:
                lines.append(line.strip())
    return lines


def get_manhattan_distance(directions: list):
    position = Point(0, 0)
    previous_facing = "E"  # given in problem description
    for direction in directions:
        facing = direction[0]
        distance = int(direction[1:])  # Could technically be an angle too if left or right...
        update_facing = False
        # Convert forward to a cardinal direction
        if facing == "F":
            facing = previous_facing
        # Handle L and R turns
        if facing == "L":
            while distance > 0:  # don't need to handle negative values for distance
                facing = get_left(previous_facing)
                distance -= 90
                previous_facing = facing
        elif facing == "R":
            while distance > 0:
                facing = get_right(previous_facing)
                distance -= 90
                previous_facing = facing
        elif facing == "N":
            position.y += distance
        elif facing == "S":
            position.y -= distance
        elif facing == "E":
            position.x += distance
        elif facing == "W":
            position.x -= distance

    return abs(position.x) + abs(position.y)


def get_left(facing: str):
    if facing == "N":
        return "W"
    elif facing == "W":
        return "S"
    elif facing == "S":
        return "E"
    elif facing == "E":
        return "N"
    assert 0, "Invalid direction"


def get_right(facing: str):
    if facing == "N":
        return "E"
    elif facing == "E":
        return "S"
    elif facing == "S":
        return "W"
    elif facing == "W":
        return "N"
    assert 0, "Invalid direction"


def get_manhattan_distance_waypoints(instructions: list, verbose: bool = False):
    ship_position = Point(0, 0)
    waypoint_position = Point(10, 1)  # given; 10 units east and 1 unit north; recall this is relative to ship
    for instruction in instructions:
        direction = instruction[0]
        distance = int(instruction[1:])
        if direction == "F":
            ship_position.x += waypoint_position.x * distance
            ship_position.y += waypoint_position.y * distance
        elif direction == "L" or direction == "R":
            rotate_waypoint(waypoint_position, direction, distance)
        elif direction == "N":
            waypoint_position.y += distance
        elif direction == "E":
            waypoint_position.x += distance
        elif direction == "S":
            waypoint_position.y -= distance
        elif direction == "W":
            waypoint_position.x -= distance
        else:
            raise ValueError(f"Invalid instruction: {instruction}")
        if verbose:
            print(f"{instruction:8} Waypoint at {waypoint_position.to_string()}; ship at {ship_position.to_string()}")
    return abs(ship_position.x) + abs(ship_position.y)


def rotate_waypoint(position: Point, direction: str, distance: int):
    # Rotate by swapping the x and y coordinate and making one negative. Which one becomes negative depends on the
    # direction of the rotation.
    # print(f"Rotate call: {position.to_string()}, {direction}, {distance}")
    # Base case
    if distance <= 0:
        # print("Returning waypoint position, ", position.to_string())
        return position
    position.x, position.y = position.y, position.x
    if direction == "L":
        position.x *= -1
    elif direction == "R":
        position.y *= -1
    return rotate_waypoint(position, direction, distance - 90)


def main(input_filename: str):
    start_time = time.time()
    directions = parse_input(input_filename)
    part1_start = time.time()
    print("Part 1: Manhattan distance: ", get_manhattan_distance(directions))
    part2_start = time.time()
    print("Part 2: Waypoint Manhattan distance: ", get_manhattan_distance_waypoints(directions))
    end_time = time.time()

    print("Elapsed Time:")
    print(f"    Parsing: {(part1_start - start_time) * 1000:.2f} ms")
    print(f"    Part 1: {(part2_start - part1_start) * 1000:.2f} ms")
    print(f"    Part 2: {(end_time - part2_start) * 1000:.2f} ms")
    print(f"    Total: {(end_time - start_time) * 1000:.2f} ms")


if __name__ == "__main__":
    def run_main():
        os.chdir(os.path.split(__file__)[0])
        main("../../inputs/2020/day12.txt")

    run_main()
